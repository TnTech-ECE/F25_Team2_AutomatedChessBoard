
# Detailed Design for Processing Unit

This document delineates the objectives of a comprehensive system design. Upon reviewing this design, the reader should have a clear understanding of:

- How the specific subsystem integrates within the broader solution
- The constraints and specifications relevant to the subsystem
- The rationale behind each crucial design decision
- The procedure for constructing the solution


## General Requirements for the Document

The document should include:

- Explanation of the subsystem’s integration within the overall solution
- Detailed specifications and constraints specific to the subsystem
- Synopsis of the suggested solution
- Interfaces to other subsystems
- A buildable diagram*
- An operational flowchart*
- A comprehensive Bill of Materials (BOM)
- Analysis of crucial design decisions

*Note: These technical documentation elements are mandatory only when relevant to the particular subsystem.

---

## Function of the Subsystem

The **Processing Unit (PU)** functions as the central intelligence of the automated chessboard system, responsible for interpreting user input, executing game logic, and coordinating communication between all major subsystems. Implemented on a **Raspberry Pi**, the PU bridges human interaction and system control, translating spoken commands into actionable instructions and managing the overall flow of gameplay.

Upon startup, the PU initializes all critical software components, including the **Vosk speech recognition engine** and the **Stockfish chess engine**, as well as the communication interfaces used to interact with peripheral devices. The PU receives voice input from a USB connected microphone, leveraging Vosk to convert speech into text based commands. These commands are then analyzed and validated by Stockfish to ensure compliance with chess rules before any move execution occurs.

Once a move has been deemed valid, the PU transmits the corresponding instruction to the **Control Unit (CU)** over a **USART** or **I²C** connection, initiating the physical relocation of pieces on the board. In parallel, the PU updates the **display interface** (connected via **I²C** or **SPI**) to provide real-time feedback to the user, including board state, game status, and system notifications.

Throughout gameplay, the PU maintains the internal representation of the chessboard, tracks both player and AI turns, and manages synchronization between speech input, motion execution, and display updates. Acting as the coordination hub of the system, the Processing Unit ensures that all subsystems operate harmoniously, maintaining a seamless and interactive chess experience from command recognition to move completion.

---

## Specifications and Constraints

The **Processing Unit (PU)** shall act as the system’s central controller, implemented on a **Raspberry Pi**, and shall perform speech recognition, board-state management, move validation, and peripheral communication. The PU shall accept voice input from a USB microphone, interpret commands with the Vosk engine, validate moves using the Stockfish engine, forward validated commands to the Control Unit (Arduino) by a serial protocol (USART or I²C), and update the display with real-time feedback. All design decisions and operational limits shall comply with applicable U.S. electrical, safety, accessibility, and consumer product standards.

---

### Performance Specifications

* **Voice capture & processing:** The PU shall accept vocal input from the USB microphone and process it using **Vosk**. The PU shall only listen after a configured wake word is detected (to protect privacy and reduce false captures).
* **Recognition accuracy & notation support:** The on-device speech recognition pipeline shall achieve a **minimum accuracy of 80%** for command recognition in typical indoor acoustic conditions, and it shall recognize algebraic chess notation and common natural-language variants (e.g., “Knight to e5”, “Bishop a4”). 
* **Processing latency:** Recognized commands shall be processed and a validated move determined **within 5 seconds** of button release or the end of voice input.
* **Display responsiveness & legibility:** Move confirmations, illegal-move alerts, and game-status updates produced by the PU shall appear on the display **within 1 second** of command processing. Displayed characters shall be **≥ 10 pt** and support high-contrast text/graphics for visibility under standard indoor lighting.
* **Inter-subsystem communication:** The PU shall transmit validated move commands to the Control Unit via **USART or I²C**, using signal rates and framing that ensure reliable transfer and deterministic command execution (protocol selection shall ensure electrical and timing compatibility with the receiving Arduino).

---

### Electrical and Signal Standards Compliance

* **EMI / Emissions:** The Processing Unit shall comply with **FCC Part 15 Subpart B (Class B)** limits for conducted and radiated emissions (conducted: ~0.15–30 MHz at 66–56 dBµV decreasing with frequency; radiated: ~30–1000 MHz at 40–54 dBµV/m at 3 m) to avoid interference with consumer electronics. [1]
* **Low-voltage operation:** The PU shall operate below **50 V DC** in accordance with UL low-voltage safety thresholds. Voltage choices and wiring practices shall avoid requirements for high-voltage insulation. [2]
* **Wiring & circuit practice:** The PU’s wiring and low-voltage circuits shall follow **NEC / NFPA 70** guidance (Article 725 where applicable), providing protection against overcurrent, correct conductor sizing, and insulation rated for the circuit’s voltage. [3]
* **Materials & consumer safety:** Components and assemblies used by the PU shall avoid materials and configurations that violate **CPSC** guidance and shall use parts with documented compliance where required. [4]
* **Cabling & connectors:** All cord sets, flexible cables, and connectors serving the PU shall meet **NEC Article 400** requirements for insulation, temperature rating, minimum bend radius, grounding continuity, and secure routing to avoid mechanical damage or tripping hazards. [8]
* **Grounding & protection:** Grounding, bonding, and circuit-level protections for the PU shall follow **OSHA 29 CFR 1910 Subpart S** to minimize electric-shock hazards; exposed conductive parts shall be appropriately bonded and protected. [9]
* **Safety labeling:** User-facing enclosures, ports, and power interfaces associated with the PU shall carry **ANSI Z535.4**-compliant safety labels where hazards exist (power indicators, service access, etc.). [10]

---

### Environmental and Safety Constraints

* **Surface temperature:** External surfaces of PU enclosures shall remain ≤ **104 °F (40 °C)** during continuous operation to prevent burns or material degradation, consistent with **UL 94** flammability guidance and **CPSC 16 CFR 1505.7** thermal limits. [6][7]
* **Operating environment:** The PU shall be rated for typical indoor educational/desktop environments (ambient **0–40 °C / 32–104 °F** and non-condensing humidity ranges typical for consumer electronics) so that the Raspberry Pi and attached peripherals operate reliably.
* **Mechanical routing & strain relief:** Cabling for the microphone, display, and interconnects shall be routed and secured to avoid pinch points, sharp edges, and accidental disconnection. Cable management shall preserve minimum bend radii and use strain reliefs where appropriate per NEC guidance. [8][6]
* **Component selection & enclosures:** Enclosure materials and construction shall meet consumer product safety expectations (no sharp edges, secure fastenings), and service access shall minimize risk of accidental contact with live circuitry.

---

### Ethical, Accessibility, and Socio-Economic Considerations

* **Privacy by design:** The PU shall prioritize **on-device** processing of voice input so that raw audio is not transmitted to external services; persistent storage of raw audio shall be avoided unless explicitly consented to and secured. This reduces privacy risk from inadvertent capture of unrelated conversations. 
* **Accessibility & inclusion:** User interfaces and feedback produced by the PU (voice prompts, text displays) shall conform to accessibility principles (Section 508 / WCAG guidance cited in project standards) and be tested across diverse accents and speech patterns to reduce recognition bias and support equitable use. [11][38]
* **Intellectual property & licensing:** The PU’s software stack (Vosk, Stockfish, OS, libraries) shall retain proper attribution and license compliance; open-source components shall be used and documented with their licenses to avoid IP infringement.
* **Educational accessibility & sustainability:** Component selection and cost decisions for the PU shall favor affordability and reproducibility for academic or community deployment, and the design shall facilitate repairability and reuse to reduce e-waste.
* **Speech privacy & command confirmation UI:** When listening, an LED or on-screen indicator must show active listening and a message must be provided after successful recognition.

## Overview of Proposed Solution

Describe the solution and how it will fulfill the specifications and constraints of this subsystem.


## Interface with Other Subsystems

Provide detailed information about the inputs, outputs, and data transferred to other subsystems. Ensure specificity and thoroughness, clarifying the method of communication and the nature of the data transmitted.


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
