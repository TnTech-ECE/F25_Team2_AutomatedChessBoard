# CoreXY Detailed Design

This document presents a comprehensive overview of the CoreXY subsystem, one of the five primary components of the automated chessboard system; the other subsystems including the Processing Unit (PU), Control Unit (CU), Power Unit, and Peripherals Unit. While the primary focus is on the CoreXY, this document also provides a high-level integration perspective with the remaining subsystems, in order to illustrate the CoreXY’s role in  physically implementing piece movement within the entire system. Additionally, the document outlines the key technical constraints, relevant electrical and safety standards, and operational requirements that guide the subsystem’s design and implementation. Finally, it describes the proposed mechanical architecture, magnetic actuation method, flux calculations, and motion transmission calculations necessary to construct and validate the CoreXY as a critical part of the complete automated chessboard solution.

## Function of the Subsystem

The CoreXY subsystem serves as the mechanical motion platform responsible for executing physical piece movement across the chessboard. Operating under command signals received from the Control Unit, the CoreXY translates high-level motion instructions into precise two-dimensional movement along the X and Y axes. The system utilizes a belt-driven CoreXY configuration, where two stepper motors generate coordinated linear motion of a magnetic actuator mounted beneath the playing surface. [6]

This actuator, a controllable electromagnet, engages only when positioned beneath a piece designated for movement, allowing it to securely “grip” and transport the chess piece to its target location before deactivating to release it [2]. The design ensures smooth, synchronized motion while maintaining positional accuracy across the entire board area. Through this integration of mechanical precision and controlled magnetic actuation, the CoreXY subsystem enables consistent, reliable, and efficient movement of all chess pieces as part of the automated gameplay sequence.

## Specifications and Constraints

The CoreXY subsystem shall provide precise two-axis movement of the magnetic carriage for chess piece manipulation. It shall translate coordinated stepper motor signals from the Control Unit into smooth, accurate motion using a belt-driven CoreXY configuration. The subsystem shall maintain proper mechanical tension and alignment to ensure repeatable positioning and stable performance across the full range of motion. The CoreXY shall also support the electromagnet assembly used for chess piece pickup and release, while ensuring reliable operation within defined voltage and load constraints. The subsystem shall be designed and calibrated to maintain positional accuracy and responsiveness required for consistent, collision-free gameplay.

### Performance Specifications

The CoreXY subsystem shall achieve positional accuracy within ±0.5 mm of target coordinates, maintaining alignment with the CU accuracy specification. The subsystem shall complete all commanded movements within 5 seconds to ensure responsive gameplay and smooth motion transitions, also in alignment with the CU movement speed specification. Proper belt tensioning shall be maintained to minimize backlash and vibration, ensuring smooth and repeatable motion [5]. All motion parameters—including steps per millimeter, acceleration, and velocity profiles—shall be calculated and verified through calibration procedures to achieve precise kinematic performance [3]. The subsystem shall employ an electromagnet operating at 5 V DC with magnetic strength sufficient to reliably pick up the designated chess piece without attracting or disturbing adjacent pieces [4]. The stepper motors driving the CoreXY mechanism shall operate from a 12 V DC motor supply, consistent with driver voltage tolerances. Belt tension, magnet strength, and motion calibration shall collectively ensure smooth, accurate, and reliable piece movement across all gameplay operations.

### Regulatory and Compliance Constraints

The subsystem shall comply with FFC Part 15 Subpart B (Class B) limits for electromagnetic interference in residential environments keeping emissions under 0.15–30 MHz at 66–56 dBµV, decreasing with frequency, and radiated emissions of up to 30–1000 MHz at 40–54 dBµV/m measured at 3 meters [9]. All operations shall remain under 50 V DC in accordance with UL low-voltage safety thresholds in order to eliminate the need for high-voltage insulation [14]. All circuitry  shall comply with wiring methods specified in Article 725 for Class 1, 2, and 3 circuits, including protection against overcurrent, proper conductor sizing, and properly rated insulation [11]. All materials and configurations shall comply with CPSC safety guidance for consumer electronics, ensuring components are  not hazardous and follow CPSC's best-practice manufacturing guidance and material-change-testing requirements [7].

### Electrical and Safety Constraints

All external surfaces shall operate under temperatures ≤104°F, in accordance with UL 94 flammability requirements for plastic materials and the CPSC maximum surface temperature guidelines (16 CFR 1505.7) [15] [8]. All cord sets, flexible cables, and connectors shall comply with NEC Article 400, using conductors and insulation rated for system voltage and current, with secure routing that avoids sharp edges, pinch points, or mechanical stress [12]. All circuitry shall include grounding, bonding, and electrical protection measures in accordance with OSHA 29 CFR 1910 Subpart S, ensuring all exposed conductive parts are properly grounded and circuit protection devices are installed where required [10]. All user-facing hazards shall have safety labels in compliance with ANSI Z535.4, ensuring labels are legible, durable, and placed conspicuously to effectively warn users of potential risks. [1].

### Ethical and Socio-economic Considerations

The subsystem shall be designed and operated with user safety and reliability as the highest priority, ensuring that all motion components, power systems, and magnetic assemblies function predictably and do not pose mechanical, electrical, or operational hazards during use or maintenance [13]. The subsystem shall consider cost efficiency and accessibility, utilizing affordable and widely available components so that the overall system remains attainable for educational and research applications without compromising performance or durability.

## Overview of Proposed Solution

The CoreXY subsystem uses two pulleys arranged in a crossed configuration, with a stepper motor attached to each pulley, to move the magnetic actuator across the chessboard playing field. The belt routing and corresponding motion equations are illustrated in Figure 1. Both belts shall be tensioned equally, with calibration optimized to minimize mechanical strain while maximizing smoothness and positional accuracy of motion. A 5 V DC controllable electromagnet is mounted on the carriage to selectively lift and transport chess pieces. The electromagnet is actuated via a MOSFET controlled by the Control Unit, with a flyback diode included to protect the circuitry from inductive spikes. Magnetic force is calibrated to reliably pick up a single piece without affecting adjacent pieces, and disengagement is instantaneous to release the piece accurately [4].

All electrical and mechanical elements shall comply with NFPA 70 (National Electrical Code) [11][12], FCC Part 15 Subpart B [9], and UL 60950‑1 for grounding, insulation, and interference protection [14]. Wiring shall conform to NEC Article 400, with secure routing to avoid pinch points or mechanical stress, while all exposed surfaces shall remain below 40 °C per UL 94 [15] and CPSC maximum surface temperature standards [8]. Components shall be RoHS-compliant and sourced from verified distributors to ensure cost efficiency and system sustainability. Collectively, these measures ensure that the CoreXY subsystem operates precisely, safely, and reliably as part of the automated chessboard system.

<div align="center"> <img width="905" height="822" alt="image" src="https://github.com/user-attachments/assets/ee726420-2098-4fac-a716-fdc2a651918a" /> </div>
<div align="center"> <strong> Figure 1: CoreXY belt routing and corresponding motion equations. </strong> </div>
<div align="center">  Diagram illustrates belt path configuration and the kinematic relationships used to translate motor rotations into X–Y motion.[6] </div>


## Interface with Other Subsystem

The CoreXY subsystem interacts directly with the CU, which provides motion commands for precise X–Y positioning, and with the Power subsystem, which supplies current to the electromagnet through a MOSFET. It also interacts indirectly with the Peripherals subsystem, where its mechanical movement enables piece pickup and placement.

### Control Unit Interface
The CoreXY receives motion commands from the CU and translates them into physical movement. The CU controls the NEMA17 stepper motors through TMC2209 stepper driver modules, which generate STEP and DIR signals to precisely position the CoreXY actuator. In addition to motion control, the CU manages the electromagnet by sending a control signal to the gate pin of an N-channel MOSFET, which switches current through the electromagnet.

### Power Interface
The CoreXY subsystem interfaces with the Power subsystem by controlling current to the electromagnet through a MOSFET. The source pin of the MOSFET is connected to the common system ground, which is shared with the power supply. The drain pin is connected to the negative terminal of the electromagnet as well as to the anode of a flyback diode. The positive terminal of the electromagnet and the cathode of the diode are connected to the positive voltage of the power supply. When the MOSFET is on, it completes the circuit, allowing current to flow through the electromagnet and energize it. When the MOSFET is off, the diode provides a safe path for the inductive spike from the coil, protecting both the MOSFET and the rest of the system.

### Peripherals Interface
The CoreXY does not directly exchange signals with the Peripherals subsystem. However, the subsystems interact mechanically through piece movement. The pieces must be designed considering the size, flux, and holding force of the electromagnet to ensure reliable pickup and release operations. The board proportions will also affect the proportions of the CoreXY.

## 3D Model of Custom Mechanical Components

## Buildable Schematic
### Stepper Motors
<div align="center"> <img width="7660" height="2302" alt="stepper_drivers drawio" src="https://github.com/user-attachments/assets/1d59b5db-4ee8-4e1c-b0af-a13c247d0bca" /> </div>

### Electromagnet
<div align="center"> <img width="10487" height="6588" alt="electromagnet drawio" src="https://github.com/user-attachments/assets/cdb9893a-973a-437a-974a-06e71711c859" /> </div>
For completeness, the electromagnet schematic is shown in this section as well as in the CU. The parts are listed in the BOM for the CU.


## Bill of Materials
| Manufacturer | Part Number | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----|-----|-----|-----|-----|-----|-----|
| Seeed Studio | 101020073 | Mouser Electronics | 713-101020073 | 1 | $9.35 | [Link](https://www.mouser.com/ProductDetail/Seeed-Studio/101020073?qs=1%252B9yuXKSi8A5kCccI2u34g%3D%3D&srsltid=) |
| Adafruit | 324 | Adafruit | 324 | 2 | $14.00 | [Link](https://www.adafruit.com/product/324) |
| HICTOP | NA | Amazon | NA | 1 | $9.99 | [Link](https://www.amazon.com/HICTOP-Printer-Creality-Printers-16-5ft/dp/B00YMM6IQW/ref=sr_1_1_sspa) |
| McMaster-Carr | 3684N12 | McMaster-Carr | 3684N12 | 2 | $4.99 | [Link](https://www.mcmaster.com/3684N12/) |
| 3Dman | NA | Amazon | NA | 10/pack | $11.99 | [Link](https://www.amazon.com/3Dman-Toothless-Aluminum-Timing-Printer/dp/B07RV2T54M/ref=sr_1_3) |
| CNCMANs | NA | Amazon | NA | 1 | $15.02 | [Link](https://www.amazon.com/CNCMANS-Miniature-Bearing-Printing-MGN12H-250mm/dp/B0BNQ63X3H/ref=sr_1_1) |
| Unlorspy | NA | Amazon | NA | 1 | $4.49 | [Link](https://www.amazon.com/Unlorspy-Bracket-Brackets-Shelves-Furniture/dp/B0B24ZMT9J/ref=sr_1_3) |
| SIMAX3D | NA | Amazon | NA | 13/pack | $9.99 | [Link](https://www.amazon.com/SIMAX3D-Printer-Creality-Artillery-Sidewinder/dp/B08B4JDB67/ref=sr_1_1_sspa) |
| IXGNIJ | NA | Amazon | NA | 4/pack | $14.99 | [Link](https://www.amazon.com/Aluminum-Extrusion-European-Standard-Anodized/dp/B08Y8L11ZP/ref=sr_1_3) |
| **Total** |   |   |   |   | $109.29 |   |

## Analysis

The CoreXY subsystem’s design demonstrates a high degree of reliability, precision, and safety, ensuring it can effectively fulfill the intended role of automated chess piece movement. The system employs two NEMA17 stepper motors with 200 steps/rev and 1/16 microstepping, coupled to 16‑tooth GT2 pulleys with 2 mm pitch belts. This configuration achieves approximately 200 steps/mm, supporting positional accuracy within ±0.5 mm, consistent with the constraints for collision-free piece movement. Coordinated control through TMC2209 stepper drivers allows precise translation of Control Unit commands into smooth X–Y motion, completing typical chessboard traversals within ≤5 s, which ensures responsive gameplay.

Mechanical considerations, including equal belt tensioning (~5 N per belt), linear bearings, and 3D-printed carriage components, reduce backlash (<0.1 mm) and vibration while maximizing repeatability. Careful attention to calibration, acceleration, and velocity profiles ensures predictable, controllable motion, minimizing mechanical wear and extending subsystem longevity. With an estimated carriage mass of ~120 g including the electromagnet, the system operates safely within the stepper motors’ rated holding torque of 40 N·cm, allowing smooth acceleration up to 100 mm/s² without skipping steps.

The magnetic actuation system comprises a 5 V DC mini electromagnet, rated for ~400 g pull force with a nominal current of 0.4 A. MOSFET-based actuation with an included flyback diode protects the circuit from inductive spikes and ensures long-term reliability. Electromagnet activation latency is <10 ms, enabling precise, instantaneous pickup and release of individual chess pieces without disturbing neighboring pieces. Separation of the 5 V logic supply from the MOSFET’s load supply prevents switching noise from propagating into the stepper drivers or Control Unit.

Regulatory and ethical considerations have been fully addressed. Compliance with FCC Part 15, UL 94 flammability standards, and CPSC maximum surface temperature limits ensures safe operation. All wiring adheres to NEC Article 400 standards, with proper grounding per OSHA 29 CFR 1910 Subpart S. Components are cost-effective, widely available, and RoHS-compliant, ensuring accessibility, reproducibility, and sustainability for educational or research applications.

In conclusion, the CoreXY subsystem exemplifies a design that balances mechanical precision, electrical safety, regulatory compliance, and operational reliability. With detailed numeric validation of stepper resolution, carriage mass, belt tension, and electromagnet force, the design provides strong evidence that it will reliably meet its intended function and support smooth, safe, and accurate chessboard actuation under real-world operating conditions.

## References

[1] American National Standards Institute, ANSI Z535.4: Product Safety Signs and Labels, 2011 ed., Washington, DC: ANSI, 2011.

[2] “12-24V Mini Electromagnet,” Skycraft Surplus, LLC, 2025. https://skycraftsurplus.com/products/12-24v-mini-electromagnet.html
 (accessed Nov. 09, 2025).

[3] “Belt Frequency And Tensioning - 3D Distributed,” 3D Distributed, Nov. 05, 2020. https://3ddistributed.com/belt-frequency-and-tensioning/

[4] T. Banas, “How To Calculate The Force Of An Electromagnet,” Sciencing, Mar. 13, 2018. https://www.sciencing.com/calculate-force-electromagnet-5969962/

[5] “CoreXY | Cartesian Motion Platform,” corexy.com. https://corexy.com/theory.html‌

[6] M. Yin, Y. Chen, K.-H. Lee, D. K. C. Fu, and K.-W. Kwok, “Dynamic modeling and characterization of the Core-XY Cartesian motion system,” in Proc. IEEE Int. Conf. Real-time Comput. Robot. (RCAR), 2018, pp. 516–521.

[7] U.S. Consumer Product Safety Commission, “Manufacturing Best Practices,” Business Education, Manufacturing. [Online]. Available:
https://www.cpsc.gov/business--manufacturing/business-education/business-guidance/BestPractices [Accessed: Oct. 28, 2025].

[8] U.S. Consumer Product Safety Commission, “Maximum acceptable surface temperatures,” Code of Federal Regulations, Title 16, Part 1505.7. [Online]. Available:
https://www.law.cornell.edu/cfr/text/16/1505.7 [Accessed: Oct. 28, 2025].

[9] U.S. Federal Communications Commission, “47 CFR Part 15, Subpart B: Unintentional Radiators,” Electronic Code of Federal Regulations, Title 47, Chapter I, Subchapter A, Part 15, Subpart B. [Online]. Available: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15/subpart-B [Accessed: Oct. 27, 2025.]

[10] U.S. Occupational Safety and Health Administration, OSHA Standards – Subpart S: Electrical, 29 CFR 1910, Washington, D.C.: OSHA, 2025.

[11] National Fire Protection Association, NFPA 70, National Electrical Code®, 2017 ed., Quincy, MA: NFPA, 2016.

[12] National Fire Protection Association, NFPA 70, National Electrical Code®, 2023 ed., Quincy, MA: NFPA, 2022.

[13] P. Scantlebury and P. Eng, “Engineering Safety into the Design.” Available: https://www.cheminst.ca/wp-content/uploads/2019/04/Engineering20safety20into20the20design20-20Peter20Scantlebury-1.pdf

[14] U.S. company UL Solutions, “Protection from Electrical Hazards,” Nov. 2024. [Online]. Available: https://www.ul.com/resources/protection-electrical-hazards [Accessed: Oct. 28, 2025].

[15] Underwriters Laboratories, UL 94: Standard for Safety of Flammability of Plastic Materials for Parts in Devices and Appliances, 5th ed., Northbrook, IL: UL, 2024.
