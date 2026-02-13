### Power Budget for the Automated Chessboard System

The table format mirrors the example: Voltage Rail, Powered Components, Estimated Current (A), Power (W), Regulator Type, Efficiency. I added columns for Average vs. Peak to meet your request. Totals account for regulator efficiencies (input power = output power/efficiency).

#### Input Source (Raspberry Pi Wall Charger)

| Source | Voltage Rail | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------|--------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| Raspberry Pi Wall Charger (SC0510) | 5V Input to UPS | 3.04 | 15.2 | 4.89 | 24.4 | N/A (AC-DC Adapter) | N/A (source) |

- **Notes on Input Source**: Provides 5V/5A (27W max) via USB-C to the UPS HAT. When plugged in, it powers the system directly with a pass-through and charges batteries. Peak is brief and supplemented by batteries. The efficiency of the charger itself is ~85-90% from the AC wall (not included here, as the budget starts at DC output).

#### 5V Rail (Logic and Peripherals; Supplied by UPS HAT from Charger or Batteries)

| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 5V | Raspberry Pi 5 (Processing Unit) | 1.0 | 5.0 | 1.0 | 5.0 (reduced during moves) | Buck/Boost (UPS internal) | 90% |
| 5V | Arduino Nano (Control Unit) | 0.02 | 0.1 | 0.05 | 0.25 | Buck/Boost (UPS internal) | 90% |
| 5V | Hosyond 3.5" TFT LCD Display (Peripherals) | 0.13 | 0.65 | 0.13 | 0.65 | Buck/Boost (UPS internal) | 90% |
| 5V | Movo MA5U Microphone (Peripherals) | 0.05 | 0.25 | 0.05 | 0.25 (reduced during moves) | Buck/Boost (UPS internal) | 90% |
| 5V | Electromagnet (CoreXY) | 0.1 | 0.5 | 0.4 | 2.0 | Buck/Boost (UPS internal) | 90% |
| 5V | TMC2209 Drivers Logic (x2; Control Unit) | 0.02 | 0.1 | 0.04 | 0.2 | Buck/Boost (UPS internal) | 90% |
| 5V | UPS HAT Overhead (Power Unit) | 0.1 | 0.5 | 0.1 | 0.5 | N/A (internal) | N/A |
| 5V | Buck Converter Input (to 3.3V for Logic/Level Shifter) | 0.05 | 0.25 | 0.1 | 0.5 | Buck/Boost (UPS internal) | 90% |
| **5V Subtotal (Direct Output, excl. MT3608 Input)** | - | **1.47** | **7.35** | **1.87** | **9.35** | - | - |

- **Notes on 5V Rail**: Output from DFRobot UPS HAT. Total input to 5V rail (from charger/batteries, accounting for 90% eff): Avg ~8.17W (7.35 / 0.9), Peak ~10.39W. Add MT3608 input below for full rail load.

#### 12V Rail (Motors; Stepped Up from 5V via MT3608)

| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 12V | Stepper Motor 1 (CoreXY; NEMA17) | 0.25 | 3.0 | 0.5 | 6.0 | Step-Up (MT3608) | 95% |
| 12V | Stepper Motor 2 (CoreXY; NEMA17) | 0.25 | 3.0 | 0.5 | 6.0 | Step-Up (MT3608) | 95% |
| **12V Subtotal (Direct Output)** | - | **0.5** | **6.0** | **1.0** | **12.0** | - | - |

- **Notes on 12V Rail**: Input from 5V rail to MT3608: Avg 1.26A / 6.3W (6.0 / 0.95), Peak 2.53A / 12.65W (12.0 / 0.95). This adds to the 5V rail load.

#### 3.3V Sub-Rail (Logic; Stepped Down from 5V via Buck Converter)

| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 3.3V | Level Shifter LV Side (CU Logic) | 0.045 | 0.15 | 0.09 | 0.3 | Buck (Adafruit 2745) | 90% |
| **3.3V Subtotal (Direct Output)** | - | **0.045** | **0.15** | **0.09** | **0.3** | - | - |

- **Notes on 3.3V Sub-Rail**: Input from 5V rail to buck converter: Avg 0.05A / 0.25W (0.15 / 0.9), Peak 0.1A / 0.5W (0.3 / 0.9). This adds to the 5V rail load.

#### System Totals (Accounting for All Efficiencies and Input)

- **Total Average Power (Output Across Rails)**: 7.35W (5V direct) + 6.0W (12V) + 0.15W (3.3V) = **13.5W**.  
- **Total Peak Power (Output Across Rails)**: 9.35W (5V direct) + 12.0W (12V) + 0.3W (3.3V) = **21.65W**.  
- **Total Input Power at Wall Charger (Including UPS Eff ~90%)**: Avg **15.2W** [(7.35W + 6.3W to MT3608 + 0.25W to buck) / 0.9], Peak **24.4W** [(9.35W + 12.65W + 0.5W) / 0.9], within adapter limits with battery surge support.  
- **Additional Notes**: Sleep mode reduces to <0.5W idle. Battery runtime >2 hours at avg load (52Wh / 15.2W ≈ 3.4 hours; actual may be lower—test recommended). Fuses protect branches as per the BOM. Peaks are non-simultaneous (e.g., RPi high load during AI, not moves).  
- **Ethical/Safety**: Low-voltage (<50V) complies with UL/NFPA; recyclable batteries minimize e-waste.
