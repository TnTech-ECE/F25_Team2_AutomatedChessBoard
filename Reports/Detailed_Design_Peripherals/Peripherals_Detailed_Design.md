# Detailed Design

In the Automated Chess Board, there are five subsystems: the Control Unit, Processing Unit, CoreXY Unit, Power Unit, and Peripherals Unit. This document serves as an in depth description and explanation of the design for the Peripherals Unit. It will explain the requirements for the peripherals, how they integrate into the larger solution, the reasoning behind important design decisions, and how to construct the Peripherals Unit.


## General Requirements for the Document

The document should include:

- Explanation of the subsystem’s integration within the overall solution
- Detailed specifications and constraints specific to the subsystem
- Synopsis of the suggested solution
- Interfaces to other subsystems
- 3D models of customized mechanical elements*
- A buildable diagram*
- A Printed Circuit Board (PCB) design layout*
- An operational flowchart*
- A comprehensive Bill of Materials (BOM)
- Analysis of crucial design decisions

*Note: These technical documentation elements are mandatory only when relevant to the particular subsystem.


## Function of the Subsystem

The function of the Peripherals Unit put simply is to interface between the player and the Processing Unit in real time. The Peripherals Unit will take in player-made spoken moves through a microphone and feed this information into the Processing Unit to be read and processed. The Peripherals will also use an LCD screen to allow players access to any information they may need from the Processing Unit. This can range from the command that is expected next, board state, last move, or anything else that needs to be communicated from the processor to the player. 

Additionally, the Peripherals Unit is responsible for the design and construction of the chess board itself, interfacing between the players and the CoreXY subsystem. The board will also be responsible for housing all other subsystems.


## Specifications and Constraints

### General Specifications

The Peripherals Unit shall include an LCD display capable of presenting movement confirmations, illegal-move alerts, and overall game-state information using characters at least 10-point in size for readability. The display shall support high-contrast text or graphics to maintain visibility under standard indoor lighting. The LCD display shall update within one second of command processing to show movement confirmations, illegal-move notifications, or overall game-state changes. The microphone shall reliably capture and transmit voice input to the Processing Unit clearly enough to be accurately processed. The microphone shall be omnidirectional, allowing it to clearly hear either player without repositioning, and it shall fit entirely within a 12cm x 12cm x 12cm area. The chessboard assembly shall weigh less than 30 pounds to allow one person to move it. The board shall contain 64 standard squares with labeled files and ranks, in addition to 32 supplemental squares for storing captured pieces. [1] Each individual square shall be large enough that a piece may pass between two adjacent occupied squares without disturbing other pieces. Each piece shall differ in height according to their ranking, with kings being the tallest and pawns being the shortest. The internal structure of the chessboard shall also provide sufficient space to house all other subsystems.

### Regulatory and Compliance Constraints

The system shall comply with electromagnetic interference requirements defined by the U.S. Federal Communications Commission under 47 CFR Part 15, which governs the emissions of unintentional radiators [2]. All electronic components shall adhere to IEC 62368-1, which provides safety requirements for audio, video, and information-technology equipment [3].

### Electrical and Safety Constraints

The system shall operate using below 12 V to reduce electrical-shock risk and simplify compliance with hazard-based safety requirements described in IEC 62368-1 [3]. User-accessible surfaces shall not expose conductive elements carrying live voltage. Overcurrent protection—such as fuses or resettable polyfuses—shall be incorporated to mitigate the risk of overheating, excessive current draw, or fire. All wiring and connectors shall be properly insulated and strain-relieved to prevent accidental short circuits. Thermal output from internal components shall remain within limits defined by manufacturer datasheets and industry safety guidelines. The system shall be robust against single-fault failures and shall not expose the user to hazardous electrical energy under any foreseeable operating condition.

### Ethical and Socioeconomic Constraints

The system shall support accessibility by providing alternatives to voice-only input where feasible, ensuring inclusive usability for individuals with speech impairments or in environments where voice commands may not be reliable. The processing of voice data shall follow ethical principles of user privacy and consent as recommended by the ACM Code of Ethics [4]. The design shall prioritize local processing of voice commands when possible, avoid unnecessary collection or storage of personal data, and ensure users maintain control over any data that might be transmitted externally. Socioeconomic considerations such as affordability, repairability, and minimizing electronic waste shall guide material selection and component sourcing, aligning with recommendations from global sustainability research on electronic waste [5].


## Overview of Proposed Solution




## Interface with Other Subsystems

The Peripherals of the Chess board interface directly with the Processing Unit (Raspberry Pi 5) and indirectly with the CoreXY Unit. The peripherals form the link between the user and the Processing Unit, transmitting data from the microphone and to the screen, while also housing the CoreXY, playing a key role in how it interacts with the pieces.

### Processing Unit Interface
There will be two main data transmissions between the Processing Unit and the Peripherals: the microphone (Movo MA5U) and the LCD screen (AREALER GS06649-01). The microphone will transmit data to the processor via a serial USB connection. 


## 3D Model of Custom Mechanical Components

<img width="1288" height="335" alt="image" src="https://github.com/user-attachments/assets/2da9dc23-e576-47fb-beaf-7720a85577fa" />

<img width="941" height="795" alt="image" src="https://github.com/user-attachments/assets/5cab5331-2d5e-4f0f-a81b-9f004788ff81" />

<img width="1256" height="288" alt="image" src="https://github.com/user-attachments/assets/904bc15e-590a-4217-82a7-f453009c514d" />

<img width="1328" height="847" alt="image" src="https://github.com/user-attachments/assets/fce88115-a54f-4c17-a138-88b9dcd5172f" />

<img width="966" height="739" alt="image" src="https://github.com/user-attachments/assets/7c8be84b-9c4e-4362-aae9-1c97b83490d8" />




## Buildable Schematic 

Integrate a buildable electrical schematic directly into the document. If the diagram is unreadable or improperly scaled, the supervisor will deny approval. Divide the diagram into sections if the text and components seem too small.

The schematic should be relevant to the design and provide ample details necessary for constructing the model. It must be comprehensive so that someone, with no prior knowledge of the design, can easily understand it. Each related component's value and measurement should be clearly mentioned.



## BOM

Provide a comprehensive list of all necessary components along with their prices and the total cost of the subsystem. This information should be presented in a tabular format, complete with the manufacturer, part number, distributor, distributor part number, quantity, price, and purchasing website URL. If the component is included in your schematic diagram, ensure inclusion of the component name on the BOM (i.e R1, C45, U4).

## Analysis

Deliver a full and relevant analysis of the design demonstrating that it should meet the constraints and accomplish the intended function. This analysis should be comprehensive and well articulated for persuasiveness.

## References
[1] Premier Chess. Back to Basics: Notation. Available at: https://premierchess.com/chess-pedagogy/back-to-basics-notation

[2] U.S. Federal Communications Commission. 47 CFR Part 15 – Radio Frequency Devices. Available at: https://www.govinfo.gov/content/pkg/CFR-2004-title47-vol1/html/CFR-2004-title47-vol1-part15.htm

[3] International Electrotechnical Commission. IEC 62368-1: Audio/Video, Information and Communication Technology Equipment – Part 1: Safety Requirements. Available at: https://webstore.iec.ch/en/publication/6932

[4] Association for Computing Machinery. ACM Code of Ethics and Professional Conduct. Available at: https://www.acm.org/code-of-ethics

[5] United Nations Institute for Training and Research. Global E-Waste Monitor 2020. Available at: https://ewastemonitor.info
