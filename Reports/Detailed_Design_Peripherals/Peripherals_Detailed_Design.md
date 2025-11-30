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

This section should provide a list of constraints applicable to the subsystem, along with the rationale behind these limitations. For instance, constraints can stem from physics-based limitations or requirements, subsystem prerequisites, standards, ethical considerations, or socio-economic factors.

The team should set specifications for each subsystem. These specifications may require modifications, which must be authorized by the team. It could be necessary to impose additional constraints as further information becomes available.

Every subsystem must incorporate at least one constraint stemming from standards, ethics, or socio-economic factors.


## Overview of Proposed Solution

Describe the solution and how it will fulfill the specifications and constraints of this subsystem.


## Interface with Other Subsystems

The Peripherals of the Chess board interface directly with the Processing Unit (Raspberry Pi 5) and indirectly with the CoreXY Unit. The peripherals form the link between the user and the Processing Unit, transmitting data from the microphone and to the screen, while also housing the CoreXY, playing a key role in how it interacts with the pieces.

### Processing Unit Interface
There will be two main data transmissions between the Processing Unit and the Peripherals: the microphone (Movo MA5U) and the LCD screen (AREALER GS06649-01). The microphone will transmit data to the processor via a serial USB connection. 


## 3D Model of Custom Mechanical Components

Should there be mechanical elements, display diverse views of the necessary 3D models within the document. Ensure the image's readability and appropriate scaling. Offer explanations as required.


## Buildable Schematic 

Integrate a buildable electrical schematic directly into the document. If the diagram is unreadable or improperly scaled, the supervisor will deny approval. Divide the diagram into sections if the text and components seem too small.

The schematic should be relevant to the design and provide ample details necessary for constructing the model. It must be comprehensive so that someone, with no prior knowledge of the design, can easily understand it. Each related component's value and measurement should be clearly mentioned.


## Printed Circuit Board Layout

Include a manufacturable printed circuit board layout.


## Flowchart

For sections including a software component, produce a chart that demonstrates the decision-making process of the microcontroller. It should provide an overview of the device's function without exhaustive detail.


## BOM

Provide a comprehensive list of all necessary components along with their prices and the total cost of the subsystem. This information should be presented in a tabular format, complete with the manufacturer, part number, distributor, distributor part number, quantity, price, and purchasing website URL. If the component is included in your schematic diagram, ensure inclusion of the component name on the BOM (i.e R1, C45, U4).

## Analysis

Deliver a full and relevant analysis of the design demonstrating that it should meet the constraints and accomplish the intended function. This analysis should be comprehensive and well articulated for persuasiveness.

## References

All sources that have contributed to the detailed design and are not considered common knowledge should be duly cited, incorporating multiple references.
