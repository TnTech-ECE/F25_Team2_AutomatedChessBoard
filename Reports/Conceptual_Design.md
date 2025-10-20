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

# Comparative Analysis of CPUs and Computers

## Raspberry Pi Boards

### Raspberry Pi 2B [29]

_Price:_ ~$35 (discontinued, used prices vary)

* _Pros:_
- Quad-core ARM Cortex-A7 CPU at 900 MHz provides basic processing for simple chessboard control tasks like GPIO motoractuation.
- 1 GB RAM sufficient for lightweight OS and basic chess AI engines without heavy computer vision.
- 40-pin GPIO header enables easy integration with stepper motors, sensors, or electromagnets for piece movement.
- Extensive community support and libraries for Python-based control, ideal for student projects.
- Low power consumption (~3W peak) allows for battery-powered or portable setups.

* _Cons:_
- Outdated architecture struggles with real-time computer vision for piece detection, requiring external modules.
- No built-in WiFi or Bluetooth, limiting remote control or app integration without add-ons.
- Limited networking (100 Mbps Ethernet) may bottleneck data transfer for updates or multiplayer features.
- Older VideoCore IV GPU lacks efficiency for any graphical chess interfaces or 4K output.
- Discontinued status means potential availability issues and no official updates.

### Raspberry Pi 3B [30]

_Price:_ ~$35

* _Pros:_
- Quad-core ARM Cortex-A53 CPU at 1.2 GHz offers improved performance over older models for basic AI chess logic and GPIO control.
- 1 GB RAM handles multitasking like running a chess engine alongside motor control scripts.
- Built-in WiFi (802.11n) and Bluetooth 4.1 enable wireless connectivity for remote monitoring or app-based chess games.
- 40-pin GPIO for seamless hardware integration with chessboard mechanics like solenoids or cameras.
- Proven ecosystem with abundant tutorials for automated projects, reducing development time.

* _Cons:_
- Power draw (~5W) higher than entry-level boards, potentially requiring better cooling in enclosed setups.
- No USB 3.0 or Gigabit Ethernet, slowing down file transfers for large AI models or firmware updates.
- VideoCore IV GPU limits advanced graphics or video processing for high-res chessboard imaging.
- Older model may not receive the latest software optimizations compared to newer Pis.
- Lacks modern features like 4K output, unsuitable for high-definition display integrations.

### Raspberry Pi 4B [31]

_Price:_ ~$35-75 (depending on RAM variant)

* _Pros:_
- Quad-core ARM Cortex-A72 CPU at 1.5-1.8 GHz delivers strong performance for computer vision libraries like OpenCV for piece recognition.
- Up to 8 GB RAM supports running complex chess AI (e.g., Stockfish) with simultaneous hardware control.
- Dual-band WiFi (802.11ac), Bluetooth 5.0, and Gigabit Ethernet for robust networking in multiplayer or cloud-synced games.
- 40-pin GPIO and USB 3.0 ports facilitate fast camera input and peripheral connections for automation.
- VideoCore VI GPU with 4K support enhances graphical interfaces or video streaming of chessboard states.

* _Cons:_
- Higher power consumption (~6-15W) may necessitate active cooling or larger power supplies.
- Older than Pi 5, so slightly less efficient for the latest AI frameworks without optimizations.
- No native PCIe support, limiting high-speed storage for large datasets or logs.
- Potential heat issues during intensive CV tasks without proper heatsinking.
- Variable pricing based on RAM could exceed budget for basic projects.

### Raspberry Pi 5 [32]

_Price:_ ~$60-80 (depending on RAM variant)

* _Pros:_
- Quad-core ARM Cortex-A76 CPU at 2.4 GHz provides top-tier performance for real-time CV and advanced chess AI processing.
- 4/8 GB LPDDR4X RAM excels in multitasking, handling vision, motor control, and game logic simultaneously.
- PCIe interface for NVMe storage boosts speed for loading models or storing game data.
- Dual-band WiFi, Bluetooth 5.0, and Gigabit Ethernet ensure seamless connectivity for remote play.
- VideoCore VII GPU at 800 MHz supports 4K60 output, ideal for high-res displays or camera feeds.

* _Cons:_
- Higher power needs (~5-25W) require a robust 5A power supply and potential cooling.
- More expensive than older Pi models, impacting group project budgets.
- Newer architecture may have fewer mature libraries compared to Pi 4's ecosystem.
- Overkill for simple chessboard automation without heavy AI components.
- Limited availability of compatible accessories early in lifecycle.

## NVIDIA Jetson Boards

### Jetson Orin Nano [26]

_Price:_ ~$249 (Super Developer Kit)

* _Pros:_
- 6-core ARM Cortex-A78AE CPU at 1.5-1.7 GHz with Ampere GPU (1024 cores, 32 tensor cores) delivers 67 TOPS for accelerated AI and CV in piece detection.
- 4/8 GB LPDDR5 RAM supports edge AI models for intelligent chess moves without cloud dependency.
- CUDA compatibility optimizes TensorFlow or PyTorch for real-time processing.
- 40-pin GPIO for motor and sensor integration, plus M.2 for WiFi/BT add-ons.
- Compact form factor with NVMe support for fast storage in data-intensive apps.

* _Cons:_
- High cost makes it less accessible for student group projects.
- Power consumption (7-25W) demands efficient power management or larger batteries.
- Steeper learning curve for NVIDIA-specific tools compared to Raspberry Pi.
- Overpowered for basic chess control, potentially wasting resources.
- Limited community resources outside AI-focused applications.

### Jetson AGX Orin [25]

_Price:_ ~$1000-2000 (Developer Kit)

* _Pros:_
- 12-core ARM Cortex-A78AE CPU at 2.2 GHz with 2048-core GPU (64 tensor cores) offers 200-275 TOPS for advanced AI chess engines and multi-camera CV.
- 32/64 GB LPDDR5 RAM handles complex simulations or multiple AI instances.
- High-end connectivity including up to 10GbE options for networked chess tournaments.
- 40-pin GPIO and robust I/O for integrating sophisticated mechanics like robotic arms.
- eMMC and NVMe storage for reliable, high-speed data handling.

* _Cons:_
- Very expensive, unsuitable for most educational budgets.
- High power draw (15-60W) requires industrial-grade power and cooling solutions.
- Bulkier setup may not fit compact chessboard enclosures.
- Excessive performance for standard automation, leading to underutilization.
- Complex setup for non-AI experts, with potential overkill on resources.

## Libre Computer Boards

### Libre Computer Tritium ALL-H3-CC [4]

_Price:_ ~$10-30

* _Pros:_
- Quad-core ARM Cortex-A7 CPU at 1.0 GHz provides cost-effective basic processing for GPIO-driven chess moves.
- Up to 2 GB DDR3 RAM sufficient for simple scripts and lightweight OS.
- 40-pin GPIO and camera interface for basic sensor or vision add-ons.
- Low power (~3-5W) ideal for energy-efficient, portable designs.
- Affordable entry point with 4K HDMI for display outputs.

* _Cons:_
- Weak Mali-400 GPU limits any graphical or CV tasks.
- Slow 10/100 Ethernet and USB 2.0 restrict data speeds.
- Limited community compared to Raspberry Pi, fewer ready-made libraries.
- Older architecture struggles with modern AI or multitasking.
- Potential compatibility issues with some peripherals.

### Libre Computer La Frite AML-S805X-AC [5]

_Price:_ ~$10-20

* _Pros:_
- Quad-core ARM Cortex-A53 CPU at 1.2 GHz offers better performance than basic boards for entry-level automation.
- Up to 1 GB DDR4 RAM for running basic chess logic and control code.
- Compact size with partial 40-pin GPIO for essential hardware connections.
- Low power (~2-4W) suits battery-operated chessboards.
- Supports H.265/VP9 decoding for media-related extensions if needed.

* _Cons:_
- Only 1080p HDMI limits high-res outputs.
- Fewer USB ports (2x USB 2.0) restrict peripheral expansions.
- No Gigabit Ethernet, slowing network features.
- Partial GPIO may require adapters for full chess mechanics.
- Weaker GPU (Mali-450) inadequate for CV.

### Libre Computer Le Potato AML-S905X-CC [6]

_Price:_ ~$35

* _Pros:_
- Quad-core ARM Cortex-A53 CPU at 1.5 GHz handles moderate processing for chess AI and motor control.
- Up to 2 GB DDR3 RAM for stable multitasking in automation scripts.
- Gigabit Ethernet and 4x USB 2.0 for better connectivity and expansions.
- 40-pin GPIO with eMMC header for reliable storage and hardware integration.
- 4K60 HDMI with Mali-450 GPU supports decent display outputs.

* _Cons:_
- No built-in WiFi/BT, requiring dongles for wireless features.
- Power (~5W) similar to Pi 3 but without the same ecosystem support.
- Limited AI capabilities without GPU acceleration.
- Potential heat at full load without cooling.
- Software compatibility may lag behind mainstream boards.

### Libre Computer Sweet Potato AML-S905X-CC-V2 [7]

_Price:_ ~$35

* _Pros:_
- Quad-core ARM Cortex-A53 CPU at 1.5 GHz with improved DDR4 for slightly better efficiency in control tasks.
- 2 GB RAM option for handling chess engines and GPIO scripting.
- Gigabit Ethernet, 4x USB 2.0, and 40-pin GPIO for comprehensive I/O.
- UEFI BIOS support for customizable booting and flexibility.
- 4K60 HDMI and SPI boot ROM enhance display and reliability.

* _Cons:_
- Similar to Le Potato but with potential DDR4 premium without major gains.
- No WiFi/BT native, limiting out-of-box wireless.
- Mali-450 GPU not suited for intensive CV or AI.
- Higher inertia in updates compared to Raspberry Pi.
- May require specific configurations for optimal performance.

# Comparative Analysis of Compute Units for Automated Chessboard Project

## Single-Board Computers

### Rock64 [14]

_Price:_ ~$45

* _Pros:_
- Rockchip RK3328 Quad-Core ARM Cortex-A53 processor at 1.5 GHz for solid performance in vision-based tasks.
- Up to 4 GB LPDDR3 RAM supports running full OS like Linux for AI chess logic or camera integration.
- Gigabit Ethernet, USB 3.0, and HDMI for easy connectivity to peripherals like cameras or displays.
- eMMC socket and MicroSD for flexible storage options in data-intensive projects.
- Compact credit-card size fits well under a chessboard enclosure.

* _Cons:_
- Higher power draw (~3W under load) may require better cooling or external power for prolonged use.
- No built-in WiFi/BT, needing add-ons for wireless control.
- Limited GPIO (40 pins) compared to some industrial boards.
- Older SoC may lag in efficiency versus newer ARM chips.
- Community support strong but not as vast as Raspberry Pi ecosystem.

### Le Potato [6]

_Price:_ ~$35

* _Pros:_
- Amlogic S905X Quad-Core ARM Cortex-A53 at 1.5 GHz with 4K video decoding for handling chess piece detection via camera.
- Up to 2 GB RAM suitable for lightweight OS and basic AI tasks.
- Ethernet, HDMI, and USB ports for straightforward interfacing.
- MicroSD and eMMC options for expandable storage.
- Similar form factor to Raspberry Pi for easy hardware swaps.

* _Cons:_
- Power consumption (~2-3W load) higher than MCUs, impacting battery life.
- No wireless connectivity built-in, requiring modules for remote apps.
- GPIO limited to 40 pins, may need expansion for complex motor setups.
- Less RAM than higher-end SBCs for intensive computations.
- Software ecosystem good but relies on community ports.

### BeagleBone Black [19]

_Price:_ ~$50

* _Pros:_
- TI AM335x ARM Cortex-A8 at 1 GHz with extensive 92 GPIO pins for robust motor and sensor control.
- 512 MB DDR3 RAM and 4 GB eMMC for reliable OS booting and storage.
- Ethernet, microHDMI, and USB for connectivity.
- Industrial-grade reliability with low power (~0.5W load).
- Supports capes for easy expansion in chessboard prototypes.

* _Cons:_
- Single-core processor may struggle with heavy AI/vision without add-ons.
- Smaller RAM limits multitasking in complex apps.
- Higher price for specs compared to newer SBCs.
- No wireless built-in, needing capes or modules.
- Larger size than pocket variants for tight enclosures.

### PocketBeagle [20]

_Price:_ ~$25

* _Pros:_
- Octavo OSD3358 ARM Cortex-A8 at 1 GHz in ultra-compact 56x35mm form for hidden chessboard integration.
- 512 MB DDR3 and MicroSD support for embedded OS.
- 72 GPIO pins for ample interfacing with sensors/motors.
- Very low power (~0.3W load) ideal for battery-powered designs.
- USB connectivity for simple setup.

* _Cons:_
- No Ethernet or HDMI, limiting to USB-based interfaces.
- Single-core may underperform in vision tasks.
- Smaller community than full BeagleBone.
- Requires add-ons for wireless or display.
- Minimal onboard storage without MicroSD.

### Onion Omega2+ [9]

_Price:_ ~$15

* _Pros:_
- MT7688 MIPS at 580 MHz with 128 MB RAM for low-power IoT control.
- 32 MB flash and MicroSD for storage.
- Built-in WiFi and optional Ethernet for remote chess apps.
- 32 GPIO pins for basic sensor/motor needs.
- Ultra-low power (~0.2W load) for energy-efficient designs.

* _Cons:_
- Slower processor limits to simple logic, not AI/vision.
- MIPS architecture may have compatibility issues with ARM software.
- Small size but limited expansion without add-ons.
- No video output, focusing on headless operation.
- Community support waning compared to ESP32.

### ClockworkPi [21]

_Price:_ ~$39

* _Pros:_
- Allwinner R16 Quad-Core ARM Cortex-A7 at 1.2 GHz with 1 GB DDR3 for basic OS tasks.
- MicroSD up to 128 GB for storage.
- Modular design with WiFi/BT, microHDMI, USB for prototypes.
- Various GPIO for custom interfaces in chess projects.
- Compact 68x48mm size for portable builds.

* _Cons:_
- Older A7 cores less efficient for modern AI.
- Power draw (~1W load) moderate but needs management.
- Limited RAM for multitasking.
- Niche ecosystem, less software than mainstream SBCs.
- May require custom enclosures for integration.

## Microcontrollers

### Teensy 4.1 [28]

_Price:_ ~$30

* _Pros:_
- ARM Cortex-M7 at 600 MHz for high-speed real-time control of motors/sensors.
- 1 MB RAM and 2 MB flash with SD option for ample code/storage.
- 40+ GPIO pins including PWM for precise chess piece movement.
- USB host and optional Ethernet for expansions.
- Low power (~0.2W load) suits embedded applications.

* _Cons:_
- No built-in wireless, needing add-ons.
- Higher cost than basic Arduinos.
- Steeper learning for advanced features.
- Small size but requires careful soldering for pins.
- Limited video capabilities without shields.

### Raspberry Pi Pico [33]

_Price:_ ~$4

* _Pros:_
- RP2040 Dual-Core ARM Cortex-M0+ at 133 MHz for basic embedded logic.
- 264 KB RAM and 2 MB flash for simple programs.
- 26 GPIO pins for sensor/motor interfacing.
- Ultra-low power (~0.1W load) for battery operation.
- Low cost ideal for multiple prototypes.

* _Cons:_
- No wireless or networking built-in.
- Limited RAM for complex tasks.
- Basic processor not suited for AI/vision.
- Requires add-ons for connectivity.
- Smaller community for advanced uses.

### Raspberry Pi Pico 2 [34]

_Price:_ ~$5

* _Pros:_
- RP2350 Dual-Core ARM Cortex-M33 (or RISC-V) at 150 MHz with improved security.
- 520 KB RAM and 4 MB flash for enhanced embedded apps.
- 26 GPIO pins similar to Pico for compatibility.
- Low power (~0.1W load) for efficiency.
- Dual-architecture option for experimentation.

* _Cons:_
- Still no built-in wireless.
- Slightly higher cost than original Pico.
- Limited to basic control, not heavy compute.
- Add-ons needed for expansions.
- Newer, so some software in beta.

### ESP32 [23]

_Price:_ ~$5

* _Pros:_
- Xtensa Dual-Core LX6 at 240 MHz for versatile control.
- 520 KB SRAM and up to 16 MB flash for programs.
- 34 GPIO pins with WiFi/BT for wireless chess interfaces.
- Low power (~0.2W load) with deep sleep modes.
- Broad ecosystem for IoT integrations.

* _Cons:_
- Variable module sizes may need careful fitting.
- Sensitive to power noise in analog tasks.
- No display output without add-ons.
- Overkill for very simple logic.
- Community vast but fragmented.

### Seeeduino V4.2 [36]

_Price:_ ~$7

* _Pros:_
- ATmega328P 8-bit AVR at 16 MHz Arduino-compatible for easy coding.
- 20 GPIO (14 digital, 6 analog) for basic interfacing.
- USB connectivity for simple setup.
- Grove ports for quick sensor additions.
- Low power (~0.05W load) for efficiency.

* _Cons:_
- Slow processor limits to basic tasks.
- Limited RAM (2 KB) for simple programs only.
- No wireless built-in.
- Larger size than Nano variants.
- Older architecture vs. 32-bit MCUs.

### Seeeduino Nano [35]

_Price:_ ~$7

* _Pros:_
- ATmega328P at 16 MHz compact Arduino-compatible.
- 22 GPIO (14 digital, 8 analog) in small 43x18mm form.
- USB for easy programming.
- Grove support for expansions.
- Very low power (~0.05W load).

* _Cons:_
- Minimal RAM/flash for basic code only.
- No wireless or advanced features.
- Slower than ARM-based MCUs.
- Requires shields for complexity.
- Breadboard-friendly but fragile pins.

### Arduino Nano [12]

_Price:_ ~$22

* _Pros:_
- ATmega328P at 16 MHz with official Arduino support.
- 22 GPIO (14 digital, 8 analog) for prototyping.
- Breadboard-friendly 45x18mm size.
- USB for straightforward use.
- Extensive library ecosystem.

* _Cons:_
- Higher price for basic specs.
- Limited to simple applications.
- No built-in wireless.
- Low RAM (2 KB) restricts multitasking.
- Older design vs. modern MCUs.

### Arduino Uno [13]

_Price:_ ~$25

* _Pros:_
- ATmega328P at 16 MHz standard Arduino board.
- 20 GPIO (14 digital, 6 analog) with shields support.
- USB for easy programming.
- Vast community and tutorials.
- Reliable for education/projects.

* _Cons:_
- Larger 69x53mm size for enclosures.
- Basic performance only.
- No wireless built-in.
- Higher cost than compatibles.
- Power-hungry vs. MCUs (~0.05W).

### BBC Micro:bit V2 [8]

_Price:_ ~$15

* _Pros:_
- Nordic nRF52833 ARM Cortex-M4 at 64 MHz with BLE.
- 128 KB RAM and 512 KB flash for educational apps.
- Built-in sensors (mic, accel) for interactive chess.
- 25 edge pins for expansions.
- Very low power (~0.05W) with educational focus.

* _Cons:_
- Slower processor for complex logic.
- Limited GPIO for full interfacing.
- BLE only, no WiFi.
- Niche for beginners, less for pros.
- Small display limits status output.

### ATMega328P [24]

_Price:_ ~$2

* _Pros:_
- 8-bit AVR at 16 MHz bare chip for custom PCBs.
- 23 GPIO for minimal designs.
- Ultra-low power (~0.02W) for efficiency.
- Low cost for mass integration.
- Arduino-compatible firmware.

* _Cons:_
- Requires custom board/soldering.
- No USB or connectivity built-in.
- Limited RAM/flash (2 KB/32 KB).
- Basic for simple tasks only.
- No peripherals without add-ons.

### LilyGo T-Display (ESP32-based) [3]

_Price:_ ~$15

* _Pros:_
- Xtensa Dual-Core LX6 at 240 MHz with integrated 1.14" LCD for chess status.
- 520 KB SRAM and 16 MB flash.
- WiFi/BT for wireless features.
- ~15 GPIO pins for interfacing.
- Low power (~0.2W) with display.

* _Cons:_
- Small exposed GPIO limits expansions.
- Display small for detailed info.
- Niche board, variable quality.
- May need custom enclosures.
- Documentation sometimes lacking.

# Raspberry Pi UPS Solutions Comparative Analysis

## Waveshare UPS HAT [38]

Price: ~$25

* _Pros:_
  -Affordable entry-level option with good community support.
  -I2C monitoring for voltage, current, power, and capacity.
  -Multi-protection circuits including overcharge/discharge, overcurrent, short circuit, and reverse polarity.
  -Seamless switch to battery during outages with safe shutdown capability.
  -Compact HAT design compatible with Pi 3/3B+/4B.

* _Cons:_

  -Limited to 2.5A continuous output, may not suffice for high-power peripherals.
  -Batteries not included; requires 2x 18650 cells without built-in protection.
  -Basic features; lacks RTC, watchdog, or advanced diagnostics.
  -Charging time around 3 hours; no fast charging.
  -Audible noise or hum possible in some setups.

## DFRobot Raspberry Pi 5 18650 Battery UPS HAT (5.1V 5A) [22]

Price: ~$50

* _Pros:_
  -Optimized for Raspberry Pi 5 with high 5.1V/5A output for demanding loads.
  -Supports up to 4x 18650 batteries for extended runtime (up to 10 hours).
  -I2C monitoring, power outage detection, and auto shutdown.
  -High-efficiency DC-DC converter (95%) with multi-protection.
  -Seamless power switching and compact design.

* _Cons:_
  -Batteries not included; must use unprotected 18650 cells.
  -No RTC or watchdog features.
  -Larger size (97x85mm) may not fit all enclosures.
  -Higher price point compared to basic HATs.
  -Potential polarity issues if not careful during setup.

## Sixfab Raspberry Pi Power Management & UPS HAT [11]

Price: ~$50

* _Pros:_

  -True UPS with seamless switching and wide input (5V-21V, solar compatible).
  -Onboard RTC, watchdog timer, and I2C monitoring for reliability.
  -Programmable power tasks, deep sleep modes, and cloud API integration.
  -Battery protection with temperature sensors and dynamic power management.
  -STEMMA QT/Qwiic connector for expansions.

* _Cons:_
  -Product retired due to component supply issues; availability limited.
  -Requires external battery (1x 18650 or LiPo).
  -More complex setup for advanced features like scheduling.
  -Higher power consumption in some modes.
  -Pogo pins may need soldering for soft power.

## Geekworm X728 UPS & Power Management Board [2]

Price: ~$45

* _Pros:_
  -High 5.1V/6A output (up to 8A max) for power-hungry setups.
  -Expandable battery capacity (2x 18650 base, up to 8+ cells).
  -RTC, buzzer alarm, I2C fuel gauge, and auto power-on.
  -AC loss detection, safe shutdown, and low battery auto-shutdown.
  -Compatible with Pi 5/4B/3B+/3B/2B.

* _Cons:_
  -Batteries not included; script installation required for full functionality.
  -Potential thermal issues at high currents without cooling.
  -Not compatible with some cases due to size.
  -May require custom enclosure for expansions.
  -Reverse polarity can damage board.

## MakerHawk Raspberry Pi UPS Power Supply [17]

Price: ~$30

* _Pros:_
  -LED power display for easy battery monitoring.
  -Synchronous charge/discharge with tap boot and long-press shutdown.
  -Multi-protection: overcurrent, overvoltage, short circuit, temperature.
  -Dual USB-A and Type-C outputs for versatility.
  -Affordable and acts as a power bank.

* _Cons:_
  -Requires 18650 batteries (not included); setup can be complex for UART features.
  -No RTC; sensitive to wiring/grounding.
  -Potential heat issues at higher currents.
  -Overkill for basic uses; lacks advanced watchdog.
  -Documentation lacks for some scenarios.

## 52Pi UPS Board with RTC & Coulometer [1]

Price: ~$20

* _Pros:_
  -Affordable with RTC and coulometer for precise monitoring.
  -I2C integration and battery level display in system.
  -Power outage detection and multi-protection.
  -OTA firmware updates in some variants.
  -Type-C output for modern compatibility.

* _Cons:_
  -Limited to lower outputs; not for high-power needs.
  -Batteries not included; requires careful polarity.
  -Potential auto-shutdown bugs in some units.
  -Basic design; may need scripts for full features.
  -Larger capacity batteries may need code adjustments.

## PiSugar S Plus Portable UPS [27]

Price: ~$45

* _Pros:_
  -Built-in 5000mAh LiPo battery for portability (up to 10+ hours).
  -Seamless UPS switch and safe low-battery shutdown.
  -Physical switch and expandable (solar/wireless).
  -Pogo pins free GPIO; compact design.
  -No I2C needed; hardware-based reliability.

* _Cons:_
  -No software monitoring (no I2C for battery status).
  -Higher price due to included battery.
  -Conflicts with I2C if using auto-boot features.
  -Limited output (5V/3A); not for high loads.
  -Manual restart after full drain.

## Geekworm X750 UPS HAT [16]

Price: ~$40

* _Pros:_
  -High 5.1V/8A max output for demanding applications.
  -Supports 4x 18650 (expandable); I2C monitoring and fuel gauge.
  -Safe shutdown, auto power-on, and multi-protection.
  -Reserves 40-pin GPIO for stacking.
  -Similar to X728 but more stackable.

* _Cons:_
  -Batteries not included; requires scripts for features.
  -Potential resonance/overshoot issues at high currents.
  -Heavier with more batteries; thermal management needed.
  -Not for Pi 5; compatibility limited.
  -Reverse connection risks damage.

## Sequent Microsystems Super Watchdog HAT with UPS [10]

Price: ~$60

* _Pros:_
  -Strong watchdog for system freezes; resets reliably.
  -RTC, battery monitoring, and overheating protection.
  -Flexible inputs (5V or 10-24V); multi-chemistry support.
  -ESD protection and self-check features.
  -Hours of runtime with 2x 18650.

* _Cons:_
  -Higher price; batteries not included.
  -Setup requires enabling I2C and commands.
  -Limited to 5V output; may need additional converters.
  -Stacking may conflict with other HATs.
  -Firmware updates needed for full functionality.

## Mini DC UPS Battery Backup (Generic Model, e.g., Shanqiu or Similar) [15]

Price: ~$35

* _Pros:_
  -Versatile multi-output (5V/3A USB, DC 5V/9V/12V up to 60W).
  -Built-in 20000mAh battery; acts as power bank.
  -Aluminum housing; supports simultaneous devices like router/modem.
  -Affordable external box design.
  -Long backup time for low-power devices.

* _Cons:_
  -Not a HAT; external and bulkier for Pi integration.
  -No Pi-specific monitoring or safe shutdown.
  -Potential polarity issues with DC outputs.
  -Not for high-power or seamless Pi stacking.
  -May not detect low voltage for auto-shutdown.

## SunFounder PiPower UPS [18]

Price: ~$20

* _Pros:_
  -Included 7.4V/2000mAh battery; 3-4 hours runtime.
  -Pass-through charging and multi-protection (overcharge/overheat).
  -Compact stand design (90x56x24mm); easy assembly.
  -Affordable for portable setups.
  -Compatible with Pi 4B/3B+/3B/Zero.

* _Cons:_
  -No advanced monitoring; basic LED indicators.
  -Limited output (5V/3A); not for heavy loads.
  -Potential data loss without software integration.
  -Assembly required; no RTC.
  -Battery life shorter than expandable options.

## Waveshare UPS HAT (E) [37]

Price: ~$35

* _Pros:_
  -High 5V/6A output with bi-directional fast charging (PD3.0 up to 40W).
  -Supports 4x 21700 batteries for longer runtime.
  -I2C fuel gauge for detailed monitoring (voltage, current, capacity).
  -Pogo pins for GPIO-free connection; USB-A output.
  -Auto reboot on power restore; system battery display.

* _Cons:_
  -Batteries not included; larger 21700 cells needed.
  -No RTC; higher price for features.
  -Potential low voltage warnings without config.
  -Charging time longer for larger batteries.
  -Compatibility mainly Pi 5/4B/3B+.

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
    - Shall operate within safe limits per UL 2054 to prevent thermal or electrical hazards.
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

Automated chessboards have emerged as innovative tools for enhancing gameplay, integrating automation and dynamic AI opponents. Below, we analyze multiple subsystem solutions to determine their suitability for addressing the challenges of affordability, automated capabilities, and accessibility.

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



### Peripheral Subsystem

_**Button Input and LED Response System**_

In this configuration, user input is handled through a small set of physical buttons, while system feedback is provided by LEDs. Each LED color corresponds to specific system states, such as move confirmation and error detection. This design is simple and inexpensive, but less intuitive and less scalable for complex command sets.

  * _Pros:_
  
    * Extremely simple, durable, and low-cost hardware.
    
    * Provides immediate and reliable feedback without display lag.
    
    * Highly power efficient and resilient to environmental noise.
    
  * _Cons:_

    * Does not meet hands-free accessibility goals of the project.
    
    * Not suitable for complex communication or detailed error reporting.
    
    * Requires user memorization of LED meanings or tone patterns.


_**Microphone and Computer-Voice Response System**_

This option uses a microphone for user voice commands and a synthesized computer voice for system feedback. The system reads back recognized commands, requests confirmation, and communicates status or errors verbally. It eliminates the need for a screen, relying entirely on audio-based interaction. While fully hands-free, this setup depends heavily on clear audio input and output, which can be unreliable in noisy or shared environments.

  * _Pros:_
  
    * Fully hands-free operation enhances user convenience and accessibility.
    
    * Provides a more interactive and conversational user experience.
    
    * Reduces physical hardware needs by removing displays or buttons.
    
  * _Cons:_
    
    * Audio feedback can be difficult to hear or distinguish in noisy environments.
    
    * Lack of visual feedback may lead to miscommunication or missed confirmations.
    
    * Requires reliable speech synthesis and recognition performance.
    
    * Adds processing overhead and complexity to handle real-time voice interaction.

_**Microphone and LCD Display System**_

This setup integrates a microphone for voice command input and an LCD display for visual feedback. The user speaks a command (e.g., "move knight to F3"), which the system processes and displays on the screen for confirmation. The LCD also reports move confirmations, invalid commands, or mechanical errors detected during operation. The player can then issue a "confirm" or "cancel" voice command to finalize or reject the action. This configuration provides a balanced mix of hands-free control and clear, visual verification for reliable gameplay.

  * _Pros:_
  
    * Offers clear, readable feedback for every system action and voice command.
    
    * Enables confirmation and error display directly on the board, improving user confidence.
    
    * Hands-free operation through voice commands enhances accessibility and modern design appeal.
    
    * Allows debugging and system messages to be shown without external devices.
    
  * _Cons:_
    
    * Requires both voice recognition and display integration, slightly increasing hardware and coding complexity.
    
    * LCD may have limited viewing angles or space for longer messages.
    
    * Voice command errors may require multiple attempts in noisy environments.

**Evaluation and Selection**

When evaluating the three interface approaches, key considerations included clarity of communication, accessibility, error handling, and ease of integration. The button and LED system, while simple and robust, cannot effectively convey complex messages or support conversational operation. The fully audio-based system offers modern appeal but lacks the reliability and clarity needed for precise chess move confirmations.

The Microphone and LCD Display System was selected as the most balanced and functional approach. It merges the hands-free convenience of voice input with the reliability of visual confirmation, allowing players to verify actions before execution. This hybrid interface supports clear communication, flexible debugging, and a polished user experience aligned with the chessboard’s intelligent design goals.

## High-Level Solution

This section presents a comprehensive, high-level solution aimed at efficiently fulfilling all specified requirements and constraints. The solution is designed to maximize stakeholder goal attainment, adhere to established constraints, minimize risks, and optimize resource utilization. Please elaborate on how your design accomplishes these objectives.


### Hardware Block Diagram

Block diagrams are an excellent way to provide an overarching understanding of a system and the relationships among its individual components. Generally, block diagrams draw from visual modeling languages like the Universal Modeling Language (UML). Each block represents a subsystem, and each connection indicates a relationship between the connected blocks. Typically, the relationship in a system diagram denotes an input-output interaction.

In the block diagram, each subsystem should be depicted by a single block. For each block, there should be a brief explanation of its functional expectations and associated constraints. Similarly, each connection should have a concise description of the relationship it represents, including the nature of the connection (such as power, analog signal, serial communication, or wireless communication) and any relevant constraints.

The end result should present a comprehensive view of a well-defined system, delegating all atomic responsibilities necessary to accomplish the project scope to their respective subsystems.

#### Processing Unit Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.

#### Control Unit Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.

#### Core XY Unit Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  

#### Peripherals Unit Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.  
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall conform to Section 508 of the Rehabilitation Act, ensuring accessible interfaces for users with disabilities.  
- Shall follow ergonomic layout guidelines from ANSI/HFES 100-2007, ensuring proper control placement and feedback.  
- Shall follow universal design principles to minimize cognitive and physical usability barriers.  

#### Power Unit Constraints: 
- Shall comply with FCC Part 15 Subpart B (Class B) for electromagnetic interference in residential environments.  
- Shall operate below 50 V DC, following UL low-voltage safety thresholds to eliminate the need for high-voltage insulation.  
- Shall meet NEC (NFPA 70) requirements for low-voltage indoor consumer systems.  
- Shall avoid any materials or configurations violating CPSC consumer electronics safety guidelines.
- Shall operate within safe limits per UL 2054 to prevent thermal or electrical hazards.
- Shall limit external surface temperatures to ≤104°F (40°C) during continuous operation (per UL 94 and general safety guidance).  
- Shall use cord sets and connectors compliant with NEC Article 400 for safe routing and reduced tripping risk.  
- Shall include grounding and protection per OSHA 1910 Subpart S to minimize shock hazards.  
- Shall include ANSI Z535.4-compliant warning labels for user-facing hazards such as moving parts and power indicators.  

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

## Atomic Subsystem Specifications

#### Processing Unit
The Processing Unit will consist of a Raspberry Pi responsible for coordinating all high-level system operations. Its primary functions are fourfold. First, it will interpret incoming audio signals from the microphone using the Vosk speech recognition engine to convert spoken commands into recognizable text, while also supplying power to the microphone. Second, it will maintain the internal state of the chessboard and verify the legality of player moves using the Stockfish chess engine. Third, it will transmit validated and legal move commands to the Control Unit (Arduino) for conversion into motion control instructions. Lastly, the Raspberry Pi will send display data to the screen, providing the user with real-time visual feedback on system activity and game status.

Functions:

  - Process voice commands and execute chess logic.
  - Coordinate overall system operations.
  - Communicate with user interface (microphone/display) and control logic.
    
Inputs:

  - Voice commands via Microphone.
  - System status from Control Unit.
  - Power from Power Unit.

    
Outputs:

  - Chess move instructions to Control Unit.
  - Feedback to user (via Screen Display).
    
Interfaces:

- Data exchange with Peripherals (Mic, Display).
- Data connection to Control Unit (Arduino).
- Power from Power Unit.
  
High-Level Requirements:

  - Shall process speech using Vosk speech recognition engine.
  - Shall interpret and validate moves using Stockfish chess engine.
  - Shall serve as the central decision-making and coordination hub.


#### Control Unit
The Control Unit will manage all motion control functions and serve as the intermediary between the Processing Unit and the mechanical subsystems. It will receive move instructions from the Raspberry Pi, interpret them into executable signals for the CoreXY motors, and transmit confirmation messages back to the Processing Unit. This will be achieved through the Arduino’s coordination of communication with stepper motor drivers housed within the Control Unit. The servo motor responsible for magnetic actuation will receive direct control signals from the Arduino to ensure precise vertical (Z-axis) movement.

Functions:

  - Translate move instructions into motor control signals.
  - Manage stepper motor drivers for coordinated movement.
  - Relay system status back to the Processing Unit.
    
Inputs:

  - Move commands from Processing Unit.
  - Power from Power Unit.

    
Outputs:

  - Control signals to motors.
  - Feedback to Processing Unit.
    
Interfaces:

  - Arduino microcontroller.
  - Motor Drivers.
  - Data connection with Processing Unit.
    
High-Level Requirements:

  - Shall convert logical chess moves into physical movement instructions.
  - Shall ensure movement reliability and position accuracy.


#### Core XY Unit
The CoreXY Unit will execute all physical motion required to reposition chess pieces on the board. Upon receiving step and direction commands from the Control Unit, it will drive two stepper motors to manipulate belts and pulleys that move a magnetic carriage across the X and Y axes. A servo-driven magnet will function as the Z-axis actuator, enabling the magnet to raise and lower as needed. This mechanism minimizes magnetic interference with nearby pieces and prevents unintentional displacement during movement.

Functions:

  - Physically move chess pieces on the board using a Core XY mechanism.
    
Inputs:

  - Power and control signals from Control Unit.
  - Power from Power Unit.

    
Outputs:

  - Physical movement of chess pieces.
    
Interfaces:

  - Stepper Motors (controlled by drivers).
  - Pulley system (for piece movement).
    
High-Level Requirements:

  - Shall move the chess pieces accurately to specified coordinates.
  - Shall allow for capturing, placing, and repositioning of chess pieces.
  - Shall execute moves smoothly and quietly.
    

#### Peripherals Unit
The Peripherals Unit consists of the system’s input and output devices — the microphone and display screen. The microphone captures user voice commands, potentially supported by software-based noise filtering to improve accuracy and clarity. The display provides feedback to the player by showing system messages such as “Not a Legal Move” or “Pawn to A5”, as well as overall game status updates. Together, these peripherals form the user interface that enables intuitive interaction with the system.

Functions:

  - Provide user interaction via input and output interfaces.
  - Capture voice commands and display system responses.
    
Inputs:

  - User voice input.
  - Data from Processing Unit.
  - Power from Power Unit.

    
Outputs:

  - Display messages, move feedback, and prompts to the user.
    
Interfaces:

The development of the Audio Actuated Chessboard—a robotic system that enables voice-commanded chess moves, automated piece movement via electromagnets and stepper motors, and integration with chess engines—presents a unique opportunity to blend recreational gaming with accessible technology. This section evaluates the project's ethical implications, professional responsibilities, and adherence to relevant standards, while assessing its broader impacts on culture, society, the environment, public health, public safety, and the economy. These considerations have directly shaped the conceptual design, imposing specific constraints, specifications, and practices to ensure responsible innovation.

### Ethical Situations Expected to Encounter
Several ethical challenges may arise during the project lifecycle. First, **privacy concerns** stem from the voice recognition component, which processes user audio inputs to interpret chess moves (e.g., "knight to e4"). Without proper safeguards, this could inadvertently capture unrelated conversations or sensitive data, raising issues of data consent and storage. To address this, the design incorporates on-device processing where feasible, and ensures audio is not persistently stored.

Second, **accessibility equity** is a key ethical tension: while the system aims to include visually impaired players, it could inadvertently exclude those with speech impairments or non-standard accents if the speech-to-text model lacks diversity in training data. Ethical sourcing of datasets (e.g., diverse voice samples) will be prioritized to avoid bias.

Third, **intellectual property (IP) risks** involve open-source chess engines (e.g., Stockfish) and hardware designs (e.g., Arduino libraries for stepper motors). Unattributed use could lead to plagiarism claims, so all code and schematics will be documented with licenses and contributions credited.

Finally, as a capstone project, team dynamics may introduce ethical dilemmas, such as unequal workload distribution or pressure to prioritize functionality over safety testing. Professional ethics, guided by the ACM Code of Ethics, will mandate transparent collaboration and peer reviews.

### Broader Impacts on the Community
The Audio Actuated Chessboard has predominantly positive, albeit modest, impacts across multiple domains, fostering inclusivity while mitigating potential negatives.

- **Cultural Impacts**: Chess is a global cultural artifact symbolizing strategy and intellectual heritage. This project enhances its cultural relevance by modernizing traditional over-the-board (OTB) play, appealing to younger, tech-savvy demographics and bridging analog and digital divides. It could revive interest in chess clubs or tournaments by making play more engaging and shareable (e.g., via integrated online play), potentially increasing cultural participation in underserved communities.

- **Societal Impacts**: On society, the board promotes cognitive health through accessible chess, which research links to improved problem-solving and memory. For the community—particularly students, hobbyists, and rehabilitation centers—it democratizes gaming, enabling remote or solo play against AI. Broader societal benefits include educational outreach; the open-source design could inspire STEM curricula, encouraging underrepresented groups to engage in robotics and AI. However, if commercialized, it risks widening the digital divide if priced accessibly only to affluent users.

- **Environmental Impacts**: As a low-volume prototype, direct environmental effects are minimal, but the design emphasizes sustainability to model responsible engineering. Components like neodymium magnets and lithium polymer batteries pose e-waste risks if not recycled; thus, modular hardware allows for easy upgrades and disassembly. Compared to mass-produced commercial boards (e.g., Square Off or GoChess), our DIY approach reduces manufacturing emissions by using off-the-shelf parts, potentially lowering the carbon footprint for hobbyist replication.

- **Public Health Impacts**: Positively, the system supports mental health by providing therapeutic, low-physical-effort recreation, ideal for elderly users or those with mobility limitations. Voice actuation reduces screen time versus app-based chess, promoting social interaction in group settings. No significant negative health risks are anticipated, assuming proper electromagnetic shielding to prevent interference with pacemakers.

- **Public Safety Impacts**: Safety is paramount in a device with moving parts (e.g., under-board actuators) and electrical components. Potential hazards include pinching from stepper mechanisms or electrical shorts, but these are mitigated through fail-safes. Overall, the project enhances safety by enabling contactless play, reducing germ transmission in shared environments like schools.

- **Economic Impacts**: For the local community (e.g., university ecosystem), the project boosts skill-building in high-demand fields like AI and mechatronics, potentially leading to startup opportunities or job placements. Economically, an open-source release could spur a niche market for custom boards, benefiting small-scale makers. However, it competes with commercial products, so IP strategies will balance innovation with fair competition.
  - Microphone (voice capture).
  - Screen Display (visual output).
  - Data connection with Processing Unit.
    
High-Level Requirements:

  - Shall receive voice input for game commands.
  - Shall display helpful information for the user while playing.

#### Power Unit
The Power Unit supplies regulated electrical power to all other subsystems. It will consist of a battery-based power source designed to provide multiple voltage levels to meet the varying current and voltage requirements of each component. The 12V rail will supply power to the stepper motors and drivers, while the 5V rail will support the Raspberry Pi, Arduino, and other control and peripheral electronics. Proper power regulation and distribution are essential to ensure safe, stable, and efficient system operation.

Functions:

  - Supply consistent power to all subsystems.
  - Enable portable and uninterrupted operation.
    
Inputs:

  - Wall outlet when charging

Outputs:

  - Regulated power to Processing, Control, Core XY, and Peripherals units.
    
Interfaces:

  - Power lines to each subsystem.
    
High-Level Requirements:

  - Shall provide stable power for all electronic components.
  - Shall have a large enough battery for extended gameplay.

Ethical, Professional, and Standards Considerations

The development of the Audio Actuated Chessboard—a robotic system that enables voice-commanded chess moves, automated piece movement via electromagnets and stepper motors, and integration with chess engines—presents a unique opportunity to blend recreational gaming with accessible technology. This section evaluates the project's ethical implications, professional responsibilities, and adherence to relevant standards, while assessing its broader impacts on culture, society, the environment, public health, public safety, and the economy. These considerations have directly shaped the conceptual design, imposing specific constraints, specifications, and practices to ensure responsible innovation.
Ethical Situations Expected to Encounter

Several ethical challenges may arise during the project lifecycle. First, privacy concerns stem from the voice recognition component, which processes user audio inputs to interpret chess moves (e.g., "knight to e4"). Without proper safeguards, this could inadvertently capture unrelated conversations or sensitive data, raising issues of data consent and storage. To address this, the design incorporates on-device processing where feasible, and ensures audio is not persistently stored.

Second, accessibility equity is a key ethical tension: while the system aims to include visually impaired players, it could inadvertently exclude those with speech impairments or non-standard accents if the speech-to-text model lacks diversity in training data. Ethical sourcing of datasets (e.g., diverse voice samples) will be prioritized to avoid bias.

Third, intellectual property (IP) risks involve open-source chess engines (e.g., Stockfish) and hardware designs (e.g., Arduino libraries for stepper motors). Unattributed use could lead to plagiarism claims, so all code and schematics will be documented with licenses and contributions credited.

Finally, as a capstone project, team dynamics may introduce ethical dilemmas, such as unequal workload distribution or pressure to prioritize functionality over safety testing. Professional ethics, guided by the ACM Code of Ethics, will mandate transparent collaboration and peer reviews.
Broader Impacts on the Community

The Audio Actuated Chessboard has predominantly positive, albeit modest, impacts across multiple domains, fostering inclusivity while mitigating potential negatives.

    Cultural Impacts: Chess is a global cultural artifact symbolizing strategy and intellectual heritage. This project enhances its cultural relevance by modernizing traditional over-the-board (OTB) play, appealing to younger, tech-savvy demographics and bridging analog and digital divides. It could revive interest in chess clubs or tournaments by making play more engaging and shareable (e.g., via integrated online play), potentially increasing cultural participation in underserved communities.

    Societal Impacts: On society, the board promotes cognitive health through accessible chess, which research links to improved problem-solving and memory. For the community—particularly students, hobbyists, and rehabilitation centers—it democratizes gaming, enabling remote or solo play against AI. Broader societal benefits include educational outreach; the open-source design could inspire STEM curricula, encouraging underrepresented groups to engage in robotics and AI. However, if commercialized, it risks widening the digital divide if priced accessibly only to affluent users.

    Environmental Impacts: As a low-volume prototype, direct environmental effects are minimal, but the design emphasizes sustainability to model responsible engineering. Components like neodymium magnets and lithium polymer batteries pose e-waste risks if not recycled; thus, modular hardware allows for easy upgrades and disassembly. Compared to mass-produced commercial boards (e.g., Square Off or GoChess), our DIY approach reduces manufacturing emissions by using off-the-shelf parts, potentially lowering the carbon footprint for hobbyist replication.

    Public Health Impacts: Positively, the system supports mental health by providing therapeutic, low-physical-effort recreation, ideal for elderly users or those with mobility limitations. Voice actuation reduces screen time versus app-based chess, promoting social interaction in group settings. No significant negative health risks are anticipated, assuming proper electromagnetic shielding to prevent interference with pacemakers.

    Public Safety Impacts: Safety is paramount in a device with moving parts (e.g., under-board actuators) and electrical components. Potential hazards include pinching from stepper mechanisms or electrical shorts, but these are mitigated through fail-safes. Overall, the project enhances safety by enabling contactless play, reducing germ transmission in shared environments like schools.

    Economic Impacts: For the local community (e.g., university ecosystem), the project boosts skill-building in high-demand fields like AI and mechatronics, potentially leading to startup opportunities or job placements. Economically, an open-source release could spur a niche market for custom boards, benefiting small-scale makers. However, it competes with commercial products, so IP strategies will balance innovation with fair competition.

Application of Identified Standards

The project has identified key standards organizations that inform the design, ensuring compliance, interoperability, and safety. These include:

    IEEE Standards Association (IEEE 802.15.4 for low-power wireless communication): Applied to Bluetooth or Zigbee modules for voice data transmission between the microphone and microcontroller. This standard ensures low-latency, energy-efficient connectivity, critical for real-time move actuation without lag that could frustrate users.

    ASTM International (ASTM F963 for toy safety, adapted for recreational devices): Guides material selection and edge rounding on the wooden board to prevent injuries, treating the chessboard as a "toy-like" interactive device.

    UL (Underwriters Laboratories) Standards (UL 60950-1 for IT equipment safety): Influences electrical design, specifying insulation and grounding for the 5-24V power supply to avoid shocks or fires.

    W3C Web Accessibility Initiative (WCAG 2.1 for voice interfaces): Ensures the speech recognition adheres to accessibility guidelines, such as providing text fallbacks for voice commands and supporting multiple languages/accents.

    ISO/IEC 27001 for information security: Applied to any data handling in voice processing, enforcing encryption for transmitted audio snippets.

These standards are not merely checkboxes; they are integrated into the requirements phase via traceability matrices, linking each to testable design elements (e.g., IEEE compliance verified through signal integrity tests).
Comprehensive Discussion: Influence on the Design

These ethical, professional, and standards considerations have profoundly influenced the conceptual design, transforming abstract concerns into actionable constraints, specifications, and practices. This iterative process—conducted through design reviews and ethical audits—ensures the final product is robust, equitable, and aligned with societal good.

Key influences include:

    Constraints Imposed: Privacy ethics constrained cloud reliance, mandating edge computing on a Raspberry Pi or Arduino, which limits processing power to lightweight models but ensures data sovereignty. Environmental concerns capped component count at <50 units per prototype, favoring reusable parts like salvaged steppers to minimize resource use. Safety standards (UL/ASTM) restricted voltage to 12V max and required physical barriers (e.g., acrylic underlay) around actuators, preventing hazards.

    Specifications Derived: Broader societal impacts drove accessibility specs, such as 95% voice command accuracy across accents (tested via diverse datasets) and adjustable audio feedback volumes (WCAG-compliant). Economic and cultural goals specified an open-source license (MIT) for schematics, with modular firmware for easy engine swaps (e.g., Stockfish integration). Professional ethics added logging features for auditing team decisions, ensuring transparency.

    Practices Implemented: Standards application manifests in validation protocols: IEEE tests for wireless reliability (e.g., <50ms latency) and ISO security scans for vulnerabilities. These practices address impacts holistically; for instance, public health specs include haptic feedback alternatives to voice, reducing exclusion risks, while economic practices like cost modeling (<$200 BOM) promote community replication.

In summary, these considerations elevate the project from a novel gadget to a thoughtful intervention in accessible gaming. By embedding them early, the design complies with expectations and allows for future scalability. Ongoing monitoring via post-prototype surveys will refine these elements, embodying continuous professional improvement.

### Application of Identified Standards
The project has identified key standards organizations that inform the design, ensuring compliance, interoperability, and safety. These include:

- **IEEE Standards Association (IEEE 802.15.4 for low-power wireless communication)**: Applied to Bluetooth or Zigbee modules for voice data transmission between the microphone and microcontroller. This standard ensures low-latency, energy-efficient connectivity, critical for real-time move actuation without lag that could frustrate users.

- **ASTM International (ASTM F963 for toy safety, adapted for recreational devices)**: Guides material selection and edge rounding on the wooden board to prevent injuries, treating the chessboard as a "toy-like" interactive device.

- **UL (Underwriters Laboratories) Standards (UL 60950-1 for IT equipment safety)**: Influences electrical design, specifying insulation and grounding for the 5-24V power supply to avoid shocks or fires.

- **W3C Web Accessibility Initiative (WCAG 2.1 for voice interfaces)**: Ensures the speech recognition adheres to accessibility guidelines, such as providing text fallbacks for voice commands and supporting multiple languages/accents.

- **ISO/IEC 27001 for information security**: Applied to any data handling in voice processing, enforcing encryption for transmitted audio snippets.

These standards are not merely checkboxes; they are integrated into the requirements phase via traceability matrices, linking each to testable design elements (e.g., IEEE compliance verified through signal integrity tests).

### Comprehensive Discussion: Influence on the Design
These ethical, professional, and standards considerations have profoundly influenced the conceptual design, transforming abstract concerns into actionable constraints, specifications, and practices. This iterative process—conducted through design reviews and ethical audits—ensures the final product is robust, equitable, and aligned with societal good.

Key influences include:

- **Constraints Imposed**: Privacy ethics constrained cloud reliance, mandating edge computing on a Raspberry Pi or Arduino, which limits processing power to lightweight models  but ensures data sovereignty. Environmental concerns capped component count at <50 units per prototype, favoring reusable parts like salvaged steppers to minimize resource use. Safety standards (UL/ASTM) restricted voltage to 12V max and required physical barriers (e.g., acrylic underlay) around actuators, preventing hazards.

- **Specifications Derived**: Broader societal impacts drove accessibility specs, such as 95% voice command accuracy across accents (tested via diverse datasets) and adjustable audio feedback volumes (WCAG-compliant). Economic and cultural goals specified an open-source license (MIT) for schematics, with modular firmware for easy engine swaps (e.g., Stockfish integration). Professional ethics added logging features for auditing team decisions, ensuring transparency.

- **Practices Implemented**: Standards application manifests in validation protocols: IEEE tests for wireless reliability (e.g., <50ms latency) and ISO security scans for vulnerabilities. These practices address impacts holistically; for instance, public health specs include haptic feedback alternatives to voice, reducing exclusion risks, while economic practices like cost modeling (<$200 BOM) promote community replication.

In summary, these considerations elevate the project from a novel gadget to a thoughtful intervention in accessible gaming. By embedding them early, the design complies with expectations and allows for future scalability. Ongoing monitoring via post-prototype surveys will refine these elements, embodying continuous professional improvement.



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


[1] https://52pi.com/products/52pi-ups-board-with-rtc-coulometer-for-raspberry-pi  
[2] https://geekworm.com/products/x728  
[3] https://lilygo.cc/products/lilygo%25C2%25AE-ttgo-t-display-1-14-inch-lcd-esp32-control-board  
[4] https://libre.computer/products/all-h3-cc/  
[5] https://libre.computer/products/aml-s805x-ac/  
[6] https://libre.computer/products/aml-s905x-cc/  
[7] https://libre.computer/products/aml-s905x-cc-v2/  
[8] https://microbit.org/buy/bbc-microbit-single/  
[9] https://onion.io/store/omega2/  
[10] https://sequentmicrosystems.com/products/super-watchdog-hat-with-battery-backup-for-raspberry-pi  
[11] https://sixfab.com/product/raspberry-pi-power-management-ups-hat/  
[12] https://store.arduino.cc/products/arduino-nano  
[13] https://store.arduino.cc/products/arduino-uno-rev3  
[14] https://wiki.pine64.org/wiki/ROCK64  
[15] https://www.amazon.com/Battery-Backup-Uninterruptible-Supply-Security/dp/B0C1YRSBMN  
[16] https://www.amazon.com/Geekworm-Raspberry-Management-Expansion-Shield/dp/B07VPWFK9H  
[17] https://www.amazon.com/MakerHawk-Raspberry-Uninterruptible-Management-Expansion/dp/B082CVWH3R  
[18] https://www.amazon.com/SunFounder-Raspberry-Expansion-Compatible-Included/dp/B0C1GFX5LW  
[19] https://www.beagleboard.org/boards/beaglebone-black  
[20] https://www.beagleboard.org/boards/pocketbeagle-original  
[21] https://www.clockworkpi.com/product-page/cpi-v3-1  
[22] https://www.dfrobot.com/product-2840.html  
[23] https://www.espressif.com/en/products/devkits/esp32-devkitc/overview  
[24] https://www.microchip.com/en-us/product/atmega328p  
[25] https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/  
[26] https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/  
[27] https://www.pisugar.com/products/pisugar-s-plus-raspberry-pi-ups  
[28] https://www.pjrc.com/store/teensy41.html  
[29] https://www.raspberrypi.com/products/raspberry-pi-2-model-b/  
[30] https://www.raspberrypi.com/products/raspberry-pi-3-model-b/  
[31] https://www.raspberrypi.com/products/raspberry-pi-4-model-b/  
[32] https://www.raspberrypi.com/products/raspberry-pi-5/  
[33] https://www.raspberrypi.com/products/raspberry-pi-pico/  
[34] https://www.raspberrypi.com/products/raspberry-pi-pico-2/  
[35] https://www.seeedstudio.com/Seeeduino-Nano-p-4111.html  
[36] https://www.seeedstudio.com/Seeeduino-V4-2-p-2517.html  
[37] https://www.waveshare.com/ups-hat-e.htm  
[38] https://www.waveshare.com/ups-hat.htm



## Statement of Contributions

Each team member is required to make a meaningful contribution to the project proposal. In this section, each team member is required to document their individual contributions to the report. One team member may not record another member's contributions on their behalf. By submitting, the team certifies that each member's statement of contributions is accurate.
