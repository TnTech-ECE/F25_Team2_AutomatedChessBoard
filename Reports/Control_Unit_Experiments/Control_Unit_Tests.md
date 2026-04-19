# Experimental Analysis

---

# DONE

## Experiment 1: Move Completion Time Test

**Purpose:** Verify that any single piece movement completes within 5 seconds of arriving at the source square, as specified in both the conceptual design and detailed design. This directly impacts gameplay pacing and user experience (slow moves frustrate players).

**Procedure:**
1. Connect the Arduino Nano to the Pi via UART. Be ready with a stopwatch to log times.
2. Home the system to (0.5, 0.5) and place the board in a known state.
3. Execute the following move categories, one at a time, recording completion time for each:
   - **Short straight:** a1 to a2 (1 square vertical)
   - **Medium straight:** a1 to a4 (3 squares vertical)
   - **Long straight:** a1 to a8 (7 squares vertical and full playing field traverse)
   - **Diagonal:** a1 to c3 (2 squares diagonal)
   - **Long Diagonal:** a1 to h8 (7 squares diagonal)
   - **Knight:** a1 to b3 (standard L-move)
   - **Discard (straight):** a1 to a11 (straight movement from playing field to discard row)
   - **Long Discard (L-shaped):** h8 to a11 (L-shaped path to discard row)
   - **Capture sequence:** two consecutive moves -> a1 to a11 (piece to discard), then a8 to a1 (attacker to destination)
4. For each move, record the time from when the piece is grabbed from it's starting position to when it is dropped off at the ending position.

**Data Collection:** Spreadsheet with columns (trial number, move category, source square, destination square, elapsed time in seconds). Calculate mean per move category. Flag any trial exceeding 5 seconds.

**Trials:** N = 10. The variety of categories ensures full coverage of the motion system.

**Potential Biases:** 
- Mechanical friction may vary with board position (mitigate by testing moves across different regions of the board).
- Belt tension changes over time may affect speed (mitigate by checking belt tension before the test session).

---

## Experiment 2: Boot Noise Test

**Purpose:** Verify that the Control Unit ignores boot noise until the `0x11` handshake is received. This behavior is implemented in the `piReady` flag.

**Procedure:**

1. Full power cycle the system with the Pi connected.
2. Mark the carriage position with tape. Observe during the ~45-second Pi boot. Verify no movement occurs.
3. After the chess software sends `0x11`, send a valid command and verify it executes.

**Data Collection:** Pass/fail table with columns (trial number, boot movement(y/n), start command received(y/n), valid command executed(y/n), pass/fail).

**Trials:** N = 3 total.

**Potential Biases:**
- Boot noise varies between boots (mitigate by testing across 3 separate cold boots).

---

## Experiment 3: Edge Boundary and Clamp Verification Test

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

**Data Collection:** Table with columns (test move, source, destination, boundary tested (X min / X max / Y min / Y max), carriage stayed within bounds (Y/N)).

**Trials:** N = 4 total observations. This covers all 4 possible collision concerns.

**Potential Biases:** 
- Accumulated positional error from previous moves could push the carriage past a boundary (mitigate by re-homing between trials).

---


## Experiment 4: Electromagnet Switching Latency Test

**Purpose:** Verify that the MOSFET-based electromagnet switching circuit activates within 10ms and reliably picks up and releases all chess piece types, as specified in the detailed design. Reliable pickup/release is essential (a dropped piece mid-move ruins the game).

**Procedure:**

1. Attach oscilloscope probes to the Arduino's MAGNET_PIN (D10) output and to the MOSFET drain (electromagnet current path).
2. Command the Arduino to toggle the electromagnet on and off using the `magnetOn()` and `magnetOff()` functions in a test loop with 2-second delays between toggles.
3. Measure the time from the rising edge of the gate signal to the point where drain current reaches 90% of steady-state (turn-on latency), and from the falling edge of the gate signal to the point where drain current drops below 10% (turn-off latency).

**Data Collection:** Table with columns (trial number, turn-on latency (ms), turn-off latency (ms)). Calculate mean and max for each.

**Trials:** N = 10 switching cycles. Ten latency measurements provide reliable mean/max values.

**Potential Biases:** 
- Oscilloscope bandwidth may limit measurement precision for fast edges (mitigate by using a scope with ≥20 MHz bandwidth). 

---

## Experiment 5: Flyback Diode Inductive Spike Test

**Purpose:** Verify that the flyback diode clamps the inductive voltage spike on the MOSFET drain to within the IRLZ44NPBF's maximum Vds rating (55V) when the electromagnet is switched off. Unclamped spikes could destroy the MOSFET, causing a permanent system failure.

**Procedure:**
1. Connect an oscilloscope probe to the MOSFET drain pin (between the electromagnet and the MOSFET).
2. Set the oscilloscope to trigger on the falling edge of the gate signal, with a voltage scale sufficient to capture spikes up to 60V.
3. Command the Arduino to energize the electromagnet for 2 seconds, then switch off.
4. Capture the drain voltage waveform during the off-switching event.
5. Record the peak voltage spike magnitude and its duration.
6. Repeat for multiple on-durations (200ms, 1s, 2s, 5s) to check if spike magnitude varies with energization time.

**Data Collection:** Table with columns: trial number, on-duration (ms), peak spike voltage (V), spike duration (µs), MOSFET Vds max (55V), pass/fail. Include oscilloscope screenshot captures for each trial.

**Trials:** N = 4 durations. Varying on-duration ensures the diode performs under different stored-energy conditions.

**Potential Biases:** 
- Probe ground lead inductance can cause ringing that appears as a larger spike than actually exists. (mitigate by using the shortest possible ground lead). 
- Ensure the probe is compensated. Ambient temperature affects diode forward voltage slightly (mitigate by recording ambient temperature).

---

# NEED TO DO

## Experiment ?: Command Latency Test

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

**Potential Biases:** 
- Arduino main loop polling rate introduces variability depending on where in the loop cycle the byte arrives (mitigate by using consistent system state (idle with no prior motion) before each trial; ensure no other serial traffic is present during measurement).

---

## Experiment ??: UART Communication Reliability Test

**Purpose:** Verify that the binary UART protocol at 115200 bps provides reliable, error-free command transfer between the Pi and Arduino during. The physical movement of the correct piece to the correct square serves as confirmation of successful transmission, parsing, and execution. Communication errors during gameplay could cause wrong moves, dropped commands, or system hangs.

**Procedure:**
1. Connect the Pi to the Arduino via the UART debug cable with logic level converter. Ensure both are set to 115200 bps.
2. Home the system to (0.5, 0.5) and set up the board with all pieces in starting positions.
3. Play a full game against Stockfish (or a second player). For each move:
   - Observe the CoreXY physically moving the correct piece from the correct source square to the correct destination square.
   - Record whether the piece moved to the correct location, an incorrect location, or did not move at all.
   - Record whether ACK or NACK was received on the Pi side (or if a timeout occurred).
4. For any captures during the game, verify the captured piece is physically moved to the correct discard row (rows 11–12 for white, rows 9–10 for black) before the attacking piece moves.
5. The game should produce at minimum 40 total moves (both sides combined) to provide sufficient command volume. If the game ends early, start another.
6. After the game, verify the system is still responsive by sending one final known-good command and confirming correct carriage movement.

**Data Collection:** Spreadsheet with columns (move number, expected source square, expected destination square, actual destination square observed, piece moved correctly (Y/N), ACK/NACK/timeout received, notes). Calculate: error rate (incorrect moves / total moves × 100%). For captures, additionally record whether the discard placement was correct.

**Trials:** N = 40 moves. A full game exercises the communication chain under realistic conditions including varied move types (straight, diagonal, knight, captures, and discard moves) in natural sequence.

**Potential Biases:**
- A single game may not cover all move types (mitigate by executing 2–3 manual commands of any skipped type, after the game ends).
- Observer may miss subtle misplacements (mitigate by verifing piece position against the Pi's displayed board state after each move).

---

## Experiment ???: Thermal Safety Test

**Purpose:** Verify that all system component surfaces remain below 40°C (104°F) during sustained operation (as required by UL 94 flammability guidance and CPSC 16 CFR 1505.7 thermal limits). Components tested include both TMC2209 driver boards, the stepper drivers, the MOSFET, the Arduino Nano, the Raspberry Pi enclosure, the display, the microphone, and the power supply. Overheating of any component could cause thermal shutdown mid-game, material degradation, or burn hazard to the user.

**Procedure:**
1. Install SMT heatsinks (Adafruit 1493) on both TMC2209 driver boards if not already installed.
2. Record the ambient room temperature using a thermometer.
3. Run a simulated full-game sequence from the Pi: continuous move commands covering varied move types (straight, diagonal, knight, captures, discards) over 30 minutes of active operation.
4. At each 10 minute interval, pause briefly and measure surface temperatures at each of the following locations using an IR thermometer:
   - TMC2209 driver board A
   - TMC2209 driver board B
   - Stepper motor A
   - Stepper motor B
   - MOSFET body
   - Arduino Nano
   - Raspberry Pi enclosure (top surface)
   - Display (back surface)
   - Microphone body
   - UPS
   - Power supply enclosure
5. Record ambient temperature at each measurement point.
6. If any component triggers a thermal fault during the test (e.g., TMC2209 DIAG pin triggers, motion stops unexpectedly), record the event and the temperature at which it occurred.

**Data Collection:** Table with columns (time point (10/20/30 min), ambient temperature (°C), and one temperature column per component (°C)). Record pass/fail for each component at each time point (pass = ≤40°C). Calculate peak temperature for each component across all measurements. Convert to °F for comparison against the 104°F spec if needed (°F = °C × 9/5 + 32).

**Trials:** N = 3 timestamps for all components.

**Potential Biases:**
- IR thermometer accuracy depends on consistent location (mitigate by measuring the same location on the material surface each time).
- Ambient temperature variation between timestamps affects results (mitigate by recording ambient temperature at every timestamp).
- Room ventilation and airflow vary by location (mitigate by running the session in a location with room-temperature ambient temperature).


---

# ON-HOLD

## Experiment ????: Positional Accuracy Verification

**Purpose:** Evaluate whether the CoreXY system achieves positional accuracy within ±0.5mm across the board. This directly supports precise chess piece placement; if the electromagnet doesn't land on the centre of a square, pieces will be misaligned or missed entirely.

**Procedure:**
1. Mark the centre of at least 10 target squares across the board using a fine-tip marker. Centres are located 28.575mm (half of 57.15mm) from each edge of the square. Target squares should include:
   - Four corners of the playing field (a1, h1, a8, h8)
   - Board centre (d4 or e5)
   - At least two discard row positions (e.g., a11, h10)
   - At least two mid-edge positions (e.g., a4, d1)
2. Home the system to (0.5, 0.5).
3. Command the CoreXY to move to each target coordinate.
4. At each position, use a ruler with millimetre precision (or calipers) to measure the distance from the centre of the electromagnet carriage to the marked centre of the target square. Measure the X offset and Y offset separately.
5. Record the deviation from the target position.
6. Re-home the system between each measurement to prevent cumulative error.
7. Repeat across all target squares for each trial.

**Data Collection:** Record data in a table with columns (trial number, target square, target position (mm), measured offset X (mm), measured offset Y (mm), total error (mm, calculated as √(X² + Y²)), pass/fail (≤0.5mm)). Calculate mean error and max error across all measurements.

**Trials:** N = 10 coordinates

**Potential Biases:**
- Human measurement error (~±0.5mm) (mitigate by using the same operator and consistent measuring method for all readings)

---


# NEEDS WORK


## Experiment ?????: Collision-Free Capture and Movement Rate Test

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

**Potential Biases:** Ambient temperature variation between sessions affects results. Mitigation: record ambient temperature at the start of each session and normalize results. IR thermometer accuracy depends on emissivity setting and measurement distance — mitigate by using the same distance and angle for all readings, and calibrate against a known temperature source if possible. Enclosure ventilation affects thermal performance — test both with and without the final enclosure to understand worst-case conditions.
