# Mechanical design

Eye Trace uses a base, pan yoke and tilt cradle with two TowerPro SG90 9 g servos and a cross-shaped horn interface. The [original archive index](../archive/README.md) records alternate assemblies, as-built evidence gaps and remapped duplicate paths.

## Selected camera correction

The recovered [native assembly](../hardware/3d-models/assembly/EyeTrace_Final_Assembly_Native_21x14.FCStd) and [camera coupon](../hardware/3d-models/fit-tests/Camera_Hole_Pattern_21x14_coupon.FCStd) open in FreeCAD 1.1.4. The camera hole axes measure ±10.5 mm horizontally and ±7 mm from the pattern center vertically. The edited layout retains an internal object name ending in 21x16, while its small bores measure 21 × 14 mm. The PCB envelope shown in the original drawings is a separate reference.

The [full-bed STL](../hardware/3d-models/STL/EyeTrace_Final_K2_SingleBed_21x14.stl) contains 13 closed components. The [native geometry test](../results/cad-readback.json) lists reopened document objects and mesh sizes. The historical motion study covers sampled axes and poses. The modeled rear uncertainty volume intersects the camera fasteners, so rear-component clearance remains open. Use the [manufacturing procedure](../hardware/printing/manufacturing.md) for physical verification.

## Clearance work

The original coupon series tests pan diametral gaps of 0.10, 0.20, 0.30, 0.40 and 0.60 mm. For a 5.00 mm tilt journal, the alternate bores are 5.05, 5.10, 5.15, 5.20 and 5.30 mm. Treat those as test choices, with nominal controls of 0.60 mm pan and 5.20 mm bore. The printable horn tests include Prototype 03 and subsequent revisions. No physical pass was recorded for the selected interfaces during this collection.

Use the original servo horn screw. The corrected BOM models M2 × 12 screws and nuts as provisional camera hardware. M1.6 × 8 was reported as evaluated during development. Check the actual camera, rear components and board clearances before selecting screw diameter, length or torque. The corrected engineering BOM calls for four M3 × 10 structural screws and matching nuts at its indicated joints.

## Design files

| Artifact | Purpose |
| --- | --- |
| [Native assembly](../hardware/3d-models/assembly/EyeTrace_Final_Assembly_Native_21x14.FCStd) | Constraints and simulated poses |
| [Editable assembly](../hardware/3d-models/FreeCAD/EyeTrace_Final_Assembly_21x14.FCStd) | Corrected mechanical assembly |
| [Editable layout](../hardware/3d-models/FreeCAD/K2_PrintLayout_21x14.FCStd) | Corrected print-bed layout |
| [STEP assembly](../hardware/3d-models/STEP/EyeTrace_Final_Assembly_21x14.step) | Neutral solid exchange |
| [Historical revisions](../archive/engineering) | Candidate assemblies, part files, engineering checks and motion studies |
