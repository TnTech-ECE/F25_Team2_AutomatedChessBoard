"""
display.py — Pygame display for Voice Chess (800 × 480)

Usage in main script:
    from display import Display
    disp = Display()
    disp.set_status("White to move")
    disp.log_move(1, "e2e4", "e7e5")
    disp.set_message("Listening...", kind="info")
    disp.update_board(board)          # pass a chess.Board object
    disp.log_binary("e2e4", "0101 0010", "0101 0100")
    # On exit:
    disp.quit()
"""

import threading
import queue
import chess
import sys

try:
    import pygame
except ImportError:
    print("pygame not found — run: pip install pygame", file=sys.stderr)
    raise

# ── Layout constants (800 × 480) ──────────────────────────────────────────────
W, H          = 800, 480
BOARD_PX      = 368          # board square width/height (fits 8×46 squares)
SQ            = BOARD_PX // 8
BOARD_X       = 8            # left margin for board
BOARD_Y       = 8
RIGHT_X       = BOARD_X + BOARD_PX + 12   # x-start of right panel
RIGHT_W       = W - RIGHT_X - 8           # width of right panel

STATUS_H      = 40
HISTORY_Y     = BOARD_Y + STATUS_H + 6
HISTORY_H     = 160
MSG_Y         = HISTORY_Y + HISTORY_H + 6
MSG_H         = H - MSG_Y - 8
MSG_LINE_H    = 20
MSG_MAX_LINES = (MSG_H - 32) // MSG_LINE_H

# Captured pieces panel — sits below the board
CAP_Y         = BOARD_Y + BOARD_PX + 18   # below board + coord labels
CAP_H         = H - CAP_Y - 8             # ~78px remaining
CAP_W         = BOARD_PX                  # same width as the board

# Standard piece point values
PIECE_POINTS = {
    chess.PAWN:   1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK:   5,
    chess.QUEEN:  9,
    chess.KING:   0,
}

# ── Palette ───────────────────────────────────────────────────────────────────
BG            = (18,  18,  20)
PANEL         = (30,  30,  34)
BORDER        = (60,  60,  66)
TEXT_PRI      = (220, 218, 210)
TEXT_SEC      = (130, 128, 120)
TEXT_MONO     = (170, 230, 170)
SQ_LIGHT      = (240, 217, 181)
SQ_DARK       = (181, 136,  99)
HIGHLIGHT     = (255, 215,   0)   # last-move highlight
WHITE_PIECE   = (245, 245, 240)
BLACK_PIECE   = ( 30,  30,  30)
PIECE_OUTLINE = (100, 100, 100)

MSG_COLORS = {
    "info":    ((40,  80, 140), (120, 180, 255)),
    "success": ((30,  90,  50), (100, 220, 130)),
    "error":   ((120, 30,  30), (255, 110, 110)),
    "warn":    ((110, 80,   0), (240, 190,  60)),
    "neutral": ((50,  50,  55), TEXT_SEC),
}

# Unicode piece glyphs — always use the solid (filled) black variant index 1
# for rendering. Color of the piece is conveyed by the draw color, not the glyph shape.
# White outline glyphs (♙♖etc) render hollow in most fonts; solid glyphs (♟♜etc)
# filled with WHITE_PIECE color look fully white on the board.
GLYPHS = {
    chess.PAWN:   ("♟", "♟"),
    chess.ROOK:   ("♜", "♜"),
    chess.KNIGHT: ("♞", "♞"),
    chess.BISHOP: ("♝", "♝"),
    chess.QUEEN:  ("♛", "♛"),
    chess.KING:   ("♚", "♚"),
}


class Display:
    """
    Thread-safe Pygame display.  All drawing happens on the main thread via an
    internal command queue; call public methods from any thread.
    """

    def __init__(self):
        self._q: queue.Queue = queue.Queue()
        self._state = {
            "board":      chess.Board(),
            "last_move":  None,
            "status":     "Ready",
            "status_sub": "",
            "history":    [],          # list of (move_no, white_uci, black_uci|"")
            "binary":     ("", "", ""),# (uci, src_bits, dst_bits)
            "messages":   [("Microphone active. Listening…", "info")],  # rolling log
        }
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        # Wait for Pygame to initialise before returning
        self._ready = threading.Event()
        self._ready.wait()

    # ── Public API (thread-safe) ──────────────────────────────────────────────

    def update_board(self, board: chess.Board, last_move=None):
        """Push a new board state.  last_move is a chess.Move or None."""
        import copy
        self._q.put(("board", copy.copy(board), last_move))

    def set_status(self, text: str, sub: str = ""):
        """Top-right banner: e.g. 'White to move', sub='Stockfish Elo 1350'."""
        self._q.put(("status", text, sub))

    def log_move(self, move_no: int, white_uci: str, black_uci: str = ""):
        """Append a move pair to the history log."""
        self._q.put(("move", move_no, white_uci, black_uci))

    def log_binary(self, uci: str, src_bits: str, dst_bits: str):
        """Display the binary encoding of the last move."""
        self._q.put(("binary", uci, src_bits, dst_bits))

    def clear_log(self):
        """Clear the move history, binary display, and message log."""
        self._q.put(("clear_log",))

    def set_message(self, text: str, kind: str = "info"):
        """Append to the message log.  kind: 'info' | 'success' | 'error' | 'warn' | 'neutral'"""
        self._q.put(("message", text, kind))

    def quit(self):
        self._q.put(("quit",))
        self._thread.join(timeout=3)

    # ── Internal render loop (main thread) ───────────────────────────────────

    def _run(self):
        pygame.init()
        # Try true fullscreen first; fall back to a borderless window
        try:
            self._screen = pygame.display.set_mode(
                (W, H), pygame.FULLSCREEN | pygame.NOFRAME
            )
        except Exception:
            self._screen = pygame.display.set_mode((W, H))

        pygame.display.set_caption("Voice Chess")
        pygame.mouse.set_visible(False)

        # Fonts — fall back gracefully if a system font is missing
        def _font(size, bold=False, mono=False):
            families = (
                ["DejaVu Sans Mono", "Courier New", "monospace"] if mono
                else ["DejaVu Sans", "Liberation Sans", "Arial", "sans-serif"]
            )
            for fam in families:
                try:
                    return pygame.font.SysFont(fam, size, bold=bold)
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        self._fnt_piece   = _font(36, mono=True)   # chess glyphs
        self._fnt_label   = _font(14)              # board coordinates
        self._fnt_body    = _font(17)
        self._fnt_body_b  = _font(17, bold=True)
        self._fnt_mono    = _font(15, mono=True)
        self._fnt_head    = _font(19, bold=True)
        self._fnt_msg     = _font(18)

        self._ready.set()
        clock = pygame.time.Clock()

        while True:
            # Drain the command queue
            try:
                while True:
                    cmd = self._q.get_nowait()
                    self._apply(cmd)
                    if cmd[0] == "quit":
                        pygame.quit()
                        return
            except queue.Empty:
                pass

            # Handle window close (useful during dev with a regular window)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            self._draw()
            pygame.display.flip()
            clock.tick(30)

    def _apply(self, cmd):
        k = cmd[0]
        s = self._state
        if k == "board":
            s["board"]     = cmd[1]
            s["last_move"] = cmd[2]
        elif k == "status":
            s["status"]     = cmd[1]
            s["status_sub"] = cmd[2]
        elif k == "move":
            _, no, w, b = cmd
            # Update existing entry for this move number, or append
            for i, (n, _, _) in enumerate(s["history"]):
                if n == no:
                    s["history"][i] = (no, w, b)
                    break
            else:
                s["history"].append((no, w, b))
            # Keep only the last 10 moves
            if len(s["history"]) > 10:
                s["history"] = s["history"][-10:]
        elif k == "binary":
            s["binary"] = (cmd[1], cmd[2], cmd[3])
        elif k == "clear_log":
            s["history"]  = []
            s["binary"]   = ("", "", "")
            s["messages"] = []
        elif k == "message":
            s["messages"].append((cmd[1], cmd[2]))
            # Keep a reasonable buffer; display will show the last MSG_MAX_LINES
            if len(s["messages"]) > 60:
                s["messages"] = s["messages"][-60:]

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _draw(self):
        scr = self._screen
        scr.fill(BG)
        self._draw_board()
        self._draw_captured()
        self._draw_status()
        self._draw_history()
        self._draw_message()

    def _panel(self, x, y, w, h, color=PANEL, radius=6):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, w, h), border_radius=radius)
        pygame.draw.rect(surf, BORDER, (0, 0, w, h), width=1, border_radius=radius)
        self._screen.blit(surf, (x, y))

    def _text(self, font, text, color, x, y, anchor="topleft"):
        surf = font.render(str(text), True, color)
        r = surf.get_rect(**{anchor: (x, y)})
        self._screen.blit(surf, r)

    # Board
    def _draw_board(self):
        board      = self._state["board"]
        last_move  = self._state["last_move"]
        last_sqs   = set()
        if last_move:
            last_sqs = {last_move.from_square, last_move.to_square}

        for rank in range(7, -1, -1):
            for file in range(8):
                sq      = chess.square(file, rank)
                px      = BOARD_X + file * SQ
                py      = BOARD_Y + (7 - rank) * SQ
                is_dark = (rank + file) % 2 == 0
                base    = SQ_DARK if is_dark else SQ_LIGHT
                if sq in last_sqs:
                    col = (
                        (min(base[0] + 40, 255),
                         min(base[1] + 40, 255),
                         min(base[2] - 20, 255))
                    )
                else:
                    col = base
                pygame.draw.rect(self._screen, col, (px, py, SQ, SQ))

                piece = board.piece_at(sq)
                if piece:
                    glyph = GLYPHS[piece.piece_type][0 if piece.color == chess.WHITE else 1]
                    col_p = WHITE_PIECE if piece.color == chess.WHITE else BLACK_PIECE
                    surf  = self._fnt_piece.render(glyph, True, col_p)
                    cx    = px + (SQ - surf.get_width())  // 2
                    cy    = py + (SQ - surf.get_height()) // 2
                    self._screen.blit(surf, (cx, cy))

        # Coordinate labels (outside board)
        files = "abcdefgh"
        for i, lbl in enumerate(files):
            self._text(self._fnt_label, lbl, TEXT_SEC,
                       BOARD_X + i * SQ + SQ // 2,
                       BOARD_Y + BOARD_PX + 2, anchor="midtop")
        for rank in range(8):
            self._text(self._fnt_label, str(rank + 1), TEXT_SEC,
                       BOARD_X - 2,
                       BOARD_Y + (7 - rank) * SQ + SQ // 2, anchor="midright")

    # Captured pieces + material advantage
    def _draw_captured(self):
        board = self._state["board"]

        # Count captured pieces by comparing starting counts to what's on the board
        start_counts = {
            chess.PAWN:   8, chess.ROOK: 2, chess.KNIGHT: 2,
            chess.BISHOP: 2, chess.QUEEN: 1, chess.KING: 1,
        }
        on_board = {chess.WHITE: {}, chess.BLACK: {}}
        for sq in chess.SQUARES:
            p = board.piece_at(sq)
            if p:
                on_board[p.color][p.piece_type] = on_board[p.color].get(p.piece_type, 0) + 1

        captured = {chess.WHITE: {}, chess.BLACK: {}}  # captured[color] = pieces that color lost
        for color in (chess.WHITE, chess.BLACK):
            for pt, start in start_counts.items():
                on = on_board[color].get(pt, 0)
                lost = start - on
                if lost > 0:
                    captured[color][pt] = lost

        # Material score (positive = white ahead)
        white_pts = sum(PIECE_POINTS[pt] * n for pt, n in captured[chess.BLACK].items())
        black_pts = sum(PIECE_POINTS[pt] * n for pt, n in captured[chess.WHITE].items())
        advantage = white_pts - black_pts

        self._panel(BOARD_X, CAP_Y, CAP_W, CAP_H)

        # Piece order: most valuable first
        order = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN]

        row_h    = (CAP_H - 8) // 2
        glyph_sz = 16   # small glyph size for captured display

        for row, (color, lost_color) in enumerate(
            [(chess.WHITE, chess.WHITE), (chess.BLACK, chess.BLACK)]
        ):
            # 'captured[color]' = pieces that *this color* lost
            # so we show white's losses on white's row using black glyphs, and vice versa
            ry       = CAP_Y + 4 + row * row_h
            cx       = BOARD_X + 8
            label     = "Black's captured:" if color == chess.WHITE else "White's captured:"
            self._text(self._fnt_label, label, TEXT_SEC, cx, ry + row_h // 2 - 7)
            cx += self._fnt_label.size(label)[0] + 8

            total_pts = 0
            for pt in order:
                count = captured[color].get(pt, 0)
                if count == 0:
                    continue
                # glyph: show the piece type that was captured (opposite color glyph)
                glyph     = GLYPHS[pt][1 if color == chess.WHITE else 0]
                glyph_col = WHITE_PIECE if color == chess.WHITE else (0, 0, 0)
                surf = self._fnt_label.render(glyph * count, True, glyph_col)
                self._screen.blit(surf, (cx, ry + row_h // 2 - surf.get_height() // 2))
                cx += surf.get_width() + 4
                total_pts += PIECE_POINTS[pt] * count

            # Advantage indicator on the winning side's row
            if advantage > 0 and color == chess.BLACK:
                self._text(self._fnt_label, f"+{advantage}", (100, 220, 130),
                           cx + 4, ry + row_h // 2 - 7)
            elif advantage < 0 and color == chess.WHITE:
                self._text(self._fnt_label, f"+{abs(advantage)}", (100, 220, 130),
                           cx + 4, ry + row_h // 2 - 7)

    # Status bar (top-right)
    def _draw_status(self):
        x, y, w, h = RIGHT_X, BOARD_Y, RIGHT_W, STATUS_H
        self._panel(x, y, w, h)
        self._text(self._fnt_body_b, self._state["status"], TEXT_PRI,
                   x + 10, y + h // 2, anchor="midleft")
        sub = self._state["status_sub"]
        if sub:
            self._text(self._fnt_label, sub, TEXT_SEC,
                       x + w - 10, y + h // 2, anchor="midright")

    # Move history
    def _draw_history(self):
        x, y, w, h = RIGHT_X, HISTORY_Y, RIGHT_W, HISTORY_H
        self._panel(x, y, w, h)
        self._text(self._fnt_head, "Move history", TEXT_PRI, x + 10, y + 8)
        pygame.draw.line(self._screen, BORDER, (x, y + 30), (x + w, y + 30))

        row_h = 22
        col_w = (w - 20) // 3   # no., white, black

        for i, (no, white, black) in enumerate(reversed(self._state["history"])):
            ry = y + 36 + i * row_h
            if ry + row_h > y + h - 4:
                break
            self._text(self._fnt_label, f"{no}.", TEXT_SEC,  x + 10,           ry)
            self._text(self._fnt_body,  white,    TEXT_PRI,  x + 10 + col_w,   ry)
            if black:
                self._text(self._fnt_body, black, TEXT_PRI,  x + 10 + col_w*2, ry)

    # Message log
    def _draw_message(self):
        x, y, w, h = RIGHT_X, MSG_Y, RIGHT_W, MSG_H
        self._panel(x, y, w, h)
        self._text(self._fnt_head, "Log", TEXT_PRI, x + 10, y + 6)
        pygame.draw.line(self._screen, BORDER, (x, y + 28), (x + w, y + 28))

        # Show the most recent MSG_MAX_LINES entries, newest at the bottom
        visible = self._state["messages"][-MSG_MAX_LINES:]
        dot_colors = {
            "info":    (120, 180, 255),
            "success": (100, 220, 130),
            "error":   (255, 110, 110),
            "warn":    (240, 190,  60),
            "neutral": (130, 128, 120),
        }

        for i, (text, kind) in enumerate(visible):
            ry = y + 34 + i * MSG_LINE_H
            dot_col = dot_colors.get(kind, dot_colors["neutral"])
            fg_col  = dot_col

            # Coloured dot
            pygame.draw.circle(self._screen, dot_col,
                               (x + 16, ry + MSG_LINE_H // 2), 4)

            # Text — truncate with ellipsis if it overflows the panel width
            max_w = w - 32
            rendered = text
            surf = self._fnt_label.render(rendered, True, fg_col)
            while surf.get_width() > max_w and len(rendered) > 4:
                rendered = rendered[:-4] + "…"
                surf = self._fnt_label.render(rendered, True, fg_col)
            self._screen.blit(surf, (x + 26, ry + (MSG_LINE_H - surf.get_height()) // 2))
