# CoreXY Detailed Design

This document presents a comprehensive overview of the CoreXY subsystem, one of the five primary components of the automated chessboard system; the other subsystems including the Processing Unit (PU), Control Unit (CU), Power Unit, and Peripherals Unit. While the primary focus is on the CoreXY, this document also provides a high-level integration perspective with the remaining subsystems, in order to illustrate the CoreXY’s role in  physically implementing piece movement within the entire system. Additionally, the document outlines the key technical constraints, relevant electrical and safety standards, and operational requirements that guide the subsystem’s design and implementation. Finally, it describes the proposed mechanical architecture, magnetic actuation method, flux calculations, and motion transmission calculations necessary to construct and validate the CoreXY as a critical part of the complete automated chessboard solution.

## Function of the Subsystem

The CoreXY subsystem serves as the mechanical motion platform responsible for executing physical piece movement across the chessboard. Operating under command signals received from the Control Unit, the CoreXY translates high-level motion instructions into precise two-dimensional movement along the X and Y axes. The system utilizes a belt-driven CoreXY configuration, where two stepper motors generate coordinated linear motion of a magnetic actuator mounted beneath the playing surface. [4]

This actuator, a controllable electromagnet, engages only when positioned beneath a piece designated for movement, allowing it to securely “grip” and transport the chess piece to its target location before deactivating to release it [15]. The design ensures smooth, synchronized motion while maintaining positional accuracy across the entire board area. Through this integration of mechanical precision and controlled magnetic actuation, the CoreXY subsystem enables consistent, reliable, and efficient movement of all chess pieces as part of the automated gameplay sequence.

## Specifications and Constraints

The CoreXY subsystem shall provide precise two-axis movement of the magnetic carriage for chess piece manipulation. It shall translate coordinated stepper motor signals from the Control Unit into smooth, accurate motion using a belt-driven CoreXY configuration. The subsystem shall maintain proper mechanical tension and alignment to ensure repeatable positioning and stable performance across the full range of motion. The CoreXY shall also support the electromagnet assembly used for chess piece pickup and release, while ensuring reliable operation within defined voltage and load constraints. The subsystem shall be designed and calibrated to maintain positional accuracy and responsiveness required for consistent, collision-free gameplay.

### Performance Specifications

The CoreXY subsystem shall achieve positional accuracy within ±0.5 mm of target coordinates, maintaining alignment with the CU accuracy specification. The subsystem shall complete all commanded movements within 5 seconds to ensure responsive gameplay and smooth motion transitions, also in alignment with the CU movement speed specification. Proper belt tensioning shall be maintained to minimize backlash and vibration, ensuring smooth and repeatable motion [7]. All motion parameters—including steps per millimeter, acceleration, and velocity profiles—shall be calculated and verified through calibration procedures to achieve precise kinematic performance [3]. The subsystem shall employ an electromagnet operating at 5 V DC with magnetic strength sufficient to reliably pick up the designated chess piece without attracting or disturbing adjacent pieces [8]. The stepper motors driving the CoreXY mechanism shall operate from a 12 V DC motor supply, consistent with driver voltage tolerances. Belt tension, magnet strength, and motion calibration shall collectively ensure smooth, accurate, and reliable piece movement across all gameplay operations.

### Regulatory and Compliance Constraints

The subsystem shall comply with FFC Part 15 Subpart B (Class B) limits for electromagnetic interference in residential environments keeping emissions under 0.15–30 MHz at 66–56 dBµV, decreasing with frequency, and radiated emissions of up to 30–1000 MHz at 40–54 dBµV/m measured at 3 meters [1]. All operations shall remain under 50 V DC in accordance with UL low-voltage safety thresholds in order to eliminate the need for high-voltage insulation [2]. All circuitry  shall comply with wiring methods specified in Article 725 for Class 1, 2, and 3 circuits, including protection against overcurrent, proper conductor sizing, and properly rated insulation [13]. All materials and configurations shall comply with CPSC safety guidance for consumer electronics, ensuring components are  not hazardous and follow CPSC's best-practice manufacturing guidance and material-change-testing requirements [9].

### Electrical and Safety Constraints

All external surfaces shall operate under temperatures ≤104°F, in accordance with UL 94 flammability requirements for plastic materials and the CPSC maximum surface temperature guidelines (16 CFR 1505.7) [5] [10]. All cord sets, flexible cables, and connectors shall comply with NEC Article 400, using conductors and insulation rated for system voltage and current, with secure routing that avoids sharp edges, pinch points, or mechanical stress [14]. All circuitry shall include grounding, bonding, and electrical protection measures in accordance with OSHA 29 CFR 1910 Subpart S, ensuring all exposed conductive parts are properly grounded and circuit protection devices are installed where required [12]. All user-facing hazards shall have safety labels in compliance with ANSI Z535.4, ensuring labels are legible, durable, and placed conspicuously to effectively warn users of potential risks. [11].

### Ethical and Socio-economic Considerations

The subsystem shall be designed and operated with user safety and reliability as the highest priority, ensuring that all motion components, power systems, and magnetic assemblies function predictably and do not pose mechanical, electrical, or operational hazards during use or maintenance [6]. The subsystem shall consider cost efficiency and accessibility, utilizing affordable and widely available components so that the overall system remains attainable for educational and research applications without compromising performance or durability.

## Overview of Proposed Solution

## Interface with Other Subsystem

The CoreXY subsystem interacts directly with the CU, which provides motion commands for precise X–Y positioning, and with the Power subsystem, which supplies current to the electromagnet through a MOSFET. It also interacts indirectly with the Peripherals subsystem, where its mechanical movement enables piece pickup and placement.

### Control Unit Interface
The CoreXY receives motion commands from the CU and translates them into physical movement. The CU controls the NEMA17 stepper motors through TMC2209 stepper driver modules, which generate STEP and DIR signals to precisely position the CoreXY actuator. In addition to motion control, the CU manages the electromagnet by sending a control signal to the gate pin of an N-channel MOSFET, which switches current through the electromagnet.

### Power Interface
The CoreXY subsystem interfaces with the Power subsystem by controlling current to the electromagnet through a GaN FET. The source pin of the GaN FET is connected to the common system ground, which is shared with the power supply. The drain pin is connected to the negative terminal of the electromagnet as well as to the anode of a flyback diode. The positive terminal of the electromagnet and the cathode of the diode are connected to the positive voltage of the power supply. When the FET is on, it completes the circuit, allowing current to flow through the electromagnet and energize it. When the FET is off, the diode provides a safe path for the inductive spike from the coil, protecting both the FET and the rest of the system.

### Peripherals Interface
The CoreXY does not directly exchange signals with the Peripherals subsystem. However, the subsystems interact mechanically through piece movement. The pieces must be designed considering the size, flux, and holding force of the electromagnet to ensure reliable pickup and release operations.

## 3D Model of Custom Mechanical Components

## Buildable Schematic

## Bill of Materials
| Manufacturer | Part Number | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----|-----|-----|-----|-----|-----|-----|
| Seeed Studio | 101020073 | Mouser Electronics | 713-101020073 | 1 | $9.35 | [Link](https://www.mouser.com/ProductDetail/Seeed-Studio/101020073?qs=1%252B9yuXKSi8A5kCccI2u34g%3D%3D&srsltid=) |
| CW-Motor | 42BYGH404 | Circuit Specialists | 42BYGH404 | 2 | $8.70 | [Link](https://www.circuitspecialists.com/nema_17_stepper_motor_42bygh404) |
| HICTOP | NA | Amazon | NA | 1 | $9 | [Link](https://www.amazon.com/HICTOP-Printer-Creality-Printers-16-5ft/dp/B00YMM6IQW/ref=sr_1_1_sspa) |
| McMaster-Carr | 3684N12 | McMaster-Carr | 3684N12 | 2 | $4.99 | [Link](https://www.mcmaster.com/3684N12/) |
| 3Dman | NA | Amazon | NA | 1 pk (10 pcs) | $11.99 | [Link](https://www.amazon.com/3Dman-Toothless-Aluminum-Timing-Printer/dp/B07RV2T54M/ref=sr_1_3) |
| CNCMANs | NA | Amazon | NA | 1 | $15.02 | [Link](https://www.amazon.com/CNCMANS-Miniature-Bearing-Printing-MGN12H-250mm/dp/B0BNQ63X3H/ref=sr_1_1) |
| Unlorspy | NA | Amazon | NA | 1 | $4.49 | [Link](https://www.amazon.com/Unlorspy-Bracket-Brackets-Shelves-Furniture/dp/B0B24ZMT9J/ref=sr_1_3) |
| SIMAX3D | NA | Amazon | NA | 1 pk (13 pcs) | $9.99 | [Link](https://www.amazon.com/SIMAX3D-Printer-Creality-Artillery-Sidewinder/dp/B08B4JDB67/ref=sr_1_1_sspa) |
| IXGNIJ | NA | Amazon | NA | 1 pk (4 pcs) | $14.99 | [Link](https://www.amazon.com/Aluminum-Extrusion-European-Standard-Anodized/dp/B08Y8L11ZP/ref=sr_1_3) |
| **Total** |   |   |   |   | $98.69 |   |

## Analysis

## References

[1] American National Standards Institute, ANSI Z535.4: Product Safety Signs and Labels, 2011 ed., Washington, DC: ANSI, 2011.

[2] T. Banas, “How To Calculate The Force Of An Electromagnet,” Sciencing, Mar. 13, 2018. https://www.sciencing.com/calculate-force-electromagnet-5969962/

[3] “Calibrating core XY printers for dimensional accuracy,” Printables.com, 2024. https://www.printables.com/model/556196-calibrating-core-xy-printers-for-dimensional-accur
 (accessed Nov. 10, 2025).

[4] “CoreXY | Cartesian Motion Platform,” corexy.com. https://corexy.com/theory.html‌

[5] https://www.facebook.com/3DDistributed
, “Belt Frequency And Tensioning - 3D Distributed,” 3D Distributed, Nov. 05, 2020. https://3ddistributed.com/belt-frequency-and-tensioning/

[6] P. Scantlebury and P. Eng, “Engineering Safety into the Design Engineering safety into the design.” Available: https://www.cheminst.ca/wp-content/uploads/2019/04/Engineering20safety20into20the20design20-20Peter20Scantlebury-1.pdf

[7] Underwriters Laboratories, UL 94: Standard for Safety of Flammability of Plastic Materials for Parts in Devices and Appliances, 5th ed., Northbrook, IL: UL, 2024.

[8] U.S. company UL Solutions, “Protection from Electrical Hazards,” Nov. 2024. [Online]. Available: https://www.ul.com/resources/protection-electrical-hazards
. [Accessed: Oct. 28, 2025].

[9] U.S. Consumer Product Safety Commission, “Manufacturing Best Practices,” Business Education, Manufacturing, [Online]. Available: https://www.cpsc.gov/business--manufacturing/business-education/business-guidance/BestPractices
. [Accessed: Oct. 28, 2025].

[10] U.S. Consumer Product Safety Commission, “Maximum acceptable surface temperatures,” Code of Federal Regulations, Title 16, Part 1505.7. [Online]. Available: https://www.law.cornell.edu/cfr/text/16/1505.7
. [Accessed: Oct. 28, 2025].

[11] U.S. Federal Communications Commission, “47 CFR Part 15, Subpart B: Unintentional Radiators,” Electronic Code of Federal Regulations, Title 47, Chapter I, Subchapter A, Part 15, Subpart B. [Online]. Available: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-B
. Accessed: Oct. 27, 2025.

[12] U.S. Occupational Safety and Health Administration, OSHA Standards – Subpart S: Electrical, 29 CFR 1910, Washington, D.C.: OSHA, 2025.

[13] National Fire Protection Association, NFPA 70, National Electrical Code®, 2017 ed. Quincy, MA: NFPA, 2016.

[14] National Fire Protection Association, NFPA 70, National Electrical Code®, 2023 ed., Quincy, MA: NFPA, 2022.

[15] “12-24V Mini Electromagnet,” Skycraft Surplus, LLC, 2025. https://skycraftsurplus.com/products/12-24v-mini-electromagnet.html
 (accessed Nov. 09, 2025).
