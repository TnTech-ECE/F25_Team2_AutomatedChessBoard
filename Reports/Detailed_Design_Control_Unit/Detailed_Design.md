# Detailed Design

## Notes (will not be included in final document)

*Buildable Diagram*:

* Create an easy-to-read, tutorial-style system diagram.

* Label all major connections, signal lines, and power paths.

* Include notes on voltage levels, communication lines/TYPES, component roles, and dimensions.

* REFERENCES!

*Operational Flowchart*:

* Show the decision-making process of the microcontroller (Arduino Nano).

* Summarize control logic and state transitions, not individual pins or low-level code steps.

* Highlight interactions with subsystems such as motors, limit switches, and electromagnet control.

*Bill of Materials (BOM)*:

* Identify backup or alternative parts where possible.

* Good U.S. Distributors (Tax-Exempt) to consider: Digi-Key, McMaster-Carr



**NOTE: REVISE THE FOLLOWING INTRO AS DOCUMENT IS FILLED OUT**

This document presents a comprehensive overview of the Control Unit (CU) subsystem, one of the four primary components of the automated chessboard system; the other subsystems including the Processing Unit, CoreXY Unit, Power Unit, and Peripherals Unit. While the primary focus is on the Control Unit, this document also provides a high-level integration perspective with the remaining subsystems, in order to illustrate the CU’s role in coordinating communication, motion, and actuation across the entire system. Additionally, the document outlines the key technical constraints, relevant electrical and safety standards, and operational requirements that guide the subsystem’s design and implementation. Finally, it describes the proposed circuitry, communication methods, and control logic necessary to construct and validate the Control Unit as a critical part of the complete automated chessboard solution.

## Function of the Subsystem

The Control Unit (CU) serves as the central command interface between the Processing Unit and the physical motion components of the automated chessboard. Acting as the intermediary between high-level logic and low-level hardware control, the CU receives validated chess move commands from the Raspberry Pi over a serial UART connection and translates them into precise motor and actuator operations. The subsystem is responsible for generating synchronized STEP and DIR signals to drive two stepper motors that operate the CoreXY mechanism, enabling coordinated movement across the chessboard’s X and Y axes.

In addition to motion control, the CU manages the piece "pickup" mechanism through an electromagnet that securely "grabs" and releases chess pieces during gameplay. To ensure safe and reliable operation, the CU continuously monitors limit switches, driver fault signals, and supply voltage, in addition to implementing safety protocols (such as immediate halting in the event of faults or out-of-range conditions). Motion profiling, including acceleration and deceleration phases, is integrated into the control logic to guarantee smooth and accurate piece movement. Through this coordinated functionality, the CU enables precise actuation of all chess moves, while both completing each move within five seconds and ensuring reliable piece capture and placement across the board.


## Specifications and Constraints

The Control Unit shall manage precise movement of the CoreXY mechanism by converting high-level commands from the Processing Unit into coordinated stepper motor signals via an Arduino Nano [2] and two TMC2209 stepper driver boards [3]. It shall also control the electromagnet assembly and monitor limit switches, driver fault pins, and supply voltage to ensure safe, predictable operation. The Control Unit shall maintain sufficient positional accuracy and responsiveness to reliably move standard chess pieces without misalignment or collision, while complying with electrical safety and communication standards.

### Performance Specifications

The Control Unit shall achieve stepper motor resolution sufficient to position the magnetic carriage within ±0.5mm of target coordinates, ensuring proper chess piece alignment on the board. This accuracy shall be maintained using microstepping features of the TMC2209 driver (up to 1/256 step precision) [3]. The subsystem shall process and execute commands from the Processing Unit with total latency under 50ms to ensure responsive gameplay and smooth motion transitions [2]. To meet gameplay requirements, the Control Unit shall complete any single piece movement within 5 seconds and achieve at least 95% successful collision-free captures across repeated operation cycles, ensuring stable and reliable play performance. TMC2209 drivers shall not exceed the rated voltage of 5V, and overtemperature or stallGuard fault conditions shall trigger a controlled stop [3]. The Arduino Nano shall operate from a 12V DC logic supply, while the motor supply shall not exceed 12V, following manufacturer voltage tolerances [2][3][5].

### Electrical and Signal Standards Compliance

The Control Unit shall comply with FCC Part 15 Subpart B regulations for unintentional radiators to prevent electromagnetic interference with nearby devices [1]. All electrical connections and enclosures shall meet the safety practices defined in UL 60950-1 (legacy IT equipment safety) and NFPA 70 (National Electrical Code) for proper grounding, wiring isolation, and overcurrent protection [5][6]. All grounding, bonding, and protective-earth connections shall comply with OSHA 29 CFR 1910 Subpart S to minimize electrical shock hazards, ensuring that all exposed conductive parts are properly bonded and protected by appropriate circuit-level fusing [9]. All flexible cables, cord sets, and connectors shall comply with NEC Article 400, using conductors and insulation rated for system voltage and current, with secure routing that avoids sharp edges, pinch points, or mechanical stress [6]. Signal-level communication between the Control Unit and Processing Unit shall occur via UART serial protocol at 9600bps, ensuring reliable and deterministic command transfer [7]. Stepper motor control signals shall operate within voltage and current ranges defined in the TMC2209 datasheet to ensure thermal stability and driver integrity [3].

### Environmental and Safety Constraints

The subsystem shall operate in ambient temperatures from 0°C to 40°C and humidity up to 70% non-condensing, suitable for indoor educational environments [2]. External surfaces shall remain below 40 °C (104 °F) during continuous operation in accordance with UL 94 flammability and CPSC thermal safety guidelines (16 CFR 1505.7) to prevent user burns or component deformation [10][11]. All wiring shall be neatly routed to avoid mechanical stress, pinch points, or accidental disconnection during operation. Insulation and cable management shall meet the minimum requirements specified in NFPA 70 [6].

### Ethical and Socio-Economic Considerations

The subsystem shall adhere to the ACM Code of Ethics [4], emphasizing accurate documentation, safe system design, and responsible development practices. Open-source hardware and software platforms (Arduino IDE and compatible libraries) shall be used to promote educational accessibility and reproducibility. To minimize cost and e-waste, components shall be sourced from domestic distributors offering tax-exempt educational sales, such as Digi-Key and McMaster-Carr, aligning with the project’s sustainability and accessibility goals [8].

## Overview of Proposed Solution

The Control Unit subsystem shall use an Arduino Nano to coordinate motion across the CoreXY mechanism (an Arduino Uno can be substituted, if the Nano cannot be ordered), generating microstepped motor signals through two TMC2209 stepper drivers (two TMC2208 stepper drivers should be able to be substituted, if the TMC2209 cannot be ordered). These drivers provide smooth, accurate positioning within ±0.5mm and support collision-free piece movement through 1/256 microstepping and controlled current regulation. The subsystem shall process UART commands from the Processing Unit at 9600bps with a total response latency under 50ms, ensuring responsive gameplay and reliable electromagnet operation for chess piece movement.

All electrical and mechanical elements shall comply with NFPA 70 (National Electrical Code), FCC Part 15 Subpart B, and UL 60950-1 for grounding, insulation, and interference protection. Wiring and enclosures shall meet NEC Article 400 and OSHA 29 CFR 1910 Subpart S for safe cable routing and protective bonding, while external surfaces shall remain below 40 °C per UL 94 and 16 CFR 1505.7 thermal safety standards. Components shall be RoHS-compliant and sourced from verified domestic distributors to support cost efficiency and sustainability. Collectively, these measures ensure the Control Unit operates precisely, safely, and reliably within the automated chess system.


## Interface with Other Subsystems

**TODO**

Provide detailed information about the inputs, outputs, and data transferred to other subsystems. Ensure specificity and thoroughness, clarifying the method of communication and the nature of the data transmitted.


## Buildable Schematic 

**TODO**

Integrate a buildable electrical schematic directly into the document. If the diagram is unreadable or improperly scaled, the supervisor will deny approval. Divide the diagram into sections if the text and components seem too small.

The schematic should be relevant to the design and provide ample details necessary for constructing the model. It must be comprehensive so that someone, with no prior knowledge of the design, can easily understand it. Each related component's value and measurement should be clearly mentioned.


## Flowchart

**TODO**

For sections including a software component, produce a chart that demonstrates the decision-making process of the microcontroller. It should provide an overview of the device's function without exhaustive detail.


## BOM

**In Progress**

| Manufacturer | Part Number | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----|-----|-----|-----|-----|-----|-----|
| Arduino | ATmega328 | Arduino | A000005 | 1 | $25.70 | [Link](https://store-usa.arduino.cc/products/arduino-nano?srsltid=AfmBOoqNFNSG0SfKF8ZFeKFBkwAtX5L50eVlOeBv6cMGf4bc8P1TCnzK) |
| Trinamic | TMC2209 | Adafruit | 6121 | 2 | $8.95 | [Link](https://www.adafruit.com/product/6121?srsltid=AfmBOoqNbFwMYs_rbP4OZemtZmfuFAdtoNUtJ39PrpSNCZA5T_JOs630) |
| **Total** |   |   |   |   | $34.65 |   |

## Analysis

**TODO**

Deliver a full and relevant analysis of the design demonstrating that it should meet the constraints and accomplish the intended function. This analysis should be comprehensive and well articulated for persuasiveness.

## References

[1] U.S. Federal Communications Commission, “47 CFR Part 15, Subpart B: Unintentional Radiators,” Electronic Code of Federal Regulations, Title 47, Chapter I, Subchapter A, Part 15, Subpart B. [Online]. Available: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-B

[2] Arduino, "Arduino Nano." Available: https://docs.arduino.cc/resources/datasheets/A000005-datasheet.pdf

[3] "POWER DRIVER FOR STEPPER MOTORS INTEGRATED CIRCUITS TMC2209 Datasheet APPLICATIONS." Available: https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2209_datasheet_rev1.09.pdf

[4] Association for Computing Machinery. (2018). ACM Code of Ethics and Professional Conduct. https://www.acm.org/code-of-ethics

[5] Underwriters Laboratories. (2019). UL 60950-1: Information Technology Equipment – Safety – Part 1: General Requirements (now superseded by UL 62368-1, but referenced for legacy applicability). https://www.shopulstandards.com

[6] National Fire Protection Association, NFPA 70, National Electrical Code®, 2023 ed., Quincy, MA: NFPA, 2022

[7] "Understanding UART," Rohde & Schwarz, 2025. https://www.rohde-schwarz.com/us/products/test-and-measurement/essentials-test-equipment/digital-oscilloscopes/understanding-uart_254524.html

[8] United Nations Environment Programme. (2020). Global E-waste Monitor 2020. https://ewastemonitor.info/

[9] U.S. Occupational Safety and Health Administration, OSHA Standards – Subpart S: Electrical, 29 CFR 1910, Washington, D.C.: OSHA, 2025

[10] Underwriters Laboratories, UL 94: Standard for Safety of Flammability of Plastic Materials for Parts in Devices and Appliances, 5th ed., Northbrook, IL: UL, 2024.

[11] U.S. Consumer Product Safety Commission, “Maximum acceptable surface temperatures,” Code of Federal Regulations, Title 16, Part 1505.7. [Online]. Available: https://www.law.cornell.edu/cfr/text/16/1505.7
