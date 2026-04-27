# Chess 2 Impress

## Executive Summary

Smart chessboards enhance the over-the-board chess experience through automated piece movement and AI opponent integration. Existing commercial options, however, cost hundreds to thousands of dollars (putting them out of reach for most players). Chess 2 Impress is a low-cost, accessible, voice-controlled chessboard (built for under $350 in materials). Players speak their moves using natural chess notation, and the board physically moves the pieces (using a CoreXY gantry with an under-board electromagnet). The system supports single-player games against the Stockfish chess engine, two-player games, and includes automated capture handling and board reset. Voice recognition runs locally on a Raspberry Pi (using the Vosk engine), requiring no internet connection. An LCD display provides real-time game feedback, and a battery-backed UPS allows over 2 hours of portable gameplay. The project demonstrates that a fully functional automated chess board can be built with off-the-shelf components (at a fraction of commercial prices), while maintaining accessibility for players with limited mobility or visual impairments.

## Capabilities

- **Voice-controlled gameplay** using the Vosk speech recognition engine, supporting algebraic notation and common variations (e.g., "move knight a six," "move c2c4," "move castle"). There was a 97% first-try recognition accuracy across multiple speakers.
- **Automated piece movement** via a CoreXY gantry system driven by two NEMA 17 stepper motors and TMC2209 drivers, with an under-board electromagnet for contactless piece manipulation.
- **Edge-lane pathing algorithm** that routes pieces along square boundaries during movement, avoiding collisions with adjacent pieces on the board.
- **AI opponent integration** using the Stockfish chess engine for single-player games, with full move validation (through python-chess). This ensures 100% correct legal/illegal move classification.
- **Capture and reset handling** where captured pieces are automatically moved to dedicated discard rows, and the board resets all pieces to starting positions at the end of a game.
- **Binary UART communication** between the Raspberry Pi (processing) and Arduino Nano (motion control), with a handshake protocol that rejects boot noise and ensures reliable command transfer.
- **Battery-powered portable operation** via a DFRobot UPS HAT with 4×18650 cells, delivering over 2 hours of continuous gameplay (with seamless switchover from wall power).
- **LCD display feedback** showing move confirmations, illegal move alerts, game status, and system messages within approximately 1 second of voice input.
- **Fault protection** including TMC2209 DIAG pin monitoring, MOSFET flyback diode clamping, software position clamping (to prevent rail collisions), and EEPROM position saving.

## Salient Outcomes

- **Voice recognition exceeded expectations**, achieving 97% first-try recognition and 95% correctness (across 5 speakers with varied accents). This was well above the 80% specification.
- **The edge-lane pathing algorithm** was one of the most complex and iterative parts of the firmware development. Pieces must travel along square edges (never through intermediate square centres) to avoid displacing adjacent pieces. The final algorithm handles straight, diagonal, knight, and arbitrary L-shaped moves (for captures and discards) using a unified exit-edge / entry-edge framework.
- **Electromagnet switching latency measured at 3 microseconds** — over 3,300 times faster than the 10ms specification, demonstrating that the MOSFET circuit adds essentially zero delay to the move-completion budget.
- **The blown fuse debugging saga** taught the team that hardware failures can mimic software bugs. Multiple debugging sessions chasing "wrong direction" firmware issues were ultimately caused by a single blown fuse disabling one stepper motor, producing diagonal movement instead of the intended axis-aligned motion.
- **Move completion time remains the primary unmet specification**. Even the shortest possible move takes over 5 seconds with current firmware settings, and worst-case moves approach 30 seconds. Increasing stepper speed and acceleration in firmware is the straightforward fix, but could not be implemented without drastic redesigns to the electromagnet and acryllic setup.

## Project Demonstration & Images

**Demo Video:** [Coming Soon — link to capstone YouTube video]

**Project Images:**

*[Images to be added]*

## About Us

### Team

- **Nathan MacPherson** (Team Leader): Designed and integrated the Peripherals Unit, including the USB microphone interface and LCD display. Managed team coordination, designed the portability and weight experiments, and maintained the component inventory.
- **Noah Beaty** (Recorder): Developed the Control Unit firmware on the Arduino Nano, including the CoreXY motion engine, edge-lane pathing algorithm, binary UART protocol, electromagnet control, and fault protection. Designed the motion, electromagnet, flyback, command latency, and edge boundary experiments.
- **Jack Tolleson** (Treasurer): Built the Processing Unit on the Raspberry Pi, implementing the Vosk speech recognition pipeline, python-chess move validation, Stockfish AI integration, and UART communication with the Arduino. Designed the voice recognition, processing latency, and move validation experiments.
- **Allison Givens**: Designed and built the CoreXY mechanical subsystem, including the aluminum extrusion frame, belt/pulley system, the 3D-printed carriage, and the trolley supports. Iterated through numerous mechanical revisions to accommodate enclosure constraints. Designed the safety compliance experiment.
- **Lewis Bates**: Designed and built the Power Unit, including the DFRobot UPS HAT integration, 4×18650 battery pack, MT3608 boost converters, fuse protection, and power distribution. Designed power-related experiments (UPS switchover, sleep-mode draw, battery runtime, voltage regulation, and power budget verification).

### Faculty Supervisor

**Dr. Charles Van Neste**: Faculty advisor for the project.

### Stakeholders

The primary customer for this project is the **Tennessee Tech Chess Club**, represented by club president Max Bottoms. The club expressed interest in an affordable automated board that could be used for club events, demonstrations, and accessible play. Beyond the chess club, the project targets chess enthusiasts, hobbyists interested in replicating the build, and players with limited mobility or visual impairments (who benefit from voice-controlled, hands-free gameplay).

### Recognitions

Special thanks to our capstone instructor Dr. Christopher Storm Johnson, Julie Mountain, Sara Vandermyde, Jeff Randolph, the Tennessee Tech Chess Club, and our respective families for their support throughout the project.

## Repo Organization

### [Reports](./Reports)

Contains all project reports, including the Conceptual Design, Detailed Design documents, Experimental Analysis, project poster, and related supporting materials.

### [Documentation](./Documentation)

Contains project documentation including signoff sheets, meeting notes, the project datasheet, and design reference materials.

### [Software](./Software)

Contains all project source code organized by subsystem, including the Arduino Control Unit firmware (`chess_corexy.ino`), the Raspberry Pi Processing Unit code, and associated README files with installation and usage instructions.
