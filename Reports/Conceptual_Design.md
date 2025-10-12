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

### Stepper Driver Boards

**Big Easy Driver** [1]

  _Price:_ ~$22
  
  * _Pros:_
  
    * Based on the common A4988 architecture with extensive community resources.
  
    * Simple STEP/DIR interface requires minimal setup.
  
    * Drives most NEMA 17 motors comfortably (up to ~1.7 A/phase).
  
    * Simplifies power wiring by providing onboard 5 V logic.
  
  * _Cons:_
  
    * Produces audible hum or whine due to older A4988 microstepping.
  
    * Only up to 16× microstepping, resulting in less smooth motion.
  
    * Requires heatsinking near 2A current draw.
  
    * Lacks stall detection, UART control, or current auto-tuning.
  
    * May underperform with heavier loads or larger motors.


**TMC2209 Stepper Driver** [2]

  _Price:_ ~$7
  
  * _Pros:_
  
    * Extremely quiet operation using StealthChop technology.
    
    * Supports up to 1/256 microstepping.
    
    * Handles up to 2.0A RMS (≈2.8A peak) with proper cooling, suitable for most NEMA 17 motors.
    
    * Includes UART communication for advanced tuning, diagnostics, and stall detection.
    
    * Compatible with both 3.3 V and 5 V logic.
  
  * _Cons:_
  
    * Slightly more complex setup when using UART or advanced features.
    
    * Requires adequate heat dissipation at higher currents to maintain stability.
    
    * More sensitive to wiring and grounding issues.
    
    * Overkill for basic motion control applications.
    
    * Some breakout boards lack onboard cooling or jumpers, requiring careful configuration.

### Stepper Motors

**StepperOnline NEMA 17 59N·cm 2A** [3]

  _Price:_ ~$10 


  * _Pros:_

    * Strong holding torque (59N·cm) gives good margin for movement and overcoming friction. 

    * Rated 2A per phase, well within the capability of both Big Easy (with cooling) and TMC2209 stepper drivers.

    * Plenty of community references and public data.

  * _Cons:_

    * Moderate power draw and heat generation, especially under load (requires good cooling).
    
    * At high speeds, inductance may limit torque delivery (requires thorough testing).
    
    * More mass/inertia than a weaker motor (may require more careful tuning of acceleration and jerk).
   

**StepperOnline NEMA 17 0.9° 2A** [4]

  _Price:_ ~$11

  * _Pros:_

    * Higher angular resolution (0.9° per step) gives finer positional control (twice the steps of a typical 1.8° motor).
    
    * 2A current rating is a good match for either driver, giving torque and flexibility.
    
    * Good choice for more precision in aligning the magnectic CoreXY attachment.

  * _Cons:_

    * Control pulses must be more frequent (higher step rate demands).
    
    * More sensitive to microstepping errors or driver jitter.
    
    * Slightly lower torque per step vs a 1.8° motor with same current (though overall torque is same if properly driven).


**StepperOnline E‑Series NEMA 17 60N·cm 2.1A** [5]

  _Price:_ ~$9

  * _Pros:_

    * Strong torque (60N·cm) offers good overhead for higher friction or heavier carriage.
    
    * Slightly higher current rating (2.1A) gives margin in design.
    
    * Economical price for a robust motor.

  * _Cons:_

    * At 2.1 A, it may push the thermal limits of simpler drivers (Big Easy especially) unless well cooled.
    
    * Heavier and more inert — slower acceleration or more stress on belts.
    
    * More demanding in driver tuning (current limiting, microsteps) to avoid overshoot or resonance.


### Magnets

**MagPop 10 Switchable Magnet** [6]

  _Price:_ ~$30

  * _Pros:_

    * Compact and lightweight design (~32g, footprint only 11mm × 15mm), ideal for small mechanisms like CoreXY.
    
    * True mechanical on/off switching.
    
    * Provides up to 10lb (4.5kg) of holding force.
    
    * Precise, low-profile form factor simplifies mounting and integration.
    
    * Manufactured by a reputable company (Magswitch), with detailed specifications and support.

  * _Cons:_

    * Requires a manual switch motion to toggle on/off (would need a servo or linkage for remote actuation).
    
    * Must have direct contact with steel for maximum holding performance; air gaps or thick board layers reduce strength.
    
    * Limited holding force compared to larger magnetic bases.
    
    * Mechanical switch may wear over long-term repeated cycles.
    
    * More expensive per-unit compared to similarly sized permanent or electromagnets.
  

**EM100-12-122 Round Electromagnet** [7]

  _Price:_ ~$28

  * _Pros:_

    * 1 inch diameter and compact design.
    
    * Holding force: 19 lbs when in direct contact with steel.
    
    * Operates at 4W. 
    
    * Includes through-hole mounting (with shoulder bolt) for mechanical attachment.

    * Quick-release design ensures the magnet disengages rapidly when power is cut.

  * _Cons:_

    * Power required is continuous while holding.
    
    * Height (~0.78") is relatively thick; may require substantial vertical clearance in carriage design.
    
    * Weight not specified by the vendor, so will need to be estimated or requested (will add carriage inertia).
    
    * Holding force is ideal under perfect steel contact, but any air gap (wood board + shim) will reduce effective pull.
    
    * Thermal considerations: prolonged current may lead to heating, so cooling or duty cycling may be required.

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

[1] "Big Easy Driver," Sparkfun.com, 2023. https://www.sparkfun.com/big-easy-driver.html

[2] "BIGTREETECH TMC2209 V1.3 Stepper Motor Driver," Biqu Equipment, 2022. https://biqu.equipment/products/bigtreetech-tmc2209-stepper-motor-driver-for-3d-printer-board-vs-tmc2208

[3] "Nema 17 Bipolar 59Ncm (84oz.in) 2A 42x48mm 4 Wires w/ 1m Cable & Connector," www.omc-stepperonline.com. https://www.omc-stepperonline.com/nema-17-bipolar-59ncm-84oz-in-2a-42x48mm-4-wires-w-1m-cable-connector-17hs19-2004s1

[4] "Nema 17 Bipolar 0.9deg 46Ncm(65.1oz.in) 2A 42x42x48mm 4 Wires - 17HM19-2004S | StepperOnline," Omc-stepperonline.com, 2024. https://www.omc-stepperonline.com/nema-17-bipolar-0-9deg-46ncm-65-1oz-in-2a-2-9v-42x42x48mm-4-wires-17hm19-2004s

[5] "E Series Nema 17 Stepper Motor 1.8deg 60Ncm(84.97oz.in) 2.1A 42x42x60mm 4 Wires - 17HE24-2104S | StepperOnline," Omc-stepperonline.com, 2024. https://www.omc-stepperonline.com/e-series-nema-17-stepper-motor-1-8deg-60ncm-84-97oz-in-2-1a-42x42x60mm-4-wires-17he24-2104s

[6] "MagPop 10 Switchable Magnet (2 pack) - 81001561-2," Magswitch Technologies, 2025. https://magswitch.com/products/magpop-10-switchable-magnet-81001561?srsltid=AfmBOoqucE-6aWsplzoEZwuSVC073VE7-7Ts_mIalXZBY2dR0Sdcex_f

[7] "EM100-12-122 - Round Electromagnet 1 inch Dia. 12 volts DC - Holding 19 lbs. - APW Company," APW Company, Sep. 29, 2025. https://apwcompany.com/em100-12-122/



## Statement of Contributions

Each team member is required to make a meaningful contribution to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
