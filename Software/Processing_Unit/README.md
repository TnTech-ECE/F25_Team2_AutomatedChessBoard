# Voice Chess — Physical Board Controller

A voice-controlled chess system running on a Raspberry Pi 5. The player speaks moves aloud, the Pi validates them using python-chess. A Pygame display shows the board state, move history, and status messages in real time.

---

## What the Software Does

The system runs three concurrent threads:

- **Audio capture** — streams raw PCM audio from a USB microphone into a queue
- **Speech recognition** — Vosk processes audio chunks and recognises spoken chess commands
- **Game loop** — validates moves, runs Stockfish AI, and coordinates the physical board

Supported features:
- Voice move input using coordinate notation (`move e two e four`) or standard algebraic notation (`move knight f three`, `move e takes d five`)
- 1-player mode against Stockfish AI (Elo 1350) or 2-player local mode
- Physical piece movement via UART binary protocol to Arduino coreXY system
- Captured piece tracking with automatic capture zone management
- Castling, en passant, and promotion with physical piece swap
- Automatic board reset at end of each game using greedy Manhattan distance algorithm
- Draw detection (threefold repetition, fifty-move rule, stalemate, insufficient material)
- Pygame display showing board, move history, captured pieces, and message log
- Vosk watchdog that automatically recovers from speech recognition freezes

---

## Dependencies

### Hardware
- Raspberry Pi 5
- USB microphone
- Arduino Nano
- BSS138 logic level shifter (3.3V ↔ 5V)
- HDMI display (800×480 minimum)

### Operating System
- Raspberry Pi OS 
- PulseAudio running 
- Hardware UART enabled 

### Python Version
- Python 3.11 or later

### Python Packages
```
vosk
sounddevice
chess
pygame
pyserial
```

Install all at once:
```bash
pip install vosk sounddevice chess pygame pyserial --break-system-packages
```

### External Programs

### Vosk Model
- `vosk-model-small-en-us-0.15` — small English model, fast enough for real-time on Pi 5

Download from [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) and extract to the project directory.


## How to Install

**1. Clone or copy the project files to the Pi:**
```
chessproject/
├── chess_voice.py
├── piece_tracker.py
├── display.py
└── vosk-model-small-en-us-0.15/
```

**2. Create and activate a Python virtual environment:**
```bash
python3 -m venv chessenv
source chessenv/bin/activate
```


**3. Install Python dependencies inside the virtual environment:**
```bash
pip install vosk sounddevice chess pygame pyserial
```

**4. Install Stockfish:**


```bash
sudo apt install stockfish
```

Or install via snap:
```bash
sudo snap install stockfish
```

Verify it installed correctly:
```bash
which stockfish
/usr/games/stockfish
```

If stockfish is installed to a different path, update this line in `chess_voice.py`:
```python
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
```

**5. Enable hardware UART on the Pi:**
```bash
sudo raspi-config
# Interface Options → Serial Port
# Login shell over serial: No
# Serial port hardware: Yes
```

**6. Allow shutdown without password** (required for "chess no" voice command):
```bash
sudo visudo
# Add this line:
server ALL=(ALL) NOPASSWD: /usr/sbin/shutdown
```


**7. (Optional) Set up autostart on boot:**

Create `/home/server/.config/autostart/chess.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Chess
Exec=bash -c 'cd /home/server/chessproject && source /home/server/chessenv/bin/activate && python3 chess_voice.py >> chess.log 2>&1'
```

---

## How to Run / How to Use

**Start the program:**
```bash
cd ~/chessproject
source ~/chessenv/bin/activate
python3 chess_voice.py
```

The program will wait for PulseAudio and the microphone to be ready before starting.

---

### Voice Commands

All commands require a wake word — either `move` for chess moves or `chess` for system commands.

**Setup commands:**
| Say | Action |
|---|---|
| `chess one` | 1-player mode vs Stockfish |
| `chess two` | 2-player mode |
| `chess white` | Play as white |
| `chess black` | Play as black |
| `chess yes` | Play again |
| `chess no` | Shut down |

**Move commands (coordinate notation):**
| Say | Example |
|---|---|
| `move [src] [dst]` | `move e two e four` |

**Move commands (algebraic notation):**
| Say | Example |
|---|---|
| Pawn to square | `move e four` |
| Piece to square | `move knight f three` |
| With "to" | `move knight to f three` |
| Pawn capture | `move e takes d five` |
| Piece capture | `move knight takes f three` |
| Disambiguated | `move rook a d one` |

**Special moves:**
| Say | Action |
|---|---|
| `move castle` | Castle (auto-detects side if only one available) |
| `move short` | Kingside castle |
| `move long` | Queenside castle |

**Promotion** — when a pawn reaches the back rank a menu appears automatically. Say:
```
move queen / move rook / move bishop / move knight
```
Only pieces the opponent has captured are available for promotion.

**Game commands:**
| Say | Action |
|---|---|
| `chess resign` | Resign — board resets immediately |

---

### Configuration

At the top of `chess_voice.py`:

```python
ARDUINO_CONNECTED = True   # False for testing without hardware (short ACK timeout)
```

At the top of `piece_tracker.py`:

```python
ack_timeout = 30.0   # seconds to wait for Arduino ACK per packet
```

In `chess_voice.py` recognition thread:

```python
WATCHDOG_TIMEOUT = 15.0   # seconds before Vosk is automatically reset
```
