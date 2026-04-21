**# Power Unit — Experimental Analysis**

---

## Experiment 1: Voltage Regulation and Ripple Test

**Purpose:**  
This experiment measures the following criteria from the Detailed Design PSU and Power Tree (Detailed_Design_PSU.md, Power_Tree.md, and Power_Budget.md):  
- The PSU shall provide a stable **5V DC rail** (up to 5 A) with ripple <5%.  
- The **12V rail** (via MT3608 step-up) shall remain stable up to 1 A for stepper motors.  
- The **3.3V sub-rail** (via Adafruit buck converter) shall remain stable.  
- All rails must stay within ±5% of nominal voltage under no-load, average-load (~15.2 W input), and peak-load (~24.4 W input) conditions as defined in the power tree and budget breakdowns.  

Stable voltage and low ripple are critical to prevent Raspberry Pi brownouts, stepper motor stalling, or electromagnet dropouts during gameplay.

**Procedure:**

1. Power the system via the Raspberry Pi wall charger (SC0510) with fully charged 4×18650 batteries installed in the DFRobot UPS HAT.  
2. Attach calibrated oscilloscope probes (or logic analyzer with voltage measurement capability) and a digital multimeter to the following test points: 5V rail (direct UPS HAT output), 12V rail (MT3608 output), and 3.3V rail (Adafruit buck converter output). Use shortest possible ground leads for accurate ripple measurement.  
3. Run the system through the four defined operating states for at least 30 seconds each while continuously monitoring and logging:  
   - State 1: Idle/sleep (RPi idle, all motors and electromagnet off).  
   - State 2: Typical chess move (stepper motors + electromagnet active).  
   - State 3: Peak simultaneous load (RPi processing + motors + electromagnet).  
   - State 4: Battery-only mode (wall power disconnected).  
4. Record steady-state DC average voltage and peak-to-peak ripple on each rail for every state.  
5. Repeat the entire sequence with wall power disconnected (pure UPS battery mode) to verify battery-side regulation.  
6. Randomize the order of operating states across trials and have different team members perform measurements.

**Data Collection:**  
Record all measurements in the spreadsheet table provided in the Experimental Analysis Excel (columns: Trial Number, Operating State, Power Source, 5V Avg (V), 5V Ripple p-p (mV), 12V Avg (V), 12V Ripple p-p (mV), 3.3V Avg (V), 3.3V Ripple p-p (mV), Min Voltage (V), Max Voltage (V), Notes). Include oscilloscope screenshots for each state showing ripple waveforms. Calculate % deviation from nominal and flag any rail outside ±5%.

**Trials:**  
N = 20 minimum (5 trials per operating state). This sample size allows statistical confirmation of stability across load conditions and power sources.

**Potential Biases:**  
Each trial will use freshly calibrated instruments; ambient temperature will be controlled (68–77°F); load states will be randomized; different team members will perform measurements. Oscilloscope probe grounding inductance can artificially inflate ripple readings (mitigate with shortest ground leads and proper probe compensation).

---

## Experiment 2: Power Consumption and Budget Verification Test

**Purpose:**  
This experiment verifies the power tree and budget calculations (Power_Budget.md) by measuring actual input power, rail power distribution, and converter efficiencies under real operating conditions. Accurate power accounting ensures the system meets runtime targets and prevents unexpected brownouts or overheating.

**Procedure:**

1. Connect a precision power meter (or calibrated multimeter in series with the SC0510 wall adapter) to measure total input voltage and current at the UPS HAT input.  
2. Simultaneously monitor output power on the 5V, 12V, and 3.3V rails using current-sense resistors or dedicated power monitors at each rail output.  
3. Execute full gameplay cycles (including idle, typical chess moves, and peak loads) while logging instantaneous and average power values.  
4. Perform dedicated peak-load trials by forcing simultaneous RPi processing, all stepper motors, and electromagnet activation.  
5. Calculate efficiencies: UPS Efficiency = (5V rail power / input power) × 100; MT3608 Efficiency = (12V rail power / 5V input to MT3608) × 100.  
6. Repeat measurements with wall power disconnected to capture battery-side consumption.

**Data Collection:**  
Record all values in the spreadsheet table provided in the Experimental Analysis Excel (columns: Trial Number, Test Mode, Input Power (W), Input Current (A), 5V Rail Power (W), 12V Rail Power (W), 3.3V Rail Power (W), UPS Efficiency (%), MT3608 Efficiency (%), Notes). Compare measured values against the budgeted figures in Power_Budget.md and flag any deviation >10%.

**Trials:**  
N = 5 minimum (3 full gameplay-cycle trials + 2 peak-load trials). This provides sufficient data to validate both average and worst-case consumption.

**Potential Biases:**  
Measurement error from meter accuracy or contact resistance (mitigate by zeroing meters before each session and using Kelvin connections where possible). Converter efficiency varies with temperature and load (mitigate by performing tests at controlled 68–77°F).

---

## Experiment 3: Battery Runtime and UPS Switching Latency Test

**Purpose:**  
This experiment measures battery runtime, UPS switchover latency, and sleep-mode power draw to confirm the DFRobot UPS HAT meets runtime and seamless failover requirements. Reliable battery backup and fast switching are essential for uninterrupted gameplay during power interruptions.

**Procedure:**

1. Fully charge the 4×18650 battery pack in the DFRobot UPS HAT.  
2. Power the complete chessboard system and begin a continuous full-gameplay loop (including moves, electromagnet actuation, and RPi processing).  
3. Use a stopwatch or automated script to measure total runtime until the system shuts down safely.  
4. For switchover latency: Connect an oscilloscope across the 5V rail and trigger on the moment wall power is physically disconnected. Measure the time from power loss to stable 5V rail restoration from battery.  
5. Perform 10 rapid wall-power disconnect/reconnect cycles while the system is in peak load.  
6. Separately measure sleep-mode power draw by placing the system in idle/sleep state with wall power connected.

**Data Collection:**  
Record all values in the spreadsheet table provided in the Experimental Analysis Excel (columns: Trial Number, Test Type, Runtime (min:sec), UPS Switch Latency (ms), Sleep Mode Power (W), Total Energy Delivered (Wh), Pass/Fail, Notes). Include oscilloscope captures of switchover events.

**Trials:**  
N = 13 minimum (1 full runtime trial + 10 UPS switch trials + 2 sleep-mode measurements). This ensures statistical confidence in latency and verifies runtime against the power budget.

**Potential Biases:**  
Battery capacity degrades with age and temperature (mitigate by using freshly charged, matched cells at controlled ambient temperature). Timing precision depends on oscilloscope trigger accuracy (use ≥1 MHz sampling).

---

## Experiment 4: Thermal Performance and Surface Temperature Test

**Purpose:**  
Verify that external surface temperature remains ≤104°F (40°C) during continuous peak-load operation. This ensures user safety and prevents component damage or enclosure deformation.

**Procedure:**

1. Place the fully assembled chessboard (including enclosure) on a flat surface in a controlled 68–77°F ambient environment.  
2. Instrument the system with calibrated digital thermometers or an IR thermal camera at the following locations: UPS HAT, MT3608 module, battery pack, and outer enclosure surface (multiple points).  
3. Run the system continuously under peak simultaneous load (RPi processing + all motors + electromagnet) for at least 30 minutes per trial.  
4. Record temperatures at 5-minute intervals.  
5. Note ambient temperature at the start and end of each trial.  
6. Flag any reading exceeding 104°F as a failure and note the hottest component.

**Data Collection:**  
Record all values in the spreadsheet table provided in the Experimental Analysis Excel (columns: Trial Number, Time (min), UPS HAT (°F), MT3608 (°F), Battery Pack (°F), Enclosure Surface (°F), Ambient (°F), Max Temp (°F), Pass/Fail, Notes). Include thermal images where possible.

**Trials:**  
N = 3. Multiple trials account for any variability in ambient conditions or component warm-up.

**Potential Biases:**  
Ambient airflow or enclosure orientation can affect readings (mitigate by testing in a draft-free area with consistent orientation). IR camera emissivity settings must be calibrated for plastic/metal surfaces (use contact thermometers for verification).

---

## Summary

These four experiments directly validate the power detailed design, power tree distribution, component breakdowns, efficiency targets, protections, and runtime/safety specifications. All raw data, oscilloscope captures, thermal images, and calculations will be compiled in the full experimental report and compared against the values in Power_Budget.md and Detailed_Design_PSU.md.

**Component Inventory Tracking**  
Use the inventory table in the Experimental Analysis Excel to log all power-related components (UPS HAT, MT3608, buck converter, batteries, etc.) with vendor, order number, storage location, date acquired, condition, and notes.

Copy the Markdown above into a new file named `Power_Unit_Tests.md` and place it in `Reports/Power_Unit_Experiments/` (following the same folder structure as the Control Unit experiments). You can then link it from your main project documentation exactly as done for the control unit. Let me know if you need any adjustments, additional experiments, or help generating the actual Excel data-entry templates!
