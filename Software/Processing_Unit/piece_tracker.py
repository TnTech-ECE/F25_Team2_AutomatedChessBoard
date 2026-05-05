"""
piece_tracker.py — Physical board piece tracking and serial communication

Grid coordinate system:
    Main board : columns a-h (x: 1-8), rows 1-8  (y: 1-8)
    Black zone : columns a-h (x: 1-8), rows 9-10  (y: 9-10)   — above board
    White zone : columns a-h (x: 1-8), rows 11-12 (y: 11-12)  — below board

Serial packet format (matches existing code):
    2 bytes per move
    Byte 1 — source : high nibble = col bits (a=0001 .. h=1000)
                      low  nibble = row bits (1=0001 .. 12=1100)
    Byte 2 — dest   : same encoding

    After each packet the Arduino sends 1 byte ACK confirming move complete.
    Packets are queued and sent one at a time in order — the chess logic
    never blocks waiting for a move to physically complete.

Usage:
    from piece_tracker import PieceTracker
    tracker = PieceTracker(port="/dev/serial0")
    tracker.send_capture(move, board)   # call BEFORE board.push()
    tracker.send_move(move, board)      # call AFTER  board.push()
    tracker.reset_board(board)          # call at start of new game
    tracker.close()
"""

import chess
import serial
import time
import threading
import queue

# ── Encoding helpers ──────────────────────────────────────────────────────────
_COL_BITS = {
    "a": 0b0001, "b": 0b0010, "c": 0b0011, "d": 0b0100,
    "e": 0b0101, "f": 0b0110, "g": 0b0111, "h": 0b1000,
}
_COL_FROM_INT = {1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h"}

def _encode_square(col: str, row: int) -> int:
    """Encode a (col letter, row int) pair into one byte: high=col bits, low=row bits."""
    return (_COL_BITS[col] << 4) | (row & 0x0F)

def _square_to_colrow(sq: chess.Square):
    """Convert a chess.Square to (col_letter, row_int) using 1-8 for the main board."""
    file = chess.square_file(sq)   # 0-7
    rank = chess.square_rank(sq)   # 0-7
    col  = _COL_FROM_INT[file + 1]
    row  = rank + 1
    return col, row

def encode_move_bytes(src_col, src_row, dst_col, dst_row) -> bytes:
    """Return the 2-byte serial packet for a physical move."""
    return bytes([_encode_square(src_col, src_row),
                  _encode_square(dst_col, dst_row)])

def move_to_binary_str(src_col, src_row, dst_col, dst_row) -> str:
    """Human-readable binary string for display/logging."""
    src = f"{_COL_BITS[src_col]:04b} {src_row:04b}"
    dst = f"{_COL_BITS[dst_col]:04b} {dst_row:04b}"
    return f"{src_col}{src_row}{dst_col}{dst_row} -> {src}  {dst}"


# ── Capture zone layout ───────────────────────────────────────────────────────
# Each zone is 2 rows × 8 columns = 16 slots.
# Slots are filled left-to-right, top-to-bottom within the zone.
#
# White captured pieces go to rows 11-12 (white lost pieces, below board)
# Black captured pieces go to rows  9-10 (black lost pieces, above board)

_WHITE_ZONE_SLOTS = [
    (_COL_FROM_INT[c], r) for r in (11, 12) for c in range(1, 9)
]  # (a,11),(b,11),...,(h,11),(a,12),...,(h,12)

_BLACK_ZONE_SLOTS = [
    (_COL_FROM_INT[c], r) for r in (9, 10) for c in range(1, 9)
]  # (a,9),(b,9),...,(h,9),(a,10),...,(h,10)

# Starting positions for every piece on a standard board
# key: (col, row)  value: (piece_type, color)
_START_POSITIONS: dict = {}

def _build_start_positions():
    global _START_POSITIONS
    back_row = [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN,
                chess.KING, chess.BISHOP, chess.KNIGHT, chess.ROOK]
    for i, pt in enumerate(back_row):
        col = _COL_FROM_INT[i + 1]
        _START_POSITIONS[(col, 1)] = (pt, chess.WHITE)
        _START_POSITIONS[(col, 8)] = (pt, chess.BLACK)
    for i in range(8):
        col = _COL_FROM_INT[i + 1]
        _START_POSITIONS[(col, 2)] = (chess.PAWN, chess.WHITE)
        _START_POSITIONS[(col, 7)] = (chess.PAWN, chess.BLACK)

_build_start_positions()


# ── PieceTracker ──────────────────────────────────────────────────────────────

class PieceTracker:
    """
    Tracks the physical location of every piece and sends serial packets
    to the board for captures and resets.

    Physical location dict:
        self._locations[(col, row)] = (piece_type, color)
        Covers main board (rows 1-8) and capture zones (rows 9-12).
    """

    def __init__(self, port: str = "/dev/serial0", baud: int = 115200,
                 move_delay: float = 0.05, ack_timeout: float = 30.0):
        """
        port        : serial port
        baud        : baud rate
        move_delay  : seconds to wait after ACK before sending next packet
        ack_timeout : seconds to wait for ACK from Arduino before giving up
        """
        self._move_delay  = move_delay
        self._ack_timeout = ack_timeout
        self._lock        = threading.Lock()

        # Physical location of every piece: (col, row) -> (piece_type, color)
        self._locations: dict = {}
        self._reset_locations()

        # Next available slot index in each capture zone
        self._white_slot_idx = 0
        self._black_slot_idx = 0

        # Serial send queue — packets are (src_col, src_row, dst_col, dst_row, label)
        # The worker thread drains this one packet at a time, waiting for ACK each time.
        self._send_queue: queue.Queue = queue.Queue()
        self._closing    = False
        self._display_cb = None   # set via set_display_callback()

        # Serial port
        try:
            self._serial = serial.Serial(port, baud, timeout=self._ack_timeout)
            time.sleep(0.1)
            self._serial_ok = True
            print(f"[Tracker] Serial open on {port} @ {baud} baud "
                  f"(ACK timeout {self._ack_timeout}s)")
        except serial.SerialException as e:
            print(f"[Tracker] WARNING: could not open serial port: {e}")
            print("[Tracker] Running in dry-run mode — packets printed only.")
            self._serial    = None
            self._serial_ok = False

        # Start the serial worker thread
        self._worker = threading.Thread(target=self._serial_worker, daemon=True)
        self._worker.start()

    # ── Public API ────────────────────────────────────────────────────────────

    def send_ready_signal(self):
        """
        Send the single-byte 0x11 handshake to the Arduino indicating the Pi
        is ready to accept moves. Call this once after the microphone is ready.
        Sent directly (not through the queue) since it is a one-time handshake.
        """
        print("[Tracker] Sending ready signal 0x11 to Arduino")
        if self._serial_ok and self._serial and self._serial.is_open:
            try:
                self._serial.write(bytes([0x11]))
                print("[Tracker] Ready signal sent")
            except serial.SerialException as e:
                print(f"[Tracker] Failed to send ready signal: {e}")
        else:
            print("[Tracker] Dry-run: ready signal 0x11 (not sent)")

    def send_capture(self, move: chess.Move, board: chess.Board):
        """
        Call this BEFORE pushing the move onto the board.
        If the move captures a piece, sends the serial packet to move that
        piece from its current square to the correct capture zone slot,
        and updates internal tracking.
        """
        if not board.is_capture(move):
            return

        with self._lock:
            # En-passant: captured pawn is not on the destination square
            if board.is_en_passant(move):
                ep_rank = chess.square_rank(move.to_square)
                # The captured pawn is on the same file as the destination
                # but on the rank of the moving pawn's source
                cap_sq = chess.square(chess.square_file(move.to_square),
                                      chess.square_rank(move.from_square))
            else:
                cap_sq = move.to_square

            captured_piece = board.piece_at(cap_sq)
            if not captured_piece:
                return

            src_col, src_row = _square_to_colrow(cap_sq)

            # Assign a capture zone slot
            if captured_piece.color == chess.WHITE:
                # white piece captured → goes to white zone (rows 11-12)
                slot = self._white_slot_idx
                if slot < len(_WHITE_ZONE_SLOTS):
                    dst_col, dst_row = _WHITE_ZONE_SLOTS[slot]
                    self._white_slot_idx += 1
                else:
                    print("[Tracker] WARNING: white capture zone full")
                    return
            else:
                # black piece captured → goes to black zone (rows 9-10)
                slot = self._black_slot_idx
                if slot < len(_BLACK_ZONE_SLOTS):
                    dst_col, dst_row = _BLACK_ZONE_SLOTS[slot]
                    self._black_slot_idx += 1
                else:
                    print("[Tracker] WARNING: black capture zone full")
                    return

            self._send_packet(src_col, src_row, dst_col, dst_row, label="CAPTURE")

            # Update internal location map
            del self._locations[(src_col, src_row)]
            self._locations[(dst_col, dst_row)] = (captured_piece.piece_type,
                                                    captured_piece.color)

    def send_move(self, move: chess.Move, board: chess.Board):
        """
        Call this AFTER pushing the move onto the board.
        Handles castling by routing the rook through a temporary free square
        so it never collides with the king mid-transit:
          1. Rook → temp square (clears the rook's start)
          2. King → destination
          3. Rook → final square
        board is the state AFTER the push (used to find empty squares for temp).
        """
        with self._lock:
            uci = move.uci()

            # (rook_src, rook_dst) for each of the 4 castling cases
            castling_rook = {
                "e1g1": (("h", 1), ("f", 1)),
                "e1c1": (("a", 1), ("d", 1)),
                "e8g8": (("h", 8), ("f", 8)),
                "e8c8": (("a", 8), ("d", 8)),
            }

            if uci in castling_rook:
                (r_src_col, r_src_row), (r_dst_col, r_dst_row) = castling_rook[uci]

                # Both destination squares are empty so no collision risk.
                # Step 1: rook → its final square
                rook_piece = self._locations.get((r_src_col, r_src_row))
                self._send_packet(r_src_col, r_src_row, r_dst_col, r_dst_row,
                                  label="CASTLE-ROOK")
                if rook_piece:
                    del self._locations[(r_src_col, r_src_row)]
                    self._locations[(r_dst_col, r_dst_row)] = rook_piece

                # Step 2: king → its final square
                src_col, src_row = _square_to_colrow(move.from_square)
                dst_col, dst_row = _square_to_colrow(move.to_square)
                king_piece = self._locations.get((src_col, src_row))
                self._send_packet(src_col, src_row, dst_col, dst_row,
                                  label="CASTLE-KING")
                if king_piece:
                    del self._locations[(src_col, src_row)]
                    self._locations[(dst_col, dst_row)] = king_piece

            else:
                # Regular move
                src_col, src_row = _square_to_colrow(move.from_square)
                dst_col, dst_row = _square_to_colrow(move.to_square)
                piece = self._locations.get((src_col, src_row))
                self._send_packet(src_col, src_row, dst_col, dst_row, label="MOVE")
                if piece:
                    del self._locations[(src_col, src_row)]
                    self._locations[(dst_col, dst_row)] = piece

    def reset_board(self, board: chess.Board, log_fn=None):
        """
        Sends serial packets to move every piece back to its starting position.
        Syncs internal tracking from the actual board state first so any drift
        during the game doesn't corrupt the reset sequence.

        board  : the chess.Board at the moment reset is triggered
        log_fn : optional callable(text, kind) e.g. disp.set_message
        """
        with self._lock:
            # ── Sync locations from the real board state ──────────────────
            # Main board: read directly from the chess.Board
            self._locations = {}
            for sq in chess.SQUARES:
                p = board.piece_at(sq)
                if p:
                    col, row = _square_to_colrow(sq)
                    self._locations[(col, row)] = (p.piece_type, p.color)

            # Capture zones: rebuild by comparing start counts to what's on board
            start_counts = {
                chess.PAWN: 8, chess.ROOK: 2, chess.KNIGHT: 2,
                chess.BISHOP: 2, chess.QUEEN: 1, chess.KING: 1,
            }
            on_board_counts = {chess.WHITE: {}, chess.BLACK: {}}
            for sq in chess.SQUARES:
                p = board.piece_at(sq)
                if p:
                    ob = on_board_counts[p.color]
                    ob[p.piece_type] = ob.get(p.piece_type, 0) + 1

            self._white_slot_idx = 0
            self._black_slot_idx = 0
            for color in (chess.WHITE, chess.BLACK):
                for pt, start in start_counts.items():
                    lost = start - on_board_counts[color].get(pt, 0)
                    for _ in range(lost):
                        if color == chess.WHITE:
                            slot = self._white_slot_idx
                            if slot < len(_WHITE_ZONE_SLOTS):
                                pos = _WHITE_ZONE_SLOTS[slot]
                                self._locations[pos] = (pt, color)
                                self._white_slot_idx += 1
                        else:
                            slot = self._black_slot_idx
                            if slot < len(_BLACK_ZONE_SLOTS):
                                pos = _BLACK_ZONE_SLOTS[slot]
                                self._locations[pos] = (pt, color)
                                self._black_slot_idx += 1

            # ── Build and send reset packets ──────────────────────────────
            # Wait for any in-flight game moves to complete first
            self._send_queue.join()

            packets = self._build_reset_sequence()
            print(f"[Tracker] Reset: sending {len(packets)} move packets")
            for src_col, src_row, dst_col, dst_row, description in packets:
                if log_fn:
                    log_fn(description, "neutral")
                self._send_packet(src_col, src_row, dst_col, dst_row, label="RESET")

            # Send home signal — coreXY navigates to a11 (physical bottom-left)
            self._send_packet("a", 11, "a", 11, label="HOME")

            # Wait for all reset + home packets to physically complete
            self._send_queue.join()

            self._reset_locations()
            self._white_slot_idx = 0
            self._black_slot_idx = 0

    def get_available_promotion_pieces(self, color: chess.Color) -> set:
        """
        Returns set of piece types available for promotion.
        White promoting → looks for white pieces above pawn in white zone (rows 11-12).
        Black promoting → looks for black pieces above pawn in black zone (rows 9-10).
        """
        zone_rows = {11, 12} if color == chess.WHITE else {9, 10}
        above_pawn = {chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT}
        with self._lock:
            return {
                pt for (col, row), (pt, pc) in self._locations.items()
                if row in zone_rows and pc == color and pt in above_pawn
            }

    def send_promotion(self, move: chess.Move, board: chess.Board,
                       promo_piece_type: chess.PieceType):
        """
        Handle the full physical sequence for a promotion move.
        Call this INSTEAD of send_capture + send_move. Call BEFORE board.push().

        Sequence:
          If capturing: captured piece → opponent's capture zone  (PROMO-CAPTURE)
          Pawn          → own capture zone                        (PROMO-PAWN)
          Promotion piece from own capture zone → destination     (PROMO-PIECE)
        """
        with self._lock:
            src_col, src_row = _square_to_colrow(move.from_square)
            dst_col, dst_row = _square_to_colrow(move.to_square)
            promoting_color  = board.piece_at(move.from_square).color

            # Step 1 — if capturing, send captured piece to its capture zone
            if board.is_capture(move):
                cap_sq        = move.to_square
                captured      = board.piece_at(cap_sq)
                if captured:
                    cap_src_col, cap_src_row = _square_to_colrow(cap_sq)
                    if captured.color == chess.WHITE:
                        slot = self._white_slot_idx
                        if slot < len(_WHITE_ZONE_SLOTS):
                            cap_dst_col, cap_dst_row = _WHITE_ZONE_SLOTS[slot]
                            self._white_slot_idx += 1
                        else:
                            print("[Tracker] WARNING: white capture zone full")
                            return
                    else:
                        slot = self._black_slot_idx
                        if slot < len(_BLACK_ZONE_SLOTS):
                            cap_dst_col, cap_dst_row = _BLACK_ZONE_SLOTS[slot]
                            self._black_slot_idx += 1
                        else:
                            print("[Tracker] WARNING: black capture zone full")
                            return
                    self._send_packet(cap_src_col, cap_src_row,
                                      cap_dst_col, cap_dst_row, label="PROMO-CAPTURE")
                    del self._locations[(cap_src_col, cap_src_row)]
                    self._locations[(cap_dst_col, cap_dst_row)] = (captured.piece_type,
                                                                    captured.color)

            # Step 2 — send pawn to its own capture zone
            if promoting_color == chess.WHITE:
                pawn_slot = self._white_slot_idx
                if pawn_slot < len(_WHITE_ZONE_SLOTS):
                    pawn_dst_col, pawn_dst_row = _WHITE_ZONE_SLOTS[pawn_slot]
                    self._white_slot_idx += 1
                else:
                    print("[Tracker] WARNING: white capture zone full for pawn")
                    return
            else:
                pawn_slot = self._black_slot_idx
                if pawn_slot < len(_BLACK_ZONE_SLOTS):
                    pawn_dst_col, pawn_dst_row = _BLACK_ZONE_SLOTS[pawn_slot]
                    self._black_slot_idx += 1
                else:
                    print("[Tracker] WARNING: black capture zone full for pawn")
                    return

            self._send_packet(src_col, src_row, pawn_dst_col, pawn_dst_row,
                              label="PROMO-PAWN")
            del self._locations[(src_col, src_row)]
            self._locations[(pawn_dst_col, pawn_dst_row)] = (chess.PAWN, promoting_color)

            # Step 3 — find the promotion piece in the capture zone and move it
            zone_rows = {11, 12} if promoting_color == chess.WHITE else {9, 10}
            promo_src = None
            for (col, row), (pt, pc) in list(self._locations.items()):
                if row in zone_rows and pc == promoting_color and pt == promo_piece_type:
                    promo_src = (col, row)
                    break

            if promo_src is None:
                print(f"[Tracker] WARNING: no {chess.piece_name(promo_piece_type)} "
                      f"available for promotion")
                return

            self._send_packet(promo_src[0], promo_src[1], dst_col, dst_row,
                              label="PROMO-PIECE")
            del self._locations[promo_src]
            self._locations[(dst_col, dst_row)] = (promo_piece_type, promoting_color)

    def wait_for_queue(self):
        """Block until all queued packets have been sent and ACKed."""
        self._send_queue.join()

    def is_queue_empty(self):
        """Return True if no packets are waiting or currently being processed."""
        return self._send_queue.unfinished_tasks == 0

    def get_capture_zone_state(self) -> dict:
        """
        Returns current contents of both capture zones.
        { (col, row): (piece_type, color), ... }
        """
        with self._lock:
            return {
                pos: piece
                for pos, piece in self._locations.items()
                if pos[1] >= 9
            }

    def close(self):
        """Wait for all queued packets to send, then close the serial port."""
        print("[Tracker] Waiting for send queue to drain...")
        self._send_queue.join()   # blocks until all task_done() calls match puts
        self._closing = True
        self._worker.join(timeout=3)
        if self._serial and self._serial.is_open:
            self._serial.close()
            print("[Tracker] Serial port closed.")

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _reset_locations(self):
        """Rebuild _locations to match the standard starting board."""
        self._locations = dict(_START_POSITIONS)

    def set_display_callback(self, cb):
        """
        Set a callback for display messages from the worker thread.
        cb(text, kind) — same signature as disp.set_message.
        """
        self._display_cb = cb

    def _notify(self, text, kind="neutral"):
        """Send a message to the display if a callback is registered."""
        if self._display_cb:
            try:
                self._display_cb(text, kind)
            except Exception:
                pass

    def _send_packet(self, src_col, src_row, dst_col, dst_row, label=""):
        """Enqueue a packet — returns immediately, worker thread handles sending."""
        packet_info = (src_col, src_row, dst_col, dst_row, label)
        self._send_queue.put(packet_info)
        binary_str = move_to_binary_str(src_col, src_row, dst_col, dst_row)
        print(f"  [QUEUED:{label}] {binary_str}  "
              f"(queue depth: {self._send_queue.qsize()})")

    def _serial_worker(self):
        """
        Background thread — drains the send queue one packet at a time.
        - ACK (0x01): success, move to next packet.
        - NACK (0x00): resend the same packet once, then skip if it fails again.
        - Timeout: display warning and skip.
        """
        MAX_RETRIES = 1   # resend once on NACK before giving up

        while not self._closing:
            try:
                src_col, src_row, dst_col, dst_row, label = \
                    self._send_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            packet     = encode_move_bytes(src_col, src_row, dst_col, dst_row)
            binary_str = move_to_binary_str(src_col, src_row, dst_col, dst_row)
            print(f"  [{label}] {binary_str}  raw={packet.hex()}")

            if self._serial_ok and self._serial and self._serial.is_open:
                success  = False
                attempts = 0
                while attempts <= MAX_RETRIES and not success:
                    try:
                        self._serial.write(packet)
                        ack = self._serial.read(1)
                        if not ack:
                            # Timeout — no response from Arduino
                            msg = f"No response from board ({binary_str})"
                            print(f"  [TIMEOUT] {msg}")
                            self._notify(f"Board timeout: {label}", kind="error")
                            break   # don't retry on timeout, just skip
                        elif ack[0] == 0x01:
                            print(f"  [ACK] 0x01 — move complete")
                            success = True
                        elif ack[0] == 0x00:
                            attempts += 1
                            if attempts <= MAX_RETRIES:
                                print(f"  [NACK] 0x00 — resending ({attempts}/{MAX_RETRIES})")
                                self._notify(f"Board fault, retrying: {label}", kind="warn")
                            else:
                                print(f"  [NACK] 0x00 — retry failed, skipping")
                                self._notify(f"Board fault, skipped: {label}", kind="error")
                        else:
                            print(f"  [ACK?] unexpected 0x{ack.hex()} — treating as ACK")
                            success = True
                    except serial.SerialException as e:
                        print(f"[Tracker] Serial error: {e}")
                        self._notify("Serial error — check connection", kind="error")
                        break

            time.sleep(self._move_delay)
            self._send_queue.task_done()

    def _build_reset_sequence(self) -> list:
        """
        Build the ordered list of physical moves to reset the board.
        Returns list of (src_col, src_row, dst_col, dst_row, description).

        Single-pass algorithm:
          For each start square that needs filling, find the closest matching
          piece anywhere on the board or in the capture zones and send it there.
          Pieces already on their correct start square are never touched.
          Processing order: nearest-source-first so each piece naturally claims
          its own home square before a more distant square steals it.
        """
        packets = []
        working = dict(self._locations)

        def col_to_int(c):
            return ord(c) - ord('a') + 1

        def distance(pos1, pos2):
            return (abs(col_to_int(pos1[0]) - col_to_int(pos2[0]))
                    + abs(pos1[1] - pos2[1]))

        def add_packet(src_col, src_row, dst_col, dst_row, pt, color):
            desc = (f"Reset: {chess.piece_name(pt)} "
                    f"{'W' if color == chess.WHITE else 'B'} "
                    f"{src_col}{src_row}→{dst_col}{dst_row}")
            packets.append((src_col, src_row, dst_col, dst_row, desc))
            if (src_col, src_row) in working:
                del working[(src_col, src_row)]
            working[(dst_col, dst_row)] = (pt, color)

        # Mark squares already correctly occupied — never touch these
        correctly_placed = set()
        for dst, (pt, color) in _START_POSITIONS.items():
            if working.get(dst) == (pt, color):
                correctly_placed.add(dst)

        # Build list of start squares that need filling
        needs_filling = [
            (dst, pt, color)
            for dst, (pt, color) in _START_POSITIONS.items()
            if dst not in correctly_placed
        ]

        # Process iteratively — on each pass find the unfilled start square
        # whose nearest available source is closest, fill it, then repeat.
        # Re-evaluating each iteration prevents stale sort keys causing wrong matches.
        remaining = list(needs_filling)

        while remaining:
            # Find the best (dst, src) pair: the unfilled square with the
            # globally closest available matching piece right now
            best_dst  = None
            best_src  = None
            best_dist = 999
            best_pt   = None
            best_col  = None

            for (dst_col, dst_row), pt, color in remaining:
                if working.get((dst_col, dst_row)) == (pt, color):
                    correctly_placed.add((dst_col, dst_row))
                    continue
                candidates = [
                    pos for pos, (t, c) in working.items()
                    if t == pt and c == color
                    and pos not in correctly_placed
                    and pos != (dst_col, dst_row)
                ]
                if not candidates:
                    continue
                src = min(candidates,
                          key=lambda pos: (distance(pos, (dst_col, dst_row)),
                                           pos[1] >= 9,        # prefer main board
                                           col_to_int(pos[0]))) # then file order
                d = distance(src, (dst_col, dst_row))
                # Tiebreak: prefer main-board source, then closest dst file
                is_capture_zone = src[1] >= 9
                dst_file = col_to_int(dst_col)
                candidate_key = (d, is_capture_zone, dst_file)
                best_key = (best_dist,
                            best_src[1] >= 9 if best_src else True,
                            col_to_int(best_dst[0]) if best_dst else 999)
                if candidate_key < best_key:
                    best_dist = d
                    best_dst  = (dst_col, dst_row)
                    best_src  = src
                    best_pt   = pt
                    best_col  = color

            if best_dst is None:
                break   # nothing left to fill

            # Apply the best move found this iteration
            add_packet(best_src[0], best_src[1],
                       best_dst[0], best_dst[1],
                       best_pt, best_col)
            correctly_placed.add(best_dst)

            # Remove from remaining (filter out filled and no-candidate entries)
            remaining = [
                item for item in remaining
                if item[0] not in correctly_placed
            ]

        return packets
