# Detailed Design

In the Automated Chessboard, there are five subsystems: the Control Unit, Processing Unit, CoreXY Unit, Power Unit, and Peripherals Unit. This document serves as an in depth description and explanation of the design for the Peripherals Unit. It will explain the requirements for the peripherals, how they integrate into the larger solution, the reasoning behind important design decisions, and how to construct the Peripherals Unit.


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

Integrate a buildable electrical schematic directly into the document. If the diagram is unreadable or improperly scaled, the supervisor will deny approval. Divide the diagram into sections if the text and components seem too small.

The schematic should be relevant to the design and provide ample details necessary for constructing the model. It must be comprehensive so that someone, with no prior knowledge of the design, can easily understand it. Each related component's value and measurement should be clearly mentioned.
<div align="center"> 
<img width="990" height="496" alt="image" src="https://github.com/user-attachments/assets/a18e9803-1349-43e9-b7a4-7a2520969387" />
</div>
<div align="center"> 
<strong> Figure 3.2. Pinout for Hosyond 3.5 inch LCD screen. [7] </strong> 
</div><br />



## BOM

| Manufacturer | Part Number | Description | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----|-----|-----|-----|-----|-----|-----|-----|
| Hosyond | ATmega328 | Microcontroller | Arduino | A000005 | 1 | $25.70 | [Link](https://store-usa.arduino.cc/products/arduino-nano?srsltid=AfmBOoqNFNSG0SfKF8ZFeKFBkwAtX5L50eVlOeBv6cMGf4bc8P1TCnzK) |
| Trinamic | TMC2209 | Stepper Driver Board | Adafruit | 6121 | 2 | $8.95 | [Link](https://www.adafruit.com/product/6121?srsltid=AfmBOoqNbFwMYs_rbP4OZemtZmfuFAdtoNUtJ39PrpSNCZA5T_JOs630) |
| Adafruit | 1493 | Stepper Driver Heatsink | Adafruit | 1493 | 2 | $1.90 | [Link](https://www.adafruit.com/product/1493?srsltid=AfmBOooGAp5R_4tQ_ICG5NDZss1rWk8G5H7ZEkV5ucMBG2qJobr0fFEz) |
| Alpha and Omega Semiconductor Inc. | AOSS32334C | MOSFET | Digikey | 785-AOSS32334CCT-ND | 1 | $0.44 | [Link](https://www.digikey.com/en/products/detail/alpha-omega-semiconductor-inc/AOSS32334C/11567505) |
| SMC Diode Solutions | MBR1045 | Flyback Diode | Digikey | 1655-1019-ND | 1 | $1.05 | [Link](https://www.digikey.com/en/products/detail/smc-diode-solutions/MBR1045/6022109) |
| Yageo | CFR-25JB-52-100K | Pulldown Resistor | Digikey | 13-CFR-25JB-52-100K-ND | 1 | $0.10 | [Link](https://www.digikey.com/en/products/detail/yageo/CFR-25JB-52-100K/245) |
| Yageo | MFR-25FRF52-100R | Gate Resistor | Digikey | 13-MFR-25FRF52-100RCT-ND | 1 | $0.10 | [Link](https://www.digikey.com/en/products/detail/yageo/MFR-25FRF52-100R/18092105) |
| Yageo | MFR-25FRF52-100R | Gate Resistor | Digikey | 13-MFR-25FRF52-100RCT-ND | 1 | $0.10 | [Link](https://www.digikey.com/en/products/detail/yageo/MFR-25FRF52-100R/18092105) |
| Adafruit | 4785 | Perfboard | Digikey | 1528-4785-ND | 1 | $2.50 | [Link](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4785/13617529) |
| **Total** |   |   |   |   |   | $40.74 |   |
Provide a comprehensive list of all necessary components along with their prices and the total cost of the subsystem. This information should be presented in a tabular format, complete with the manufacturer, part number, distributor, distributor part number, quantity, price, and purchasing website URL. If the component is included in your schematic diagram, ensure inclusion of the component name on the BOM (i.e R1, C45, U4).

## Analysis

Deliver a full and relevant analysis of the design demonstrating that it should meet the constraints and accomplish the intended function. This analysis should be comprehensive and well articulated for persuasiveness.

## References
[1] Premier Chess. Back to Basics: Notation. Available at: https://premierchess.com/chess-pedagogy/back-to-basics-notation

[2] U.S. Federal Communications Commission. 47 CFR Part 15 – Radio Frequency Devices. Available at: https://www.govinfo.gov/content/pkg/CFR-2004-title47-vol1/html/CFR-2004-title47-vol1-part15.htm

[3] International Electrotechnical Commission. IEC 62368-1: Audio/Video, Information and Communication Technology Equipment – Part 1: Safety Requirements. Available at: https://webstore.iec.ch/en/publication/6932

[4] Association for Computing Machinery. ACM Code of Ethics and Professional Conduct. Available at: https://www.acm.org/code-of-ethics

[5] United Nations Institute for Training and Research. Global E-Waste Monitor 2020. Available at: https://ewastemonitor.info

[6] "Serial Peripheral Interface," Available at: https://en.wikipedia.org/wiki/Serial_Peripheral_Interface

[7] Amazon. LCD Display Listing and Specifications. Available at: https://www.amazon.com/Hosyond-480x320-Screen-Display-Raspberry/dp/B0BJDTL9J3
