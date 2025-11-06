# Detailed Design

**NOTE: REVISE INTRO AS DOCUMENT IS FILLED OUT**

This document presents a comprehensive overview of the Control Unit (CU) subsystem, one of the four primary components of the automated chessboard system; the other subsystems including the Processing Unit, CoreXY Unit, Power Unit, and Peripherals Unit. While the primary focus is on the Control Unit, this document also provides a high-level integration perspective with the remaining subsystems, in order to illustrate the CU’s role in coordinating communication, motion, and actuation across the entire system. Additionally, the document outlines the key technical constraints, relevant electrical and safety standards, and operational requirements that guide the subsystem’s design and implementation. Finally, it describes the proposed circuitry, communication methods, and control logic necessary to construct and validate the Control Unit as a critical part of the complete automated chessboard solution.

## Function of the Subsystem

The Control Unit (CU) serves as the central command interface between the Processing Unit and the physical motion components of the automated chessboard. Acting as the intermediary between high-level logic and low-level hardware control, the CU receives validated chess move commands from the Raspberry Pi over a serial UART connection and translates them into precise motor and actuator operations. The subsystem is responsible for generating synchronized STEP and DIR signals to drive two stepper motors that operate the CoreXY mechanism, enabling coordinated movement across the chessboard’s X and Y axes.

In addition to motion control, the CU manages the piece "pickup" mechanism through an electromagnet that securely "grabs" and releases chess pieces during gameplay. To ensure safe and reliable operation, the CU continuously monitors limit switches, driver fault signals, and supply voltage, in addition to implementing safety protocols (such as immediate halting in the event of faults or out-of-range conditions). Motion profiling, including acceleration and deceleration phases, is integrated into the control logic to guarantee smooth and accurate piece movement. Through this coordinated functionality, the CU enables precise actuation of all chess moves, while both completing each move within five seconds and ensuring reliable piece capture and placement across the board.


## Specifications and Constraints

This section should provide a list of constraints applicable to the subsystem, along with the rationale behind these limitations. For instance, constraints can stem from physics-based limitations or requirements, subsystem prerequisites, standards, ethical considerations, or socio-economic factors.

The team should set specifications for each subsystem. These specifications may require modifications, which must be authorized by the team. It could be necessary to impose additional constraints as further information becomes available.

Every subsystem must incorporate at least one constraint stemming from standards, ethics, or socio-economic factors.


## Overview of Proposed Solution

Describe the solution and how it will fulfill the specifications and constraints of this subsystem.


## Interface with Other Subsystems

Provide detailed information about the inputs, outputs, and data transferred to other subsystems. Ensure specificity and thoroughness, clarifying the method of communication and the nature of the data transmitted.


## Buildable Schematic 

Integrate a buildable electrical schematic directly into the document. If the diagram is unreadable or improperly scaled, the supervisor will deny approval. Divide the diagram into sections if the text and components seem too small.

The schematic should be relevant to the design and provide ample details necessary for constructing the model. It must be comprehensive so that someone, with no prior knowledge of the design, can easily understand it. Each related component's value and measurement should be clearly mentioned.


## Flowchart

For sections including a software component, produce a chart that demonstrates the decision-making process of the microcontroller. It should provide an overview of the device's function without exhaustive detail.


## BOM

| Manufacturer | Part Number | Distributor | Distributor Part Number | Quantity | Price | Purchasing Website URL |
|-----|-----|-----|-----|-----|-----|-----|
| Arduino Nano | A000005 | Arduino | ..... | 1 | $25.70 | [Link](https://store-usa.arduino.cc/products/arduino-nano?srsltid=AfmBOoqNFNSG0SfKF8ZFeKFBkwAtX5L50eVlOeBv6cMGf4bc8P1TCnzK) |
| **Total** |   |   |   |   | **....** |   |

## Analysis

Deliver a full and relevant analysis of the design demonstrating that it should meet the constraints and accomplish the intended function. This analysis should be comprehensive and well articulated for persuasiveness.

## References

All sources that have contributed to the detailed design and are not considered common knowledge should be duly cited, incorporating multiple references.
