## Fully Formulated Problem

The primary objective of this project is to design and build a low-cost, accessible, and intelligent automated chess board that enhances the traditional over-the-board (OTB) chess experience by integrating online play, AI-based solo play, and voice command functionality. The system shall support physical gameplay while interfacing with online platforms and allow players with physical or visual disabilities to engage in independent play through voice control and automated piece movement.

The system shall be constructed using affordable and readily available components to ensure replicability by hobbyists. In doing so, the board shall bridge the gap between digital and physical chess play while improving accessibility and reducing cost barriers.

### Specifications

The chessboard will meet the following requirements to ensure reliability and operability:

1. Vocal Processing System: The system shall enable players to control gameplay using spoken commands. 

    - Processing Unit: The unit shall execute software to process and filter voice input with a minimum accuracy of 80%. It shall listen for input only while a designated button is pressed or after a command word is detected, recognize commands in algebraic chess notation and common variations (e.g., “Knight to e5,” “Bishop a4”), and process commands within 5 seconds of button release or the end of voice input.
2. Piece Positioning XY Frame: The system shall magnetically drag pieces to the proper square using stepper motors to position pieces based on their x and y coordinants.

    - Axes/Stepper Motors: The unit shall enable precise positioning of the magnetic actuator to relocate pieces within 0.5 inches of the center of each square, complete any movement within 5 seconds, and remove 95% of captured pieces without collision.
    - Magnets: The unit shall maintain a secure magnetic connection between the actuator and each chess piece to ensure all pieces remain upright and stable during movement.
3. Board Assembly: The system shall be assembled to minimize overall weight, support ease of transport, and improve user accessibility.
   
    - Structure and Weight: The total board assembly shall weigh less than 30 pounds to allow transport by a single user.
    - Portability Features: The design shall include features that facilitate transport, such as a carrying handle or detachable cover.
    - Labeling: Each file and rank shall be clearly labeled to assist users in locating squares during gameplay.
4. Power Supply System: The board shall include a sleep mode to reduce power consumption when idle and shall operate using either a 12V DC adapter or a rechargeable battery capable of supporting at least 2 hours of active gameplay.
5. System Design and Modularity: The final board shall cost no more than $350 USD in materials and have a modular design allowing for individual upgrades.

##TODO: fix the first sentence after we talk to people
Thus far these specifications have been determined by us, and I'm just writing this here til that changes. They have been developed to best meet the functional requirements while maintaining compliance with relevant industry standards and regulations. The design prioritizes accessibility and user inclusion without compromising on affordability or overall system performance.

### Constraints
- Regulatory and Compliance Constraints: To ensure the system meets U.S. consumer electronics and electrical standards.
 - Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
 - Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
 - Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
 - Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.
- Electrical and Safety Constraints: To prevent electrical, thermal, and physical hazards during operation.
 - Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
 - Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
 - Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
 - Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  
- Accessibility and Ergonomic Constraints: To ensure usability for a wide range of users.
 - Shall conform to Section 508 of the Rehabilitation Act, ensuring accessible interfaces for users with disabilities.  
 - Shall follow ergonomic layout guidelines from ANSI/HFES 100-2007, ensuring proper control placement and feedback.  
 - Shall follow universal design principles to minimize cognitive and physical usability barriers.

#### Key Features

1. idk
2. idk
3. idk
4. idk
5. idk
6. idk
7. idk
________________________________________
