# Project Proposal

This document provides a comprehensive explanation of what a project proposal should encompass. The content here is detailed and is intended to highlight the guiding principles rather than merely listing expectations. The sections that follow contain all the necessary information to understand the requirements for creating a project proposal.


## General Requirements for the Document
- All submissions must be composed in markdown format.
- All sources must be cited unless the information is common knowledge for the target audience.
- The document must be written in third person.
- The document must identify all stakeholders including the instuctor, supervisor, and customer.
- The problem must be clearly defined using "shall" statements.
- Existing solutions or technologies that enable novel solutions must be identified.
- Success criteria must be explicitly stated.
- An estimate of required skills, costs, and time to implement the solution must be provided.
- The document must explain how the customer will benefit from the solution.
- Broader implications, including ethical considerations and responsibilities as engineers, must be explored.
- A list of references must be included.
- A statement detailing the contributions of each team member must be provided.


## Introduction

The introduction must be the opening section of the proposal. It acts as the "elevator pitch" of the project, briefly introducing the objective, its importance, and the proposed solution. Because readers may only read this section, it should effectively capture their attention and encourage them to read further.

Toward the end of the introduction, include a subsection that outlines what the proposal will cover. This helps set reader expectations for the ensuing sections.


## Formulating the Problem

Formulating the problem or objective involves clearly defining it through background information, specifications, and constraints. Think of it as "fencing in" the objective to make it unambiguously clear what is and is not being addressed and why.

Questions to consider:
- Who does the problem affect (i.e. who is your customer)?
- Why do we need this solution?
- What challenges necessitate a dedicated, multi-person engineering team?
- Why aren’t off-the-shelf solutions sufficient?

### Background

Provide context and details necessary to define the problem clearly and delineate its boundaries.

### Specifications and Constraints

Specifications and constraints define the system's requirements. They can be positive (do this) or negative (don't do that). They can be mandatory (shall or must) or optional (may). They can cover performance, accuracy, interfaces, or limitations. Regardless of their origin, they must be unambiguous and impose measurable requirements.

#### Specifications

Specifications are requirements imposed by **stakeholders** to meet their needs. If a specification seems unattainable, it is necessary to discuss and negotiate with the stakeholders.

#### Constraints

Constraints often stem from governing bodies, standards organizations, and broader considerations beyond the requirements set by stakeholders.

Questions to consider:
- Do governing bodies regulate the solution in any way?
- Are there industrial standards that need to be considered and followed?
- What impact will the engineering, manufacturing, or final product have on public health, safety, and welfare?
- Are there global, cultural, social, environmental, or economic factors that must be considered?


## Survey of Existing Solutions

Research existing solutions, whether in literature, on the market, or within the industry. Present these findings in a coherent, organized manner. Remember to cite all information that is not common knowledge.

DIY Solutions: Our GitHub search revealed several repositories with designs of varying complexity. Some use stepper motors and Arduinos to control piece movement, while others employ Raspberry Pis and computer vision to track pieces and issue precise directions via microcontrollers.

Below are selected repositories with pros, cons, and key features, highlighting their feasibility for our project.

8/8: Smart Chess Board [1]

Features:
- Uses a mechanism which will let the piece move at any given point on the board that is consistent with the motion a 3D printer makes while printing.
-	Uses two lead screw mechanism to make movements in the XY direction.
-	Moves the chess pieces with the electromagnetic head, utilizing pieces with magnetic bottoms.
-	Controlled using a Raspberry Pi.
-	Showcases stepper motors as the drivers.

Pros: 
-	Has a method for Collision Avoidance.

Cons: 
-	Project has experience notable failures with the stepper motor design.
-	Incomplete BOM


Techievince 8.0, Electronics Club IITG Project [2]

Features
-	Highlights of the technology used were Arduino, Embedded C and for AI Micro Max chess program is used based on Minimax and Alpha-Beta algorithms.
-	Utilizes Stepper motors on a XY trolley system with magnetized pieces and a electromagnet head used to move the pieces.
-	Uses a magnetic sensor, Reed Switch, to determine the displacement of the chess piece.
-	Multiplexers are used to connect the 64 sensors to arduino.

Pros
-	Complete BOM
-	README thoroughly documents the team's thought process and specifics for each piece of the project.

Cons
-	 No obvious Cons


Chess Automation Using Computer Vision [3]

Features
-	Leverages Computer Vision (CV) techniques to automate chessboard detection and piece tracking in real-time.
-	Tracks the Game using a camera, identifies the piece(s) and the positions on the board, and determines the game moves.
-	Uses OpenCV and Numpy to process images or video feeds of a chessboard. 
-	Has a Game History Log.	

Pros
-	Includes a step-by-step Installation process.
-	Has a project structure.

Cons
- No obvious Cons


Industrial Solutions: ...............

## Measures of Success

Define how the project’s success will be measured. This involves explaining the experiments and methodologies to verify that the system meets its specifications and constraints.


## Resources

Each project proposal must include a comprehensive description of the necessary resources.

### Budget

Provide a budget proposal with justifications for expenses such as software, equipment, components, testing machinery, and prototyping costs. This should be an estimate, not a detailed bill of materials.

### Personel

Identify the skills present in the team and compare them to those required to complete the project. Address any skill gaps with a plan to acquire the necessary knowledge.

Besides the team, also state who you choose to be you supervisor and why.

State who your instrucotr is and what role you expect them to play in the project.

### Timeline

Provide a detailed timeline, including all major deadlines and tasks. This should be illustrated with a professional Gantt chart.


## Specific Implications

Explain the implications of solving the problem for the customer. After reading this section, the reader should understand the tangible benefits and the worthiness of the proposed work.


## Broader Implications, Ethics, and Responsibility as Engineers

Consider the project’s broader impacts in global, economic, environmental, and societal contexts. Identify potential negative impacts and propose mitigation strategies. Detail the ethical considerations and responsibilities each team member bears as an engineer.


## References

All sources used in the project proposal that are not common knowledge must be cited. Multiple references are required.

[1] https://github.com/MFOSSociety/8-8
[2] https://github.com/sumit11899/Automated-ChessBoard
[3] https://github.com/simarmehta/chessAutomation_CV

## Statement of Contributions

Each team member must contribute meaningfully to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
