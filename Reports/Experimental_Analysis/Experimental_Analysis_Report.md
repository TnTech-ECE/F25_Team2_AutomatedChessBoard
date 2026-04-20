# Experimental Analysis

**Project Title:** _Chess 2 Impress_

**Team Name:** _Team 2_

**Team Members:** _Allison Givens, Noah Beaty, Jack Tolleson, Lewis Bates, Nathan MacPherson_

**Course:** _ECE 4971_

**Instructor:** _Christopher Johnson_

**Submission Date:** _4-22-2026_

**Repository Link:** _https://github.com/TnTech-ECE/F25_Team2_AutomatedChessBoard_

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Critical Success Criteria](#2-critical-success-criteria)
3. [Experiment 1: Move Completion Time](#3-experiment-1-move-completion-time)
4. [Experiment 2: Boot Noise](#4-experiment-2-boot-noise)
5. [Experiment 3: Edge Boundary and Clamp Verification](#5-experiment-3-edge-boundary-and-clamp-verification)
6. [Experiment 4: Electromagnet Switching Latency](#6-experiment-4-electromagnet-switching-latency)
7. [Experiment 5: Flyback Diode Inductive Spike](#7-experiment-5-flyback-diode-inductive-spike)
8. [Experiment 6: Command Latency](#8-experiment-6-command-latency)
9. [Experiment 7: Voice Recognition Accuracy](#9-experiment-7-voice-recognition-accuracy)
10. [Experiment 8: Processing Latency / Display Responsiveness](#10-experiment-8-processing-latency--display-responsiveness)
11. [Experiment 9: Move Validation Correctness](#11-experiment-9-move-validation-correctness)
12. [Planned Experiments (Not Yet Conducted)](#12-planned-experiments-not-yet-conducted)
13. [Summary of Findings](#13-summary-of-findings)
14. [Component Inventory](#14-component-inventory)
15. [Statement of Contributions](#15-statement-of-contributions)

---

## 1. Introduction

### 1.1 Project Overview
The "_Chess 2 Impress_" automated chessboard is a low-cost, accessible, voice-controlled chess platform, combining traditional play with automated piece movement and AI opponent integration. The system captures spoken commands via a USB microphone, processes them using the Vosk speech recognition engine (on a Raspberry Pi), validates moves using python-chess (with Stockfish as the AI opponent in single-player mode), and executes physical moves through a CoreXY gantry (driven by an Arduino Nano and TMC2209 stepper drivers). An under-board electromagnet repositions the magnetic chess pieces without disturbing neighboring pieces. The project is aimed at chess enthusiasts, players with limited mobility or visual impairments, and hobbyists who want an automated chess experience at a fraction of commercial prices.

### 1.2 Purpose of This Report
This report documents the experimental evaluation of the _Chess 2 Impress_ system against the critical specifications and success criteria (established in the conceptual and detailed design documents). Each experiment is designed to quantitatively verify that a specific subsystem or integrated behavior meets its required performance, safety, or reliability target.

### 1.3 Scope
This report covers experiments evaluating the following aspects of the system:
- **Motion subsystem:** move completion time, edge boundary/clamp safety, positional accuracy
- **Electromagnet subsystem:** switching latency, inductive spike clamping, capture reliability
- **Communication subsystem:** UART command latency, communication reliability, boot-noise rejection
- **Voice/processing subsystem:** recognition accuracy, end-to-end processing latency, move validation correctness
- **Power and safety:** thermal limits, voltage rails, EMI practices, mechanical/electrical compliance, fault behavior

---

## 2. Critical Success Criteria

Below are the critical requirements and success criteria identified by the team and approved by the advisor. These are drawn directly from the conceptual design specifications.

| # | Criterion | Target / Specification | Source (Customer Need / Design Requirement) | Associated Experiment |
|---|-----------|------------------------|--------------------------------------|-----------------------|
| 1 | Piece movement completion time | ≤ 5 seconds per move | Gameplay pacing / customer experience | Experiment 1 |
| 2 | Boot-noise rejection | No motion before `0x11` handshake | Safety / system integrity | Experiment 2 |
| 3 | CoreXY travel bounds | X ∈ [0.5, 7.5], Y ∈ [0.5, 13.5] squares | Mechanical safety / rail protection | Experiment 3 |
| 4 | Electromagnet switching latency | ≤ 10 ms on and off | Reliable piece pickup/release | Experiment 4 |
| 5 | Flyback diode clamping | Peak Vds ≤ 55 V (IRLZ44N max) | MOSFET protection / system longevity | Experiment 5 |
| 6 | Command latency (Arduino processing time) | ≤ 50 ms | Responsiveness / user experience | Experiment 6 |
| 7 | Voice recognition accuracy | ≥ 80% | Accessibility / usability | Experiment 7 |
| 8 | End-to-end processing latency (Pi) | ≤ 5 seconds from end of speech to display | Gameplay pacing | Experiment 8 |
| 9 | Move validation correctness | 100% correct legal/illegal classification | Game integrity | Experiment 9 |
| 10 | UART communication reliability | Error-free command transfer during full game | System reliability | Planned (UART Reliability) |
| 11 | Thermal safety | All surfaces ≤ 40 °C (104 °F) | UL 94 / CPSC 16 CFR 1505.7 | Planned (Thermal Safety) |
| 12 | Collision-free movement rate | ≥ 95% of moves collision-free | Conceptual design (Arduino spec) | Planned (Collision Rate) |
| 13 | Positional accuracy | ±0.5 mm across board | Precise piece placement | Planned (Positional Accuracy) |
| 14 | Voltage safety | All rails < 50 V DC | UL low-voltage threshold [2] | Planned (Voltage Safety) |
| 15 | EMI / low-noise design | Proper decoupling, low ripple, no interference | FCC Part 15 Subpart B [1] | Planned (EMI Indirect) |
| 16 | Mechanical & electrical safety compliance | Pass standardized inspection checklist | NEC / OSHA / ANSI Z535.4 [8][9][10] | Planned (Safety Compliance) |
| 17 | Fault-tolerant behavior | Safe, predictable response to power loss and obstruction | Reliability / user safety | Planned (Reliability & Failure) |

**Advisor Approval:**
- Approved by: _Dr. Van Neste_
- Date: _04-22-2026_

---

## 3. Experiment 1: Move Completion Time

### 3.1 Purpose and Justification
Verify that any single piece movement completes within 5 seconds of arriving at the source square, as specified in both the conceptual design and detailed design. This directly impacts gameplay pacing and user experience (slow moves frustrate players and reduce the perceived quality of the automated board).

### 3.2 Hypothesis / Expected Results
All move categories (short straight, long diagonal, knight, discard, and capture sequences) will complete under the 5-second spec, with long diagonal and full-field traverses taking the most time (expected ~3-4 s). Short straight moves are expected to complete in under 1 s.

### 3.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions, room temperature, normal lighting.

**Preparation Steps:**
1. Connect the Arduino Nano to the Pi via UART.
2. Verify belt tension on both CoreXY axes.
3. Home the system to (0.5, 0.5) and place the board in a known state.

**Procedure Steps:**
1. Execute the following move categories, one at a time, recording completion time for each:
   - **Short straight:** a1 → a2 (1 square vertical)
   - **Medium straight:** a1 → a4 (3 squares vertical)
   - **Long straight:** a1 → a8 (7 squares vertical, full playing-field traverse)
   - **Diagonal:** a1 → c3 (2 squares diagonal)
   - **Long diagonal:** a1 → h8 (7 squares diagonal)
   - **Knight:** a1 → b3 (standard L-move)
   - **Discard (straight):** a1 → a11 (playing field to discard row)
   - **Long discard (L-shaped):** h8 → a11 (L-shaped path to discard row)
   - **Capture sequence:** a1 → a11 (piece to discard), then a8 → a1 (attacker to destination)
2. For each move, record time from when the piece is grabbed at its starting position to when it is dropped off at its ending position.
3. Re-home between categories to eliminate cumulative positional drift.

### 3.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Elapsed time | seconds | Phone Timer (start on grab, stop on release) | Per trial | Spreadsheet |
| Move category | — | Manual log | Per trial | Spreadsheet |
| Source / destination | square | Manual log | Per trial | Spreadsheet |
| Exceeds 5 s | Y/N | Derived from time | Per trial | Spreadsheet |

### 3.5 Trials
- **Number of trials:** N = 10 per category.
- **Justification:** The variety of categories ensures full coverage of the motion system; 10 trials per category provides meaningful mean and max values.

### 3.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Mechanical friction varies with board position | Test moves across different regions of the board |
| Belt tension changes over time | Check belt tension before the test session |
| Human timer reaction time | Use a single operator; average across many trials |

### 3.7 Actual Results

**Raw Data:**

| Trial | Move Category | Source → Dest | Elapsed Time (s) | Notes |
|-------|---------------|---------------|------------------|-------|
| 1 | Short straight | a1 → a2 | 5.58 | Exceeds 5 s spec |
| 2 | Medium straight | a1 → a4 | 8.13 | Exceeds 5 s spec |
| 3 | Long straight | a1 → a8 | 12.86 | Exceeds 5 s spec |
| 4 | Diagonal | a1 → c3 | 9.30 | Exceeds 5 s spec |
| 5 | Long diagonal | a1 → h8 | 22.04 | Exceeds 5 s spec |
| 6 | Knight | a1 → b3 | 11.21 | Exceeds 5 s spec |
| 7 | Discard (straight) | a1 → a11 | 7.94 | Exceeds 5 s spec |
| 8 | Long discard (L-shaped) | h8 → a11 | 30.00 | Exceeds 5 s spec (worst case) |
| 9 | Capture seq 1 (piece → discard) | a1 → a11 | 8.34 | Exceeds 5 s spec |
| 10 | Capture seq 2 (attacker → dest) | a8 → a1 | 12.63 | Exceeds 5 s spec |

**Summary Statistics:**
- Overall mean: 12.80 s
- Min: 5.58 s (shortest move, still exceeds spec)
- Max: 30.00 s (long L-shaped discard)
- Number of trials exceeding 5 s: **10 / 10**

### 3.8 Interpretation and Conclusions
The system failed to meet the 5-second spec on every single trial, including the shortest possible move. The overall mean of 12.8 s is more than double the target, and worst-case moves approach 30 s. The data shows a clear pattern: longer paths take longer (as expected), but even the minimum-distance move at 5.58 s falls outside the spec. This means the issue is not simply "long paths are slow", the issue is that the baseline is already at or above the limit. The primary contributor is a conservative stepper speed/acceleration in the current CoreXY firmware.

### 3.9 Pass / Fail Against Criterion
- **Criterion Target:** ≤ 5 s per move
- **Measured Result:** 10 / 10 trials exceeded 5 s; mean 12.80 s, max 30.00 s
- **Outcome:** Fail

### 3.10 Components Used / Damaged / Replaced
No components were damaged during the session.
- _Arduino Nano (A000005)_
- _Raspberry Pi 5_
- _CoreXY gantry assembly_
- _TMC2209 stepper drivers (both)_
- _Electromagnet + MOSFET_
- _Phone timer_

---

## 4. Experiment 2: Boot Noise

### 4.1 Purpose and Justification
Verify that the Control Unit (Arduino) ignores all UART traffic during Raspberry Pi boot until the `0x11` handshake byte is received. This behavior is implemented in the `piReady` flag. Without this protection, random characters sent by the Pi during boot could be misinterpreted as move commands and cause unintended motion (which is a safety hazard for both the mechanism and anyone near the board).

### 4.2 Hypothesis / Expected Results
The carriage will remain stationary throughout the about-45-second Pi boot. After `0x11` is received, the next valid command will execute normally. We expect 3/3 passes.

### 4.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Power off the entire system.
2. Mark the carriage position with a piece of tape on the rail.

**Procedure Steps:**
1. Full power-cycle the system with the Pi connected.
2. Observe the carriage continuously during the about-45-second Pi boot. Verify no movement occurs.
3. After the chess software sends `0x11`, send a valid command and verify it executes correctly.
4. Power off and repeat for 3 total cold boots.

### 4.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Boot-time movement | Y/N | Visual observation | Per trial | Pass/fail table |
| `0x11` received | Y/N | Correct Execution | Per trial | Pass/fail table |
| Post-handshake command executed | Y/N | Visual | Per trial | Pass/fail table |

### 4.5 Trials
- **Number of trials:** N = 3 cold boots.
- **Justification:** Boot noise varies slightly between boots; 3 trials confirms repeatability of the handshake gate.

### 4.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Boot noise varies between boots | Test across 3 separate cold boots |

### 4.7 Actual Results

| Trial | Boot Movement (Y/N) | Start Command Received (Y/N) | Valid Command Executed (Y/N) | Pass/Fail |
|-------|---------------------|------------------------------|------------------------------|-----------|
| 1 | No | Yes | Yes | Pass |
| 2 | No | Yes | Yes | Pass |
| 3 | No | Yes | Yes | Pass |

**Summary Statistics:** Pass rate: 3 / 3 (100%)

### 4.8 Interpretation and Conclusions
The `piReady` flag successfully gated all UART input during boot across all three cold-boot trials. The carriage remained stationary during each about-45-second Pi boot, the handshake byte `0x11` was correctly received in every trial, and the first valid post-handshake command executed correctly every time. This confirms that boot-time noise on the UART line cannot trigger spurious motion.

### 4.9 Pass / Fail Against Criterion
- **Criterion Target:** No motion during boot; handshake required before commands execute
- **Measured Result:** 3 / 3 pass
- **Outcome:** Pass

### 4.10 Components Used / Damaged / Replaced
No components were damaged.
- _Arduino Nano (A000005)_
- _Raspberry Pi 5_
- _CoreXY gantry assembly_

---

## 5. Experiment 3: Edge Boundary and Clamp Verification

### 5.1 Purpose and Justification
Verify that the software clamping logic prevents the CoreXY head from moving beyond the center of any edge square (X ∈ [0.5, 7.5], Y ∈ [0.5, 13.5] in square units), and that the edge-travel algorithm correctly avoids the outermost board edges. This is a safety-critical requirement, as exceeding travel limits could damage the CoreXY mechanism or dislodge the carriage from the rails.

### 5.2 Hypothesis / Expected Results
Clamping logic will hold the carriage within the specified X and Y bounds for all four tested boundary conditions. Expected: 4/4 passes.

### 5.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Home the system to (0.5, 0.5).
2. Visually confirm the rail limits on each of the four sides.

**Procedure Steps:**
1. Execute the following edge/boundary moves:
   - **Column a vertical:** a1 → a8 (X must not reach 0.0)
   - **Column h vertical:** h1 → h8 (X must not reach 8.0)
   - **Discard from column a:** a1 → a11 (Y must not go below 0.5)
   - **Discard from column h:** h8 → h10 (Y must not go above 13.5)
2. Visually confirm the carriage never reaches or crosses the outermost rail.
3. Record pass/fail. If a violation is observed, record approximate position and axis.
4. Re-home between each trial to prevent cumulative error.

### 5.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Boundary tested | X min / X max / Y min / Y max | Test case assignment | Per trial | Table |
| Carriage stayed within bounds | Y/N | Visual observation | Per trial | Table |
| Violation position (if any) | square units | Visual estimate | As needed | Table |

### 5.5 Trials
- **Number of trials:** N = 4 (one per boundary condition).
- **Justification:** Covers all four possible rail-collision concerns.

### 5.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Cumulative positional error from prior moves | Re-home between trials |

### 5.7 Actual Results

| Test Move | Source | Destination | Boundary Tested | Stayed Within Bounds (Y/N) |
|-----------|--------|-------------|-----------------|----------------------------|
| a1 → a8 | a1 | a8 | X left (X min) | Y |
| h1 → h8 | h1 | h8 | X right (X max) | Y |
| a1 → a11 | a1 | a11 | Y bottom (Y min) | Y |
| h8 → h10 | h8 | h10 | Y top (Y max) | Y |

**Summary Statistics:** Pass rate: 4 / 4 (100%)

### 5.8 Interpretation and Conclusions
The software clamping logic successfully constrained the carriage to within the specified X and Y bounds on all four boundary tests. The carriage never reached or crossed the outermost physical rail on any side during these trials. This confirms that the edge-travel algorithm and the clamping code in the CoreXY firmware work as designed, and that the mechanism is protected from rail collisions that could dislodge the carriage.

### 5.9 Pass / Fail Against Criterion
- **Criterion Target:** Carriage remains within X ∈ [0.5, 7.5], Y ∈ [0.5, 13.5] for all moves
- **Measured Result:** 4 / 4 pass
- **Outcome:** Pass

### 5.10 Components Used / Damaged / Replaced
No components were damaged.
- _Arduino Nano (A000005)_
- _CoreXY gantry assembly_

---

## 6. Experiment 4: Electromagnet Switching Latency

### 6.1 Purpose and Justification
Verify that the MOSFET-based electromagnet switching circuit activates within 10 ms, as specified in the detailed design. Quick pickup/release is essential, as a dropped piece mid-move ruins the game (from the customer's perspective).

### 6.2 Hypothesis / Expected Results
Turn-on and turn-off latencies will both be well under 10 ms.

### 6.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Attach oscilloscope probes to the Arduino's MAGNET_PIN (D10) output and to the MOSFET drain.

**Procedure Steps:**
1. Command the Arduino to toggle the electromagnet on and off using `magnetOn()` and `magnetOff()` in a test loop with 2-second delays between toggles.
2. Measure the time from the rising edge of the gate signal to the point where drain current reaches 90% of steady state (turn-on latency).
3. Measure the time from the falling edge of the gate signal to the point where drain current drops below 10% (turn-off latency).
4. Repeat for 10 switching cycles.

### 6.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Turn-on latency | µs | Oscilloscope cursor | Per cycle | Spreadsheet |
| Turn-off latency | µs | Oscilloscope cursor | Per cycle | Spreadsheet |

### 6.5 Trials
- **Number of trials:** N = 10 switching cycles.
- **Justification:** Ten measurements provide reliable mean and max values to confirm the <10 ms spec.

### 6.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Oscilloscope bandwidth limits edge precision | Use a scope with ≥ 20 MHz bandwidth |

### 6.7 Actual Results

| Trial | Turn-On Latency (µs) | Turn-Off Latency (µs) |
|-------|----------------------|------------------------|
| 1  | 3.0 | 3.0 |
| 2  | 2.7 | 2.8 |
| 3  | 3.0 | 2.9 |
| 4  | 2.8 | 2.9 |
| 5  | 2.6 | 2.7 |
| 6  | 3.0 | 3.0 |
| 7  | 2.7 | 2.6 |
| 8  | 2.8 | 2.8 |
| 9  | 2.9 | 3.0 |
| 10 | 2.8 | 2.7 |

**Summary Statistics:**
- Turn-on: Mean 2.83 µs, Max 3.0 µs
- Turn-off: Mean 2.84 µs, Max 3.0 µs
- Both values are about 3300× faster than the 10 ms spec.

**Visualizations:**

![Electromagnet turn-on rising edge on oscilloscope](./Images/Electromagnet_Rising_Edge_example.jpg)

_Figure 6.1 — Oscilloscope capture of the gate and drain waveforms during electromagnet turn-on (rising edge)._

![Electromagnet turn-off falling edge on oscilloscope](./Images/Electromagnet_Falling_Edge_example.jpg)

_Figure 6.2 — Oscilloscope capture of the gate and drain waveforms during electromagnet turn-off (falling edge)._

### 6.8 Interpretation and Conclusions
Turn-on and turn-off latencies are both in the low-microsecond range, far below the 10 ms specification. The IRLZ44NPBF logic-level MOSFET responds almost immediately to the gate signal, and the measured variation between trials (2.6–3.0 µs) is small enough to be attributable to measurement noise and cursor placement on the oscilloscope. This result demonstrates that the electromagnet switching path introduces negligible delay into the overall move-completion budget.

### 6.9 Pass / Fail Against Criterion
- **Criterion Target:** ≤ 10 ms turn-on and turn-off
- **Measured Result:** Max 3.0 µs on both edges
- **Outcome:** Pass

### 6.10 Components Used / Damaged / Replaced
No components were damaged.
- _Arduino Nano (A000005)_
- _IRLZ44NPBF MOSFET_
- _Electromagnet coil_
- _Oscilloscope (≥ 20 MHz bandwidth)_

---

## 7. Experiment 5: Flyback Diode Inductive Spike

### 7.1 Purpose and Justification
Verify that the flyback diode clamps the inductive voltage spike on the MOSFET drain to within the IRLZ44NPBF's maximum Vds rating (55 V) when the electromagnet is switched off. An unclamped spike could destroy the MOSFET, causing permanent system failure.

### 7.2 Hypothesis / Expected Results
The clamped spike will peak well below 55 V (expected about 13–15 V, just above the 12 V rail) and remain essentially constant (regardless of energization duration).

### 7.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions; ambient temperature recorded per trial.

**Preparation Steps:**
1. Connect the oscilloscope probe to the MOSFET drain pin with the shortest possible ground lead.
2. Set scope to trigger on falling edge of the gate signal; set vertical scale sufficient to capture spikes up to 60 V.

**Procedure Steps:**
1. Command the Arduino to energize the electromagnet for the specified on-duration, then switch off.
2. Capture the drain voltage waveform during the off-switching event.
3. Record the peak voltage spike magnitude and its duration.
4. Repeat for on-durations of 200 ms, 1 s, 2 s, and 5 s.

### 7.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| On-duration | s | Test case parameter | Per trial | Table |
| Peak spike voltage | V | Oscilloscope cursor | Per trial | Table |
| Ambient temperature | °F | Thermometer | Per trial | Table |

### 7.5 Trials
- **Number of trials:** N = 4 on-durations.
- **Justification:** Varying on-duration ensures the diode performs under different stored-energy conditions.

### 7.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Probe ground-lead inductance causes ringing | Use shortest possible ground lead |
| Ambient temperature affects diode Vf | Record ambient temperature per trial |

### 7.7 Actual Results

| Trial | On-Duration (s) | Peak Spike (V) | Ambient (°F) | Pass/Fail |
|-------|------------------|----------------|--------------|-----------|
| 1 | 0.2 | 5 | 62 | Pass |
| 2 | 1.0 | 5 | 62 | Pass |
| 3 | 2.0 | 5 | 63 | Pass |
| 4 | 5.0 | 5 | 62 | Pass |

**Summary Statistics:** Max spike: 5 V (well below the 55 V Vds limit).

**Visualizations:**

![Flyback diode clamped spike and fall waveform on oscilloscope](./Images/Diode_Spike_and_Fall_example.jpg)

_Figure 7.1 — Representative oscilloscope capture of the clamped inductive spike and the decay back to the rail voltage._

### 7.8 Interpretation and Conclusions
The flyback diode clamps the inductive spike to about 5 V across all tested energization durations (200 ms to 5 s), which is far below the 55 V Vds limit of the IRLZ44NPBF MOSFET. The peak spike magnitude is essentially independent of on-duration, which matches expected behavior: once the coil has reached its steady-state current, the stored inductive energy is the same regardless of how long the on-time has been (and the diode clamps that energy to approximately one diode drop above the rail). The measured peak is lower than the about 13–15 V hypothesis because the low coil current combined with the diode's forward-voltage characteristic kept the observed peak near about 5 V. The MOSFET is safely protected against destructive spikes under all tested conditions.

### 7.9 Pass / Fail Against Criterion
- **Criterion Target:** Peak Vds ≤ 55 V
- **Measured Result:** Max 5 V observed
- **Outcome:** Pass

### 7.10 Components Used / Damaged / Replaced
No components were damaged.
- _IRLZ44NPBF MOSFET_
- _Flyback diode_
- _Electromagnet coil_
- _Oscilloscope_
- _Thermometer_

---

## 8. Experiment 6: Command Latency

### 8.1 Purpose and Justification
Verify that the Control Unit processes and begins executing a received UART command within 50 ms of receipt, as required by detailed design. Low latency is critical from the customer's perspective to ensure the board feels responsive during gameplay.

### 8.2 Hypothesis / Expected Results
Command latency will be well below 50 ms (expected about 2–10 ms, dominated by the Arduino main loop polling interval) and consistent across move types.

### 8.3 Procedure

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Connect the Arduino Nano to the Pi via UART (with logic level converter).
2. Attach oscilloscope probes to the Arduino RX pin (D0) and to a TMC2209 STEP output (D6).
3. Ensure the system is powered, homed, and idle.

**Procedure Steps:**
1. Send a single valid 2-byte binary move command from the Pi (e.g., `0x12 0x14` for a1 → a3).
2. Trigger the scope on the falling edge of the RX start bit.
3. Measure the time delta from the end of the second received byte to the first rising edge on the STEP pin.
4. Repeat for 7 straight-move trials, then 3 additional trials with diagonal and knight moves.

### 8.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Latency | µs | Oscilloscope cursor | Per trial | Spreadsheet |
| Move type | — | Manual log | Per trial | Spreadsheet |

### 8.5 Trials
- **Number of trials:** N = 10 (7 straight + 3 special).
- **Justification:** 10 trials provide sufficient data to identify outliers and confirm consistency across move types.

### 8.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Arduino main loop polling position varies | Keep system in consistent idle state before each trial |
| Unrelated serial traffic | Ensure no other serial traffic during measurement |

### 8.7 Actual Results

| Trial | Move | Move Type | Latency (µs) |
|-------|------|-----------|--------------|
| 1  | A2 → A4 | Straight (startup) | 736 |
| 2  | A7 → A45 | Straight | 596 |
| 3  | B2 → B3 | Straight | 598 |
| 4  | B8 → A6 | L-move | 610 |
| 5  | C1 → A3 | Diagonal | 618 |
| 6  | B7 → B6 | Straight | 600 |
| 7  | H2 → H3 | Straight (startup) | 758 |
| 8  | G7 → G5 | Straight | 608 |
| 9  | H1 → H3 | Straight | 618 |
| 10 | G8 → F6 | L-move | 622 |

**Summary Statistics:**
- Mean: 636.4 µs (about 0.636 ms)
- Standard deviation: 56.1 µs
- Min: 596 µs / Max: 758 µs

### 8.8 Interpretation and Conclusions
Command latency is consistently in the sub-millisecond range (max 0.758 ms), roughly 66× faster than the 50 ms specification. Move type (straight, diagonal, or L-move) has no meaningful effect on latency; all measurements cluster tightly around about 600 µs, with the two highest values (736 and 758 µs) occurring on the first commands after system startup. This "startup" pattern is consistent with one-time initialization or cache warming on the Arduino's first move after power-on. After the first move, steady-state latency settles to about 596–622 µs and shows very low variability (standard deviation about 56 µs). The Arduino main loop therefore meets the responsiveness spec, with a comfortable margin regardless of move type.

### 8.9 Pass / Fail Against Criterion
- **Criterion Target:** ≤ 50 ms
- **Measured Result:** Mean 0.636 ms, Max 0.758 ms
- **Outcome:** Pass

### 8.10 Components Used / Damaged / Replaced
No components were damaged.
- _Arduino Nano (A000005)_
- _Raspberry Pi 5_
- _UART debug cable (with logic level converter)_
- _TMC2209 stepper driver_
- _Oscilloscope_

---

## 9. Experiment 7: Voice Recognition Accuracy

### 9.1 Purpose and Justification
Verify the Vosk speech recognition pipeline meets the 80% minimum accuracy requirement under typical indoor conditions, as specified in the conceptual design. This is a core accessibility feature, as users with limited mobility depend on reliable voice control.

### 9.2 Hypothesis / Expected Results
Accuracy will exceed 80% across most speakers, with some variation based on accent and microphone placement. We expect some drop for non-native speakers or speakers with quieter voices.

### 9.3 Procedure

**Equipment & Inventory Items Used:**
- _[Item # — USB microphone]_
- _[Item # — Raspberry Pi 5 (running Vosk)]_

**Environmental Conditions:**
- Standard indoor conditions; quiet room; fixed microphone position (speaker at ~25 inches from microphone, medium speaking volume). A loud background fan was present during early trials but was turned off partway through the session.

**Preparation Steps:**
1. Prepare a list of 20 standardized test commands covering all types:
   - Move commands (coordinate form and named-piece form, e.g. "move b2b4", "move knight a six", "move bishop e three")
   - System commands ("chess resign", "chess yes", "Chess Two")
   - Castle command ("move castle")
2. Fix microphone position for all speakers.

**Procedure Steps:**
1. Each speaker reads each of the 20 prepared commands once at normal conversational pace.
2. Record whether Vosk recognized the command on the first try (Y/N) and whether the recognition result was correct (Y/N).
3. Calculate accuracy across speakers.

**Scoring definitions (per the spreadsheet notes):**
- **Recognized (Y)** = recognized on the first try (no re-prompt needed).
- **Correct (Y)** = correct after being recognized.

### 9.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Command spoken | — | Test script | Per trial | Spreadsheet |
| Recognized on first try | Y/N | System response | Per trial | Spreadsheet |
| Correct after recognition | Y/N | Manual comparison | Per trial | Spreadsheet |
| Speaker | name | Manual log | Per trial | Spreadsheet |

### 9.5 Trials
- **Number of trials:** N = 100 (20 commands × 5 speakers) planned. Actual dataset reported below covers the 4 speakers whose sessions were fully scored. Nathan's session was run but the Recognized/Correct columns were not filled in and are excluded from the numeric totals below (he will be re-run or scored retrospectively before final submission).
- **Justification:** Provides statistically meaningful accuracy and captures speaker variation.

### 9.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Speaker familiarity with command list | Speakers read from script without prior rehearsal |
| Microphone placement variation | Fix microphone position for all trials |
| Background noise | Test in a consistent quiet room; loud fan turned off partway through |

### 9.7 Actual Results

| Speaker | Recognized on First Try | Correct After Recognition | Recognized (%) | Correct (%) |
|---------|-------------------------|----------------------------|----------------|-------------|
| Jack    | 20 / 20 | 20 / 20 | 100% | 100% |
| Allison | 20 / 20 | 18 / 20 | 100% | 90% |
| Noah    | 19 / 20 | 20 / 20 | 95% | 100% |
| Lewis   | 20 / 20 | 20 / 20 | 100% | 100% |
| Nathan  | _[not scored]_ | _[not scored]_ | — | — |

**Summary Statistics (4 scored speakers, N = 80):**
- Overall recognition rate on first try: 79 / 80 = **98.8%**
- Overall correctness after recognition: 78 / 80 = **97.5%**
- Failing trials: Noah trial 8 (`move d1d3`, not recognized on first try); Allison trials 9 and 10 (`move knight h six` and `move bishop e three`, recognized but returned incorrect moves).

**Visualizations:**
_[Figure 9.1 — per-speaker accuracy bar chart — repo image name TBD]_

### 9.8 Interpretation and Conclusions
Voice recognition clearly exceeds the 80% spec, with both first-try recognition (98.8%) and post-recognition correctness (97.5%) in the high-90s range across the four scored speakers. The small number of failures fall into two categories: one missed first-try recognition (a command that used coordinate form), and two commands using named-piece form ("move knight h six" and "move bishop e three") that were misinterpreted as different moves. This suggests the pipeline is nearly perfect for coordinate-form commands but has slightly weaker disambiguation on named-piece commands for some speakers. Nathan's session needs to be re-run or scored retrospectively before final submission so all five speakers are represented. Overall, the system comfortably passes the spec under these test conditions.

### 9.9 Pass / Fail Against Criterion
- **Criterion Target:** ≥ 80% overall
- **Measured Result:** 98.8% recognition / 97.5% correctness across 4 scored speakers (N = 80)
- **Outcome:** ☒ Pass

### 9.10 Components Used / Damaged / Replaced
No components were damaged.

---

## 10. Experiment 8: Processing Latency / Display Responsiveness

### 10.1 Purpose and Justification
Verify that from end of voice input to validated move determination/display takes under 5 seconds, as specified in the conceptual design. This is a customer-facing responsiveness requirement.

### 10.2 Hypothesis / Expected Results
End-to-end latency will be under 5 s for legal moves and comparable for illegal moves (rejection shown promptly). Stockfish move generation is NOT included in this measurement — only voice-to-display pipeline.

### 10.3 Procedure

**Equipment & Inventory Items Used:**
- _[Item # — USB microphone]_
- _[Item # — Raspberry Pi 5 (chess program)]_
- _[Item # — Display screen]_
- _[Item # — Stopwatch or audio recording]_

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Set up the Pi with chess program running in 1-player (vs. Stockfish) or 2-player mode.

**Procedure Steps:**
1. Using a stopwatch or audio recording, measure time from when the player stops speaking to when the move is either executed or rejected on screen.
2. Include both legal and illegal moves to measure rejection latency.
3. Record 40 total moves.

### 10.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Time from end of speech to display update | s | Stopwatch / audio | Per trial | Spreadsheet |
| Legal / illegal | — | Manual | Per trial | Spreadsheet |

### 10.5 Trials
- **Number of trials:** N = 40.
- **Justification:** Mix of legal and illegal moves provides broad coverage of the voice-processing path.

### 10.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Stockfish thinking time inflates total latency | Separate voice-processing time from engine time in analysis |
| Stopwatch reaction time | Use audio recording with waveform markers where possible |

### 10.7 Actual Results

| Trial | Command | Legal/Illegal | Speech-to-Display (s) |
|-------|---------|---------------|------------------------|
| 1  | c2c4 | L | 1.06 |
| 2  | f3f5 | i | 1.01 |
| 3  | h7h5 | L | 1.16 |
| 4  | g1f4 | i | 0.98 |
| 5  | g1f3 | L | 1.03 |
| 6  | h1h7 | i | 0.84 |
| 7  | h8h6 | L | 0.97 |
| 8  | c1c3 | i | 1.41 |
| 9  | b1a3 | L | 0.96 |
| 10 | f3d4 | i | 1.08 |
| 11 | h6d6 | L | 1.21 |
| 12 | d6d4 | i | 1.16 |
| 13 | d1a4 | L | 0.95 |
| 14 | h1h1 | i | 0.61 |
| 15 | d6d4 | L | 0.88 |
| 16 | castle | i | 1.04 |
| 17 | d2d3 | L | 1.18 |
| 18 | h5g4 | i | 0.95 |
| 19 | h5h4 | L | 1.10 |
| 20 | f1g8 | i | 0.80 |
| 21 | c1d2 | L | 0.68 |
| 22 | d4c5 | i | 1.06 |
| 23 | d4c4 | L | 1.25 |
| 24 | castle | i | 0.93 |
| 25 | d2c3 | L | 1.01 |
| 26 | b8a5 | i | 1.06 |
| 27 | b8a6 | L | 0.96 |
| 28 | e7e5 | i | 0.91 |
| 29 | castle | L | 1.11 |
| 30 | d4a3 | i | 0.85 |
| 31 | c4a4 | L | 0.71 |
| 32 | c1a1 | i | 0.96 |
| 33 | c1d2 | L | 0.81 |
| 34 | e2e5 | i | 0.88 |
| 35 | a4a3 | L | 0.81 |
| 36 | g2f1 | i | 0.88 |
| 37 | g2g4 | L | 0.76 |
| 38 | h4h2 | i | 0.84 |
| 39 | h4g3 (en passant) | L | 1.01 |
| 40 | a1a8 | i | 0.98 |

**Summary Statistics:**
- Mean: 0.971 s
- Standard deviation: 0.161 s
- Min: 0.61 s / Max: 1.41 s
- All 40 trials well below the 5 s spec.

**Visualizations:**
_[Figure 10.1 — histogram or box plot of latency by legal/illegal — repo image name TBD]_

### 10.8 Interpretation and Conclusions
End-to-end processing latency from end of speech to display update is consistently around 1 second, with a maximum of 1.41 s across 40 trials — approximately 3.5× faster than the 5 s spec. There is no meaningful difference in latency between legal and illegal moves, which confirms that python-chess validation executes quickly enough that rejection is presented with the same responsiveness as acceptance. This means that even when a user issues an illegal move, they get feedback in roughly the same time as for a valid move, which is important for a good user experience.

### 10.9 Pass / Fail Against Criterion
- **Criterion Target:** ≤ 5 s
- **Measured Result:** Mean 0.97 s, Max 1.41 s
- **Outcome:** ☒ Pass

### 10.10 Components Used / Damaged / Replaced
No components were damaged.

---

## 11. Experiment 9: Move Validation Correctness

### 11.1 Purpose and Justification
Verify that python-chess correctly accepts legal moves and rejects illegal ones, and that the system communicates rejections clearly via the display. Misvalidation would break the core promise of a chess board — maintaining game integrity.

### 11.2 Hypothesis / Expected Results
100% correct classification of legal vs. illegal moves. Rejection messages will appear on the display within the 1-second spec.

### 11.3 Procedure

**Equipment & Inventory Items Used:**
- _[Item # — Raspberry Pi 5]_
- _[Item # — Display screen]_
- _[Item # — USB microphone]_

**Environmental Conditions:**
- Standard indoor lab conditions.

**Preparation Steps:**
1. Prepare 20 legal moves and 20 illegal moves covering edge cases:
   - Castling (legal/illegal)
   - Moves from wrong-color pieces
   - En passant
   - Captures (legal/illegal)

**Procedure Steps:**
1. Input each move via voice command.
2. Record whether the system correctly accepted or rejected each.
3. Verify that rejection messages appear on display within spec.

### 11.4 Data Collection Plan

| Variable | Units | Measurement Method | Frequency | Recording Format |
|----------|-------|--------------------|-----------|------------------|
| Move | algebraic | Test script | Per trial | Spreadsheet |
| Expected result | legal/illegal | Test script | Per trial | Spreadsheet |
| Actual result | legal/illegal | System response | Per trial | Spreadsheet |
| Correct | Y/N | Derived | Per trial | Spreadsheet |

### 11.5 Trials
- **Number of trials:** N = 40 (20 legal + 20 illegal).
- **Justification:** Covers all major chess rules including edge cases.

### 11.6 Potential Biases and Mitigation

| Potential Bias / Source of Error | Mitigation Strategy |
|----------------------------------|---------------------|
| Voice mis-recognition could masquerade as validation error | Confirm recognized command on display before counting result |
| Non-representative move selection | Include diverse rule edge cases |

### 11.7 Actual Results

| Trial | Command | Expected (L/i) | Correct (Y/N) |
|-------|---------|----------------|----------------|
| 1  | c2c4 | L | Y |
| 2  | f3f5 | i | Y |
| 3  | h7h5 | L | Y |
| 4  | g1f4 | i | Y |
| 5  | g1f3 | L | Y |
| 6  | h1h7 | i | Y |
| 7  | h8h6 | L | Y |
| 8  | c1c3 | i | Y |
| 9  | b1a3 | L | Y |
| 10 | f3d4 | i | Y |
| 11 | h6d6 | L | Y |
| 12 | d6d4 | i | Y |
| 13 | d1a4 | L | Y |
| 14 | h1h1 | i | Y |
| 15 | d6d4 | L | Y |
| 16 | castle | i | Y |
| 17 | d2d3 | L | Y |
| 18 | h5g4 | i | Y |
| 19 | h5h4 | L | Y |
| 20 | f1g8 | i | Y |
| 21 | c1d2 | L | Y |
| 22 | d4c5 | i | Y |
| 23 | d4c4 | L | Y |
| 24 | castle | i | Y |
| 25 | d2c3 | L | Y |
| 26 | b8a5 | i | Y |
| 27 | b8a6 | L | Y |
| 28 | e7e5 | i | Y |
| 29 | castle | L | Y |
| 30 | d4a3 | i | Y |
| 31 | c4a4 | L | Y |
| 32 | c1a1 | i | Y |
| 33 | c1d2 | L | Y |
| 34 | e2e5 | i | Y |
| 35 | a4a3 | L | Y |
| 36 | g2f1 | i | Y |
| 37 | g2g4 | L | Y |
| 38 | h4h2 | i | Y |
| 39 | h4g3 (en passant) | L | Y |
| 40 | a1a8 | i | Y |

**Summary Statistics:** Correct: **40 / 40 (100%)**

**Visualizations:** _None required — all 40 trials returned the expected result._

### 11.8 Interpretation and Conclusions
Move validation returned the correct legal/illegal classification on all 40 trials, including all tested edge cases (legal and illegal castling, en passant, wrong-color pieces, and illegal captures). This perfect result confirms that python-chess is correctly configured as the validation engine and that the system's communication of validation decisions to the display works as designed for every tested rule category. Game integrity is preserved.

### 11.9 Pass / Fail Against Criterion
- **Criterion Target:** 100% correct
- **Measured Result:** 40 / 40 correct (100%)
- **Outcome:** ☒ Pass

### 11.10 Components Used / Damaged / Replaced
No components were damaged.

---

## 12. Planned Experiments (Not Yet Conducted)

The following experiments are designed and awaiting execution. Each is listed with full Purpose / Procedure / Data Collection / Trials / Biases in the same format as above, but with **Hypothesis, Results, Interpretation, and Pass/Fail sections intentionally blank** — they will be completed after execution.

### 12.1 UART Communication Reliability

**Purpose and Justification:** Verify that the binary UART protocol at 115200 bps provides reliable, error-free command transfer between the Pi and Arduino during gameplay. The physical movement of the correct piece to the correct square serves as confirmation of successful transmission, parsing, and execution. Communication errors during gameplay could cause wrong moves, dropped commands, or system hangs.

**Procedure:**
1. Connect the Pi to the Arduino via the UART debug cable (with logic level converter). Both set to 115200 bps.
2. Home the system to (0.5, 0.5) and set up starting positions.
3. Play a full game against Stockfish (or a second player). For each move:
   - Observe the CoreXY physically moving the correct piece from source to destination.
   - Record whether the piece moved correctly, incorrectly, or not at all.
   - Record whether ACK / NACK / timeout was received on the Pi side.
4. For captures, verify the captured piece is moved to the correct discard row before the attacker moves.
5. Target ≥ 40 total moves. Start a second game if needed.
6. After the game, send one final known-good command to confirm system responsiveness.

**Data Collection:** Columns (move number, expected source, expected destination, actual destination, piece moved correctly (Y/N), ACK/NACK/timeout, notes). Calculate error rate. For captures, record correctness of discard placement.

**Trials:** N = 40 moves. Exercises the communication chain under realistic conditions.

**Potential Biases:**
- A single game may not cover all move types → execute 2–3 manual commands of any skipped type after the game ends.
- Observer may miss subtle misplacements → verify piece position against Pi's displayed board state after each move.

---

### 12.2 Thermal Safety

**Purpose and Justification:** Verify that all system component surfaces remain below 40 °C (104 °F) during sustained operation (UL 94 flammability guidance and CPSC 16 CFR 1505.7). Overheating could cause thermal shutdown mid-game, material degradation, or burn hazard.

**Procedure:**
1. Install SMT heatsinks (Adafruit 1493) on both TMC2209 driver boards.
2. Record ambient room temperature.
3. Run simulated full-game sequence: continuous move commands over 30 minutes.
4. At each 10-minute interval, measure surface temperatures at each of the following components. "A" components are mounted on the left side of the board (closest to a wall) and "B" components are mounted on the right side (closest to the gap for the Pi/UPS):
   - Motor A
   - Motor B
   - Stepper Driver A
   - Stepper Driver B
   - MOSFET
   - Flyback diode
   - Arduino Nano
   - Electromagnet
   - Raspberry Pi 5
   - Screen (back surface)
   - UPS
   - Battery pack
   - UPS/Pi plastic mount
   - Booster 1
   - Booster 2
   - (Acrylic) board surface (top of board)
5. Record ambient temperature at each measurement point.
6. Note any thermal fault events (e.g., TMC2209 DIAG trigger).

**Data Collection:** Columns (trial, time (10/20/30 min), ambient (°F), one temperature column per component (°F), max temp, pass/fail at each time point). Calculate peak temperature per component across all measurements.

**Trials:** N = 3 timestamps × all components listed above.

**Potential Biases:**
- IR thermometer point consistency → measure the same surface location each time.
- Ambient variation between timestamps → record ambient every time.
- Airflow variation → run session in a consistent indoor location.

---

### 12.3 Positional Accuracy Verification _(on hold)_

**Purpose and Justification:** Evaluate whether the CoreXY system achieves positional accuracy within ±0.5 mm across the board. Directly supports precise chess piece placement.

**Procedure:**
1. Mark the center of at least 10 target squares (28.575 mm from each edge of a 57.15 mm square). Include: four corners (a1, h1, a8, h8), board center (d4 or e5), ≥ 2 discard row positions (a11, h10), ≥ 2 mid-edge positions (a4, d1).
2. Home to (0.5, 0.5).
3. Command the carriage to each target.
4. Measure X offset and Y offset from electromagnet center to marked center using a mm ruler or calipers.
5. Re-home between measurements.
6. Repeat across all target squares.

**Data Collection:** Columns (trial, target, target position (mm), X offset (mm), Y offset (mm), total error √(X² + Y²), pass/fail ≤ 0.5 mm). Calculate mean and max error.

**Trials:** N = 10 coordinates.

**Potential Biases:**
- Human measurement error ~±0.5 mm → same operator and method for all readings.

---

### 12.4 Collision-Free Capture and Movement Rate _(needs additional work)_

**Purpose and Justification:** Verify the system achieves ≥ 95% collision-free piece movements including captures. Piece collisions disrupt the game and damage user trust.

**Procedure:**
1. Place all 32 pieces in standard starting position.
2. Execute a predefined sequence of 30 moves covering:
   - 8 straight-line moves
   - 6 diagonal moves
   - 4 knight moves
   - 6 capture sequences
   - 4 discard/reset moves
   - 2 edge-boundary moves
3. For each move, record whether any non-target piece was displaced.
4. Restore displaced pieces before continuing.

**Data Collection:** Columns (move number, move type, source, destination, pass/fail, notes). Calculate success rate overall and per move type.

**Trials:** N = 30 moves (~±4.5% at 95% confidence).

**Potential Biases:**
- Piece placement consistency → center pieces before each session.
- Electromagnet strength varies with piece type → include all piece types.

---

### 12.5 Electrical Noise / EMI (Indirect)

**Purpose and Justification:** Evaluate whether the system follows low-noise design practices in the absence of formal EMI measurement equipment. Required by FCC Part 15 Subpart B [1] as a design-practice check rather than a formal compliance test.

**Procedure:**
1. Inspect the circuit for proper decoupling capacitors at each IC and grounding practices.
2. Measure voltage ripple on the 12 V and 5 V rails using an oscilloscope (if available).
3. Operate the system near sensitive electronics (e.g., AM radio, phone, nearby computers).
4. Observe any interference.

**Data Collection:** Columns (session, decoupling caps present (Y/N), voltage ripple (V), observed interference (Y/N), notes).

**Trials:** ≥ 3 observation sessions.

**Potential Biases:**
- No formal EMI chamber → document the limitation.
- Environmental noise varies → test in a consistent location.

---

### 12.6 Voltage Safety Verification

**Purpose and Justification:** Ensure all system voltage rails remain below the 50 V DC low-voltage safety threshold defined by UL [2] and NEC/NFPA 70 Article 725 [3].

**Procedure:**
1. Measure all voltage rails (12 V, 5 V, 3.3 V, any bus between the UPS and the rest of the system) using a calibrated multimeter during operation.
2. Record maximum observed voltage on each rail.

**Data Collection:** Columns (voltage rail, measured voltage (V), pass/fail < 50 V).

**Trials:** ≥ 3 measurements per rail.

**Potential Biases:**
- Meter accuracy → use a calibrated multimeter.

---

### 12.7 Mechanical & Electrical Safety Compliance

**Purpose and Justification:** Verify compliance with safety standards for wiring, grounding, labeling, and physical hazards. Addresses NEC Article 725 & 400 [3][8], OSHA 29 CFR 1910 Subpart S [9], and ANSI Z535.4 [10].

**Procedure:**
1. Inspect the system using a standardized checklist:
   - Wiring (NEC Article 725 & 400)
   - Grounding and circuit protection
   - Safety labels and accessibility
2. Verify grounding continuity with a multimeter.
3. Re-run inspection after any hardware modification.

**Data Collection:** Columns (category, checklist item, pass/fail, notes).

**Trials:** Single full inspection; repeat after modifications.

**Potential Biases:**
- Subjective inspection → use a standardized checklist.

---

### 12.8 System Reliability and Failure Behavior

**Purpose and Justification:** Ensure safe and predictable operation under fault conditions (power loss and mechanical obstruction).

**Procedure:**
1. Simulate power loss during an active move and observe the system response.
2. Introduce a mechanical obstruction in the path of the carriage during motion and observe the response.
3. Observe whether the system halts safely, reports the fault, and recovers predictably.

**Data Collection:** Columns (test type, system response, pass/fail, notes).

**Trials:** ≥ 3 per fault condition.

**Potential Biases:**
- Inconsistent obstruction placement → standardize method (same location, same object).

---

## 13. Summary of Findings

### 13.1 Overall Results vs. Success Criteria

| # | Criterion | Target | Measured Result | Met? |
|---|-----------|--------|-----------------|------|
| 1 | Move completion time | ≤ 5 s | Mean 12.80 s, Max 30.00 s (10 / 10 trials exceeded spec) | **N** |
| 2 | Boot-noise rejection | No motion before handshake | 3 / 3 pass | Y |
| 3 | CoreXY travel bounds | X ∈ [0.5, 7.5], Y ∈ [0.5, 13.5] | 4 / 4 pass | Y |
| 4 | Electromagnet switching latency | ≤ 10 ms | Max 3.0 µs (on and off) | Y |
| 5 | Flyback diode clamping | ≤ 55 V Vds | Max 5 V | Y |
| 6 | Command latency | ≤ 50 ms | Mean 0.636 ms, Max 0.758 ms | Y |
| 7 | Voice recognition accuracy | ≥ 80% | 98.8% recognition / 97.5% correctness (N = 80, 4 speakers) | Y |
| 8 | End-to-end processing latency | ≤ 5 s | Mean 0.97 s, Max 1.41 s | Y |
| 9 | Move validation correctness | 100% | 40 / 40 correct | Y |
| 10–17 | _Planned experiments_ | See §12 | Pending | Pending |

### 13.2 Did the Project Meet Its Success Criteria?
Of the nine success criteria that have been experimentally evaluated to date, eight are met — most of them by very wide margins (electromagnet switching is ~3,300× faster than spec, command latency is ~66× faster, flyback clamping is ~11× below the Vds limit, and processing latency, voice recognition, move validation, boot-noise rejection, and edge clamping all pass cleanly). The sole unmet criterion is move completion time: every trial exceeded the 5-second target, with a mean of 12.8 s and a worst case of 30 s. Eight additional criteria (thermal, UART reliability, collision-free rate, positional accuracy, voltage safety, EMI, safety compliance, and fault tolerance) remain to be tested. Based on present evidence the system's electrical, logical, and communication subsystems meet requirements, while the mechanical motion subsystem does not meet the completion-time spec and requires rework.

### 13.3 Discrepancies and Unmet Criteria
- **Move Completion Time (Exp 1, Criterion #1 — FAIL):** Measured times ranged 5.58 s (shortest move) to 30.00 s (long L-shaped discard), versus a 5 s target. The fact that even a single-square move exceeds the spec indicates the baseline per-move overhead is already at or above the limit, which points to conservative acceleration/speed settings in the CoreXY firmware, magnet dwell time during pickup/release, and homing overhead between moves as the primary contributors rather than just path length.

### 13.4 Proposed Improvements / Next Steps
- **Priority 1:** Retune the CoreXY firmware — increase stepper acceleration and maximum speed, reduce unnecessary homing between moves, and minimize magnet dwell time to the shortest value that still reliably couples and decouples pieces. Re-run Experiment 1 after each change to isolate which contributor is dominant.
- Complete the planned experiments in §12, prioritizing the thermal safety and UART reliability tests since those are the closest to being ready to execute.
- Re-run or retroactively score Nathan's voice-recognition session so all five speakers are represented in Experiment 7.

### 13.5 Lessons Learned
_[To be completed as a team reflection once all experiments are done — intended to cover methodology (e.g., stopwatch vs. logged timing), teamwork, and any unexpected findings that came out of the process.]_

---

## 14. Component Inventory

### 14.1 Initial Inventory

| Item # | Description | Quantity | Vendor/Source | Order # / ID | Storage Location | Date Acquired | Condition | Notes |
|--------|-------------|----------|---------------|--------------|------------------|---------------|-----------|-------|
| 001 | Raspberry Pi 5 | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Processing Unit |
| 002 | Arduino Nano (A000005) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Control Unit |
| 003 | TMC2209 stepper driver (A, left side) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY left side |
| 004 | TMC2209 stepper driver (B, right side) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY right side |
| 005 | Stepper motor (A, left side) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY left side |
| 006 | Stepper motor (B, right side) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY right side |
| 007 | IRLZ44N MOSFET | _[qty]_ | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Magnet switching |
| 008 | Flyback diode (1N400x) | _[qty]_ | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Magnet coil |
| 009 | Electromagnet coil | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Piece actuation |
| 010 | USB microphone | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Peripherals |
| 011 | Display screen | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Peripherals |
| 012 | Belt & pulley set | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY |
| 013 | CoreXY frame / rails | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | CoreXY |
| 014 | Chessboard frame / acrylic board surface | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Structural; top surface is acrylic |
| 015 | Chess piece set (magnetic base) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Structural |
| 016 | DFRobot UPS HAT | 1 | DFRobot | _[order #]_ | _[location]_ | _[date]_ | New | Power Unit |
| 017 | Battery pack (4×18650) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Power Unit |
| 018 | MT3608 booster (Booster 1) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Power rail step-up |
| 019 | MT3608 booster (Booster 2) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Power rail step-up |
| 020 | Raspberry Pi wall charger (SC0510) | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Primary input power |
| 021 | UPS/Pi plastic mount | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Structural mount |
| 022 | MicroSD card | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | Processing Unit |
| 023 | Logic level converter | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | UART debug |
| 024 | UART debug cable | 1 | _[vendor]_ | _[order #]_ | _[location]_ | _[date]_ | New | UART debug |
| 025 | SMT heatsinks (Adafruit 1493) | 2 | Adafruit | _[order #]_ | _[location]_ | _[date]_ | New | TMC2209 thermal |
| 026 | Stopwatch / phone timer | 1 | Team-owned | — | — | — | — | Shared |
| 027 | Oscilloscope (≥ 20 MHz) | 1 | Lab equipment | — | Lab | — | — | Shared lab equipment |
| 028 | Multimeter (calibrated) | 1 | Lab equipment | — | Lab | — | — | Shared lab equipment |
| 029 | IR thermometer | 1 | Lab equipment | — | Lab | — | — | Shared lab equipment |
| 030 | Thermometer (ambient) | 1 | Lab equipment | — | Lab | — | — | Shared lab equipment |
| ... | _[add rows for prototyping materials, wire, connectors, mounts, etc.]_ | | | | | | | |

### 14.2 Usage Log

| Date | Item # | Experiment | Action | Notes |
|------|--------|------------|--------|-------|
| _[date]_ | 001, 002, 003, 004, 005, 006, 007, 008, 009, 012, 013 | Exp 1 (Move Completion) | Used | Full CoreXY + electromagnet path |
| _[date]_ | 001, 002, 013 | Exp 2 (Boot Noise) | Used | — |
| _[date]_ | 002, 003, 004, 005, 006, 013 | Exp 3 (Edge Boundary) | Used | — |
| _[date]_ | 002, 007, 008, 009, 027 | Exp 4 (EM Switching Latency) | Used | — |
| _[date]_ | 007, 008, 009, 027, 030 | Exp 5 (Flyback Spike) | Used | — |
| _[date]_ | 001, 002, 023, 024, 027 | Exp 6 (Command Latency) | Used | — |
| _[date]_ | 001, 010 | Exp 7 (Voice Recognition) | Used | 4 of 5 speakers scored |
| _[date]_ | 001, 010, 011 | Exp 8 (Processing Latency) | Used | — |
| _[date]_ | 001, 010, 011 | Exp 9 (Move Validation) | Used | — |

### 14.3 Final Inventory Check (End of Semester)

- [ ] All items accounted for (returned, stored, or documented)
- [ ] Lab station clean and organized
- [ ] No missing items
- [ ] Inventory table fully updated

| Item # | Description | Final Status | Verified By | Date |
|--------|-------------|--------------|-------------|------|
| 001 | Raspberry Pi 5 | _[status]_ | _[name]_ | _[date]_ |
| 002 | Arduino Nano | _[status]_ | _[name]_ | _[date]_ |
| ... | ... | | | |

> ⚠️ **Reminder:** Missing items or incomplete documentation will result in **automatic failure of the Experimental Analysis report**.

---

## 15. Statement of Contributions

> Each team member must write their own contribution statement. One member may NOT write on behalf of another. By submitting this report, the team collectively certifies the accuracy of all statements below.

### Allison Givens
- **Experiment Design:** Contributed to the design of the command latency experiment (Experiment 6). Also contributed to the voice recognition accuracy experiment (Experiment 7).
- **Experiment Execution:** Participated in running Experiment 6 and Experiment 7.
- **Data Analysis:** _[describe your specific contributions]_
- **Report Writing:** _[describe your specific contributions]_
- **Signature / Initials:** _____   **Date:** _______

### Noah Beaty
- **Experiment Design:** Co-designed Experiments 1 (Move Completion Time) and 2 (Boot Noise). Co-designed Experiment 6 (Command Latency). Solo-designed Experiments 3 (Edge Boundary), 4 (Electromagnet Switching Latency), and 5 (Flyback Diode Inductive Spike). Also contributed to the voice recognition accuracy experiment (Experiment 7).
- **Experiment Execution:** Ran Experiments 1 and 2 (with Jack). Ran Experiments 3, 4, and 5 solo. Co-executed Experiment 6 (with Jack and Allison). Participated in Experiment 7.
- **Data Analysis:** _[describe your specific contributions]_
- **Report Writing:** _[describe your specific contributions]_
- **Signature / Initials:** _____   **Date:** _______

### Jack Tolleson
- **Experiment Design:** Co-designed Experiments 1 (Move Completion Time) and 2 (Boot Noise). Co-designed Experiment 6 (Command Latency). Solo-designed Experiments 8 (Processing Latency) and 9 (Move Validation Correctness). Also contributed to the voice recognition accuracy experiment (Experiment 7). Leading the planned UART Communication Reliability test (§12.1) and co-leading the planned Thermal Safety test (§12.2).
- **Experiment Execution:** Co-executed Experiments 1 and 2 (with Noah). Co-executed Experiment 6 (with Noah and Allison). Ran Experiments 8 and 9 solo. Participated in Experiment 7. Will run the UART Communication Reliability test and will co-run the Thermal Safety test with Nathan.
- **Data Analysis:** _[describe your specific contributions]_
- **Report Writing:** _[describe your specific contributions]_
- **Signature / Initials:** _____   **Date:** _______

### Lewis Bates
- **Experiment Design:** Contributed to the voice recognition accuracy experiment (Experiment 7).
- **Experiment Execution:** Participated in Experiment 7.
- **Data Analysis:** _[describe your specific contributions]_
- **Report Writing:** _[describe your specific contributions]_
- **Signature / Initials:** _____   **Date:** _______

### Nathan MacPherson
- **Experiment Design:** Contributed to the voice recognition accuracy experiment (Experiment 7). Co-leading the planned Thermal Safety test (§12.2) with Jack.
- **Experiment Execution:** Participated in Experiment 7. Will co-run the Thermal Safety test with Jack.
- **Data Analysis:** _[describe your specific contributions]_
- **Report Writing:** _[describe your specific contributions]_
- **Signature / Initials:** _____   **Date:** _______

---

## Appendices (Optional)

### Appendix A: Raw Data Files
_[Links to CSVs, spreadsheets, or video recordings in the repo.]_

### Appendix B: Calibration Records
_[Instrument calibration data, datasheets.]_

### Appendix C: Additional Figures
_[Supplementary charts, schematics, photos — including any images from the repository.]_
