
### Power Tree Diagram


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

