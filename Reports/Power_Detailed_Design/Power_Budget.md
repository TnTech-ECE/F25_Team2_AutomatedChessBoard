
### Power Budget for the Automated Chessboard System

The table format mirrors the example: Voltage Rail, Powered Components, Estimated Current (A), Power (W), Regulator Type, Efficiency. I added columns for Average vs. Peak to meet your request. Totals account for regulator efficiencies (input power = output power/efficiency).

#### Input Source (Raspberry Pi Wall Charger)
| Source | Voltage Rail | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------|--------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| Raspberry Pi Wall Charger (SC0510) | 5V Input to UPS | 4.47 | 22.35 | 9.22 (capped by 5A/25W) | 46.1 (capped by 27W spec) | N/A (AC-DC Adapter) | N/A (source) |

- **Notes on Input Source**: Provides 5V/5A (27W max) via USB-C to the UPS HAT. When plugged in, it powers the system directly with a pass-through and charges batteries. Peak exceeds 27W theoretical but is unrealistic for sustained operation; UPS batteries buffer short peaks. The efficiency of the charger itself is ~85-90% from the AC wall (not included here, as the budget starts at DC output).

#### 5V Rail (Logic and Peripherals; Supplied by UPS HAT from Charger or Batteries)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 5V | Raspberry Pi 5 (Processing Unit) | 1.0 | 5.0 | 2.4 | 12.0 | Buck/Boost (UPS internal) | 90% |
| 5V | Arduino Nano (Control Unit) | 0.02 | 0.1 | 0.05 | 0.25 | Buck/Boost (UPS internal) | 90% |
| 5V | Hosyond 3.5" TFT LCD Display (Peripherals) | 0.13 | 0.65 | 0.13 | 0.65 | Buck/Boost (UPS internal) | 90% |
| 5V | Movo MA5U Microphone (Peripherals) | 0.05 | 0.25 | 0.1 | 0.5 | Buck/Boost (UPS internal) | 90% |
| 5V | Electromagnet (CoreXY) | 0.1 | 0.5 | 0.4 | 2.0 | Buck/Boost (UPS internal) | 90% |
| 5V | TMC2209 Drivers Logic (x2; Control Unit) | 0.02 | 0.1 | 0.04 | 0.2 | Buck/Boost (UPS internal) | 90% |
| 5V | UPS HAT Overhead (Power Unit) | 0.1 | 0.5 | 0.1 | 0.5 | N/A (internal) | N/A |
| 5V | Buck Converter Input (to 3.3V for Logic/Level Shifter) | 0.05 | 0.25 | 0.1 | 0.5 | Buck/Boost (UPS internal) | 90% |
| **5V Subtotal (Direct Output, excl. MT3608 Input)** | - | **1.47** | **7.35** | **3.36** | **16.6** | - | - |

- **Notes on 5V Rail**: Output from DFRobot UPS HAT. Total input to 5V rail (from charger/batteries, accounting for 90% eff): Avg ~8.17W (7.35 / 0.9), Peak ~18.44W. Add MT3608 input below for full rail load.

#### 12V Rail (Motors; Stepped Up from 5V via MT3608)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 12V | Stepper Motor 1 (CoreXY; NEMA17) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| 12V | Stepper Motor 2 (CoreXY; NEMA17) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| **12V Subtotal (Direct Output)** | - | **1.0** | **12.0** | **2.0** | **24.0** | - | - |

- **Notes on 12V Rail**: Input from 5V rail to MT3608: Avg 2.5A / 12.5W (12.0 / 0.95), Peak 5.1A / 25.5W (24.0 / 0.95). This adds to the 5V rail load.

#### 3.3V Sub-Rail (Logic; Stepped Down from 5V via Buck Converter)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 3.3V | Level Shifter LV Side (CU Logic) | 0.045 | 0.15 | 0.09 | 0.3 | Buck (Adafruit 2745) | 90% |
| **3.3V Subtotal (Direct Output)** | - | **0.045** | **0.15** | **0.09** | **0.3** | - | - |

- **Notes on 3.3V Sub-Rail**: Input from 5V rail to buck converter: Avg 0.05A / 0.25W (0.15 / 0.9), Peak 0.1A / 0.5W (0.3 / 0.9). This adds to the 5V rail load.

#### System Totals (Accounting for All Efficiencies and Input)
- **Total Average Power (Output Across Rails)**: 7.35W (5V direct) + 12.0W (12V) + 0.15W (3.3V) = **19.5W**.
- **Total Peak Power (Output Across Rails)**: 16.6W (5V direct) + 24.0W (12V) + 0.3W (3.3V) = **40.9W**.
- **Total Input Power at Wall Charger (Including UPS Eff ~90%)**: Avg **22.35W** [(7.35W + 12.5W to MT3608 + 0.25W to buck) / 0.9], Peak **46.1W** [(16.6W + 25.5W + 0.5W) / 0.9], capped by charger/battery limits.
- **Additional Notes**: Sleep mode reduces to <0.5W idle. Battery runtime >6 hours at avg load (146Wh / 22.35W ≈ 6.55 hours; actual may be lower if capacity overstated—test recommended). Fuses protect branches as per the BOM.
- **Ethical/Safety**: Low-voltage (<50V) complies with UL/NFPA; recyclable batteries minimize e-waste.

