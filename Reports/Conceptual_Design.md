## Fully Formulated Problem

The primary objective of this project is to design and build a low-cost, accessible, and intelligent automated chess board that enhances the traditional over-the-board (OTB) chess experience by integrating online play, AI-based solo play, and voice command functionality. The system shall support physical gameplay while interfacing with online platforms and allow players with physical or visual disabilities to engage in independent play through voice control and automated piece movement.

The system shall be constructed using affordable and readily available components to ensure replicability by hobbyists. In doing so, the board shall bridge the gap between digital and physical chess play while improving accessibility and reducing cost barriers.

### Specifications

The chessboard will meet the following requirements to ensure reliability and operability:

1. Vocal Processing System: The system shall enable players to control gameplay using spoken commands. 

    - Microphone (Peripheral Input): The device shall capture vocal output from users and transmit it to the processing unit for analysis.
    - Processing Unit: The unit shall utilize Vosk to process and filter voice input with a minimum accuracy of 80%. It shall listen for input only while a designated button is pressed or after a command word is detected, recognize commands in algebraic chess notation and common variations (e.g., “Knight to e5,” “Bishop a4”), and process commands within 5 seconds the end of voice input.
2. Piece Positioning XY Frame: The system shall magnetically drag pieces to the proper square using stepper motors to position pieces based on their x and y coordinates.

    - Processing Unit: The unit shall utilize Stockfish to enable single-player gameplay against an AI opponent.
    - Control Unit: The unit shall use an Arduino with Big Easy Drivers to interpret vocal commands, drive the XY movement, complete any piece movement within 5 seconds, and remove 95% of captured pieces without collision.
    - Core XY: The unit shall precisely position the magnetic actuator to relocate pieces while ensuring all pieces remain upright and stable during movement.

3. Visual Output: The system shall output game data to optimize user experience.
    - Display Screen (Peripheral Output): The device shall display move confirmations, illegal move alerts, and overall game status updates within 1 second of command processing. It shall display characters ≥ 10 pt for readability and support high-contrast text or graphics for clear visibility under standard indoor lighting.
4. Board Assembly: The system shall be assembled to minimize overall weight, support ease of transport, and improve user accessibility. The board shall weigh less than 30 pounds to allow transport by a single user and include features that facilitate transportability. File and rank labels shall be clearly displayed to assist users in locating squares during gameplay.
5. Power Supply System: The board shall include a sleep mode to reduce power consumption when idle and shall operate using rechargeable battery capable of supporting at least 2 hours of active gameplay.
6. System Design and Modularity: The final board shall cost no more than $350 USD in materials and have a modular design allowing for individual upgrades.

These specifications were developed in collaboration with stakeholders to define the system’s ideal functions while minimizing cost. They are designed to meet the functional requirements effectively, comply with relevant industry standards and regulations, and prioritize accessibility and user inclusion—all without compromising affordability or overall system performance.

### Constraints
- Regulatory and Compliance Constraints: To ensure the system meets U.S. consumer electronics and electrical standards.
    - Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
    - Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
    - Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
    - Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.
    - Shall operate within safe limits per UL 2054 to prevent thermal or electrical hazards.
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

1. Voice Controls
    - The microphone captures user commands upon a voice command trigger.
    - The processing unit uses Vosk to process and filter voice commands, recognizing different accents and speech patterns.
2. Automated Piece Movement
    - The Arduino interprets processed voice commands and controls Big Easy Drivers to operate the stepper motors.
    - Stepper motors precisely drive the magnetic carriage to reposition chess pieces accurately on the board.
3. Visual Feedback
    - Display screen shows move confirmations, illegal move alerts, and game status.
    - Supports accessibility for players who may have hearing impairments or require additional visual cues.
4. User Accessibility
    - The system design emphasizes simplicity and intuitive use, minimizing the need for direct physical interaction.
    - Voice recognition supports a variety of player voices, including different accents and frequencies.
5. Power and Efficiency
    - The system includes an idle or sleep mode to conserve energy when not in active use.
    - The board provides at least 2 hours of continuous gameplay on battery power.
6. Modularity and Scalability
    - The design supports easy upgrades or replacements of individual subsystems by hobbyists or users.
    - Comprehensive documentation facilitates user modifications and future development.
7. Portability and Durability
    - The board is lightweight for easy transport and includes a carrying method for convenience.
    - The system is constructed from durable materials to prevent damage during normal use.
8. Cost Efficiency
    - The system is designed to remain under $350 USD in material costs while maintaining or exceeding the quality of comparable solutions.
________________________________________

#### Processing Unit 
The Processing Unit will consist of a Raspberry Pi responsible for coordinating all high-level system operations. Its primary functions are fourfold. First, it will interpret incoming audio signals from the microphone using the Vosk speech recognition engine to convert spoken commands into recognizable text, while also supplying power to the microphone. Second, it will maintain the internal state of the chessboard and verify the legality of player moves using the Stockfish chess engine. Third, it will transmit validated and legal move commands to the Control Unit (Arduino) for conversion into motion control instructions. Lastly, the Raspberry Pi will send display data to the screen, providing the user with real-time visual feedback on system activity and game status.

Relevant Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.

Control Unit
The Control Unit will manage all motion control functions and serve as the intermediary between the Processing Unit and the mechanical subsystems. It will receive move instructions from the Raspberry Pi, interpret them into executable signals for the CoreXY motors, and transmit confirmation messages back to the Processing Unit. This will be achieved through the Arduino’s coordination of communication with stepper motor drivers housed within the Control Unit. The servo motor responsible for magnetic actuation will receive direct control signals from the Arduino to ensure precise vertical (Z-axis) movement.

Relevant Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.

Core XY Unit
The CoreXY Unit will execute all physical motion required to reposition chess pieces on the board. Upon receiving step and direction commands from the Control Unit, it will drive two stepper motors to manipulate belts and pulleys that move a magnetic carriage across the X and Y axes. A servo-driven magnet will function as the Z-axis actuator, enabling the magnet to raise and lower as needed. This mechanism minimizes magnetic interference with nearby pieces and prevents unintentional displacement during movement.

Relevant Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  

Peripherals Unit
The Peripherals Unit consists of the system’s input and output devices — the microphone and display screen. The microphone captures user voice commands, potentially supported by software-based noise filtering to improve accuracy and clarity. The display provides feedback to the player by showing system messages such as “Not a Legal Move” or “Pawn to A5”, as well as overall game status updates. Together, these peripherals form the user interface that enables intuitive interaction with the system.

Relevant Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall conform to Section 508 of the Rehabilitation Act, ensuring accessible interfaces for users with disabilities.  
- Shall follow ergonomic layout guidelines from ANSI/HFES 100-2007, ensuring proper control placement and feedback.  
- Shall follow universal design principles to minimize cognitive and physical usability barriers.  

Power Unit
The Power Unit supplies regulated electrical power to all other subsystems. It will consist of a battery-based power source designed to provide multiple voltage levels to meet the varying current and voltage requirements of each component. The 12V rail will supply power to the stepper motors and drivers, while the 5V rail will support the Raspberry Pi, Arduino, and other control and peripheral electronics. Proper power regulation and distribution are essential to ensure safe, stable, and efficient system operation.

Relevant Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.
- Shall operate within safe limits per UL 2054 to prevent thermal or electrical hazards.
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  
