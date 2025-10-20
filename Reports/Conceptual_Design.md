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
