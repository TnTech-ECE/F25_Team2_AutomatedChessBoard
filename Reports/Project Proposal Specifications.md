# Chess 2 Impress

## Introduction

As chess continues to grow in popularity, the demand for new, more interesting chess technology has become increasingly apparent. One of the newest innovations made to meet this demand is the automated chess board. Automated chess boards are capable of moving each piece around the board without human intervention, allowing users to play over the board against computers, people with disabilities, and friends across the world. Although this advancement has provided many new and exciting opportunities in the world of chess, automated boards prove to be too expensive for widespread use by average consumers. This project aims to design an automated chess board at a cheaper price, providing its benefits to more people around the world.


This project will serve two main purposes:

1. **Moving chess pieces automatically:** Automated chess board movement allows people with disabilities or vision issues to enjoy the game of chess more, while also being an interesting and new experience for a general audience. This chess board will individually grab, move and capture pieces to provide a clean user experience.
   
2. **Making automatic chess more accessible:** Most existing automated chess boards are extremely expensive, preventing a wide audience from being able to enjoy it. By not operating for profit and keeping detailed notes on the creation and assembly of the board, this chess board will be dramatically cheaper than existing solutions.

By allowing the autonomous movement of pieces upon receiving a spoken command at a cheaper price, this product will allow a larger audience to enjoy the experience and impact of automated chess boards.

## Formulating the Problem

Current automated chess boards are expensive and lack features such as online functionality, voice recognition, and unobstructed movement. The goal of this implementation is to improve these features, reduce cost, use accessible parts for easy hobbyist replication, and to make the game more accessible for players with disabilities. Beyond individual use, this new technology could attract new customers to businesses related to board games or leisure locations through its novelty and fascination. Challenges of this project include digital signal processing for voice controls, artificial intelligence (AI) implementation for solo-play, and automating piece movement. 

### Background


During the pandemic, chess increased in popularity [5]. Online chess specifically had a major influx of activity, with Chess.com adding 1 million accounts from March to November 2020, and a 2.8 million member increase in November alone [5]. This newfound popularity opens up opportunities for innovation on this classic game. An automated chess board would support primarily online chess players who want to improve their over-the-board (OTB) game.

AI has had a major impact in the world of chess, especially in the context of online play [6]. It provides learning opportunities, as certain AI can beat any human player. Chess games played OTB do not usually have this capability except for automated boards. AI in OTB implementations will allow players to improve by progressively increasing the strength of their opponent. This function would aid online players transitioning to OTB play, as they could play against AI before a human opponent. This feature also supports those who want to play OTB chess but cannot do so alone.

Many efforts have been made to ensure that chess tournaments are accommodating to those with disabilities [7]. These accommodations still could be improved upon for player autonomy and ease in preparing. For those with Alzheimer’s, other dementias, dyslexia, dysgraphia, fine/gross motor needs, who are blind, or those with a temporary disability such as a broken hand, an accommodation that can be made is the assignment of a Game Assistant (GA) [7]. In cases such as these, the GA may be needed for piece movement, clock pressing, and/or scoring [7]. An automated board could help as an alternative to a GA by helping with piece movement, automatically keeping time, and automating scoring. This would allow players more independence, as they would not have to rely on the assistance of a GA, and fewer volunteers would be needed for tournaments.

## Specifications

The chess board will meet the following requirements to ensure reliability and operability:

1. **Voice Input**

    - Board shall recognize voice input with an accuracy of at least 80%.
    - Board shall listen for input while a button is pressed to avoid accidental moves.
    - Board shall recognize commands in algebraic chess notation and other common variations (Knight to e5, Bishop a4, etc.).
    - Board shall process commands within 2 seconds of button release.
2. **Automated Piece Movement**

    - Board shall move pieces within half an inch of the center of each square.
    - Board shall ensure that all pieces remain upright and stable while moving.
    - Board shall finish any single piece move within 5 seconds of beginning the movement.
    - Board shall notice and remove 95% of captured pieces without piece collision.
3. **Portability and Accessibility**

    - Board shall weigh less than 30 pounds such that it can be moved by one person.
    - Board shall have labels on each file and rank to assist users in locating each square.
    - Board may have a carrying case or handle.
4. **Power and Safety**

    - Board shall have a sleep mode to reduce power consumption when not in immediate use.
    - Board shall be powered by a 12V DC adapter or rechargeable battery supporting at least 2 hours of active gameplay.
5. **Affordability and Modifications**

    - Board shall cost no more than $350 USD in materials
    - Board shall have a modular design allowing for upgrades to individual systems.
## Constraints
The chessboard will be designed to operate efficiently while adhering to the following safety and regulatory requirements:

1. **Regulatory and Compliance Constraints**

    - Board shall comply with FCC Part 15, Subpart B (Class B) regulations, ensuring that electromagnetic interference is within acceptable limits for residential and public environments.
    - Board shall operate below 50V DC in accordance with UL low-voltage safety thresholds, removing the need for additional electrical insulation and protection.
    - Board shall meet applicable requirements of the National Electrical Code (NEC NFPA 70) for low-voltage consumer electronic systems intended for indoor use.
    - Board shall avoid materials or component configurations that would violate CPSC (Consumer Product Safety Commission) regulations regarding consumer electronics used in public settings.

2. **Electrical and Safety Constraints**

    - Board shall prevent hazardous surface temperatures, maintaining an external temperature of no more than 104°F (40°C) under continuous operation, per UL 94 and general consumer safety guidelines.
    - Board shall utilize standard cord sets and connectors compliant with NEC Article 400 to ensure safe installation and minimal tripping or disconnection hazards in public spaces.
    - Board shall ensure proper grounding and protection of all power connections to conform to OSHA 1910 Subpart S electrical safety practices for general-use electronic systems.
    - Board shall display clear warning labels for user-facing hazards (e.g., moving parts, power status) in accordance with ANSI Z535.4 standards for safety signage and communication.

3. **Accessibility and Ergonomic Constraints**

    - Board shall conform to the Section 508 of the Rehabilitation Act for electronic systems, ensuring digital interfaces (e.g., voice command, status indicators) are accessible to users with disabilities.
    - Board shall follow ergonomic interface design principles from ANSI/HFES 100-2007, including appropriate control placement, spacing, and feedback mechanisms.
    - Board shall avoid design elements that may cause confusion or usability issues for individuals with cognitive or motor impairments, adhering to universal design principles where possible.

## Survey of Existing Solutions

Existing solutions for automated chessboards range from DIY projects to commercially-produced boards:

* **Industrial Solutions**: Several companies offer high-end automated boards with AI opponents and online connectivity. These solutions, however, are often too expensive for the average user, making them impractical for this application.

Below are multiple Industrial solutions that have implications for our project:

*ChessUp 2 Smart Chess Board [1]: A WiFi-enabled smart chessboard featuring chip recognition technology and direct integration with Chess.com, offered at a relatively lower cost of $399.99.

Cons:
* Cannot move pieces autonomously.
* Requires a stable WiFi connection to Chess.com for AI functionality.

*Miko Chess Grand [2]: A premium wooden smart chessboard equipped with a magnetic robotic arm beneath the surface for automated piece movement. It includes wooden pieces, a high-quality 12-pound wooden board, and dedicated storage space for captured pieces, priced at $549.99.

Cons:
* The board’s weight makes it less portable.
* High-quality materials increase overall cost.
* The robotic arm cannot make moves for the first player except when removing pieces from the board.
* Does not include voice recognition functionality.

*Chessnut Move [3]: An advanced robotic chessboard featuring integrated voice command support, offline AI gameplay, and connectivity with Chess.com. Priced at $899.99, it provides one of the most interactive experiences currently available.

Cons:
* Pieces occasionally collide during automated movement.
* The design relies on each piece containing its own robotic base, which significantly increases cost.
* Oversized piece bases reduce aesthetic appeal and make the board feel crowded.

*GoChess Mini [4]: A compact and lightweight smart chessboard featuring illuminated path indicators for piece movement, Bluetooth connectivity, adjustable AI difficulty, and Chess.com integration. Priced at $249.95 and weighing 6.6 pounds, it offers an affordable entry point into smart chessboards.

Cons:
* Battery-powered system requires two hours to fully charge, supporting up to 100 hours of playtime (reduced to about five hours when lights are enabled).
* Does not support automated piece movement, requiring players to manually move all pieces.
* Lacks an automated reset function for returning pieces to their starting positions.


* **DIY Solutions**: Several open-source projects present designs of varying complexity. Some rely on stepper motors and Arduinos for piece movement, while others incorporate Raspberry Pis and computer vision to track pieces and issue precise directions via microcontrollers.

Below are multiple DIY solutions that have implications for our project:


*8x8 Smart Chess Board [9]: A Raspberry Pi–controlled prototype that uses stepper motors, lead screw mechanisms, and an electromagnetic head to move magnetized chess pieces. The design mimics the motion of a 3D printer to achieve movement across the XY plane. The design utilizes a min-max algorithm to generate the best move predictions.

Cons:
* The stepper motor system has experienced notable failures.
* The bill of materials (BOM) is incomplete.

*Techievince 8.0 – Electronics Club IITG Project [10]: An Arduino-based system programmed in Embedded C that integrates the Micro Max chess engine using Minimax and Alpha-Beta algorithms. It employs an XY trolley system with stepper motors, magnetized pieces, and an electromagnetic head, along with multiplexed reed switch sensors for piece displacement detection.

Cons:
* Visually less appealing compared to other designs.
* Requires specialized magnetic chess pieces, increasing overall cost.
* Does not include voice recognition functionality.

*Chess Automation Using Computer Vision [11]: A computer vision–driven approach that uses a camera, OpenCV, and NumPy to detect the chessboard, track pieces in real time, and record game history. The system identifies moves directly from image or video input without requiring embedded magnets or sensors.

Cons:
* Lacks integrated AI functionality.
* Cannot move pieces autonomously.
* Lacks an automated reset function for returning pieces to their starting positions.


Despite the availability of existing affordable smart chessboard solutions, challenges such as high cost, limited offline functionality, lack of voice recognition, and frequent piece collisions remain key barriers for the average user. The development of a new system should prioritize affordability, lightweight design, seamless voice integration, and reliable automated piece movement with full reset functionality for both players.

This project aims to bridge the gap between current offerings by delivering a cost-effective, user-friendly, and offline-capable automated chessboard that eliminates common frustrations while enhancing accessibility for everyday players.

## Measures of Success

The success of this project will be evaluated based on its ability to meet functional, technical, and usability requirements during hands-on, public use of the automated chessboard. The following key performance indicators (KPIs) and verification methodologies will be used to ensure the system meets its specifications and constraints.

### **1. Input Consistency and Reliability**


**Objective**: Verify that voice commands are consistently recognized across varying conditions and accurately synchronized with expected chessboard inputs.

**Methodology**:

* **Volume Variation**: Conduct recognition trials at different decibel levels and distances from the microphone to ensure consistent accuracy.
* **Speaker Variability**: Evaluate system performance in regard to varying players with different tones, accents, and pronunciations.
* **Command Completion**: Verify that the system consistently processes entire commands before producing an output, ensuring no premature or truncated recognition.
* **Integration Validation**: Confirm that correctly recognized commands result in accurate and legal piece movements on the automated chessboard.

### **2. Mechanical Accuracy and Responsiveness**


**Objective**: Verify that chess pieces move accurately, reliably, and within acceptable response times in accordance with input commands.

**Methodology**:

* **Movement Consistency**: Conduct repeated trials across multiple games to confirm that piece movements occur in a uniform manner and within predictable timeframes.
* **Localization Accuracy**: Verify that pieces consistently align to the center of their designated destination squares after each move.
* **Stability Evaluation**: Ensure that pieces remain upright throughout movement and are not displaced or knocked over by adjacent moving pieces.
* **Response Time Measurement**: Record the interval between input recognition and movement initiation to confirm timely execution.
* **Captured Piece Handling**: Verify that captured pieces are consistently removed from play and stored without interfering with ongoing gameplay.
* **Board Reset Testing**: Ensure that the system reliably returns to the initial configuration within a defined time limit.

### **3. Portability and Ergonomic Design**


**Objective**: Ensure that the chessboard is lightweight, easy to transport, and designed with a form factor that supports comfortable play without hindrance in various environments.

**Methodology**:

* **Weight Benchmarking**: Measure total system weight and verify that it remains within the team’s portability threshold for single-person transport.
* **Form Factor Assessment**: Evaluate board dimensions and height to confirm they do not interfere with gameplay or piece movement.
* **User Testing**: Conduct trials with target users to gather feedback on size, shape, and portability in public settings.
* **Transport Simulation**: Test relocation scenarios (e.g., carrying, packing, setup/teardown) to ensure ease of handling and minimal risk of damage.

### **4. Power Efficiency and Safety**


**Objective**: Verify that the chessboard operates for extended periods with minimal power consumption, maintains safe operating conditions, and uses a power connection that is practical and safe in typical play environments.

**Methodology**:

* **Low-Power Evaluation**: Assess the effectiveness of energy-saving modes or optimizations in reducing overall consumption.
* **Thermal Safety**: Monitor operating temperatures under normal and extended use to confirm the system does not overheat or damage surfaces.
* **Electrical Safety Verification**: Ensure that power circuitry does not overload the supply or pose risks of short-circuiting.
* **Power Supply Assessment**: Confirm that the power connection is safe, unobtrusive, and appropriate for public and home settings (e.g., no excessive cord length or tripping hazards).

### **5. Affordability and Future Expansion**


**Objective**: Demonstrate that the system offers a cost-efficient alternative to existing commercial solutions while maintaining the ability to expand for future requirements.

**Methodology**:

* **Cost Evaluation**: Assess the total project cost and compare it against comparable commercial automated chessboard systems.
* **Maintenance and Longevity Review**: Track required upkeep, component replacement frequency, and overall durability to determine long-term affordability.

By meeting these success criteria, the project will demonstrate its effectiveness in bridging the gap between low-cost DIY solutions and expensive, commercially manufactured chessboards.


## Resources
This project will include various hardware components, software, and mechanical parts in order to effectively move the chess pieces autonomously, integrate AI, process voice recognition, and present everything in a professional-looking chessboard. 

#### Hardware Components
1. Processing Unit: A Raspberry Pi 4 will handle Stockfish chess AI, voice recognition software, and communication with the Arduino [14].
2. Control Unit: An Arduino Uno or Mega will directly control the stepper drivers and coordinate motor movement [18].
3. Microphone: A USB microphone will capture player voice commands for the Vosk speech recognition engine [17].
4. Power Supply: Provides regulated 12V for the stepper motors and 5V for the Raspberry Pi and control electronics [15] [16].
   
#### Software 

Stockfish: Open-source chess engine that will handle AI decision-making and gameplay logic [12].

Vosk: Lightweight offline speech recognition engine for translating spoken commands into text for system input [13].

#### CoreXY 
The CoreXY mechanism uses two stepper motors and a system of belts and pulleys arranged so that coordinated motor movements move a single carriage in both X and Y directions [14]. The carriage will hold a strong neodymium magnet, which moves underneath the board to drag metal-based chess pieces across the surface. This setup allows smooth, precise, and fast motion across the entire 8×8 chess grid.

### Budget
<!-- This will increase/change over time not 100% sure about materials -->
This is an estimate of the cost for the major materials needed:
| Item                      | Description / Notes                      | Quantity | Approx Cost (USD) |
|---------------------------|------------------------------------------|----------|-------------------|
| Raspberry Pi 4 Model B    | 4GB RAM, runs Stockfish + voice software | 1        | $55–$65           |
| MicroSD Card              | 32 GB, Class 10, holds OS + software     | 1        | $8–$12            |
| Microphone                | USB for voice recognition                | 1        | $10–$20           |
| NEMA 17 Stepper Motors    | Moves the pulley system                  | 2        | $12–$15 each      |
| GT2 Belt + Pulleys        | 6mm width, 2m length + 2 pulleys         | 1 set    | $8–$12            |
| CoreXY / XY Framework     | Rails, idlers, frame                     | 1        | $40–$80           |
| Arduino Uno / Mega        | Controls stepper drivers (from Pi input) | 1        | $10–$20           |
| Stepper Driver Boards     | Big Easy Driver / A4988 / DRV8825        | 2        | $5–$20 each       |
| Neodymium Magnet          | 20–30 mm diameter, strong grade (N42+)   | 1–2      | $5–$10            |
| Power Supply              | 12V (for motors) + 5V 3A (for Pi)        | 1        | $15–$25           |
| Chessboard Frame          | Wooden or 3D printed                     | 1        | $20–$40           |
| Chess Piece Set           | With metal washers in bases              | 1        | $15–$30           |

Primary Costs: The largest expenses will be the Raspberry Pi (for AI + speech recognition) and the CoreXY mechanical framework (belts, rails, and frame) [14] [15].

Cost-Saving Options: The chessboard and pieces could be 3D printed to reduce costs. Drawer slides or DIY wood rails could possibly replace linear rails for a cheaper CoreXY build.

Total Estimated Cost: The project should fall within $250 on average, with a maximum of $350 if higher-quality parts are chosen.



### Personnel

#### Required Skills  

**Software & Programming:** Programming, AI / API / Networking, MATLAB, R  
**Hardware & Systems:** Microcontroller knowledge, Embedded Systems / Digital Systems, Magnetics, Power Electronics, Mechanical Systems  
**Design & Simulation Tools:** LTspice, CAD / 3D Printing  
**Theory & Analysis:** Signal Processing  

#### Team Skills

**Nathan MacPherson**  
- *Current Skills:* Digital Systems, Programming, Networks, Electrical CAD  
- *Skills to Learn:* Magnetics, Mechanical Systems, CAD / 3D Printing  

**Noah Beaty**  
- *Current Skills:* Digital Systems, Programming, Microcontroller knowledge, R  
- *Skills to Learn:* Signal Processing, MATLAB, Mechanical Systems  

**Jack Tolleston**  
- *Current Skills:* Digital Systems, Programming, Microcontroller knowledge, R, API / Networking  
- *Skills to Learn:* AI, Embedded Systems, Magnetics  

**Allison Givens**  
- *Current Skills:* Microcontroller knowledge, Programming, CAD / 3D Printing  
- *Skills to Learn:* MATLAB, Magnetics, Power Electronics, LTspice  

**Lewis Bates**  
- *Current Skills:* Digital Systems, Embedded Systems, Microcontroller knowledge, Power Electronics, R  
- *Skills to Learn:* Signal Processing, AI, Magnetics  

*Note:* This list highlights each member’s strongest skills. Depending on the project, required skills or assignments may change.  


#### Supervisor
- **Professor Van Neste:** Chosen to provide guidance on physical implementation.

#### Instructor
- **Professor Storm:** Will approve pieces of the project before finalization.

### Timeline

#### Gantt Chart (Note that the chart will be subject to modification)
<img width="1802" height="596" alt="image" src="https://github.com/user-attachments/assets/55324b80-8e8f-4788-8511-b92a371fea24" />


## Specific Implications

By developing an audio-actuated automated chessboard, this project aims to address key challenges faced by local board game lounges, including limited space, high maintenance costs associated with physical games, and the need to attract a diverse range of patrons in a competitive entertainment market. The solution enables voice-controlled gameplay, where players verbally announce moves, and the board automates piece movements via integrated robotics, magnets, and speech recognition technology. Outlined below are the tangible benefits for the lounge owner (our customer), demonstrating the project's value in enhancing operations, customer satisfaction, and revenue potential.

1. Increased Customer Engagement and Retention:

    The automated board allows for seamless, hands-free chess sessions, appealing to groups who might otherwise avoid traditional setups due to complexity or physical demands. For instance, patrons could play while enjoying drinks or snacks without knocking over pieces, reducing downtime and frustrations.
    Tangible Benefit: This could boost dwell time by 20-30% per visit, as players stay longer for multiple games. In a lounge setting, longer stays translate to higher sales of food, beverages, and entry fees.
    Worthiness: With board game lounges relying on repeat visits, this innovation fosters loyalty among casual players, families, and chess enthusiasts, helping the lounge differentiate from competitors like arcades or casinos.


2. Expanded Accessibility and Inclusivity:

    Voice actuation makes chess accessible to patrons with disabilities, such as those with limited mobility or visual impairments, who might otherwise be excluded from playing traditional-style board games. 
    Tangible Benefit: Attracts a broader demographic, including seniors, families with children, or disabled individuals, potentially increasing foot traffic from underserved community segments. This aligns with inclusive business practices, possibly qualifying the lounge for grants or more positive reviews on platforms like Yelp.
    Worthiness: By emphasizing diversity, this positions the lounge as a community hub, enhancing its reputation and social impact while complying with accessibility standards like the ADA.


3. Operational Efficiency and Cost Savings:

    Automation minimizes wear and tear on physical pieces, reduces setup/cleanup time, and prevents disputes over moves through built-in rule validation.
    Tangible Benefit: Staff can focus on customer service rather than game maintenance, saving a considerable amount of time in a busy lounge. Additionally, the board's durability could lower replacement costs for damaged sets.
    Worthiness: For small businesses like local lounges operating on thin margins, these efficiencies directly improve profitability.


Overall, solving this problem not only streamlines daily operations but transforms the lounge into a forward-thinking space that combines nostalgia with modern technology. The worthiness lies in its potential to revitalize local businesses, promote social interaction, and inspire similar adaptations for other games, ultimately contributing to the sustainability of community-oriented entertainment venues. This senior design project thus delivers real-world value, bridging engineering innovation with practical business needs.


## Broader Implications, Ethics, and Responsibility as Engineers

The audio-actuated automated chessboard project extends beyond enhancing a local board game lounge's operations, influencing broader contexts through technological innovation in recreational gaming. By integrating voice recognition, robotics, and user-friendly interfaces, it promotes accessible entertainment while raising considerations in global scalability, economic viability, environmental sustainability, and societal equity. This section explores these impacts, identifies potential negatives with mitigation strategies, and outlines the ethical responsibilities our engineering team will be faced with throughout the project.

1. Global Impacts:

    The project could inspire scalable adaptations for international markets, such as multilingual voice support for diverse languages, enabling chess lounges in non-English-speaking regions to adopt similar tech. This fosters global cultural exchange through chess, a universally recognized game, potentially integrating with online platforms for international tournaments.
    Broader Context: In a connected world, this contributes to the democratization of technology.


2. Economic Impacts:

    For the lounge, it drives revenue through innovative attractions, but on a larger scale, it could stimulate job creation in tech-manufacturing or software development for similar devices. Affordable prototyping (using open-source components) lowers barriers for small businesses, potentially boosting local economies in entertainment sectors.
    Broader Context: Amid economic shifts toward experiential leisure post-2025, this supports small enterprises against digital gaming giants, promoting economic resilience in community-based industries.


3. Environmental Impacts:

    The board's electronics and motors require materials like rare earth metals, but energy-efficient design (e.g., low-power microphones) minimizes operational footprint. Recyclable components could reduce e-waste compared to disposable games.
    Broader Context: It encourages sustainable tech in consumer products, aligning with global efforts to cut electronic waste, which reached 62 million tons annually by 2024 data trends.


4. Societal Impacts:

    Enhances community building by making lounges more inclusive, supporting mental health through social gaming. It could educate users on AI ethics via interactive features, raising awareness of voice tech in daily life.
    Broader Context: Promotes societal well-being by bridging generational gaps—appealing to tech-savvy youth and traditional players—while addressing isolation in urban settings.


5. Potential Negative Impacts and Mitigation Strategies:

  - Privacy Risks: Audio actuation involves recording voices, potentially capturing sensitive conversations in a public lounge.
  - Mitigation: Implement on-device processing to avoid cloud storage, use anonymized data, and include user consent prompts with clear opt-out options, complying with regulations like GDPR or CCPA.
  - Technological Exclusion: Reliance on voice tech could alienate users with speech impairments or accents not recognized by the system.
  -  Mitigation: Incorporate fallback controls and train models on diverse datasets to improve accuracy, tested via user trials.
  -  Environmental Drawbacks: Manufacturing could contribute to resource depletion if scaled. Mitigation: Prioritize eco-friendly materials (e.g., biodegradable plastics) and design for modularity to extend product lifespan, partnering with recycling programs.
  -  Economic Displacement: Automation might reduce staff needs for game setup. Mitigation: Repurpose roles toward customer engagement or tech maintenance, with training provided to lounge employees.
  -  Over-Reliance on Tech: System failures could disrupt lounge activities. Mitigation: Include manual override modes and robust testing for reliability, with redundancy in power sources.

6. Ethical Considerations and Responsibilities:
    As engineers, we adhere to codes like the National Society of Professional Engineers (NSPE) principles, emphasizing public welfare, competence, and honesty. Ethical considerations include ensuring equitable access (avoiding bias in voice recognition algorithms), protecting user data integrity, and transparently communicating limitations (e.g., accuracy rates). We must avoid overhyping benefits to prevent misleading the customer.


In summary, this project holds promise for positive, broader impacts by advancing inclusive, sustainable technology in entertainment. By proactively addressing negatives and upholding ethical standards, our team fulfills its engineering duty to create solutions that benefit society without undue harm, demonstrating responsible innovation in our senior design work.

## References

[1] ChessUp 2 Smart Chess Board. Bryght Labs. (n.d.). https://playchessup.com/products/chessup-2

[2] Miko Chess Grand. Miko. (n.d.). https://miko.ai/pages/miko-chess-grand 

[3] Chessnutech. (n.d.). Chessnut move - advanced robotic chessboard with Plastic Pieces. Chessnut. https://www.chessnutech.com/products/chessnut-move-advanced-robotic-chessboard-with-plastic-pieces 

[4] GoChess Mini. Particula. (n.d.). https://particula-tech.com/products/gochess-mini?variant=45806634402040&country=US&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOooAY445sOW--M7GA0T4jbNkHE609yl_YKlFLR9iyhF7eX9KFsd9ubc

[5] R. Lahood, "The Queen’s Gambit, the Chess Boom, and the Future of Chess," Michigan Journal of Economics, Apr. 5, 2021. https://sites.lsa.umich.edu/mje/2021/04/05/the-queens-gambit-the-chess-boom-and-the-future-of-chess/.

[6] D. M. D. Iliescu, "The Impact of Artificial Intelligence on the Chess World," *JMIR Serious Games*, vol. 8, no. 4, p. e24049, Dec. 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7759436/.

[7] US Chess, "US Chess Guidelines for Accessible Chess Events," Apr. 2020. https://new.uschess.org/sites/default/files/wp-thumbnails/2020/04/Accessibility-Guidelines-April-2020.pdf.

[8] Davis, E. (2023, November 12). The Rise of Board Game Cafes: Socializing through Analog Entertainment. Medium. https://ethan-davis.medium.com/the-rise-of-board-game-cafes-socializing-through-analog-entertainment-51857183f856

[9] MFOSSociety. (n.d.). MFOSSociety/8-8: 8/8: Smart Chess Board: An Automated Ai Chess Board. GitHub. https://github.com/MFOSSociety/8-8 

[10] sumit11899. (n.d.). SUMIT11899/automated-chessboard. GitHub. https://github.com/sumit11899/Automated-ChessBoard 

[11] Simarmehta. (n.d.). Simarmehta/CHESSAUTOMATION_CV. GitHub. https://github.com/simarmehta/chessAutomation_CV 

[12] Stockfish. (n.d.). Stockfish. https://stockfishchess.org/

[13] VOSK Offline Speech Recognition API. (n.d.). VOSK Offline Speech Recognition API. https://alphacephei.com/vosk/

[14] Instructables. (2019, September 13). CoreXY CNC Plotter. Instructables. https://www.instructables.com/CoreXY-CNC-Plotter/

[15] PiShop. (n.d.). Raspberry Pi 4 Model B/4GB. PiShop.us. https://www.pishop.us/product/raspberry-pi-4-model-b-4gb/

[16] Industries, A. (n.d.). Stepper motor - NEMA-17 size - 200 steps/rev, 12V 350mA. https://www.adafruit.com/product/324

[17] (Amazon.com: NowTH USB Microphone Lavalier Lapel Clip on Mic With 6.56ft Cable for Laptop, Computer, PC, Streaming Conferencing,Interviews, Online Singing, Skype, MSN, Audio Video Recording : Electronics, n.d.)

[18] Amazon.com: ELEGOO UNO R3 Board ATmega328P with USB Cable(Arduino-Compatible) for Arduino : Electronics. (n.d.). https://www.amazon.com/ELEGOO-Board-ATmega328P-ATMEGA16U2-Compliant/dp/B01EWOE0UU

## Statement of Contributions


Nathan MacPherson - Introduction, Specifications and Constraints

Jack Tolleson - Resources, Budget, Formulating the Problem, Background

Noah Beaty - Measures of Success, Survey of Existing Solutions

Allison Givens - Formulating the Problem, Background, Personnel, Timeline

Lewis Forrest Bates - Specific Implications, Broader Implications, Ethics, and Responsibility as Engineers, Survey of Existing Solutions

All - Proofreading and Editing
