### Power Budget for the Automated Chessboard System

The table format mirrors the example: Voltage Rail, Powered Components, Estimated Current (A), Power (W), Regulator Type, Efficiency. I added columns for Average vs. Peak to meet your request. Totals account for regulator efficiencies (input power = output power / efficiency).


#### Input Source (Raspberry Pi Wall Charger)
| Source | Voltage Rail | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------|--------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| Raspberry Pi Wall Charger (SC0510) | 5V Input to UPS | 4.42 | 22.1 | 9.18 (capped by 5A/25W) | 45.9 (capped by 27W spec) | N/A (AC-DC Adapter) | N/A (source) |

- **Notes on Input Source**: Provides 5V/5A (27W max) via USB-C to the UPS HAT. When plugged in, it powers the system directly with pass-through and charges batteries. Peak exceeds 27W theoretical but is unrealistic for sustained operation; UPS batteries buffer short peaks. Efficiency of charger itself is ~85-90% from AC wall (not included here, as budget starts at DC output).

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
| **5V Subtotal (Direct Output, excl. MT3608 Input)** | - | **1.42** | **7.1** | **3.26** | **16.1** | - | - |

- **Notes on 5V Rail**: Output from DFRobot UPS HAT. Total input to 5V rail (from charger/batteries, accounting for 90% eff): Avg ~7.9W (7.1 / 0.9), Peak ~17.9W. Add MT3608 input below for full rail load.

#### 12V Rail (Motors; Stepped Up from 5V via MT3608)
| Voltage Rail | Powered Components | Estimated Current Avg (A) | Power Avg (W) | Estimated Current Peak (A) | Power Peak (W) | Regulator Type | Efficiency (Avg) |
|--------------|--------------------|---------------------------|---------------|-----------------------------|----------------|----------------|------------------|
| 12V | Stepper Motor 1 (CoreXY; NEMA17) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| 12V | Stepper Motor 2 (CoreXY; NEMA17) | 0.5 | 6.0 | 1.0 | 12.0 | Step-Up (MT3608) | 95% |
| **12V Subtotal (Direct Output)** | - | **1.0** | **12.0** | **2.0** | **24.0** | - | - |

- **Notes on 12V Rail**: Input from 5V rail to MT3608: Avg 2.5A / 12.5W (12.0 / 0.95), Peak 5.1A / 25.5W (24.0 / 0.95). This adds to the 5V rail load.

#### System Totals (Accounting for All Efficiencies and Input)
- **Total Average Power (Output Across Rails)**: 7.1W (5V direct) + 12.0W (12V) = **19.1W**.
- **Total Peak Power (Output Across Rails)**: 16.1W (5V direct) + 24.0W (12V) = **40.1W**.
- **Total Input Power at Wall Charger (Including UPS Eff ~90%)**: Avg **22.1W** [(7.1W + 12.5W to MT3608) / 0.9], Peak **45.9W** [(16.1W + 25.5W) / 0.9], capped by charger/battery limits.
- **Additional Notes**: Sleep mode reduces to <0.5W idle. Battery runtime >2 hours at avg load (48Wh / 22.1W ≈ 2.2 hours). Fuses protect branches as per BOM.

### Power Tree Diagram (Textual Representation)

Based on the example image (a hierarchical tree with regulators, efficiencies, currents, and loads), I've generated a similar textual/ASCII representation. It starts from the Raspberry Pi Wall Charger and branches down to the motors, incorporating values from the updated budget. This mirrors the example's structure with summaries, losses/efficiencies, and end loads.

```
Power Tree for Automated Chessboard System
 (Values include Avg/Peak Power where applicable)

Raspberry Pi Wall Charger (SC0510)
  5V / 5A Max
  Avg Input Power: ~22.1W (system total incl. eff losses)
  Peak Input Power: ~45.9W
  |
  v
DFRobot UPS HAT (FIT0992)
  Eff: 90% Avg
  Handles Charging of 4x 18650 Batteries (~48Wh)
  Output: 5V Rail
  |
  v
5V Rail
  Avg: 1.42A / 7.1W (direct loads) + 2.5A / 12.5W (to MT3608) = 3.92A / 19.6W
  Peak: 3.26A / 16.1W + 5.1A / 25.5W = 8.36A / 41.6W
  Branches:
    |-- Raspberry Pi 5: Avg 1.0A / 5W, Peak 2.4A / 12W
    |-- Arduino Nano: Avg 0.02A / 0.1W, Peak 0.05A / 0.25W
    |-- TFT LCD Display: 0.13A / 0.65W
    |-- Microphone: Avg 0.05A / 0.25W, Peak 0.1A / 0.5W
    |-- Electromagnet: Avg 0.1A / 0.5W, Peak 0.4A / 2W
    |-- TMC2209 Logic (x2): Avg 0.02A / 0.1W, Peak 0.04A / 0.2W
    |-- UPS Overhead: 0.1A / 0.5W
    |
    v
  MT3608 Step-Up Converter
    Eff: 95% Avg
    Input from 5V: Avg 2.5A / 12.5W, Peak 5.1A / 25.5W
    |
    v
  12V Rail
    Avg: 1.0A / 12W, Peak 2.0A / 24W
      |-- Stepper Motor 1: Avg 0.5A / 6W, Peak 1.0A / 12W
      |-- Stepper Motor 2: Avg 0.5A / 6W, Peak 1.0A / 12W
```

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
