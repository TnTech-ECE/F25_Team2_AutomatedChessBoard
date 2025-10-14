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

The introduction is intended to reintroduce the fully formulated problem. 


## Restating the Fully Formulated Problem

The fully formulated problem is the overall objective and scope complete with the set of shall statements. This was part of the project proposal. However, it may be that the scope has changed. So, state the fully formulated problem in the introduction of the conceptual design and planning document. For each of the constraints, explain the origin of the constraint (customer specification, standards, ethical concern, broader implication concern, etc).


## Comparative Analysis of Potential Solutions

Automated chessboards have emerged as innovative tools for enhancing gameplay, integrating automation and dynamic AI opponents. Below, we analyze multiple existing solutions to determine their suitability for addressing the challenges of affordability, automated capabilities, and accessibility.

### Chess Piece Movement

_**Robotic Arm Manipulator System**_

The robotic arm manipulator system consists of a multi-jointed mechanical arm mounted above the chessboard, equipped with a claw or gripper to pick up and move chess pieces between positions. Controlled by servo or stepper motors, this approach mimics human motion, offering precise vertical and horizontal control for piece manipulation.

  * _Pros:_
  
    * Provides full 3D control and can directly lift pieces instead of sliding them.
    
    * Capable of handling a wide range of object shapes and sizes with a properly designed gripper.
    
    * Visually engaging and intuitive to observers due to its human-like movement.
    
    * Modular and programmable for other potential tasks or demonstrations.

  * _Cons:_
    
    * Mechanically complex with multiple degrees of freedom requiring advanced kinematic control.
    
    * Requires precise calibration to avoid collisions with other pieces or the board.
    
    * Considerably slower than planar motion systems.
    
    * Bulky structure obstructs the player's view.
    
    * Increased cost and mechanical wear due to multiple servos or stepper motors.
    
    * Noise and vibration from multiple moving joints can degrade precision.
    
    * Requires a robust frame or enclosure to maintain stability and alignment.

_**Individual Micro-Robot System**_

This system places a small, self-contained micro-robot beneath each chess piece. Each robot can move independently under the board, guided by sensors or wireless communication, to reposition its corresponding piece as commanded. This concept is similar to systems used in high-end commercial robotic chessboards (such as the Chessnut Move[1]).

  * _Pros:_
  
    * Allows completely independent movement of each chess piece.
    
    * Eliminates the need for moving gantries, belts, or overhead mechanisms.
    
    * Offers smooth and realistic piece motion directly from below the board.

  * _Cons:_
    
    * Extremely expensive and complex to implement, requiring many individual actuators.
    
    * Difficult to synchronize multiple robots for coordinated movement.
    
    * Maintenance is cumbersome: each unit must be powered, calibrated, and serviced individually.
    
    * Requires precise alignment with chessboard grid and consistent magnetic coupling.
    
    * Limited battery life and power management challenges under a closed board.
    
    * Communication interference or loss can result in desynchronized or failed moves.

_**CoreXY Motion System**_

The CoreXY motion system uses two stepper motors connected through a pair of pulley and belt assemblies to enable precise, planar motion along the X and Y axes. A magnet is mounted to the movable head, allowing the system to position and actuate magnetic pieces from below the chessboard. This design provides a compact, fast, and mechanically efficient method for two-dimensional positioning, without requiring independent motorized axes.
  
  * _Pros:_
  
    * Provides high-speed, precise planar movement using only two motors.
    
    * Lightweight and mechanically efficient due to stationary motors and crossed belt layout.
    
    * Compatible with a wide range of stepper drivers.
    
    * Smooth, coordinated motion reduces mechanical vibration and improves accuracy.
  
  * _Cons:_
    
    * Requires careful calibration to prevent skewed or uneven motion.
    
    * Mechanical backlash or belt stretch can reduce repeatability over time.
    
    * Limited Z-axis functionality unless supplemented by another mechanism.
    
    * Performance depends on magnet strength and carriage rigidity for consistent actuation.


**Evaluation and Selection**

When evaluating the three systems, several key factors were considered: mechanical complexity, cost, precision, scalability, and ease of maintenance. The robotic arm, while versatile, introduces high mechanical complexity, slower operation speeds, and increased cost due to multiple motors and linkages. The micro-robot system provides independent piece control but is prohibitively expensive, difficult to synchronize, and challenging to maintain.

The CoreXY motion system was determined to be the most balanced and practical approach. Its two-motor planar configuration minimizes mechanical components while maximizing precision and speed. It integrates smoothly with magnetic actuation methods, provides consistent and predictable motion, and offers an excellent trade-off between performance and design simplicity.


### Processing and Control Subsystem

_**Centralized Processing Unit**_

In this setup, a single embedded processor (such as a Raspberry Pi) handles all major system functions, including speech recognition, chess logic, and motion control. The processor directly interfaces with motor driver boards, eliminating the need for a secondary control unit. This approach simplifies wiring and reduces communication overhead between devices, but places greater computational and timing demands on the processor.

  * _Pros:_
  
    * Simplified system architecture with fewer components and communication links.
    
    * Reduced latency and failure points, since all logic resides on one board.
    
    * Compact, space-efficient design requiring minimal wiring.
    
    * Suitable for small-scale prototypes or cost-sensitive builds.
  
  * _Cons:_
    
    * The single processor is not optimized for precise real-time control, potentially introducing motor timing inconsistencies.
    
    * Processor overload may occur when running several chess management programs and motion control tasks simultaneously.
    
    * A single hardware failure halts all system functionality.
    
    * Difficult to scale or maintain if additional sensors or actuators are later added.

_**Cloud-Assisted or Network-Based Processing**_

In this configuration, the chessboard’s hardware handles only low-level control, while cloud or networked servers perform computationally heavy tasks such as speech recognition and chess AI. The local system sends input data (like voice or board state) to remote services, which return processed results. This approach leverages powerful external resources, but introduces significant dependency on network availability.

  * _Pros:_
  
    * Reduces on-board processing requirements, enabling smaller and lower-power hardware.
    
    * Allows use of advanced AI models beyond embedded capabilities.
    
    * Simplifies software maintenance through centralized, remotely updatable systems.
  
  * _Cons:_
    
    * Requires continuous internet connectivity, meaning the system is non-functional offline.
    
    * Introduces latency that can affect responsiveness in move execution and voice feedback.
    
    * Raises data security and privacy concerns.
    
    * Dependent on third-party APIs or services that may change or become unavailable.
    
    * Reduces autonomy and portability, making it unsuitable for standalone operation.

_**Distributed Processing and Control System**_

This architecture separates high-level processing from real-time motor control. A Raspberry Pi acts as the main processing unit, running the voice recognition and chess piece tracking programs. It communicates with a dedicated Arduino control unit, which manages the CoreXY stepper motors through two motor driver boards. The Arduino executes time-critical control loops for precise movement, while the Raspberry Pi handles strategic computation and user interaction.

  * _Pros:_
  
    * Divides workload between two optimized processors, improving performance and reliability.
    
    * Provides smooth, accurate motion via the Arduino’s real-time control capabilities.
    
    * Enhances modularity, wherer each subsystem can be tested, replaced, or upgraded independently.
    
    * Allows the Raspberry Pi to focus on higher-level logic and communication, without timing interruptions.
    
    * Supports future expansion with minimal redesign.
  
  * _Cons:_
    
    * Requires careful synchronization between Pi and Arduino via serial or I²C communication.
    
    * Slightly higher cost and wiring complexity.
    
    * Debugging inter-device communication can be more challenging.
    
    * Adds a small latency overhead in transmitting commands between processors.


**Evaluation and Selection**

For this project, we prioritized reliable offline performance, precise motion control, and efficient processing distribution. The centralized processing system, while simple, risks performance bottlenecks when running both AI and motor control on one processor, and a single failure would disable the entire board. The cloud-assisted approach, although powerful, depends on constant internet connectivity and introduces latency, making it unreliable for real-time, portable use.

The Distributed Processing and Control System offers the best balance between responsiveness, modularity, and performance. By assigning real-time motion control to the Arduino and high-level processing to the Raspberry Pi, the system maintains smooth CoreXY operation (while supporting advanced features like voice recognition and chess logic). This design ensures scalability, reliability, and consistent offline operation, meeting all project goals effectively.


### Power System

_**Corded Power System**_

The corded power configuration supplies energy directly from a wall outlet through a DC power adapter, providing continuous and stable voltage to all internal components. This setup eliminates the need for internal energy storage and simplifies circuit design, relying entirely on an external power connection for operation.

  * _Pros:_
  
    * Provides stable, uninterrupted power during operation.
    
    * Simplifies internal circuitry, with no need for charging or battery management systems.
    
    * Reduces weight by eliminating onboard batteries.
    
    * Inexpensive and straightforward to implement.
  
  * _Cons:_
    
    * Requires a constant connection to a wall outlet, limiting portability.
    
    * Operation is impossible without external power.
    
    * Increases cable clutter and reduces design aesthetics.
    
    * Potential tripping or cable strain hazards in user environments.
    
    * Less appealing for demonstration or mobile use cases due to lack of autonomy.

_**Wireless Inductive Power System**_

A wireless inductive power setup transfers energy through magnetic coupling between a transmitter coil (in a base station) and a receiver coil integrated into the chessboard. This provides a cable-free appearance and continuous power when the board is positioned on its charging pad.

  * _Pros:_
  
    * Provides a modern, cable-free aesthetic for clean presentation.
    
    * Reduces wear on connectors from frequent plugging and unplugging.
    
    * Safe, low-voltage energy transfer suitable for consumer environments.
  
  * _Cons:_
    
    * Significantly lower power transfer efficiency.
    
    * Requires precise alignment between coils for consistent operation.
    
    * Limited power output, unsuitable for high-current loads like motors or magnets.
    
    * Increased system cost and design complexity.
    
    * Inefficient for continuous or high-load use, especially with moving actuators.
    
    * Thermal buildup during long operation could reduce component lifespan.
   
 _**Hybrid Power System**_

The hybrid power system integrates a rechargeable battery pack with an AC adapter and power management circuitry. This configuration allows the chessboard to operate from wall power while simultaneously charging the batteries, and to continue functioning seamlessly on battery power when unplugged. It ensures both reliability and portability, making it ideal for extended demonstrations or classroom use.

  * _Pros:_
  
    * Enables uninterrupted operation whether plugged in or running on battery power.
    
    * Provides portability without sacrificing power availability.
    
    * Extends battery life through managed charging cycles and pass-through power.
    
    * Offers redundancy, where if one power source fails, the other maintains functionality.
    
    * Clean, professional design with minimal cable dependency.
    
  * _Cons:_
    
    * Slightly higher cost due to the inclusion of power management circuitry.
    
    * Requires careful design to balance charging and discharge loads.
    
    * Batteries will eventually require replacement after several hundred charge cycles.
    
    * Slightly heavier than a purely corded design.


**Evaluation and Selection**

When comparing the three power configurations, the hybrid system clearly offers the best balance of reliability, mobility, and functionality. The corded design, while simple and inexpensive, limits the system’s usability by requiring a constant power connection. The wireless inductive setup, although sleek, introduces inefficiency and insufficient power transfer for motor-driven systems.

The Hybrid Power System was therefore selected as the most practical and flexible option. It provides uninterrupted operation whether plugged in or on battery power, supports demonstrations and transportability, and ensures a professional, user-friendly design well-suited for the automated chessboard.

## High-Level Solution

This section presents a comprehensive, high-level solution aimed at efficiently fulfilling all specified requirements and constraints. The solution is designed to maximize stakeholder goal attainment, adhere to established constraints, minimize risks, and optimize resource utilization. Please elaborate on how your design accomplishes these objectives.


### Hardware Block Diagram

Block diagrams are an excellent way to provide an overarching understanding of a system and the relationships among its individual components. Generally, block diagrams draw from visual modeling languages like the Universal Modeling Language (UML). Each block represents a subsystem, and each connection indicates a relationship between the connected blocks. Typically, the relationship in a system diagram denotes an input-output interaction.

In the block diagram, each subsystem should be depicted by a single block. For each block, there should be a brief explanation of its functional expectations and associated constraints. Similarly, each connection should have a concise description of the relationship it represents, including the nature of the connection (such as power, analog signal, serial communication, or wireless communication) and any relevant constraints.

The end result should present a comprehensive view of a well-defined system, delegating all atomic responsibilities necessary to accomplish the project scope to their respective subsystems.


### Operational Flow Chart

Similar to a block diagram, the flow chart aims to specify the system, but from the user's point of view rather than illustrating the arrangement of each subsystem. It outlines the steps a user needs to perform to use the device and the screens/interfaces they will encounter. A diagram should be drawn to represent this process. Each step should be represented in the diagram to visually depict the sequence of actions and corresponding screens/interfaces the user will encounter while using the device.


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

[1] Chessnutech. (n.d.). Chessnut move - advanced robotic chessboard with Plastic Pieces. Chessnut. https://www.chessnutech.com/products/chessnut-move-advanced-robotic-chessboard-with-plastic-pieces



## Statement of Contributions

Each team member is required to make a meaningful contribution to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
