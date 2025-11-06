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

As chess continues to grow in popularity, the demand for new, more interesting chess technology has become increasingly apparent. One of the newest innovations made to meet this demand is the automated chess board. Automated chess boards are capable of moving each piece around the board without human intervention, allowing users to play over the board against computers, people with disabilities, and friends across the world. Although this advancement has provided many new and exciting opportunities in the world of chess, automated boards prove to be too expensive for widespread use by average consumers. This project aims to design an automated chess board at a cheaper price, providing its benefits to more people around the world.

#TODO: HELP!!!

By allowing the autonomous movement of pieces upon receiving a spoken command at a cheaper price, this product will allow a larger audience to enjoy the experience and impact of automated chess boards.


The introduction must be the opening section of the proposal. It acts as the "elevator pitch" of the project, briefly introducing the objective, its importance, and the proposed solution. Because readers may only read this section, it should effectively capture their attention and encourage them to read further.

Toward the end of the introduction, include a subsection that outlines what the proposal will cover. This helps set reader expectations for the ensuing sections.


## Formulating the Problem

Current automated chess boards are expensive and lack features such as online functionality, voice recognition, and unobstructed movement. The goal of this implementation is to improve these features, reduce cost, use accessible parts for easy hobbyist replication, and to make the game more accessible for players with disabilities. Beyond individual use, this new technology could attract new customers to businesses related to board games or leisure locations through its novelty and fascination. Challenges of this project include digital signal processing for voice controls, artificial intelligence (AI) implementation for solo-play, and automating piece movement. 

### Background

During the pandemic, chess increased in popularity [5]. Online chess specifically had a major influx of activity, with Chess.com adding 1 million accounts from March to November 2020, and a 2.8 million member increase in November alone [5]. This newfound popularity opens up opportunities for innovation on this classic game. An automated chess board would support primarily online chess players who want to improve their over-the-board (OTB) game.

AI has had a major impact in the world of chess, especially in the context of online play [6]. It provides learning opportunities, as certain AI can beat any human player. Chess games played OTB do not usually have this capability except for automated boards. AI in OTB implementations will allow players to improve by progressively increasing the strength of their opponent. This function would aid online players transitioning to OTB play, as they could play against AI before a human opponent. This feature also supports those who want to play OTB chess but cannot do so alone.

Many efforts have been made to ensure that chess tournaments are accommodating to those with disabilities [7]. These accommodations still could be improved upon for player autonomy and ease in preparing. For those with Alzheimer’s, other dementias, dyslexia, dysgraphia, fine/gross motor needs, who are blind, or those with a temporary disability such as a broken hand, an accommodation that can be made is the assignment of a Game Assistant (GA) [7]. In cases such as these, the GA may be needed for piece movement, clock pressing, and/or scoring [7]. An automated board could help as an alternative to a GA by helping with piece movement, automatically keeping time, and automating scoring. This would allow players more independence, as they would not have to rely on the assistance of a GA, and fewer volunteers would be needed for tournaments.


## Survey of Existing Solutions

Existing solutions for automated chessboards range from DIY projects to commercially-produced boards:

* **DIY Solutions**: Several open-source projects present designs of varying complexity. Some rely on stepper motors and Arduinos for piece movement, while others incorporate Raspberry Pis and computer vision to track pieces and issue precise directions via microcontrollers.
* **Industrial Solutions**: Several companies offer high-end automated boards with AI opponents and online connectivity. These solutions, however, are often too expensive for the average user, making them impractical for this application.

Below are multiple current solutions, complete with lists of reasons as to why any particular solution would not work for solving this problem.

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


Despite the availability of existing smart chessboard solutions, challenges such as high cost, limited offline functionality, lack of voice recognition, and frequent piece collisions remain key barriers for the average user. The development of a new system should prioritize affordability, lightweight design, seamless voice integration, and reliable automated piece movement with full reset functionality for both players.

This project aims to bridge the gap between current offerings by delivering a cost-effective, user-friendly, and offline-capable automated chessboard that eliminates common frustrations while enhancing accessibility for everyday players.

## Measures of Success

Define how the project’s success will be measured. This involves explaining the experiments and methodologies to verify that the system meets its specifications and constraints.


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
- **Student Success:** Chosen for potential project presentation opportunities at Tech.  

#### Instructor
- **Professor Van Neste:** Chosen to provide guidance on physical implementation.

### Timeline

#### Gantt Chart (Note that it could be subject to modification)
<img width="1817" height="403" alt="image" src="https://github.com/user-attachments/assets/63c91eea-4e48-4255-aa9e-86ea99886951" />

## Specific Implications

"Explain the implications of solving the problem for the customer. After reading this section, the reader should understand the tangible benefits and the worthiness of the proposed work."

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

"Consider the project’s broader impacts in global, economic, environmental, and societal contexts. Identify potential negative impacts and propose mitigation strategies. Detail the ethical considerations and responsibilities each team member bears as an engineer."

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
    As engineers, we adhere to codes like the NSPE (National Society of Professional Engineers) principles, emphasizing public welfare, competence, and honesty. Ethical considerations include ensuring equitable access (avoiding bias in voice recognition algorithms), protecting user data integrity, and transparently communicating limitations (e.g., accuracy rates). We must avoid overhyping benefits to prevent misleading the customer.


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

Each team member must contribute meaningfully to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
