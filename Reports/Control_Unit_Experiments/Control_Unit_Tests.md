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

## Experiment 6: Fault Detection and Safe Halt Test

**Purpose:** Verify that the Control Unit detects TMC2209 DIAG pin faults mid-move, rejects invalid UART commands with NACK, and ignores boot noise until the `0x11` handshake is received. These behaviors are implemented in `checkFault()`, the UART parser's nibble validation, and the `piReady` flag respectively.

**Procedure:**

*Test A — Stall Detection:*
1. Temporarily set home position in `setup()` to (2.0, 0.5) while the carriage is physically near the left rail.
2. Command a leftward move. The carriage should stall against the rail.
3. Verify: motors stop, electromagnet turns off, NACK is sent to the Pi.
4. Send a new valid command and verify the system recovers and executes correctly.

*Test B — Invalid UART Rejection:*
1. With `piReady = true`, send invalid byte pairs from the Pi: column nibble = 0 (`0x02, 0x14`), column nibble = 9 (`0x92, 0x14`), row nibble = 0 (`0x10, 0x14`), and row nibble = 13 (`0x1D, 0x14`).
2. Verify NACK is received for each and no motor movement occurs.
3. Send a valid command afterward and verify it executes correctly.

*Test C — Boot Noise Rejection:*
1. Full power cycle the system with the Pi connected.
2. Mark the carriage position with tape. Observe during the ~45-second Pi boot. Verify no movement occurs.
3. After the chess software sends `0x11`, send a valid command and verify it executes.

**Data Collection:** Pass/fail table with columns (sub-test (A/B/C), trial number, fault condition, expected behavior, actual behavior, pass/fail, notes).

**Trials:** N = 10 total (3 iterations for Test A, 4 invalid pairs for Test B, and 3 iterations for Test C).

**Potential Biases:**
- Soft stalls may not trigger the DIAG pin (mitigate by ensuring the carriage hits a hard physical stop).
- Boot noise varies between boots (mitigate by testing across 3 separate cold boots).

---

## Experiment 7: UART Communication Reliability Test

**Purpose:** Verify that the binary UART protocol at 115200 bps provides reliable, error-free command transfer between the Pi and Arduino, as specified in the detailed design. Communication errors during gameplay would cause wrong moves, dropped commands, or system hangs. This test overlaps with Jack's Processing Unit tests (he tests the sending side; this test verifies the receiving/parsing side via response correctness).

**Procedure:**
1. Connect the Pi to the Arduino via the UART debug cable with logic level converter. Ensure both are set to 115200 bps.
2. Home the system to (0.5, 0.5). Ensure `piReady` is set by sending the `0x11` handshake byte first.
3. Write a Python test script on the Pi that sends a predefined sequence of 110 binary commands (100 valid + 10 invalid), waiting for the 1-byte ACK/NACK response after each command before sending the next. The script should log: command number, bytes sent (hex), expected response (ACK or NACK), actual response received, and whether they match.
4. The 100 valid commands should cover:
   - All 8 columns used as both source and destination at least once
   - Rows 1–12 each used at least once (including discard rows 9–12)
   - Straight moves (horizontal and vertical)
   - Diagonal moves
   - Knight moves
   - Discard/capture moves (L-shaped paths)
   - Home signal commands (src == dst)
5. The 10 invalid commands should be interspersed throughout the sequence (not all at the end) and should include:
   - Column nibble = 0 (e.g., `0x02, 0x14`)
   - Column nibble = 9 (e.g., `0x92, 0x14`)
   - Row nibble = 0 (e.g., `0x10, 0x14`)
   - Row nibble = 13 (e.g., `0x1D, 0x14`)
   - Row nibble = 15 (e.g., `0x1F, 0x14`)
   - Duplicate invalid entries to confirm consistent rejection
6. For each command, the Pi script records whether the response byte matches the expected value: `0x01` (ACK) for valid commands, `0x00` (NACK) for invalid commands. Also record the response time (time from send to response received).
7. If any valid command receives NACK or any invalid command receives ACK, flag it as a mismatch.
8. If no response is received within 30 seconds for any command, flag it as a timeout (potential system hang).

**Data Collection:** Record data in a spreadsheet with columns (command number, sent source byte (hex), sent destination byte (hex), expected response (ACK/NACK), actual response received (ACK/NACK/timeout), match (Y/N), response time (seconds)). Calculate: total error rate (mismatches / 110 × 100%), valid command error rate (mismatches among valid / 100 × 100%), invalid command error rate (mismatches among invalid / 10 × 100%), and mean/max response time for valid commands. Flag any timeouts separately.

**Trials:** N = 110 commands. 110 total commands help identify intermittent errors caused by electrical noise.

**Potential Biases:**
- The order of commands may matter if the system accumulates state errors over many moves (mitigate by including a home signal command every 20 commands in the sequence to reset the carriage to a known position).
- Response time for valid commands varies by move distance, as something like a short move completes faster than a full-board traverse (mitigate by recording move type alongside response time and analyze timing per move category rather than as a single average).

---


**NEEDS WORK**


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
