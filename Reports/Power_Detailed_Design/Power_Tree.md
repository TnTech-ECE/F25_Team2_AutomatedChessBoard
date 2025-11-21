
### Power Tree Diagram (Textual Representation)



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

