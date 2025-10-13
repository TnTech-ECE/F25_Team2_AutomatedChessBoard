##CHANGE ME

# Conceptual Design

This document outlines the objectives of a conceptual design. After reading your conceptual design, the reader should understand:

- The fully formulated problem.
- The fully decomposed conceptual solution.
- Specifications for each of the atomic pieces of the solution.
- Any additional constraints and their origins.
- How the team will accomplish their goals given the available resources.

With these guidelines, each team is expected to create a suitable document to achieve the intended objectives and effectively inform their stakeholders.


## General Requirements for the Document
- Submissions must be composed in Markdown format. Submitting PDFs or Word documents is not permitted.
- All information that is not considered common knowledge among the audience must be properly cited.
- The document should be written in the third person.
- An introduction section should be included.
- The latest fully formulated problem must be clearly articulated using explicit "shall" statements.
- A comparative analysis of potential solutions must be performed
- The document must present a comprehensive, well-specified high-level solution.
- The solution must contain a hardware block diagram.
- The solution must contain an operational flowchart.
- For every atomic subsystem, a detailed functional description, inputs, outputs, and specifications must be provided.
- The document should include an acknowledgment of ethical, professional, and standards considerations, explaining the specific constraints imposed.
- The solution must include a refined estimate of the resources needed, including: costs, allocation of responsibilities for each subsystem, and a Gantt chart.


## Introduction

Chess is a complex and strategic game that allows players to compete against each other on an even playing field with no hidden information. 
As it has grown more popular, new ways to enjoy this age old game have been developed. One of the most interesting examples of this is the automated chess board.
Automated chess boards are able to improve the user experience by changing the way that they interact with over the board chess. 
Vocal input is often used, making the board more accessible to people with a reduced range of motion while also being a fresh and new way to play.
These chess boards must also be able to move pieces around the board on their own, allowing users to compete against a computer and even other opponents online.
Although automated chess enhances over the board play, it is inaccessible to most due to its high price point. 

The demand for a cheaper option that does not compromise on functionality is clear. The proposed project aims to create a chess board that reliably recognizes voice input, automates piece movement, and integrates with computer opponents, all while continuing to be affordable.
The primary objective of this board is to bring the benefits that come with automated chess to a wider audience.

The conceptual design document will:
- Outline and define constraints to ensure that it is functional, reliable, and affordable.
- Examine potential solutions, comparing them and determining the best approach to meet the project's goals.
- Present a high level solution, detailing the board's internal architecture as well as its operational flow.
- Specify the details of individual subsystems.
- Address the standards the project must adhere to, as well as ethical and professional specifications.


## Fully Formulated Problem

The primary objective of this project is to design and build a low-cost, accessible, and intelligent automated chess board that enhances the traditional over-the-board (OTB) chess experience by integrating online play, AI-based solo play, and voice command functionality. The system shall support physical gameplay while interfacing with online platforms and allow players with physical or visual disabilities to engage in independent play through voice control and automated piece movement.

The system shall be constructed using affordable and readily available components to ensure replicability by hobbyists. In doing so, the board shall bridge the gap between digital and physical chess play while improving accessibility and reducing cost barriers.

### Specifications

The chessboard will meet the following requirements to ensure reliability and operability:

1. Vocal Processing System: The system shall enable players to control gameplay using spoken commands. 

    - Microphone (Peripheral Input): The device shall capture vocal output from users and transmit it to the processing unit for analysis.
    - Processing Unit: The unit shall utilize Vosk to process and filter voice input with a minimum accuracy of 80%. It shall listen for input only while a designated button is pressed or after a command word is detected, recognize commands in algebraic chess notation and common variations (e.g., “Knight to e5,” “Bishop a4”), and process commands within 5 seconds of button release or the end of voice input.
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
- Electrical and Safety Constraints: To prevent electrical, thermal, and physical hazards during operation.
    - Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
    - Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
    - Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
    - Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  
- Accessibility and Ergonomic Constraints: To ensure usability for a wide range of users.
    - Shall conform to Section 508 of the Rehabilitation Act, ensuring accessible interfaces for users with disabilities.  
    - Shall follow ergonomic layout guidelines from ANSI/HFES 100-2007, ensuring proper control placement and feedback.  
    - Shall follow universal design principles to minimize cognitive and physical usability barriers.


## Comparative Analysis of Potential Solutions

In this section, various potential solutions are hypothesized, design considerations are discussed, and factors influencing the selection of a solution are outlined. The chosen solution is then identified with justifications for its selection.


## High-Level Solution

This section presents a comprehensive, high-level solution aimed at efficiently fulfilling all specified requirements and constraints. The solution is designed to maximize stakeholder goal attainment, adhere to established constraints, minimize risks, and optimize resource utilization. Please elaborate on how your design accomplishes these objectives.


### Hardware Block Diagram

Block diagrams are an excellent way to provide an overarching understanding of a system and the relationships among its individual components. Generally, block diagrams draw from visual modeling languages like the Universal Modeling Language (UML). Each block represents a subsystem, and each connection indicates a relationship between the connected blocks. Typically, the relationship in a system diagram denotes an input-output interaction.

In the block diagram, each subsystem should be depicted by a single block. For each block, there should be a brief explanation of its functional expectations and associated constraints. Similarly, each connection should have a concise description of the relationship it represents, including the nature of the connection (such as power, analog signal, serial communication, or wireless communication) and any relevant constraints.

The end result should present a comprehensive view of a well-defined system, delegating all atomic responsibilities necessary to accomplish the project scope to their respective subsystems.


### Operational Flow Chart

Similar to a block diagram, the flow chart aims to specify the system, but from the user's point of view rather than illustrating the arrangement of each subsystem. It outlines the steps a user needs to perform to use the device and the screens/interfaces they will encounter. A diagram should be drawn to represent this process. Each step should be represented in the diagram to visually depict the sequence of actions and corresponding screens/interfaces the user will encounter while using the device.

#### Key Features

1. Voice Controls
   - The microphone captures user commands upon a designated button press or voice command trigger.
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


## Atomic Subsystem Specifications

Based on the high-level design, provide a comprehensive description of the functions each subsection will perform.

Inclued a description of the interfaces between this subsystem and other subsystems:
- Give the type of signal (e.g. power, analog signal, serial communication, wireless communication, etc).
- Clearly define the direction of the signal (input or output).
- Document the communication protocols used.
- Specifying what data will be sent and what will be received.

Detail the operation of the subsystem:
- Illustrate the expected user interface, if applicable.
- Include functional flowcharts that capture the major sequential steps needed to achieve the desired functionalities.

For all subsystems, formulate detailed "shall" statements. Ensure these statements are comprehensive enough so that an engineer who is unfamiliar with your project can design the subsystem based on your specifications. Assume the role of the customer in this context to provide clear and precise requirements.


## Ethical, Professional, and Standards Considerations

In the project proposal, each team must evaluate the broader impacts of the project on culture, society, the environment, public health, public safety, and the economy. Additionally, teams must consider relevant standards organizations that will inform the design process. A comprehensive discussion should be included on how these considerations have influenced the design. This includes detailing constraints, specifications, and practices implemented as a result, and how these address the identified considerations.


## Resources

You have already estimated the resources needed to complete the solution. Now, let's refine those estimates.

### Budget

Develop a budget proposal with justifications for expenses associated with each subsystem. Note that the total of this budget proposal can also serve as a specification for each subsystem. After creating the budgets for individual subsystems, merge them to create a comprehensive budget for the entire solution.

### Division of Labor

First, conduct a thorough analysis of the skills currently available within the team, and then compare these skills to the specific requirements of each subsystem. Based on this analysis, appoint a team member to take the specifications for each subsystem and generate a corresponding solution (i.e. detailed design). If there are more team members than subsystems, consider further subdividing the solutions into smaller tasks or components, thereby allowing each team member the opportunity to design a subsystem.

### Timeline

Revise the detailed timeline (Gantt chart) you created in the project proposal. Ensure that the timeline is optimized for detailed design. Address critical unknowns early and determine if a prototype needs to be constructed before the final build to validate a subsystem. Additionally, if subsystem $A$ imposes constraints on subsystem $B$, generally, subsystem $A$ should be designed first.


## References

All sources utilized in the conceptual design that are not considered common knowledge must be properly cited. Multiple references should be included.


## Statement of Contributions

Each team member is required to make a meaningful contribution to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
