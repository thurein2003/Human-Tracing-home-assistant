# Fresh Creality toolpath inspection

Both `.3mf` files were actually loaded and sliced by the installed Creality Print CLI. The emitted G-code reports application version 7.3.1.6378; no warning, invalid-mesh, outside-bed, or conflict warning appeared in the slicer logs. `conflict_check` in the log is the slicer's normal check stage, not a reported conflict.

## Full 13-part ABS plate

- 13 build items and meshes; 599 layer-change markers and 952,239 extrusion moves.
- Model G-code bounds: X 12.00–229.10, Y 12.00–230.00, Z 0–67.18 mm.
- Actual extruding path bounds, including brim and support: X 6.644–228.788, Y 6.644–234.439 mm. All are inside the 260 × 260 mm build area.
- Slicer estimate: 124.33 g ABS, 11 h 45 m 59 s.
- G-code contains 546 support feature blocks. Per-object Creality settings enable tree_slim support for the base, pan yoke and tilt cradle; camera plate and all precision interface components have support disabled.
- First layer has 21,510 extrusion moves. G-code has 599 layers, matching its header. No unanchored-island or mesh-import error was logged.

## Camera pattern coupon

- Single mesh/build item; 10 layer-change markers and 6,858 extrusion moves.
- Extruding path bounds including brim: X 116.972–153.028, Y 93.972–123.028 mm.
- Slicer estimate: 1.35 g ABS, 8 min 34 s. No support feature blocks; four-millimeter brim retained.

These checks establish that the revised jobs slice and fit on the defined bed. They do not establish actual camera fit, correct ABS shrinkage for a particular spool, or successful physical printing. The output G-code is retained in `../CHECKS/SLICE_FULL/plate_1.gcode` and `../CHECKS/SLICE_CAMERA/plate_1.gcode` for inspection.
