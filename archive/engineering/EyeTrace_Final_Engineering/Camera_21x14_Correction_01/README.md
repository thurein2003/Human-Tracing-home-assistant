# Eye Trace camera correction — 21 × 14 mm

This independent revision corrects the camera mounting-hole center pattern from 21 × 16 mm to the user supplied 21 × 14 mm. The existing PCB envelope remains a separate provisional 38 × 38 × 1.6 mm parameter. Previous candidates and print files remain unchanged.

## Main files

- Editable assembly: `CAD/EyeTrace_Final_Assembly_21x14.FCStd`
- Updated native simulation assembly: `CAD/EyeTrace_Final_Assembly_Native_21x14.FCStd`
- STEP assembly: `CAD/EyeTrace_Final_Assembly_21x14.step`
- Exact full-bed Creality Print project: `Creality_Print/EyeTrace_K2_ABS_Full_21x14.3mf`
- Full-bed STL matching those 13 project meshes: `STL/EyeTrace_Final_K2_SingleBed_21x14.stl`
- Camera coupon to print first: `FIT_TESTS/Camera_Hole_Pattern_21x14_ABS.stl`
- Coupon Creality Print project: `FIT_TESTS/Camera_21x14_ABS_FitTest.3mf`
- Actual sliced coupon and full-bed G-code: `CHECKS/SLICE_CAMERA/plate_1.gcode` and `CHECKS/SLICE_FULL/plate_1.gcode`
- Validation: `CHECKS/final_validation.json`, `CHECKS/motion_collision_validation.json`, `CHECKS/native_motion_validation.json`

## Actual FreeCAD images

- `RENDERS/assembly_21x14_iso.png`
- `RENDERS/camera_mount_21x14_iso.png`
- `RENDERS/camera_plate_21x14_front.png`
- `RENDERS/camera_coupon_21x14_top.png`
- `RENDERS/k2_13_part_bed_21x14.png`

## Release

CAD geometry, STEP/STL readback, corrected pattern, native simulation and slicer jobs pass their software checks. Camera hardware fit remains unverified. The provisional rear-component envelope intersects the modeled four M2 screw assemblies, so full printing remains on hold pending actual-camera rear clearance inspection and a successful coupon test.
