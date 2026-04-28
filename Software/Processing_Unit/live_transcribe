import sys
import queue
import threading
import subprocess
import time
import sounddevice as sd
import vosk
import json
import chess
import chess.engine
from display import Display
from piece_tracker import PieceTracker

vosk.SetLogLevel(-1)

# ── Display ───────────────────────────────────────────────────────────────────
disp = Display()

# ── Piece tracker (serial) ────────────────────────────────────────────────────
# Set ARDUINO_CONNECTED = True when the Arduino is physically connected.
# False uses a short timeout so testing without hardware doesn't freeze.
ARDUINO_CONNECTED = True
_ack_timeout = 30.0 if ARDUINO_CONNECTED else 0.5

tracker = PieceTracker(port="/dev/serial0", baud=115200, ack_timeout=_ack_timeout)
tracker.set_display_callback(disp.set_message)

# ── Vosk setup ────────────────────────────────────────────────────────────────
model_path = "vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)

audio_q = queue.Queue()
move_q  = queue.Queue()

samplerate = 48000
device     = 1
channels   = 1

grammar = [
    "a", "b", "c", "d", "e", "f", "g", "h",
    "one", "two", "three", "four", "five", "six", "seven", "eight",
    "resign", "chess", "move", "redo", "castle", "short", "long",
    "white", "black",
    "yes", "no",
    "queen", "rook", "bishop", "knight", "king",
    "takes", "to",
]

num_map = {
    "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8"
}

# ── SAN voice parsing ─────────────────────────────────────────────────────────
_FILE_WORDS  = set("abcdefgh")
_SAN_PIECE_MAP = {
    "knight": chess.KNIGHT,
    "bishop": chess.BISHOP,
    "rook":   chess.ROOK,
    "queen":  chess.QUEEN,
    "king":   chess.KING,
}
# All words that can legally appear in a spoken SAN move (after wake word)
_SAN_VOCAB = (
    _FILE_WORDS
    | set(num_map.keys())        # one..eight
    | set("12345678")            # in case already converted
    | set(_SAN_PIECE_MAP.keys())
    | {"takes", "to", "check"}
)

def _san_candidates(board, piece_type, to_sq,
                    disambig_file=None, disambig_rank=None,
                    capture_required=False):
    """Filter legal_moves to those matching the given criteria."""
    result = []
    for m in board.legal_moves:
        p = board.piece_at(m.from_square)
        if not p:
            continue
        if piece_type is not None and p.piece_type != piece_type:
            continue
        if m.to_square != to_sq:
            continue
        if capture_required and not board.is_capture(m):
            continue
        if disambig_file is not None:
            if chess.square_file(m.from_square) != ord(disambig_file) - ord('a'):
                continue
        if disambig_rank is not None:
            if chess.square_rank(m.from_square) != disambig_rank - 1:
                continue
        # Exclude promotion variants — those are handled separately
        if m.promotion and m.promotion != chess.QUEEN:
            continue
        result.append(m)
    return result

def _resolve(candidates, move_desc):
    """Return (move, error) from a candidate list."""
    if len(candidates) == 1:
        return candidates[0], None
    if len(candidates) == 0:
        return None, f"Illegal move: {move_desc}"
    # Ambiguous — tell the player what to specify
    from_names = sorted({chess.square_name(m.from_square)[0] for m in candidates})
    return None, f"Ambiguous — say which {move_desc}: {' or '.join(from_names)}"

def find_move_from_san_tokens(payload, board):
    """
    Convert a list of spoken SAN tokens into a chess.Move using legal_moves
    filtering.  Numbers are converted (one→1), 'to' and 'check' are stripped.
    Returns (chess.Move, None) on success or (None, error_str) on failure.
    """
    # Convert word numbers, strip 'to' and 'check'
    tokens = [num_map.get(t, t) for t in payload
              if t not in ("to", "check")]

    if not tokens:
        return None, "Empty move"

    # ── Piece present? ────────────────────────────────────────────────────
    piece_type = _SAN_PIECE_MAP.get(tokens[0])

    if piece_type is None:
        # ── PAWN move ────────────────────────────────────────────────────
        if "takes" in tokens:
            # e takes d 5  →  [src_file, "takes", dst_file, dst_rank]
            if (len(tokens) == 4 and tokens[1] == "takes"
                    and tokens[0] in _FILE_WORDS
                    and tokens[2] in _FILE_WORDS
                    and tokens[3].isdigit()):
                try:
                    to_sq = chess.parse_square(tokens[2] + tokens[3])
                except ValueError:
                    return None, "Invalid destination square"
                src_file = tokens[0]
                cands = _san_candidates(board, chess.PAWN, to_sq,
                                        disambig_file=src_file,
                                        capture_required=True)
                return _resolve(cands, f"pawn {src_file}x{tokens[2]}{tokens[3]}")
            return None, "Invalid pawn capture — say 'move e takes d five'"

        # Simple pawn destination: e 4
        if (len(tokens) == 2 and tokens[0] in _FILE_WORDS
                and tokens[1].isdigit()):
            try:
                to_sq = chess.parse_square(tokens[0] + tokens[1])
            except ValueError:
                return None, "Invalid destination square"
            cands = _san_candidates(board, chess.PAWN, to_sq)
            # For promotion squares, return base move — caller checks promotion
            if not cands:
                # Check if it would be a promotion
                for suffix in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT):
                    pm = chess.Move.null()
                    for m in board.legal_moves:
                        if (m.to_square == to_sq
                                and board.piece_at(m.from_square)
                                and board.piece_at(m.from_square).piece_type == chess.PAWN
                                and m.promotion == suffix):
                            cands = [m]
                            break
                    if cands:
                        break
            return _resolve(cands, f"pawn to {tokens[0]}{tokens[1]}")

        return None, "Invalid pawn move — say 'move e four'"

    # ── PIECE move ────────────────────────────────────────────────────────
    rest = tokens[1:]   # everything after the piece name
    is_capture = "takes" in rest
    rest = [t for t in rest if t != "takes"]

    # rest is now one of:
    #   [dst_file, dst_rank]                      — no disambiguation
    #   [disambig_file_or_rank, dst_file, dst_rank] — disambiguated
    dst_file       = None
    dst_rank_str   = None
    disambig_file  = None
    disambig_rank  = None

    if len(rest) == 2 and rest[0] in _FILE_WORDS and rest[1].isdigit():
        dst_file, dst_rank_str = rest[0], rest[1]

    elif len(rest) == 3 and rest[1] in _FILE_WORDS and rest[2].isdigit():
        disambig = rest[0]
        dst_file, dst_rank_str = rest[1], rest[2]
        if disambig in _FILE_WORDS:
            disambig_file = disambig
        elif disambig.isdigit():
            disambig_rank = int(disambig)
        else:
            return None, f"Invalid disambiguation '{disambig}'"
    else:
        pname = [k for k, v in _SAN_PIECE_MAP.items() if v == piece_type][0]
        return None, f"Invalid {pname} move format"

    try:
        to_sq = chess.parse_square(dst_file + dst_rank_str)
    except ValueError:
        return None, f"Invalid destination {dst_file}{dst_rank_str}"

    pname = [k for k, v in _SAN_PIECE_MAP.items() if v == piece_type][0]
    cands = _san_candidates(board, piece_type, to_sq,
                            disambig_file=disambig_file,
                            disambig_rank=disambig_rank,
                            capture_required=is_capture)
    return _resolve(cands, f"{pname} to {dst_file}{dst_rank_str}")


def is_san_payload(payload):
    """Return True if payload looks like SAN (not a coordinate or castle)."""
    converted = [num_map.get(t, t) for t in payload]
    # Existing 4-token coordinate: letter digit letter digit
    if (len(converted) == 4
            and converted[0] in _FILE_WORDS
            and converted[1].isdigit()
            and converted[2] in _FILE_WORDS
            and converted[3].isdigit()):
        return False
    # Castle commands
    if len(payload) == 1 and payload[0] in ("castle", "short", "long"):
        return False
    # Single resign-like token
    if len(payload) == 1 and payload[0] == "resign":
        return False
    # Check if all tokens are SAN vocabulary
    return bool(payload) and all(t in _SAN_VOCAB for t in payload)

# ── Promotion helpers ─────────────────────────────────────────────────────────
_PIECE_NAME_MAP = {
    "queen":  (chess.QUEEN,  "q"),
    "rook":   (chess.ROOK,   "r"),
    "bishop": (chess.BISHOP, "b"),
    "knight": (chess.KNIGHT, "n"),
}
_PIECE_DISPLAY = {
    chess.QUEEN:  "Q",
    chess.ROOK:   "R",
    chess.BISHOP: "B",
    chess.KNIGHT: "N",
}

def is_promotion_attempt(user_input, board):
    """Return True if user_input is a 4-char UCI that leads to a promotion square."""
    if len(user_input) != 4:
        return False
    try:
        for suffix in ["q", "r", "b", "n"]:
            move = chess.Move.from_uci(user_input + suffix)
            if move in board.legal_moves:
                return True
    except ValueError:
        pass
    return False

def handle_promotion(uci_base, board):
    """
    Show available promotion pieces, listen for player choice.
    Returns (chess.Move, piece_type) or (None, None) if unavailable.
    """
    color     = board.turn
    available = tracker.get_available_promotion_pieces(color)

    if not available:
        msg = "No pieces to promote — opponent must capture above pawn"
        print(msg)
        disp.set_message(msg, kind="error")
        return None, None

    avail_str = " ".join(
        _PIECE_DISPLAY[pt] for pt in
        [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        if pt in available
    )
    prompt = f"Promote to? Available: {avail_str}"
    print(prompt)
    disp.set_status("Promotion!")
    disp.set_message(prompt, kind="info")

    while True:
        choice = get_voice("promote")
        if choice not in _PIECE_NAME_MAP:
            disp.set_message(f"Say: move queen/rook/bishop/knight. Available: {avail_str}",
                             kind="warn")
            continue
        pt, suffix = _PIECE_NAME_MAP[choice]
        if pt not in available:
            disp.set_message(
                f"{choice.capitalize()} not available. Available: {avail_str}",
                kind="error")
            continue
        try:
            move = chess.Move.from_uci(uci_base + suffix)
            if move in board.legal_moves:
                return move, pt
        except ValueError:
            pass
        disp.set_message("Invalid promotion — try again", kind="error")

def get_stockfish_promotion_piece(color):
    """
    Return the best available promotion piece for Stockfish.
    Prefers queen, falls back down the priority list.
    Returns None if nothing is available.
    """
    available = tracker.get_available_promotion_pieces(color)
    for pt in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
        if pt in available:
            return pt
    return None

# All 4 castling UCIs — kingside preferred when both are legal
def resolve_castle_input(user_input, board):
    """
    Translate a castle voice command into a UCI string.
    Returns (uci_string, error_message) — one will be None.
    """
    if user_input == "castle-kingside":
        uci = resolve_castle(board, preference="kingside")
        if uci is None:
            return None, "Kingside castling not available"
        return uci, None

    if user_input == "castle-queenside":
        uci = resolve_castle(board, preference="queenside")
        if uci is None:
            return None, "Queenside castling not available"
        return uci, None

    if user_input == "castle":
        uci = resolve_castle(board)
        if uci is None:
            # Check if both are available — need player to specify
            legal_ucis = {m.uci() for m in board.legal_moves}
            white = board.turn == chess.WHITE
            ks = "e1g1" if white else "e8g8"
            qs = "e1c1" if white else "e8c8"
            if ks in legal_ucis and qs in legal_ucis:
                return None, "Both castles available — say 'move short' or 'move long'"
            return None, "No castling available"
        return uci, None

    return user_input, None   # not a castle command, pass through unchanged

def resolve_castle(board, preference=None):
    """
    Return the UCI string for the requested castling move, or None.
    preference: 'kingside', 'queenside', or None (auto).
    If both are legal and no preference given, returns None and the caller
    should ask the player to specify.
    """
    legal_ucis  = {m.uci() for m in board.legal_moves}
    white       = board.turn == chess.WHITE
    kingside    = "e1g1" if white else "e8g8"
    queenside   = "e1c1" if white else "e8c8"
    ks_ok       = kingside  in legal_ucis
    qs_ok       = queenside in legal_ucis

    if preference == "kingside":
        return kingside if ks_ok else None
    if preference == "queenside":
        return queenside if qs_ok else None

    # No preference — only valid if exactly one option is available
    if ks_ok and not qs_ok:
        return kingside
    if qs_ok and not ks_ok:
        return queenside
    return None   # both available — caller must ask player to specify

# ── Move → binary encoding ────────────────────────────────────────────────────
_col_bits = {"a":"0001","b":"0010","c":"0011","d":"0100",
             "e":"0101","f":"0110","g":"0111","h":"1000"}
_row_bits = {"1":"0001","2":"0010","3":"0011","4":"0100",
             "5":"0101","6":"0110","7":"0111","8":"1000"}

def move_to_binary(uci):
    src = _col_bits[uci[0]] + _row_bits[uci[1]]
    dst = _col_bits[uci[2]] + _row_bits[uci[3]]
    return src, dst

def print_move_binary(uci, label=""):
    src, dst = move_to_binary(uci)
    tag = f"[{label}] " if label else ""
    print(f"  {tag}{uci} -> {src} {dst}")
    disp.log_binary(uci, src, dst)

def announce_check(board):
    """Print check or checkmate status after a move."""
    if board.is_checkmate():
        print("*** CHECKMATE! ***")
        disp.set_message("CHECKMATE!", kind="error")
    elif board.is_check():
        in_check = "White" if board.turn == chess.WHITE else "Black"
        print(f"*** CHECK! {in_check} is in check! ***")
        disp.set_message(f"CHECK! {in_check} is in check!", kind="warn")

def check_draw_claim(board):
    """
    Returns True and updates display if a draw can be claimed.
    Covers threefold repetition and fifty-move rule.
    The game loop should break when this returns True.
    """
    if board.is_repetition(3):
        print("*** DRAW — Threefold repetition! ***")
        disp.set_status("Game over — Draw!")
        disp.set_message("Draw: threefold repetition", kind="neutral")
        return True
    if board.can_claim_fifty_moves():
        print("*** DRAW — Fifty move rule! ***")
        disp.set_status("Game over — Draw!")
        disp.set_message("Draw: fifty move rule", kind="neutral")
        return True
    return False

vosk_paused = threading.Event()   # set = recognition paused, clear = running

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    if not vosk_paused.is_set():
        audio_q.put(bytes(indata))

# ── Listen mode state ─────────────────────────────────────────────────────────
listen_mode = "move"
listen_lock = threading.Lock()

def set_mode(mode):
    global listen_mode
    with listen_lock:
        listen_mode = mode

def get_mode():
    with listen_lock:
        return listen_mode

def process_text(text):
    tokens = text.split()
    if not tokens:
        return None
    mode = get_mode()

    if mode == "players":
        if tokens[0] != "chess":
            return None
        elif "one" in tokens:
            return "1"
        elif "two" in tokens:
            return "2"

    elif mode == "colour":
        if tokens[0] != "chess":
            return None
        elif "white" in tokens:
            return "white"
        elif "black" in tokens:
            return "black"

    elif mode == "yesno":
        if tokens[0] != "chess":
            return None
        elif "yes" in tokens:
            return "yes"
        elif "no" in tokens:
            return "no"

    elif mode == "promote":
        if tokens[0] != "move":
            return None
        payload = tokens[1:]
        if len(payload) == 1 and payload[0] in _PIECE_NAME_MAP:
            return payload[0]

    elif mode == "move":
        if tokens[0] == "move":
            payload   = tokens[1:]
            converted = [num_map.get(t, t) for t in payload]
            # Existing coordinate: exactly 4 tokens forming letter-digit-letter-digit
            if (len(converted) == 4
                    and converted[0] in _FILE_WORDS and converted[1].isdigit()
                    and converted[2] in _FILE_WORDS and converted[3].isdigit()):
                return "".join(converted)
            # Castle commands
            if len(payload) == 1:
                if payload[0] == "castle":
                    return "castle"
                if payload[0] == "short":
                    return "castle-kingside"
                if payload[0] == "long":
                    return "castle-queenside"
            # SAN: anything else whose tokens are all SAN vocabulary
            if is_san_payload(payload):
                return "san:" + " ".join(payload)  # raw words for board-aware parsing
        elif tokens[0] == "chess":
            payload = tokens[1:]
            if len(payload) == 1 and payload[0] == "resign":
                return payload[0]

    return None

def recognition_thread():
    rec = vosk.KaldiRecognizer(model, samplerate, json.dumps(grammar))
    last_result_time = time.time()
    WATCHDOG_TIMEOUT = 15.0   # seconds of silence before resetting Vosk

    while True:
        data = audio_q.get()
        if data is None:
            break

        # Watchdog — if Vosk has been silent too long, recreate the recogniser
        if time.time() - last_result_time > WATCHDOG_TIMEOUT:
            print("[Vosk] Watchdog triggered — resetting recogniser")

            # Pause the audio callback so no new frames arrive during recovery
            vosk_paused.set()

            # Drain everything currently in the queue
            while not audio_q.empty():
                try:
                    audio_q.get_nowait()
                except queue.Empty:
                    break

            # Brief settle — let any in-flight overflow frames pass
            time.sleep(1.0)

            # Recreate recogniser with clean state
            rec = vosk.KaldiRecognizer(model, samplerate, json.dumps(grammar))
            last_result_time = time.time()

            # Resume audio
            vosk_paused.clear()
            print("[Vosk] Recogniser reset — listening again")
            continue

        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "").strip()
            last_result_time = time.time()   # reset watchdog on any result
            if text:
                print(f"[Vosk] '{text}'")
            result = process_text(text)
            if result:
                move_q.put(result)
        else:
            rec.PartialResult()   # drain partial to keep Vosk state clean

def get_voice(mode):
    while not move_q.empty():
        try:
            move_q.get_nowait()
        except queue.Empty:
            break
    set_mode(mode)
    while True:
        try:
            return move_q.get(timeout=0.5)
        except queue.Empty:
            continue

def ask(prompt, mode):
    print(prompt)
    disp.set_message(prompt, kind="info")
    answer = get_voice(mode)
    print(f"  → {answer}")
    return answer

def wait_for_physical(board, move, label):
    """
    1. Update the digital board immediately so the move is visible.
    2. Show 'Processing move...' in grey while the coreXY physically executes.
    3. Always block until the tracker queue is fully drained (queue.join).
    4. Flush stale audio that built up during the wait so Vosk is clean.
    5. Confirm completion in the message log.
    """
    disp.update_board(board, move)
    disp.set_message(f"{label} played {move.uci()}", kind="success")
    disp.set_status("Board moving...")
    disp.set_message("Processing move...", kind="neutral")

    tracker.wait_for_queue()

    # Flush audio and move queues — during a long physical wait (or ACK
    # timeout) the audio buffer fills with stale data that would confuse
    # Vosk. Clear both queues so the next get_voice() starts fresh.
    while not audio_q.empty():
        try:
            audio_q.get_nowait()
        except queue.Empty:
            break
    while not move_q.empty():
        try:
            move_q.get_nowait()
        except queue.Empty:
            break

    disp.set_status("")
    disp.set_message(f"{label} played {move.uci()} — done", kind="success")


def resolve_user_move(user_input, board):
    """
    Unified move resolver — handles coordinate UCI, SAN, and castle commands.
    Returns (chess.Move, promo_piece_type_or_None, error_str_or_None).
    Promotion detection is included so callers don't need to check separately.
    """
    # ── Castle ────────────────────────────────────────────────────────────
    if user_input in {"castle", "castle-kingside", "castle-queenside"}:
        uci, err = resolve_castle_input(user_input, board)
        if err:
            return None, None, err
        try:
            return chess.Move.from_uci(uci), None, None
        except ValueError:
            return None, None, f"Invalid castle UCI: {uci}"

    # ── SAN ───────────────────────────────────────────────────────────────
    if user_input.startswith("san:"):
        payload = user_input[4:].split()
        move, err = find_move_from_san_tokens(payload, board)
        if err:
            return None, None, err
        # Check if this is a promotion
        if move and move.promotion:
            uci_base = (chess.square_name(move.from_square)
                        + chess.square_name(move.to_square))
            promo_move, promo_pt = handle_promotion(uci_base, board)
            return promo_move, promo_pt, None if promo_move else (None, None, "Promotion cancelled")
        if move and is_promotion_attempt(
                chess.square_name(move.from_square) + chess.square_name(move.to_square),
                board):
            uci_base = (chess.square_name(move.from_square)
                        + chess.square_name(move.to_square))
            promo_move, promo_pt = handle_promotion(uci_base, board)
            if promo_move is None:
                return None, None, "Promotion not available"
            return promo_move, promo_pt, None
        return move, None, None

    # ── Coordinate UCI ────────────────────────────────────────────────────
    # Check promotion before regular move
    if is_promotion_attempt(user_input, board):
        promo_move, promo_pt = handle_promotion(user_input, board)
        if promo_move is None:
            return None, None, "Promotion not available"
        return promo_move, promo_pt, None

    try:
        move = chess.Move.from_uci(user_input)
        if move in board.legal_moves:
            return move, None, None
        return None, None, f"Illegal move: {user_input}"
    except ValueError:
        return None, None, f"Invalid format: {user_input}"

# ── Chess engine ──────────────────────────────────────────────────────────────
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
engine.configure({
    "UCI_LimitStrength": True,
    "UCI_Elo": 1350
})

def play_game():
    board = chess.Board()
    move_number = 1

    # ── Setup ──────────────────────────────────────────────────────────────
    disp.clear_log()
    disp.update_board(board)
    disp.set_status("Voice Chess", "Setting up…")

    mode = ask('How many players? Say "chess one" or "chess two".', "players")

    if mode == "1":
        side = ask('Play as white or black? EX: Say "chess white"', "colour")
        human_is_white = (side == "white")
        player_label = "White" if human_is_white else "Black"
        print(f"\n1-player | You are {player_label} | Stockfish Elo 1350")
        disp.set_status(f"You are {player_label}", "Stockfish Elo 1350")
    else:
        human_is_white = True   # unused in 2P but keeps the variable defined
        print("\n2-player | White goes first")
        disp.set_status("2-player game", "White goes first")

    print('Say "move e2e4" or "move knight f three" to make a move, "chess resign" to resign.\n')
    disp.set_message('Say "move e2e4" or "move knight f three".', kind="info")

    resigned = False

    # Track partial move pairs for the log
    pending_white = {}   # move_number -> white uci

    while not board.is_game_over():
        print(board)
        disp.update_board(board)
        whites_turn = (board.turn == chess.WHITE)

        if mode == "2":
            current_player = "White" if whites_turn else "Black"
            print(f"\n{current_player}'s turn — say your move...")
            disp.set_status(f"{current_player} to move")
            disp.set_message(f"{current_player}: say your move", kind="info")

            user_input = get_voice("move")

            if user_input in {"resign"}:
                print(f"{current_player} resigned!")
                disp.set_message(f"{current_player} resigned!", kind="error")
                resigned = True
                disp.set_status("Resetting board…")
                tracker.reset_board(board, log_fn=disp.set_message)
                break

            move, promo_pt, err = resolve_user_move(user_input, board)
            if err:
                print(f"{err}, try again.\n")
                disp.set_message(f"{err} — try again", kind="error")
                continue

            is_promo = promo_pt is not None
            if whites_turn:
                pending_white[move_number] = move.uci()
                if is_promo:
                    tracker.send_promotion(move, board, promo_pt)
                else:
                    tracker.send_capture(move, board)
                board.push(move)
                if not is_promo:
                    tracker.send_move(move, board)
                wait_for_physical(board, move, current_player)
                disp.log_move(move_number, move.uci())
            else:
                white_uci = pending_white.pop(move_number, "")
                if is_promo:
                    tracker.send_promotion(move, board, promo_pt)
                else:
                    tracker.send_capture(move, board)
                board.push(move)
                if not is_promo:
                    tracker.send_move(move, board)
                wait_for_physical(board, move, current_player)
                disp.log_move(move_number, white_uci, move.uci())
                move_number += 1
            label = "2P-PROMO" if is_promo else "2P"
            print_move_binary(move.uci()[:4], label)
            announce_check(board)
            if check_draw_claim(board):
                break

        else:  # 1-player
            human_turn = (whites_turn == human_is_white)

            if human_turn:
                print("\nYour turn — say your move...")
                disp.set_status("Your turn")
                disp.set_message("Listening for your move…", kind="info")

                user_input = get_voice("move")

                if user_input in {"resign"}:
                    print("You resigned. Stockfish wins.")
                    disp.set_message("You resigned. Stockfish wins.", kind="error")
                    resigned = True
                    disp.set_status("Resetting board…")
                    tracker.reset_board(board, log_fn=disp.set_message)
                    break

                move, promo_pt, err = resolve_user_move(user_input, board)
                if err:
                    print(f"{err}, try again.\n")
                    disp.set_message(f"{err} — try again", kind="error")
                    continue

                is_promo = promo_pt is not None
                if human_is_white:
                    pending_white[move_number] = move.uci()
                    if is_promo:
                        tracker.send_promotion(move, board, promo_pt)
                    else:
                        tracker.send_capture(move, board)
                    board.push(move)
                    if not is_promo:
                        tracker.send_move(move, board)
                    wait_for_physical(board, move, "You")
                    disp.log_move(move_number, move.uci())
                else:
                    white_uci = pending_white.pop(move_number, "")
                    if is_promo:
                        tracker.send_promotion(move, board, promo_pt)
                    else:
                        tracker.send_capture(move, board)
                    board.push(move)
                    if not is_promo:
                        tracker.send_move(move, board)
                    wait_for_physical(board, move, "You")
                    disp.log_move(move_number, white_uci, move.uci())
                    move_number += 1
                label = "Human-PROMO" if is_promo else "Human"
                print_move_binary(move.uci()[:4], label)
                announce_check(board)
                if check_draw_claim(board):
                    break

            else:
                print("\nStockfish is thinking...")
                disp.set_status("Stockfish thinking…", "Elo 1350")
                disp.set_message("Stockfish is thinking…", kind="neutral")

                result = engine.play(board, chess.engine.Limit(time=0.1))
                sf_move = result.move
                sf_uci  = sf_move.uci()
                print(f"Engine plays: {sf_move}")

                # Check if Stockfish is promoting
                if sf_move.promotion is not None:
                    # Find the best available piece (Stockfish's choice may not be available)
                    promo_pt = get_stockfish_promotion_piece(board.turn)
                    if promo_pt is None:
                        # No pieces available — promote to queen in logic only
                        # (physical board can't swap, just note it)
                        print("[Stockfish] WARNING: no pieces available for promotion")
                        disp.set_message("Stockfish promotes — no physical piece available",
                                         kind="warn")
                        promo_pt = sf_move.promotion
                    else:
                        # Rebuild move with the available piece if different
                        if promo_pt != sf_move.promotion:
                            sf_move = chess.Move(sf_move.from_square,
                                                 sf_move.to_square, promo_pt)
                            sf_uci  = sf_move.uci()
                    if human_is_white:
                        white_uci = pending_white.pop(move_number, "")
                        tracker.send_promotion(sf_move, board, promo_pt)
                        board.push(sf_move)
                        wait_for_physical(board, sf_move, "Stockfish")
                        disp.log_move(move_number, white_uci, sf_uci)
                        move_number += 1
                    else:
                        pending_white[move_number] = sf_uci
                        tracker.send_promotion(sf_move, board, promo_pt)
                        board.push(sf_move)
                        wait_for_physical(board, sf_move, "Stockfish")
                        disp.log_move(move_number, sf_uci)
                    print_move_binary(sf_uci[:4], "SF-PROMO")
                else:
                    if human_is_white:
                        white_uci = pending_white.pop(move_number, "")
                        tracker.send_capture(sf_move, board)
                        board.push(sf_move)
                        tracker.send_move(sf_move, board)
                        wait_for_physical(board, sf_move, "Stockfish")
                        disp.log_move(move_number, white_uci, sf_uci)
                        move_number += 1
                    else:
                        pending_white[move_number] = sf_uci
                        tracker.send_capture(sf_move, board)
                        board.push(sf_move)
                        tracker.send_move(sf_move, board)
                        wait_for_physical(board, sf_move, "Stockfish")
                        disp.log_move(move_number, sf_uci)
                    print_move_binary(sf_uci, "Stockfish")

                announce_check(board)
                if check_draw_claim(board):
                    break
    print("\n" + str(board))
    disp.update_board(board)

    if not resigned:
        # Claimed draw (threefold repetition or fifty-move rule) —
        # message already set by check_draw_claim, just set status
        if board.is_repetition(3) or board.can_claim_fifty_moves():
            disp.set_status("Game over — Draw!")
        elif board.is_game_over():
            outcome = board.outcome()
            if outcome.winner is None:
                print("\nIt's a draw!")
                disp.set_status("Game over — Draw!")
                disp.set_message("It's a draw!", kind="neutral")
            elif outcome.winner == chess.WHITE:
                print("\nWhite wins!")
                disp.set_status("Game over")
                disp.set_message("White wins!", kind="success")
            else:
                print("\nBlack wins!")
                disp.set_status("Game over")
                disp.set_message("Black wins!", kind="success")

        # Reset after natural game ending
        disp.set_status("Resetting board…")
        tracker.reset_board(board, log_fn=disp.set_message)

    return board, resigned

# ── Main ──────────────────────────────────────────────────────────────────────
rec_thread = threading.Thread(target=recognition_thread, daemon=True)
rec_thread.start()

# ── Wait for the USB microphone to be ready ───────────────────────────────────
# On boot the USB audio device may be enumerated but not yet fully initialised.
# Keep trying to open a short test stream until it succeeds.
def wait_for_mic(device, samplerate, channels, timeout=60, retry_delay=3):
    import time
    import subprocess

    print("Waiting for audio system to be ready...")
    disp.set_message("Waiting for microphone...", kind="neutral")
    deadline = time.time() + timeout

    # Step 1 — wait for PulseAudio to be running before touching the device
    while time.time() < deadline:
        try:
            result = subprocess.run(
                ["pactl", "info"],
                capture_output=True, timeout=3
            )
            if result.returncode == 0:
                print("  PulseAudio is running.")
                break
        except Exception:
            pass
        print(f"  PulseAudio not ready, retrying in {retry_delay}s...")
        time.sleep(retry_delay)
    else:
        print("  WARNING: PulseAudio did not start in time, continuing anyway.")

    # Step 2 — small fixed delay after PulseAudio confirms ready,
    # giving ALSA/PortAudio time to finish registering the device
    time.sleep(2)

    # Step 3 — probe the actual device with a short test stream
    while time.time() < deadline:
        try:
            test = sd.RawInputStream(
                samplerate=samplerate,
                blocksize=1024,
                dtype="int16",
                channels=channels,
                device=device,
            )
            test.start()
            time.sleep(0.5)
            test.stop()
            test.close()
            print("Microphone ready.")
            disp.set_message("Microphone ready.", kind="success")
            return True
        except Exception as e:
            print(f"  Mic not ready ({e}), retrying in {retry_delay}s...")
            disp.set_message(f"Mic not ready, retrying...", kind="warn")
            time.sleep(retry_delay)

    print("WARNING: microphone did not become ready in time, continuing anyway.")
    disp.set_message("Mic timeout — check connection", kind="error")
    return False

wait_for_mic(device, samplerate, channels)

# Open the main stream — retry a few times in case PulseAudio hiccups once more
import time as _time
_stream = None
for _attempt in range(10):
    try:
        _stream = sd.RawInputStream(
            samplerate=samplerate,
            blocksize=16000,
            dtype="int16",
            channels=channels,
            callback=audio_callback,
            device=device,
        )
        _stream.start()
        break
    except Exception as _e:
        print(f"  Stream open failed ({_e}), retrying in 3s...")
        _time.sleep(3)

if _stream is None:
    print("FATAL: could not open audio stream after retries. Exiting.")
    disp.quit()
    raise SystemExit(1)

with _stream:
    print("=== Voice Chess ===")
    print("Microphone active. Listening...\n")
    disp.set_status("Voice Chess", "Microphone active")
    disp.set_message("Microphone active. Listening…", kind="info")

    # Tell the Arduino the Pi is ready — clears the startup lockout
    tracker.send_ready_signal()

    while True:
        _, resigned = play_game()
        answer = ask('\nPlay again? Say "chess yes" or "chess no".', "yesno")
        if answer == "no":
            print("Thanks for playing! Shutting down...")
            disp.set_status("Shutting down…")
            disp.set_message("Thanks for playing! Goodbye.", kind="success")
            tracker.wait_for_queue()
            time.sleep(2)
            subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)
            break

engine.quit()
tracker.close()
disp.quit()
audio_q.put(None)
rec_thread.join()
