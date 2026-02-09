# Detailed Design

In the Automated Chessboard, there are five subsystems: the Control Unit, Processing Unit, CoreXY Unit, Power Unit, and Peripherals Unit. This document serves as an in depth description and explanation of the design for the Peripherals Unit. It will explain the requirements for the peripherals, how they integrate into the larger solution, the reasoning behind important design decisions, and how to construct the Peripherals Unit.


## Function of the Subsystem

The function of the Peripherals Unit put simply is to interface between the player and the Processing Unit in real time. The Peripherals Unit will take in player-made spoken moves through a microphone and feed this information into the Processing Unit to be read and processed. The Peripherals will also use an LCD screen to allow players access to any information they may need from the Processing Unit. This can range from the command that is expected next, board state, last move, or anything else that needs to be communicated from the processor to the player. 

Additionally, the Peripherals Unit is responsible for the design and construction of the chessboard itself, interfacing between the players and the CoreXY subsystem. The board will also be responsible for housing all other subsystems.


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

The Peripherals Unit shall use a Hosyond 3.5 inch 480x320 LCD screen to interface with the users. This screen is large enough and clear enough to display any information needed in a way that is clear and readable, while still updating quickly by communicating with the Processing Unit via SPI. The subsystem shall use a Movo MA5U microphone to fit the small form factor while still capturing any voice input clearly. The microphone will also allow for easy communication via USB, connecting first to a USB mounting bracket on the surface of the board which then connects to the Processing Unit.

Each chess piece shall be 2.8cm wide, with 2.5 cm mild steel washers embedded in the bases to allow them to be moved with an electromagnet. Each chess piece shall have varying heights according to their ranking, with the king being 8.1cm tall and pawns being 5.1cm tall. To allow each piece to slide between two occupied squares freely, each chess square shall be 6.4cm wide. The full chessboard shall have 64 squares on the main playing area, with 16 extra squares on each side to store captured pieces of each color. The inside area of the chessboard shall be 12.7cm tall to allow the CoreXY to fit inside, with a compartment separate from the main playing area for the LCD, Microphone, Processing Unit, and Power Unit. The board shall be constructed out of plywood and acrylic to ensure that it is both structurally sound and portable.

To ensure compliance with heat and safety standards, the board shall include holes to allow for better airflow and cooling. The board shall operate below 12V to comply with IEC 62368 [3].



## Interface with Other Subsystems

The Peripherals Unit of the chessboard interfaces directly with the Processing Unit (Raspberry Pi 5) and indirectly with the CoreXY Unit. The Peripherals Unit forms the link between the user and the Processing Unit, transmitting data from the microphone to the processor, and receiving data from the processor to display on the screen. The Peripherals Unit also houses the CoreXY Unit, playing a role in how strong the magnetic force on the pieces will be.

### Processing Unit Interface
There will be two main data transmissions between the Processing Unit and the Peripherals: the microphone and the LCD screen. The microphone will transmit data to the processor via a serial USB connection. It will plug into a USB mounting bracket on top of the board, which has another female connector on the inside. The Processing Unit will connect to the other side of this mounting bracket, allowing the microphone and Raspberry Pi to communicate. The LCD screen will also be mounted on top of the chessboard above the Processing Unit, with a ribbon cable (listed in the Processing Unit's detailed design) connecting the two. The LCD and Raspberry Pi will communicate via SPI, with the LCD acting as the slave [6].

### CoreXY Unit Interface
While the Peripherals Unit and the CoreXY Unit are not directly linked in any way, the Peripherals Unit is heavily involved in the CoreXY's operation. The size of each piece, the metal embedded in the bottom of them, and the distance between the electromagnet and the base of the piece are all very important factors to the CoreXY's magnetic force. The Peripherals also house the CoreXY as a whole and indirectly interface with its operation.


## 3D Model of Custom Mechanical Components

### Chessboard 3D Models

Below are 3D models of the chessboard. All measurements displayed are in centimeters.

<div align="center"> 
<img width="1427" height="373" alt="image" src="https://github.com/user-attachments/assets/3cbf8265-b0f0-478f-acb9-62d011d5b42e" />
</div>
<div align="center"> 
<strong> Figure 1.1. Front view of chessboard. </strong> 
</div><br />

<div align="center"> 
<img width="1349" height="405" alt="image" src="https://github.com/user-attachments/assets/2965da42-851f-4b1c-8bef-a1d060ec4caa" />
</div>
<div align="center"> 
<strong> Figure 1.2. Side view of chessboard. </strong> 
</div><br />

<div align="center"> 
<img width="962" height="834" alt="image" src="https://github.com/user-attachments/assets/84b3f107-448e-4eb5-82fe-90c21fd58a7c" />
</div>
<div align="center"> 
<strong> Figure 1.3. Top view of chessboard. </strong> 
</div>
</div><br />

<div align="center"> 
<img width="1051" height="738" alt="image" src="https://github.com/user-attachments/assets/d1860d07-10d7-4914-ac8b-7b1babe2c186" />
</div>
<div align="center"> 
<strong> Figure 1.4. Isometric view of chessboard </strong> 
</div><br />


<img width="966" height="739" alt="image" src="https://github.com/user-attachments/assets/7c8be84b-9c4e-4362-aae9-1c97b83490d8" />
</div>
<div align="center"> 
<strong> Figure 1.5. Visualization of subsystem/component placement </strong> 
</div><br />


### Chess Piece 3D Models

Below are 3D models of the chess pieces. All measurements displayed are in centimeters.

<div align="center"> 
<img width="629" height="584" alt="image" src="https://github.com/user-attachments/assets/71a82e44-2fd8-48c7-901c-462b1e298a38" />
</div>
<div align="center"> 
<strong> Figure 2.1. Isometric view of white king. </strong> 
</div><br />

<div align="center"> 
<img width="629" height="580" alt="image" src="https://github.com/user-attachments/assets/0062aaaa-8678-4660-9f50-fdff21af0b92" />
</div>
<div align="center"> 
<strong> Figure 2.2. Isometric view of white queen. </strong> 
</div><br />

<div align="center"> 
<img width="690" height="554" alt="image" src="https://github.com/user-attachments/assets/e8f62c26-8186-4dad-ad9f-81aad606f0b4" />
</div>
<div align="center"> 
<strong> Figure 2.3. Isometric view of white bishop. </strong> 
</div><br />

<div align="center"> 
<img width="584" height="502" alt="image" src="https://github.com/user-attachments/assets/6b029f14-89bf-47f6-9ce8-5fc5196fa47d" />
</div>
<div align="center"> 
<strong> Figure 2.4. Isometric view of white knight. </strong> 
</div><br />

<div align="center"> 
<img width="716" height="575" alt="image" src="https://github.com/user-attachments/assets/6b63dee6-ed6e-4d6e-af16-ad20c09a063b" />
</div>
<div align="center"> 
<strong> Figure 2.5. Isometric view of white rook. </strong> 
</div><br />

<div align="center"> 
<img width="702" height="479" alt="image" src="https://github.com/user-attachments/assets/c260f4d3-834b-4fe1-bea3-0becc19ced8c" />
</div>
<div align="center"> 
<strong> Figure 2.6. Isometric view of white pawn. </strong> 
</div><br />









## Buildable Schematic 



<div align="center"> 
<img width="557" height="266" alt="image" src="https://github.com/user-attachments/assets/d097df1a-0aa6-4e88-8a4f-f7abbfd4ccea" />
</div>
<div align="center"> 
<strong> Figure 3.1. Buildable Electrical Schematic. </strong> 
</div><br />

The microphone will be plugged into a USB coupler that will plug into the Raspberry Pi, keeping the microphone wiring clean, strong, and interchangeable. The LCD will plug directly into the Raspberry Pi with a ribbon cable, communicating via SPI. Below is a pinout for the LCD screen.

<div align="center"> 
<img width="990" height="496" alt="image" src="https://github.com/user-attachments/assets/a18e9803-1349-43e9-b7a4-7a2520969387" />
</div>
<div align="center"> 
<strong> Figure 3.2. Pinout for Hosyond 3.5 inch LCD screen. [7] </strong> 
</div><br />




## BOM

| Manufacturer           | Part Number           | Description                     | Distributor | Quantity | Price   | Purchasing Website URL |
|------------------------|------------------------|---------------------------------|-------------|----------|---------|-------------------------|
| Hosyond                | B0BJDTL9J3             | 3.5 inch LCD Screen             | Amazon      | 1        | $17.99  | [Link](https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3) |
| XMSJSIY                | B0DT4D13CK             | Mounted USB Coupler             | Amazon      | 1        | $13.99  | [Link](https://www.amazon.com/XMSJSIY-Threaded-Extension-Charging-Connector/dp/B0DT4D13CK) |
| Movo                   | MA5U                   | USB Microphone                  | Amazon      | 1        | $9.95   | [Link](https://www.amazon.com/dp/B08ZQSCJS3) |
| ProWood                | 211799                 | 4 foot x 4 foot Plywood         | Home Depot  | 2        | $38.24  | [Link](https://www.homedepot.com/p/ProWood-23-32-in-x-4-ft-x-4-ft-BCX-Sanded-Plywood-211799/205723975) |
| Professional Plastics  | SPCCL.125X24X48FM      | 4 foot x 4 foot Acrylic Sheet   | Lowe's      | 1        | $38.95  | [Link](https://www.lowes.com/pd/Professional-Plastics-Clear-Polycarbonate-Sheet-1-8TX24WX48L/7134358) |
| Creality               | 3301010337             | 2kg black and white PLA Filament| Amazon      | 1        | $23.99  | [Link](https://www.amazon.com/gp/aw/d/B0C4TNQZYY) |
| Everbilt               | 800362                 | 100 (50 if available) 1" Steel Fender Washers | Home Depot | 1 | $12.62 | [Link](https://www.homedepot.com/p/Everbilt-1-8-in-x-1-in-Zinc-Plated-Fender-Washer-100-Piece-800362/204276365) |
| Grip-Rite              | 114CDWS1               | Drywall Screws, 1 lb Box        | Home Depot  | 1        | $6.97   | [Link](https://www.homedepot.com/p/Grip-Rite-6-x-1-1-4-in-2-Phillips-Bugle-Head-Coarse-Thread-Sharp-Point-Drywall-Screws-1-lb-Box-114CDWS1/100152392) |
| **Total**              |                        |                                 |             |          | **$200.94** |                         |



## Analysis

The proposed Peripherals Unit successfully meets its functional requirements by providing a clear, reliable interface between the players, the Processing Unit, and the CoreXY mechanism. The choice of a compact omnidirectional USB microphone ensures that spoken moves are captured cleanly from either player without repositioning, while the digital USB connection eliminates analog noise issues and fits within the allotted space. The 3.5-inch SPI LCD display provides fast, readable visual feedback, updating within one second as required and offering sufficient resolution for move confirmations, alerts, and prompts. Together, these components create a dependable communication loop between the players and the Raspberry Pi 5.

The physical design of the chessboard is also well aligned with system requirements and the needs of the CoreXY subsystem. Each 6.4-cm square is large enough for pieces to pass between adjacent occupied squares without collision, while the use of embedded steel washers in the 2.8-cm piece bases ensures consistent magnetic coupling with the electromagnet. The 12.7-cm internal cavity provides enough vertical space for each subsystem as well as airflow channels and wiring paths. Plywood and acrylic construction keeps the board lightweight enough for a single person to lift while maintaining structural rigidity and offering low thermal conductivity for user safety.

The subsystem clearly satisfies regulatory, electrical, and safety constraints. Operating below 12 volts reduces electrical hazard risk and eases compliance with IEC 62368-1 [3], while ventilation holes, insulated wiring, strain relief, and overcurrent protection all support safe operation and tolerance for single-fault failures. The electronics chosen—consumer-grade USB and SPI components—are inherently compliant with FCC Part 15 for conducted and radiated emissions [2]. These design choices minimize hazards while ensuring long-term reliability and ease of maintenance.

The Peripherals Unit also reflects thoughtful ethical and socioeconomic considerations. The LCD interface provides an alternative to voice-only control, supporting accessibility for users with speech impairments or in noisy environments. Voice processing occurs locally on the Raspberry Pi, protecting user privacy in line with ACM ethical guidelines[4]. Material choices such as plywood, acrylic, and PLA minimize cost, promote repairability, and reduce electronic waste by allowing easy component replacement [5]. Overall, the Peripherals Unit design is cohesive, achievable, and well matched to the constraints, enabling it to fulfill its role as a robust and user-friendly subsystem within the Automated Chessboard.

## References
[1] Premier Chess. Back to Basics: Notation. Available at: https://premierchess.com/chess-pedagogy/back-to-basics-notation

[2] U.S. Federal Communications Commission. 47 CFR Part 15 – Radio Frequency Devices. Available at: https://www.govinfo.gov/content/pkg/CFR-2004-title47-vol1/html/CFR-2004-title47-vol1-part15.htm

[3] International Electrotechnical Commission. IEC 62368-1: Audio/Video, Information and Communication Technology Equipment – Part 1: Safety Requirements. Available at: https://webstore.iec.ch/en/publication/6932

[4] Association for Computing Machinery. ACM Code of Ethics and Professional Conduct. Available at: https://www.acm.org/code-of-ethics

[5] United Nations Institute for Training and Research. Global E-Waste Monitor 2020. Available at: https://ewastemonitor.info

[6] "Serial Peripheral Interface," Available at: https://en.wikipedia.org/wiki/Serial_Peripheral_Interface

[7] Amazon. LCD Display Listing and Specifications. Available at: https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3
