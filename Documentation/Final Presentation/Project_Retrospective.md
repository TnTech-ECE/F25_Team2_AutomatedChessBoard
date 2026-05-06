# Project Retrospective

## Lessons Learned

- **Order and test parts as early as possible.** Our first screen arrived faulty and took out needed GPIO voltage pins. Because we tested early, we were able to reorder before it became a bottleneck.
- **Flatness of the playing surface is a critical mechanical requirement.** Individually, the acrylic bow, the mid-span wooden support, and the uneven CoreXY frame supports looked like minor assembly issues, but together they made two of our planned tests impossible to run.
- **Account for wire AWG throughout the design process** to manage thermal and current-load concerns.
- **Build small-scale prototypes and assemble all CAD drawings together** to physically surface design flaws earlier.
- **Be generous with tolerances.** It is always easier to remove more material later than to recover from removing too much.

## Future Work

### Playing Surface and Structure
- Improve playing-surface flatness with a stiffer board or additional supports to ensure consistent electromagnet pickup.
- Add a glass top (in place of the acrylic) for greater rigidity.
- If a glass top is added, sand down or shorten the wooden midsection support to match.

### Electromagnet and Pieces
- Replace the electromagnet with a stronger, higher-voltage alternative so it can sit lower and pieces no longer need to rely on base magnets to be held.
- Swap the current electromagnet mount for a lower-height mount. If the electromagnet is upgraded to a stronger one, raise the mount instead and reintroduce the washers in each chess piece in place of the neodymium magnets currently at each piece's base.

### Motion System
- Increase motion speed by raising the available motor voltage, optimizing microstepping settings, and reducing frictional losses in the CoreXY path.
- Improve adhesion of the jumper wires (for the stepper motor boosters) to the UPS.

### Software and AI
- Add selectable difficulty levels for the AI.
- Add the ability to redo moves.
- Fix an Arduino bug in the capture routine: pieces are occasionally dragged through the middle of the squares in the top or bottom discard rows.
