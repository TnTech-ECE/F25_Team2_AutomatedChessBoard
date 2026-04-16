# Control Unit — Experimental Analysis

---

## Experiment 1: Command Latency Test

**Purpose:** Verify that the Control Unit processes and begins executing a received UART command within 50ms of receipt, as required by the detailed design performance specification. Low latency is critical from the customer's perspective to ensure the board feels responsive during gameplay.

**Procedure:**
1. Connect the Arduino Nano (A000005) to the Raspberry Pi5 via the UART debug cable (with logic level converter between the two).
2. Attach an oscilloscope probe to the Arduino's UART RX pin (D0) and a second probe to one of the TMC2209 STEP output pins (either D2 or D6).
3. Ensure the system is powered, homed, and idle (no pending moves).
4. Send a single valid 2-byte binary move command from the Pi (e.g., `0x12 0x14` for a1 to a3).
5. On the oscilloscope, trigger on the falling edge of the RX start bit. Measure the time delta from the end of the second received byte to the first rising edge on the STEP pin.
6. Reset the head to home position between trials to ensure consistent starting conditions.
7. Repeat for 10 trials using the same move command, then repeat 5 additional trials with varied move types (diagonal, knight, straight).

**Data Collection:** Record each latency measurement in milliseconds in a spreadsheet table with columns for trial number, move type, and measured latency (ms). Calculate mean, standard deviation, min, and max across all trials.

**Trials:** N = 15 (10 identical and 5 varied). 15 trials provide sufficient data to identify any outliers and confirm consistency across move types.

**Potential Biases:** Arduino main loop polling rate introduces variability depending on where in the loop cycle the byte arrives (mitigate by using consistent system state (idle with no prior motion) before each trial; ensure no other serial traffic is present during measurement).

---

## Experiment 2: Move Completion Time Test

**Purpose:** Verify that any single piece movement completes within 5 seconds of command receipt, as specified in both the conceptual design and detailed design. This directly impacts gameplay pacing and user experience (slow moves frustrate players).

**Procedure:**
1. Connect the Arduino Nano to the Pi via UART. Be ready with a stopwatch to log times.
2. Home the system to (0.5, 0.5) and place the board in a known state.
3. Execute the following move categories, one at a time, recording completion time for each:
   - **Short straight:** a1 to a2 (1 square vertical)
   - **Medium straight:** a1 to a4 (3 squares vertical)
   - **Long straight:** a1 to a8 (7 squares vertical and full playing field traverse)
   - **Diagonal:** a1 to c3 (2 squares diagonal)
   - **Knight:** a1 to b3 (standard L-move)
   - **Discard (straight):** a1 to a11 (straight movement from playing field to discard row)
   - **Discard (L-shaped):** b2 to a11 (L-shaped path to discard row)
   - **Capture sequence:** two consecutive moves — a1 to a11 (piece to discard), then a8 to a1 (attacker to destination)
4. For each move, record the time from when the piece is grabbed from it's starting position to when it is dropped off at the ending position.

**Data Collection:** Spreadsheet with columns (trial number, move category, source square, destination square, elapsed time in seconds). Calculate mean per move category. Flag any trial exceeding 5 seconds.

**Trials:** N = 9. The variety of categories ensures full coverage of the motion system.

**Potential Biases:** Mechanical friction may vary with board position (mitigate by testing moves across different regions of the board). Belt tension changes over time may affect speed (mitigate by checking belt tension before the test session).

---

## Experiment 3: Electromagnet Switching Latency Test

**Purpose:** Verify that the MOSFET-based electromagnet switching circuit activates within 10ms and reliably picks up and releases all chess piece types, as specified in the detailed design. Reliable pickup/release is essential (a dropped piece mid-move ruins the game).

**Procedure:**

1. Attach oscilloscope probes to the Arduino's MAGNET_PIN (D10) output and to the MOSFET drain (electromagnet current path).
2. Command the Arduino to toggle the electromagnet on and off using the `magnetOn()` and `magnetOff()` functions in a test loop with 2-second delays between toggles.
3. Measure the time from the rising edge of the gate signal to the point where drain current reaches 90% of steady-state (turn-on latency), and from the falling edge of the gate signal to the point where drain current drops below 10% (turn-off latency).

**Data Collection:** Table with columns (trial number, turn-on latency (ms), turn-off latency (ms)). Calculate mean and max for each.

**Trials:** N = 10 switching cycles. Ten latency measurements provide reliable mean/max values.

**Potential Biases:** Oscilloscope bandwidth may limit measurement precision for fast edges (mitigate by using a scope with ≥20 MHz bandwidth). 

---

## Experiment 4: Flyback Diode Inductive Spike Test

**Purpose:** Verify that the flyback diode clamps the inductive voltage spike on the MOSFET drain to within the IRLZ44NPBF's maximum Vds rating (55V) when the electromagnet is switched off. Unclamped spikes could destroy the MOSFET, causing a permanent system failure.

**Procedure:**
1. Connect an oscilloscope probe to the MOSFET drain pin (between the electromagnet and the MOSFET).
2. Set the oscilloscope to trigger on the falling edge of the gate signal, with a voltage scale sufficient to capture spikes up to 60V.
3. Command the Arduino to energize the electromagnet for 2 seconds, then switch off.
4. Capture the drain voltage waveform during the off-switching event.
5. Record the peak voltage spike magnitude and its duration.
6. Repeat for multiple on-durations (200ms, 1s, 2s, 5s) to check if spike magnitude varies with energization time.

**Data Collection:** Table with columns: trial number, on-duration (ms), peak spike voltage (V), spike duration (µs), MOSFET Vds max (55V), pass/fail. Include oscilloscope screenshot captures for each trial.

**Trials:** N = 5 per on-duration × 4 durations = 20 total measurements. Five repetitions per condition confirm consistency; varying on-duration ensures the diode performs under different stored-energy conditions.

**Potential Biases:** Probe ground lead inductance can cause ringing that appears as a larger spike than actually exists. (mitigate by using the shortest possible ground lead). Ensure the probe is compensated. Ambient temperature affects diode forward voltage slightly (mitigate by recording ambient temperature).

---

## Experiment 5: Edge Boundary and Clamp Verification Test

**Purpose:** Verify that the software clamping logic prevents the CoreXY head from moving beyond the centre of any edge square (X ∈ [0.5, 7.5], Y ∈ [0.5, 13.5] in square units), and that the edge-travel algorithm correctly avoids the outermost board edges. This is a safety-critical requirement, as exceeding travel limits could damage the CoreXY mechanism or dislodge the carriage from the rails.

**Procedure:**
1. Home the system to (0.5, 0.5).
2. Execute the following moves that involve edge squares and boundary conditions:
   - **Column a vertical:** a1 to a8 (left column, full playing field traverse) -> X exit edge should not move to X = 0.0
   - **Column h vertical:** h1 to h8 (right column) -> X exit edge should not move to X = 8.0
   - **Discard from column a:** a1 to a11 (bottom discard row) -> Y must not go below Y = 0.5
   - **Discard from column h:** h8 to h10 (top discard row) -> Y must not go above Y = 13.5
3. For each move, visually observe and confirm that the carriage never reaches or crosses the outermost physical rail on any side.0
4. Record pass/fail for each move. If a boundary violation is observed, record the approximate position and which axis was violated.

**Data Collection:** Table with columns (test move, source, destination, boundary tested (X min / X max / Y min / Y max), carriage stayed within bounds (Y/N), notes).

**Trials:** N = 4 total observations. This covers all 4 possible collision concerns.

**Potential Biases:** Accumulated positional error from previous moves could push the carriage past a boundary (mitigate by re-homing between trials).

---

## Experiment ?: Fault Detection and Safe Halt Test

**Purpose:** Verify that the Control Unit correctly detects TMC2209 DIAG pin fault signals, rejects invalid UART commands, and ignores Pi boot noise before the `0x11` handshake, as implemented in the current firmware. The code's `checkFault()` function monitors DIAG_A (pin 5) and DIAG_B (pin 9) every iteration of the motion loop inside `moveToSteps()`. When either pin reads HIGH, the function disables both motor drivers (EN pins set HIGH), calls `motorA.stop()` and `motorB.stop()`, turns off the electromagnet via `magnetOff()`, sets the `faultOccurred` flag to true, and saves the current motor positions to EEPROM. The UART parser validates that column nibbles decode to 0–7 and row nibbles decode to 1–12, sending NACK (0x00) and flushing the serial buffer for any values outside those ranges. The `piReady` handshake flag prevents any move commands from being processed until a `0x11` byte is received, discarding all prior bytes. Safe fault handling prevents mechanical damage, protects the user, and ensures the system fails predictably. This test overlaps with Allison's Experiment 9 (System Reliability and Failure Behavior); the Control Unit's focus is specifically on the Arduino firmware's fault detection and UART rejection logic, while the CoreXY Unit's focus is on overall system behavior during faults.

**Procedure:**

*Test A — TMC2209 DIAG Pin Stall Detection:*
1. Home the system and deliberately set the motor position to a value that does not match the physical location (e.g., in `setup()`, temporarily set home to (2.0, 0.5) while the carriage is physically near the left rail). This causes the Arduino to believe it has room to move left, when physically it does not.
2. Command a move that requires leftward travel (e.g., `movePiece(0, 11, 0, 11)` to navigate to a11, which would require moving left from the code's perspective).
3. Observe and record whether the following occur:
   - The motors stall and stop (carriage stops moving).
   - The electromagnet turns off (if it was on).
   - The system sends NACK (0x00) back over UART (verify on Pi side).
   - The system does not accept further move commands (send another command and verify no motion occurs until the fault is cleared).
4. Send one more valid command and verify the system re-enables drivers (the code calls `enableDrivers()` when a new command arrives while `faultOccurred` is true) and executes the move correctly.

*Test B — Invalid UART Data Rejection:*
1. Ensure the system is running with `piReady = true` and no fault condition active.
2. From the Pi, send the following invalid byte pairs one at a time, waiting for a response after each:
   - Column nibble = 0: send `0x02, 0x14` (column 0 is invalid, columns are 1–8).
   - Column nibble = 9: send `0x92, 0x14` (column 9 exceeds maximum of 8).
   - Row nibble = 0: send `0x10, 0x14` (row 0 is invalid, rows are 1–12).
   - Row nibble = 13: send `0x1D, 0x14` (row 13 exceeds maximum of 12).
   - Send a single byte `0x12` with no second byte, wait 5 seconds, then send a valid 2-byte command.
3. For each invalid pair, verify on the Pi side that NACK (0x00) is received.
4. Verify no motor movement occurs for any invalid command (observe the carriage).
5. After all invalid commands, send a valid command (e.g., `0x12, 0x14` for a2→a4) and verify it is accepted and executed correctly. This confirms the system recovers from invalid input without requiring a reset.

*Test C — Handshake Boot Noise Rejection:*
1. Power off the entire system (Pi and Arduino).
2. Power on the system. The Pi will begin its boot sequence, during which it outputs kernel messages and other data on its UART TX line.
3. Observe the CoreXY head during the entire Pi boot sequence (approximately 45 seconds). Record whether any movement occurs.
4. After the Pi chess software starts and sends the `0x11` handshake byte, send a valid move command from the Pi.
5. Verify the move command is accepted and the carriage moves to the correct position.
6. This test must be performed as a cold boot (full power cycle), not a software restart, to capture the full range of boot noise.

**Data Collection:** Record results in a pass/fail table with the following columns: sub-test (A/B/C), trial number, specific fault condition or invalid input, expected system behavior, actual observed behavior, pass/fail, notes. For Test A, also note whether the EEPROM position was saved correctly (if verifiable). For Test B, record the exact bytes sent and the response byte received. For Test C, record the boot duration and whether any carriage movement was detected.

**Trials:** N = 3 per sub-test (A, B, C) = 9 total trials. Three trials per fault type confirm consistent behavior. Fault handling must achieve 100% reliability — any single failure indicates a firmware bug that must be fixed. For Test C, each trial must be a full cold boot to capture different boot noise patterns.

**Potential Biases:**
- TMC2209 StallGuard sensitivity depends on motor current, speed, and the StallGuard threshold configured in the driver. A soft stall (low friction, slow speed) may not trigger the DIAG pin. Mitigation: ensure the physical stop provides a hard stall condition (carriage firmly against the rail). If DIAG does not trigger, document the limitation and note that StallGuard threshold tuning may be required.
- Pi boot noise content varies between boots depending on system state, connected peripherals, and OS updates. Mitigation: test across 3 separate cold boots on different occasions to capture variation.
- The single-byte UART test (Test B, step 5) depends on timing — the Arduino code waits indefinitely for `Serial.available() >= 2`, so a lone byte will simply sit in the buffer until the next byte arrives. The subsequent valid command's first byte will pair with the orphaned byte, potentially causing a misparse. Mitigation: document this behavior, as it represents a real edge case in the current firmware. If it causes issues, note it as a known limitation that could be addressed with a receive timeout.
- Observer bias in detecting small carriage movements during Test C. Mitigation: place a small mark or piece of tape at the carriage position before boot and check for displacement after boot completes.


---

## Experiment ?: UART Communication Reliability Test

**Purpose:** Verify that the binary UART protocol at 115200 bps provides reliable, error-free command transfer between the Pi and Arduino (as specified in the detailed design). Communication errors during gameplay would cause wrong moves or system hangs.

**Procedure:**
1. Connect the Pi to the Arduino via the UART debug cable with logic level converter.
2. Write a Python test script on the Pi that sends a predefined sequence of 100 valid binary move commands, each followed by waiting for the 1-byte ACK/NACK response before sending the next command.
3. The test sequence should include: all 8 columns as source and destination, rows 1–12, diagonal moves, knight moves, straight moves, discard moves, and the home signal (src==dst).
4. On the Arduino side, add temporary debug logging that prints each received source and destination (col, row) to a secondary output (SoftwareSerial on spare pins, or logged to an array and dumped after the test).
5. Compare the Pi's sent commands against the Arduino's received/parsed commands. Record any mismatches.
6. Also record ACK/NACK responses on the Pi side and verify each matches the expected outcome (ACK for valid moves, NACK for intentionally invalid test commands).
7. Include 10 intentionally invalid commands interspersed in the sequence to verify NACK handling.

**Data Collection:** Spreadsheet with columns: command number, sent bytes (hex), expected col/row parsed values, actual parsed values (from Arduino log), ACK/NACK expected, ACK/NACK received, match (Y/N). Calculate total error rate (mismatches / total commands × 100%). Report separately for valid and invalid commands.

**Trials:** N = 3 sessions × 110 commands = 330 total commands. Three sessions at different times help identify intermittent errors caused by electrical noise or timing variations.

**Potential Biases:** Baud rate mismatch between Pi and Arduino causes systematic errors — mitigate by verifying both are set to 115200 bps before testing. Logic level converter quality may introduce bit errors at high speeds — mitigate by inspecting UART signals on an oscilloscope if errors are detected. Ground loop between Pi and Arduino power supplies can inject noise — mitigate by ensuring a common ground reference between all connected systems.

---



## Experiment ???: Collision-Free Capture and Movement Rate Test

**Purpose:** Verify that the system achieves 95% or higher collision-free piece movements, including captures (as specified in the detailed design). Piece collisions during automated play would disrupt the game and damage user trust in the system.

**Procedure:**
1. Set up the board with a standard chess starting position (all 32 pieces placed on the board in their standard squares).
2. Execute a predefined sequence of 30 moves covering all move types:
   - 8 straight-line moves (vertical and horizontal, varied distances)
   - 6 diagonal moves (varied distances)
   - 4 knight moves
   - 6 capture sequences (piece to discard, then attacker to destination)
   - 4 discard/reset moves (L-shaped paths to/from discard rows)
   - 2 edge-boundary moves (pieces on columns a and h)
3. For each move, observe and record whether any non-target piece was displaced, knocked over, or visibly shifted from its square centre.
4. Record a pass/fail for each move, along with any notes on which piece was affected and how.
5. Restore any displaced pieces to their correct positions before continuing the sequence to prevent cascading failures.

**Data Collection:** Spreadsheet with columns (move number, move type, source, destination, pass/fail, notes (which piece affected, severity)). Calculate overall success rate (passes / total × 100%). Break down success rate by move type.

**Trials:** N = 30 moves. 30 observations give a 95% confidence interval of approximately ±4.5% on the success rate.

**Potential Biases:** Piece placement consistency affects results (mitigate by ensuring pieces are centred on squares before each session). Electromagnet strength variation between piece types (pawns vs. rooks) may affect capture reliability (mitigate by including all piece types in the test sequence).

---

## Experiment ???: Motor Driver Thermal Test

**Purpose:** Verify that the TMC2209 driver surface temperatures remain below 40°C (104°F) with heatsinks installed during sustained operation, as required by the detailed design and UL 94/CPSC thermal safety constraints. Overheating could cause thermal shutdown mid-game, halting play unexpectedly.

**Procedure:**
1. Install SMT heatsinks (Adafruit 1493) on both TMC2209 driver boards per manufacturer recommendations.
2. Record the ambient room temperature using a thermometer.
3. Run a simulated full-game sequence: send a continuous stream of move commands (approximately 40 moves per side, 80 total moves) from the Pi, representing a typical chess game. Include varied move types and captures.
4. After every 10 moves, pause for 5 seconds and measure the surface temperature of each TMC2209 heatsink and the MOSFET using an IR thermometer (or thermocouple).
5. After completing all 80 moves, continue measuring every 2 minutes for an additional 10 minutes to observe cool-down behavior.
6. If at any point a driver enters thermal shutdown (motion stops unexpectedly, DIAG pin triggers), record the event and the temperature at which it occurred.

**Data Collection:** Table with columns: measurement point (move count or time), ambient temperature (°C), driver A heatsink temperature (°C), driver B heatsink temperature (°C), MOSFET temperature (°C), thermal fault (Y/N). Plot temperature vs. move count as a line graph. Calculate peak temperature for each component.

**Trials:** N = 3 full game simulations. Three sessions (ideally on different days or with full cool-down between) confirm that thermal behavior is consistent and not dependent on initial conditions.

**Potential Biases:** Ambient temperature variation between sessions affects results. Mitigation: record ambient temperature at the start of each session and normalize results. IR thermometer accuracy depends on emissivity setting and measurement distance — mitigate by using the same distance and angle for all readings, and calibrate against a known temperature source if possible. Enclosure ventilation affects thermal performance — test both with and without the final enclosure to understand worst-case conditions.
