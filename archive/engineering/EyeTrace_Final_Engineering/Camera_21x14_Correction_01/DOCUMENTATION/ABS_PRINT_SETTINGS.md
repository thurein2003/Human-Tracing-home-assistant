# Creality K2 ABS settings

The revised full-bed and camera-coupon `.3mf` jobs were sliced with the installed Creality Print 7.3.1.6378 CLI profile/project data for the Creality K2, 0.4 mm nozzle.

## Full 13-part job

- ABS; nozzle 255 °C (project material range 250–260 °C); first-layer bed 100 °C as recorded in emitted G-code.
- Layer height 0.20 mm; four walls; 35% gyroid infill.
- Tree slim supports on the base, pan yoke, and tilt cradle only. No support on the camera plate, holes, spacers, or precision bores.
- Part-specific brim widths/support flags are retained in the Creality project. XY/hole compensation is zero; no global scaling or uncalibrated shrink compensation is applied.
- Actual slice estimate: 124.33 g, 11 h 45 m 59 s, 599 layers.

## Camera coupon

- 0.20 mm layers, 3 walls, 100% infill, 4 mm brim, support off; 255 °C nozzle and 100 °C first-layer bed in emitted G-code.
- Actual slice estimate: 1.35 g, 8 min 34 s, 10 layers.

Use the material maker’s ABS temperature range and the printer’s current limits. Enclosure/chamber, ventilation and bed preparation remain printer/material setup choices; the `.3mf` does not prove that the actual ABS spool will print without warping. Do not scale the coupon or assembly.
