### Power Budget for the Automated Chessboard System

Based on the provided documents (e.g., Lewis_Detailed_Design_1.md, Noah_Detailed_Design_2.md, Detailed_Design_CoreXY.md, Detailed_Design_PU.md, and Conceptual_Design.md), I have compiled an itemized power budget. This includes all major power-consuming components across subsystems, grouped by voltage rail (as in the example image). Estimates are derived from:

- Documented specs (e.g., electromagnet at 400mA/5V from Noah's analysis; system peak load up to 20W and average 10W from Lewis's specs).
- Referenced datasheets and tool results (e.g., web searches for component power consumption).
- Assumptions for usage: 
  - **Average power**: Typical operation (e.g., idle processing with intermittent motion; motors at 50% duty cycle for chess moves; electromagnet on briefly ~25% duty during moves).
  - **Peak power**: Worst-case simultaneous load (e.g., both motors moving, electromagnet active, Pi under stress).
  - Efficiencies from regulators (e.g., MT3608 step-up at ~95% average from search results [web:40, web:42, web:43]).
  - No significant 3.3V or 1.8V external rails (internal to Pi/Arduino); focus on main 5V (logic/peripherals) and 12V (motors) rails.
  - UPS HAT overhead: Ultra-low standby (~0.5W average from ); assume 10% efficiency loss for UPS boost/charge (typical for Li-ion UPS, ~90% eff).
  - Total system: Excludes negligible items (e.g., resistors, diodes <0.01W). Battery runtime calculation aligns with >2 hours at average load (using 4x 18650 ~48Wh capacity).

The table format mirrors the example: Voltage Rail, Powered Components, Estimated Current (A), Power (W), Regulator Type, Efficiency. I added columns for Average vs. Peak to meet your request. Totals account for regulator efficiencies (input power = output power / efficiency).

#### 5V Rail (Logic and Peripherals; Supplied Directly by UPS HAT)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 5V | Raspberry Pi 5 (Processing Unit; idle ~3-5W, stress ~12W per [web:1, web:4]) | 1.0 | 5.0 | 2.4 | 12.0 | Buck (UPS internal) | 90% |
| 5V | Arduino Nano (Control Unit; ~20mA idle, up to 50mA active per [web:8, web:9]) | 0.02 | 0.1 | 0.05 | 0.25 | Buck (UPS internal) | 90% |
| 5V | Hosyond 3.5" TFT LCD Display (Peripherals; backlight ~120mA per [web:26, web:29]) | 0.13 | 0.65 | 0.13 | 0.65 | Buck (UPS internal) | 90% |
| 5V | Movo MA5U Microphone (Peripherals; typical USB mic ~50-100mA; low-power per product desc ) | 0.05 | 0.25 | 0.1 | 0.5 | Buck (UPS internal) | 90% |
| 5V | Electromagnet (CoreXY; 400mA peak per docs, duty ~25% avg) | 0.1 | 0.5 | 0.4 | 2.0 | Buck (UPS internal) | 90% |
| 5V | TMC2209 Drivers Logic (x2; Control Unit; ~10mA each avg per datasheet ) | 0.02 | 0.1 | 0.04 | 0.2 | Buck (UPS internal) | 90% |
| 5V | UPS HAT Overhead (Power Unit; ultra-low standby ~0.5W per ) | 0.1 | 0.5 | 0.1 | 0.5 | N/A (internal) | N/A |
| **5V Subtotal (Direct Output)** | - | **1.42** | **7.1** | **3.26** | **16.1** | - | - |

- **Notes on 5V Rail**: Sourced from DFRobot UPS HAT (FIT0992). Efficiency assumes ~90% for internal buck/boost from battery (3.7V nominal). Total input to 5V rail (accounting for eff): Avg ~7.9W (7.1 / 0.9), Peak ~17.9W (16.1 / 0.9). No separate 3.3V rail needed (Pi handles internally).

#### 12V Rail (Motors; Stepped Up from 5V via MT3608)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 12V | Stepper Motor 1 (CoreXY; NEMA17 42BYGH404; ~0.5A avg during motion, 50% duty; rated 1-1.7A per [web:16, web:19]) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| 12V | Stepper Motor 2 (CoreXY; same as above) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| **12V Subtotal (Direct Output)** | - | **1.0** | **12.0** | **2.0** | **24.0** | - | - |

- **Notes on 12V Rail**: Sourced from MT3608 step-up converter (from 5V UPS output). Efficiency ~95% per [web:40, web:42]. Input power from 5V: Avg ~12.6W (12.0 / 0.95), Peak ~25.3W (24.0 / 0.95). Input current to MT3608 at 5V: Avg ~2.5A (12.6W / 5V), Peak ~5.1A (25.3W / 5V). Motors via TMC2209 (RMS up to 2A total per docs [web:13, web:14]); peak assumes simultaneous full load (unlikely, but worst-case).

#### System Totals (Accounting for All Efficiencies)
- **Total Average Power (Output)**: 7.1W (5V) + 12.0W (12V) = **19.1W** (aligns with docs' ~10W average if assuming lower motor duty; adjusted for intermittent chess moves ~50% activity).
- **Total Peak Power (Output)**: 16.1W (5V) + 24.0W (12V) = **40.1W** (exceeds docs' 20W peak, but realistic worst-case; in practice, limited by UPS 5A output and fuses).
- **Total Input Power at Source (Battery/Wall, Including UPS Eff ~90%)**:
  - Average: [7.1W (5V direct) + 12.6W (12V input)] / 0.9 = **22.1W** (from battery ~3.7V nominal; supports >2hr runtime on ~48Wh 18650 pack: 48Wh / 22.1W ≈ 2.2hr).
  - Peak: [16.1W (5V direct) + 25.3W (12V input)] / 0.9 = **45.9W** (short bursts; UPS limits to 5A/25.5W at 5.1V).
- **Additional Notes**:
  - Sleep mode (docs: <500mW idle) reduces to ~1-2W total (Pi/Arduino low-power + UPS standby).
  - No other rails (e.g., no 3.3V external like example's 4G/WiFi; Pi handles internally).
  - Fuses (from BOM) protect branches: e.g., 5A for Pi, 3A for 12V drivers.
  - Ethical/Safety: Low-voltage (<50V) complies with UL/NFPA; recyclable batteries minimize e-waste.
