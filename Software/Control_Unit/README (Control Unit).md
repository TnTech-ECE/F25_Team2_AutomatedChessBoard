# Control Unit (CoreXY Controller)

## What It Does

This firmware runs on an Arduino Nano and controls a CoreXY-based automated chessboard. It receives binary move commands over UART (from a Raspberry Pi), translates them into coordinated stepper motor movements, and uses an electromagnet to pick up/transport/release chess pieces.

Key features:
- **Piece movement** via CoreXY kinematics (two stepper motors driving X/Y axes through belts and pulleys)
- **Edge-lane pathing** ensures pieces travel along square edges (never through the center of intermediate squares), to avoid collisions with other pieces
- **Move types supported:** straight (rook-like), diagonal (bishop-like), knight (L-shaped), and arbitrary L-shaped moves (for captures/discards)
- **Electromagnet control** via MOSFET switching circuit (for piece pickup and release)
- **Binary UART protocol** for communication with the Raspberry Pi (2 bytes per move, 1-byte ACK/NACK response)
- **Startup handshake** (`0x11` byte) prevents the system from acting on Pi boot noise
- **Software position clamping** keeps the head within safe travel limits
- **EEPROM position saving** preserves motor position on fault (for potential recovery)
- **TMC2209 DIAG pin monitoring** for overtemperature and short-circuit fault detection

## Dependencies
- [Arduino IDE](https://www.arduino.cc/en/software)
- [AccelStepper library](https://www.airspayce.com/mikem/arduino/AccelStepper/) (install via Arduino Library Manager)
- Built-in EEPROM library (included with Arduino IDE, no separate install needed)

## How to Install

1. Install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software).
2. Open the Arduino IDE. Go to **Sketch -> Include Library -> Manage Libraries**. Search for `AccelStepper` and click **Install**.
3. Open `chess_corexy.ino` in the Arduino IDE.
4. Connect the Arduino Nano to your computer via USB. **Disconnect the Pi's UART TX wire from the Arduino's RX pin (D0) before uploading** to avoid conflicts.
5. Select **Tools -> Board -> Arduino Nano** and **Tools -> Port -> (your COM port)**.
6. Click **Upload**.
7. Reconnect the Pi's UART TX wire to Arduino D0 after upload completes.

## How to Use

### Normal Operation (with Raspberry Pi)
1. Power on the system with the CoreXY head physically positioned at the center of the bottom-left square (a11 in Pi coordinates / physical row 1, column a).
2. The Arduino waits for the Pi to send a `0x11` handshake byte before accepting any commands.
3. The Pi sends move commands as 2 binary bytes:
   - **Byte 1 (source):** high nibble = column (a=1 ... h=8), low nibble = row (1–12)
   - **Byte 2 (destination):** same encoding
   - Example: a2 to a4 = `0x12, 0x14`
4. The Arduino executes the move and responds with `0x01` (ACK) on success or `0x00` (NACK) on error/fault.
5. The Pi must wait for the ACK/NACK before sending the next command.
6. **Home signal:** sending source == destination (e.g., `0x1B, 0x1B` for a11→a11) moves the head to that position, without engaging the magnet.

### Board Layout (Pi Row Numbering)
| Pi Row | Physical Row | Purpose |
|--------|-------------|---------|
| 1–8 | 4–11 | Playing field |
| 9 | 13 | Black pawn discard |
| 10 | 14 | Black special discard |
| 11 | 1 | White special discard |
| 12 | 2 | White pawn discard |
| — | 3, 12 | Gaps (not addressable) |

### Pin Assignments
| Pin | Function |
|-----|----------|
| D2 | Motor A STEP |
| D3 | Motor A DIR |
| D4 | Motor A EN |
| D5 | Motor A DIAG |
| D6 | Motor B STEP |
| D7 | Motor B DIR |
| D8 | Motor B EN |
| D9 | Motor B DIAG |
| D10 | Electromagnet (MOSFET gate) |

### Configuration
- **Square size:** 57.15 mm (2.25 in)
- **Steps per mm:** 40.0 (200 steps/rev × 8 microsteps ÷ 40mm pulley circumference)
- **Baud rate:** 115200
- **Motor speed:** 4000 steps/sec max, 1500 steps/sec² acceleration
