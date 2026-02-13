# Detailed Design for Power Supply Unit

---

## Function of the Subsystem

The Power Supply Unit (PSU) acts as the central power management and distribution subsystem for the automated chessboard system, ensuring stable, regulated power to all other subsystems (Processing Unit [PU], Control Unit [CU], CoreXY Unit, and Peripherals Unit). It supports both AC wall-powered operation and portable battery mode, with uninterruptible power supply (UPS) functionality to handle seamless transitions and prevent interruptions during gameplay. The PSU regulates a primary 5V rail for logic components (e.g., Raspberry Pi 5 in PU, Arduino Nano in CU, display and microphone in Peripherals) and a 12V rail for high-power elements (e.g., stepper motors in CoreXY). It also provides a dedicated 5V connection to the input of a buck converter (for stepping down to 3.3V logic as needed in interfaces like the CU's level shifter) and a separate 5V connection directly to the HV side of the level shifter in the CU. Aligned with the conceptual design, the PSU incorporates sleep mode for energy efficiency, overcurrent protection, and battery management to achieve at least 2 hours of active gameplay runtime, while maintaining low-voltage operation for safety.

---

## Specifications and Constraints

The PSU shall deliver regulated 5V and 12V DC outputs across the system, handling a peak load of up to 21.35W (capped by hardware limits) while supporting UPS failover and sleep mode. It must use rechargeable batteries for at least 2 hours of runtime at average load, adhering to electrical safety, environmental, and ethical standards.

### Performance Specifications

- Voltage Outputs and Load Handling: The PSU shall provide a stable 5V DC rail at up to 5A (including branches for PU, CU, Peripherals, buck converter input, and HV side of CU level shifter) with ripple <5%, and a 12V DC rail at up to 1A for motors. It shall include a buck converter stepping down from 5V to 3.3V for low-voltage logic (e.g., LV side of CU level shifter), with output adjustable to 3.3V at up to 3A.

- Battery Runtime and Charging: Batteries shall support >2 hours at 13.7W average draw (based on realistic 3500mAh capacity per cell; actual tested capacity may vary), with automatic low-battery cutoff at 20% capacity. Charging via 5V/5A wall adapter shall complete in <12 hours with pass-through support (extended due to higher claimed capacity; verify with DFRobot UPS HAT charging limits).

- Sleep Mode and UPS: Sleep mode shall activate after 5 minutes of inactivity (signaled from PU), reducing idle draw to <500mW. UPS shall ensure <20ms switching latency during outages up to 10 seconds.

- Protection: All rails shall include overcurrent fuses (1.5x nominal per branch) and overvoltage protection.

### Electrical and Signal Standards Compliance

- EMI / Emissions: Comply with FCC Part 15 Subpart B (Class B) for emissions (conducted: 0.15–30 MHz at 66–56 dBµV; radiated: 30–1000 MHz at 40–54 dBµV/m at 3m) to prevent interference [1].

- Low-Voltage Operation: Operate below 50V DC per UL thresholds, avoiding high-voltage needs [2].

- Wiring and Circuits: Follow NEC/NFPA 70 Article 725 for low-voltage circuits, with 18 AWG conductors, 60°C-rated insulation, and overcurrent protection [3].

- Batteries and Charging: Meet UL 2054 for safety (temperature limits: 32–140°F charging, -4–140°F discharging; protection against overcharge/short-circuit) [4].

- Cabling and Connectors: Comply with NEC Article 400 for flexible cables, ensuring secure routing and minimum bend radii [3].

- Grounding and Protection: Adhere to OSHA 29 CFR 1910 Subpart S for shock prevention; bond exposed parts [5].

- Safety Labeling: Use ANSI Z535.4-compliant labels for hazards (e.g., battery warnings) [6].

### Environmental and Safety Constraints

Surface Temperature: External surfaces ≤104°F (40°C) during operation, per UL 94 and CPSC 16 CFR 1505.7 [7][8].  
Operating Environment: Rated for indoor use (32–104°F, 10–90% RH non-condensing), per CPSC best practices [9].

### Ethical and Socio-Economic Constraints

Use recyclable Li-ion batteries to minimize e-waste (per UNEP Global E-waste Monitor) [10]; total cost < $150 to ensure affordability for hobbyists, aligning with ACM Code of Ethics for equitable access [11].

---

## Overview of Proposed Solution

The PSU uses a DFRobot UPS HAT mounted to the Raspberry Pi 5 (PU) for 5V regulation and battery management, with four 18650 batteries (~52Wh realistic capacity) for portability. The 5V rail powers logic components directly, with dedicated branches: one 5V to the buck converter input (Adafruit 2745, adjusted to 3.3V output for LV logic in CU level shifter) and another 5V directly to the HV side of the SparkFun Logic Level Converter in the CU. A MT3608 step-up converter boosts 5V to 12V for motors. Inline fuses protect branches, and a Pi Switch enables clean shutdowns. This hybrid design meets runtime/safety specs while keeping costs low.

---

## Interface with Other Subsystems

- Inputs: 5V/5A from wall charger (USB-C to UPS HAT); inactivity signal from PU (via GPIO) for sleep mode.

- Outputs:  
  5V rail (up to 5A) to PU (Raspberry Pi 5), Peripherals (display/microphone), CU (Arduino Nano and TMC2209 logic), and CoreXY (electromagnet).  
  Dedicated 5V branch to buck converter input (Adafruit 2745; outputs 3.3V to LV side of CU level shifter via jumper wires).  
  Dedicated 5V branch directly to HV side of CU level shifter (SparkFun Bi-Directional) via jumper wires for UART communication (TX/RX at 5V).  
  12V rail (up to 1A) to CoreXY (stepper motors via TMC2209 drivers in CU).

- Data/Communication: No direct data; power-only. Sleep mode triggered by PU signal over shared GPIO.

- Physical Connections: USB-C for charger; 18650 battery sockets for batteries; jumper wires (female-to-male, 8-inch) for 5V branches to buck and level shifter; screw terminals for 12V to CU/CoreXY.

---

## 3D Model of Custom Mechanical Components

N/A (No custom mechanical components; uses off-the-shelf enclosures for batteries and converters).

---

## Buildable Schematic

```
Peak Input Power: ~23.7W
|
v
DFRobot UPS HAT (FIT0992)
Eff: 90% Avg
Handles Charging of 4x 18650 Batteries (~52Wh realistic)
Output: 5V Rail
|
v
5V Rail
Avg: 1.47A / 7.35W (direct loads) + 1.26A / 6.3W (to MT3608) = 2.73A / 13.65W
Peak: 1.87A / 9.35W + 2.53A / 12.65W = 4.4A / 22W
Branches:
|-- Raspberry Pi 5: Avg 1.0A / 5W, Peak 1.0A / 5W (reduced during moves)
|-- Arduino Nano: Avg 0.02A / 0.1W, Peak 0.05A / 0.25W
|-- TFT LCD Display: 0.13A / 0.65W
|-- Microphone: Avg 0.05A / 0.25W, Peak 0.05A / 0.25W (reduced during moves)
|-- Electromagnet: Avg 0.1A / 0.5W, Peak 0.4A / 2W
|-- TMC2209 Logic (x2): Avg 0.02A / 0.1W, Peak 0.04A / 0.2W
|-- UPS Overhead: 0.1A / 0.5W
|-- Buck Converter Input (to 3.3V for Logic/Level Shifter): Avg 0.05A / 0.25W, Peak 0.1A / 0.5W
|
v
MT3608 Step-Up Converter
Eff: 95% Avg
Input from 5V: Avg 1.26A / 6.3W, Peak 2.53A / 12.65W
|
v
12V Rail
Avg: 0.5A / 6W, Peak 1.0A / 12W
|-- Stepper Motor 1: Avg 0.25A / 3W, Peak 0.5A / 6W
|-- Stepper Motor 2: Avg 0.25A / 3W, Peak 0.5A / 6W
|
v
Buck Converter (Adafruit 2745)
Eff: 90% Avg
Input from 5V: Avg 0.05A / 0.25W, Peak 0.1A / 0.5W
Output: 3.3V Sub-Rail (for LV Logic/Level Shifter)
Avg: 0.045A / 0.15W, Peak 0.09A / 0.3W
```

---

## Printed Circuit Board Layout

N/A (Uses off-the-shelf modules; no custom PCB required).

---

## Flowchart

N/A (No software in PSU; power management is hardware-based, with sleep triggered externally from PU).

---

## BOM

| Component | Manufacturer | Part Number | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----------|--------------|-------------|-------------|--------------------------|----------|-------|------------------------|
| UPS HAT for Raspberry Pi | DFRobot | FIT0992 | DFRobot | FIT0992 | 1 | $53.00 | [Link](https://www.dfrobot.com/product-2840.html) |
| Raspberry Pi Power Supply (5V/5A USB-C) | Raspberry Pi | SC0510 | Raspberry Pi | SC0510 | 1 | $12.95 | [Link](https://www.raspberrypi.com/products/27w-power-supply/) |
| MT3608 Step-Up Converter Module | Generic | MT3608 | Amazon | B07RNBJK5F | 1 | $12.99 | [Link](https://www.amazon.com/HiLetgo-MT3608-Converter-Adjustable-Arduino/dp/B07RNBJK5F) |
| Adafruit Adjustable Buck Converter (to 3.3V) | Adafruit | 2745 | Adafruit | 2745 | 1 | $4.95 | [Link](https://www.adafruit.com/product/2745) |
| SparkFun Logic Level Converter (Bi-Directional) | SparkFun | BOB-12009 | SparkFun | BOB-12009 | 1 | $3.95 | [Link](https://www.sparkfun.com/products/12009) |
| 18650 Rechargeable Li-ion Batteries (3500mAh each) | Samsung | INR18650-35E | IMR Batteries | INR18650-35E | 4 | $26.99 | [Link](https://imrbatteries.com/products/samsung-35e-18650-3500mah-8a-battery) |
| Inline Fuse Holders with Fuses (various ratings) | Generic | - | Amazon | B07D3QKF5S | 5 | $35.99 | [Link](https://www.amazon.com/InstallerParts-Inline-Holder-Waterproof-Automotive/dp/B07D3QKF5S) |
| Pi Switch (for safe shutdown) | Pi Supply | - | PiShop.us | Pi-Supply-Switch | 1 | $4.95 | [Link](https://www.pishop.us/product/pi-supply-switch/) |
| Jumper Wires (Female-to-Male, 8-inch) | Generic | - | Amazon | B01LZF1ZSZ | 1 pack (40) | $6.98 | [Link](https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78) |
| **Total** |   |   |   |   |   | **$122.4 ** |   |

---

## Analysis

The PSU design provides stable power distribution while addressing peak load concerns through realistic component assumptions and non-simultaneous peaks. The 5V rail peak draw is calculated at 4.4A (22W), below the 5A adapter rating, by assuming the Raspberry Pi operates at reduced load (1A/5W) during motor moves (when the PU is idle/waiting) and motors/electromagnet peak briefly (<1s during acceleration/pickup). This is justified as speech/AI processing (RPi high load) occurs before/after physical moves, avoiding overlap. The MT3608 boost converter's continuous output rating at 12V is ~1A (limited by the chip's 4A switch current, duty cycle ~0.583 for 5V-to-12V, yielding max I_out ≈1.67A theoretical, but module heat limits recommend 1A continuous; with 95% eff, input at 1A out = ~2.53A peak from 5V, well within for short bursts). Boosting magnifies input current (e.g., 12W out requires ~2.53A in), but reduced motor currents (0.5A total peak at 12V, suitable for light CoreXY load in chessboard) keep total under limits. Batteries (Samsung INR18650-35E, 3500mAh realistic vs. fake 9900mAh) provide ~52Wh, yielding >2 hours runtime at 13.7W avg system draw (accounting for eff losses), meeting specs. UPS batteries supplement brief surges, as the HAT parallels adapter/battery output. This ensures safe, efficient operation compliant with standards.

---

## Updated Power_Tree.md

```
Power Tree for Automated Chessboard System
 (Values include Avg/Peak Power where applicable)

Raspberry Pi Wall Charger (SC0510)
  5V / 5A Max
  Avg Input Power: ~15.2W (system total incl. eff losses)
  Peak Input Power: ~24.4W
  |
  v
DFRobot UPS HAT (FIT0992)
  Eff: 90% Avg
  Handles Charging of 4x 18650 Batteries (~52Wh realistic)
  Output: 5V Rail
  |
  v
5V Rail
  Avg: 1.47A / 7.35W (direct loads) + 1.26A / 6.3W (to MT3608) = 2.73A / 13.65W
  Peak: 1.87A / 9.35W + 2.53A / 12.65W = 4.4A / 22W
  Branches:
    |-- Raspberry Pi 5: Avg 1.0A / 5W, Peak 1.0A / 5W (during moves)
    |-- Arduino Nano: Avg 0.02A / 0.1W, Peak 0.05A / 0.25W
    |-- TFT LCD Display: 0.13A / 0.65W
    |-- Microphone: Avg 0.05A / 0.25W, Peak 0.05A / 0.25W (during moves)
    |-- Electromagnet: Avg 0.1A / 0.5W, Peak 0.4A / 2W
    |-- TMC2209 Logic (x2): Avg 0.02A / 0.1W, Peak 0.04A / 0.2W
    |-- UPS Overhead: 0.1A / 0.5W
    |-- Buck Converter Input (to 3.3V for Logic/Level Shifter): Avg 0.05A / 0.25W, Peak 0.1A / 0.5W
    |
    v
  MT3608 Step-Up Converter
    Eff: 95% Avg
    Input from 5V: Avg 1.26A / 6.3W, Peak 2.53A / 12.65W
    |
    v
  12V Rail
    Avg: 0.5A / 6W, Peak 1.0A / 12W
      |-- Stepper Motor 1: Avg 0.25A / 3W, Peak 0.5A / 6W
      |-- Stepper Motor 2: Avg 0.25A / 3W, Peak 0.5A / 6W
  |
  v
Buck Converter (Adafruit 2745)
  Eff: 90% Avg
  Input from 5V: Avg 0.05A / 0.25W, Peak 0.1A / 0.5W
  Output: 3.3V Sub-Rail (for LV Logic/Level Shifter)
    Avg: 0.045A / 0.15W, Peak 0.09A / 0.3W
```

---

## Updated Power_Budget.md

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

---

## References

[1] U.S. Federal Communications Commission, “47 CFR Part 15, Subpart B,” 2024. https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-B  

[2] UL Solutions, “Protection from Electrical Hazards,” 2024. https://www.ul.com/resources/protection-electrical-hazards   

[3] NFPA, NFPA 70, National Electrical Code®, 2023 ed., 2022.   

[4] UL, UL 2054 Standard for Household and Commercial Batteries, 3rd ed., 2021.   

[5] OSHA, OSHA Standards – Subpart S: Electrical, 29 CFR 1910, 2025.   

[6] ANSI, ANSI Z535.4: Product Safety Signs and Labels, 2011 ed., 2011.   

[7] UL, UL 94: Standard for Safety of Flammability of Plastic Materials, 5th ed., 2024.   

[8] CPSC, “Maximum acceptable surface temperatures,” 16 CFR 1505.7, 2024. https://www.law.cornell.edu/cfr/text/16/1505.7   

[9] CPSC, “Manufacturing Best Practices,” 2024. https://www.cpsc.gov/business--manufacturing/business-education/business-guidance/BestPractices   

[10] UNEP, Global E-waste Monitor 2020, 2020. https://ewastemonitor.info/  

[11] ACM, ACM Code of Ethics and Professional Conduct, 2018. https://www.acm.org/code-of-ethics  

--- 
