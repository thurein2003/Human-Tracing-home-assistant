# Creality K2 ABS starting setup

The spool brand is unknown; the bundled profile is a starting point. Follow that spool maker's instructions within printer limits.

## Full 13-part bed
- Creality K2, 0.4 mm nozzle, 260 x 260 x 260 mm build area.
- Nozzle 255 C; bed 100 C. The K2 bed limit is 100 C, so do not select 105 or 110 C.
- 0.20 mm layers on every part; 4 walls; 35% gyroid; five top/bottom layers.
- Slim-tree supports on base, pan yoke and tilt cradle only. Supports are not fused into the STL.
- Brims: default 5 mm; base/cradle/pillar 6 mm; pan yoke 8 mm; outer-only, 0.1 mm object gap.
- Part fan 0-15%, off first five layers; chamber control disabled because K2 is not a heated-chamber model.
- Outer 35 mm/s, inner 55, infill 65, first layer 20; conservative accelerations are embedded.

## Seven fit coupons
0.20 mm layers, 3 walls, 100% rectilinear infill, 4 mm brim, supports off.

## Dimensional compensation
The custom profile uses 100% shrink factor (no scale compensation). XY hole/contour and elephant-foot compensation are zero. No measured spool shrink or calibration justifies compensation. Do not globally scale or alter the 21 x 16 mm centers. Measure fully cooled coupons first; any later compensation must be dimension-specific and supported by measured error.

## Open in Creality Print
Full bed: Creality_Print/EyeTrace_K2_ABS_Supported_Project_v2.3mf. It embeds all 13 parts, ABS settings, slim-tree support painting and brims. The STL is part geometry only and has no fused support solids.

Fit bed: FIT_TESTS/Creality_Print/EyeTrace_ABS_FitTest_Project_v5.3mf. Estimates are slicer estimates, not print guarantees.

