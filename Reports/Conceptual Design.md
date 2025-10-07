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

Automated chessboards have emerged as innovative tools for enhancing gameplay, integrating automation and dynamic AI opponents. Current solutions range from DIY implementations to commercially-available smart boards, each offering unique advantages and drawbacks. Below, we analyze multiple existing solutions to determine their suitability for addressing the challenges of affordability, automated capabilities, and accessibility.

**DIY Solutions**

....

Advantages:

* ....
* ....
* ....

**Commercial Solutions**

Commercial smart chessboards provide refined integrations of automation, AI, and connectivity but often come at a premium cost and complexity level. Below is the analysis of several existing options:

1. **ChessUp 2 Smart Chess Board**

   * Cost: $399.99
 
   * Pros: Provides piece placement tracking, piece movement lights, and an adjustable AI skill level
 
   * Cons:
 
     * Cannot move pieces autonomously.
     * Requires a stable WiFi connection to Chess.com for AI functionality.
   
2. **Miko Chess Grand**

  * Cost: $549.00
  
  * Pros: Offers online connectivity, an automatic board reset, and an adaptive AI.

  * Cons:
 
   * The board’s weight makes it less portable.
   * High-quality materials increase overall cost.
   * The robotic arm cannot make moves for the first player except when removing pieces from the board.
   * Does not include voice recognition functionality.

3. **Chessnut Move**

   * Cost: $899.00
 
   * Pros: Offers unique micro-robotics piece movement, precise piece tracking, and simulataneous piece movement.
 
   * Cons:
 
     * Pieces occasionally collide during automated movement.
     * The design relies on each piece containing its own robotic base, which significantly increases cost.
     * Oversized piece bases reduce aesthetic appeal and make the board feel crowded.

4. **GoChess Mini**

   * Cost: $299.95
 
   * Pros: Compact, lightweight, and simple to set up
 
   * Cons:
 
     * Battery-powered system requires two hours to fully charge, supporting up to 100 hours of playtime (reduced to about five hours when lights are enabled).
     * Does not support automated piece movement, requiring players to manually move all pieces.
     * Lacks an automated reset function for returning pieces to their starting positions.

**Analysis and Selection**

Current solutions often remain too costly or inaccessible for the average user. In addition, many systems lack essential capabilities such as offline functionality, voice recognition, and reliable automated piece movement, leading to frequent piece collisions and reduced usability.

After assessing the strengths and limitations of existing systems, it is evident that a new solution must address the following shortcomings:

1. __CHECK MEASURES OF SUCCESS(?)__
2. ...
3. ...
4. ...
5. ...

By integrating these features into a single cohesive system, the proposed design aims to bridge the gap between DIY and commercial smart chessboards, delivering a cost-effective, lightweight, and user-friendly solution that enhances accessibility and functionality for disabled chess players.

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

[1] Adafruit Industries. (n.d.). Stepper motor - NEMA-17 size - 200 steps/rev, 12V 350mA. https://www.adafruit.com/product/324

[2] Amazon.com: ELEGOO UNO R3 Board ATmega328P with USB Cable(Arduino-Compatible) for Arduino : Electronics. (n.d.). https://www.amazon.com/ELEGOO-Board-ATmega328P-ATMEGA16U2-Compliant/dp/B01EWOE0UU

[3] Amazon.com: NowTH USB Microphone Lavalier Lapel Clip on Mic With 6.56ft Cable for Laptop, Computer, PC, Streaming Conferencing,Interviews, Online Singing, Skype, MSN, Audio Video Recording : Electronics, n.d.

[4] Chessnutech. (n.d.). Chessnut move - advanced robotic chessboard with Plastic Pieces. Chessnut. https://www.chessnutech.com/products/chessnut-move-advanced-robotic-chessboard-with-plastic-pieces

[5] ChessUp 2 Smart Chess Board. Bryght Labs. (n.d.). https://playchessup.com/products/chessup-2

[6] D. M. D. Iliescu, "The Impact of Artificial Intelligence on the Chess World," JMIR Serious Games, vol. 8, no. 4, p. e24049, Dec. 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7759436/.

[7] Davis, E. (2023, November 12). The Rise of Board Game Cafes: Socializing through Analog Entertainment. Medium. https://ethan-davis.medium.com/the-rise-of-board-game-cafes-socializing-through-analog-entertainment-51857183f856

[8] GoChess Mini. Particula. (n.d.). https://particula-tech.com/products/gochess-mini?variant=45806634402040&country=US&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOooAY445sOW--M7GA0T4jbNkHE609yl_YKlFLR9iyhF7eX9KFsd9ubc

[9] Instructables. (2019, September 13). CoreXY CNC Plotter. Instructables. https://www.instructables.com/CoreXY-CNC-Plotter/

[10] MFOSSociety. (n.d.). MFOSSociety/8-8: 8/8: Smart Chess Board: An Automated Ai Chess Board. GitHub. https://github.com/MFOSSociety/8-8

[11] Miko Chess Grand. Miko. (n.d.). https://miko.ai/pages/miko-chess-grand

[12] PiShop. (n.d.). Raspberry Pi 4 Model B/4GB. PiShop.us. https://www.pishop.us/product/raspberry-pi-4-model-b-4gb/

[13] R. Lahood, "The Queen’s Gambit, the Chess Boom, and the Future of Chess," Michigan Journal of Economics, Apr. 5, 2021. https://sites.lsa.umich.edu/mje/2021/04/05/the-queens-gambit-the-chess-boom-and-the-future-of-chess/.

[14] Simarmehta. (n.d.). Simarmehta/CHESSAUTOMATION_CV. GitHub. https://github.com/simarmehta/chessAutomation_CV

[15] Stockfish. (n.d.). Stockfish. https://stockfishchess.org/

[16] sumit11899. (n.d.). SUMIT11899/automated-chessboard. GitHub. https://github.com/sumit11899/Automated-ChessBoard

[17] US Chess, "US Chess Guidelines for Accessible Chess Events," Apr. 2020. https://new.uschess.org/sites/default/files/wp-thumbnails/2020/04/Accessibility-Guidelines-April-2020.pdf.

[18] VOSK Offline Speech Recognition API. (n.d.). VOSK Offline Speech Recognition API. https://alphacephei.com/vosk/


## Statement of Contributions

Each team member is required to make a meaningful contribution to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
