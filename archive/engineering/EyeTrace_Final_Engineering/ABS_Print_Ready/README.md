# Eye Trace — ABS Print Preparation

This is a print-preparation add-on to the existing validated CAD project. Original PETG files and the full-print release status are preserved. No physical fit tests have been performed.

## Open this first

Open `Creality_Print/EyeTrace_K2_ABS_Supported_Project_v2.3mf` in Creality Print 7.3.1.6378. It contains all 13 printable components, ABS profile settings, painted slim-tree supports, per-part brims and 0.20 mm layers. Review the plate and slice again in the installed slicer before printing. Do not use the older unversioned 3MF draft.

The single-bed STL at `STL/EyeTrace_K2_ABS_SingleBed.stl` contains the 13 translated part meshes only; supports are slicer-generated and are in the 3MF project, not fused into this STL.

## Print the fit bed before the complete design

Use `FIT_TESTS/Creality_Print/EyeTrace_ABS_FitTest_Project_v5.3mf` for the seven ABS fit coupons. The matching plain STL is `FIT_TESTS/STL/EyeTrace_ABS_FitTests_SevenCoupons_FINAL.stl`. Read `FIT_TESTS/ABS_FIT_TEST_GUIDE.html` first. The original SG90 servos and horns, camera, and hardware are needed for their respective checks.

## Actual slicer results

- Full bed: 13 parts, 599 layers; 124.34 g (49.71 m) and estimated 11 h 46 m 25 s.
- Fit bed: 7 coupons, 21 layers; 12.06 g and estimated 1 h 21 m 12 s.
- Both final slices completed with Creality Print CLI exit code 0 and no reported slicing warnings. These are software estimates, not guaranteed consumption or time.
- `RENDERS/ABS_FullBed_FirstLayer_ActualToolpaths.png` and the coupon guide images are plotted from actual sliced G-code.

## ABS starting conditions

255 C nozzle, 100 C bed (the base K2 bed limit), 0.20 mm layers, four walls and 35% gyroid for the complete bed. Three walls, full rectilinear infill, supports off and 4 mm brim for the coupons. The filament maker’s instructions take precedence within printer limits. Chamber control is disabled; do not apply global scaling or shrink compensation without calibration measurements.

## Release status

The ABS projects are slicer-checked and fit-test ready. Physical dimensional fit, shrinkage, warping, support removal, strength and motion are not verified. Full-print readiness and the existing release status remain unchanged pending coupon/hardware checks.
