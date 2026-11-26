# Plate 02 final mechanical and print validation

## Release verdict
**HOLD.** This folder preserves the latest Plate 02 repair candidate for review. It is not a print approval. Plate 01, its circular base geometry, and its print file were not modified or copied as part of the repair operation.

## Tilt horn / screws
The local CAD probe reports 10.602875 mm³ common volume between the simplified tilt horn proxy and each of two TiltDrive M3x10 screw solids. It reports 73.263511 mm³ between the same proxy and the SG90 reference at the output axis. The proxy is a simplified solid without measured small horn holes or the actual underside/axial shape. Therefore these overlaps **cannot distinguish actual interference from proxy material that should be relieved by the horn's real holes or intended shaft engagement**. No screw was moved and no carrier material was removed based on this proxy result. Verdict: **UNVERIFIED / HOLD** pending measured horn hole coordinates/diameters and axial geometry or direct assembly confirmation.

## R15 pocket comparison
Master source BREP is `CrossHorn_ABS_Revision_01/PROTOTYPE_04_REVISION_15/CrossHorn_UltraMinimal_FitTest_04R15.FCStd`. Master cutter reports 39.2 × 20.2 mm envelope, 1.7 mm depth, and Ø8.0 mm center bore. The repaired pan carrier was cut with the exact transformed master tool and has 0.000 mm³ intersection with its pocket void. The tilt carrier probe records those nominal values and valid one-solid geometry, but a direct transformed BREP Boolean/deviation comparison of the complete tilt pocket against the R15 master was not executed in this run. Tilt exact-profile match is **UNVERIFIED**; dimensions alone are not a shape-identity check. No R15 geometry was changed in this validation.

## Assembly checks
- Pan repaired carrier: valid one main solid; zero measured carrier common volume against the checked retainer, four screw models, servo body, unchanged-base thrust support, and thrust ring. Pan axis transform is inherited unchanged from the R16 source.
- Tilt carrier: valid one solid; local checks show zero carrier common volume against the tilt cover, four screw models, servo reference, idler pillar, journal sleeve, idler bolt, and washer. These are static overlap results, not surface-gap measurements.
- Tilt horn proxy screw intersections remain unresolved as above.
- Native joint graph, complete assembly/disassembly sequence, representative motion sweep, and quantitative minimum clearances were not verified. Motion clearance: **HOLD**.
- Camera mounting pattern remains nominally 21 × 14 mm in source checks; no camera component was modified.
- Base compatibility: carrier-to-base thrust support common volume is 0.000 mm³ in the local check; the R16 base geometry/transform was unchanged. This does not certify all assembly contacts or free rotation.

## Plate 02 package
The exact copied 3MF is a valid ZIP package with 12 build items (IDs 102–113); the final-validation STL folder contains 12 part files. Creality Print 7.2.1 is installed, but an interactive slicer session and completed slicing/toolpath inspection could not be performed in this run. Consequently first-layer paths, supports/interfaces, brim clearance, precision pocket layers, and overhang paths remain **UNVERIFIED**. No screenshot of sliced preview is included.

Inherited project metadata—not independently confirmed slicer settings—lists K2, 0.4 mm nozzle, Generic ABS, nozzle 255 °C (first layer 250 °C), textured PEI, bed first layer 70 °C, 3 walls, 20% gyroid, fan 0–15%, and 5 mm brim. The actual spool guidance/build surface compatibility has not been verified.

| Metric | Result |
|---|---|
| Printable components | 12 |
| ABS consumption | Not available; exact plate not sliced |
| Print time | Not available; exact plate not sliced |
| Mechanical release | HOLD |
| Slicer release | HOLD |

## Required to release
1. Compare the actual white tilt horn’s axial geometry and small-hole centers/diameters against the screw positions; confirm screw compatibility without forcing M3 into the horn.
2. Directly compare the transformed tilt-pocket BREP to the R15 master BREP.
3. Verify assembled tilt/pan motion, screw access, base rotation, and practical installation/removal.
4. In Creality Print 7.2.1, open the exact copied Plate 02 3MF, select the actual K2/ABS setup, slice fully, inspect all first-layer/support/horn-pocket toolpaths, and capture slicer previews. Save the sliced project under a new name only after those checks pass.

This validation did not change any CAD geometry. Corrected STLs were not generated because no additional geometry change was justified by the proxy evidence.

## 2026-11-18 addendum — Plate 02 slice completed

Creality Print opened the exact Plate 02 source and completed slicing. The embedded slicer build is 7.3.2.6412 (the installation path/registry calls the folder 7.2). Preview reports 94.26 g ABS / 37.68 m and 10 h 21 min. K2, 0.4 mm nozzle, Textured PEI, EyeTrace ABS 255C K2 100C; 255 °C nozzle, 100 °C textured plate, fan 0–15%, 3 walls, 20% gyroid, tree supports and global 5 mm brim. Sliced preview screenshot: `RENDERS/Plate02_Sliced_Toolpaths.png`.

The tilt pocket has a direct BREP difference result of 0.000 mm³ extra void and 0.000 mm³ missing void versus the R15 master. Static minimum clearances and sampled local ±20° carrier diagnostics are documented in `EyeTrace_R17_PLATE_02_ASSEMBLY_REPAIR/REPORTS/PLATE02_BLOCKER_RESOLUTION.md`.

Plate 02 remains **HOLD**: the two 10.603 mm³ tilt proxy/screw intersections cannot be resolved without actual horn-hole dimensions; intended travel limits/full rigid-body motion were not established; first-layer and critical pocket-layer inspection is incomplete. No job was sent. Plate 01 remains untouched.

Sliced project: `EyeTrace_R17_PLATE_02_ASSEMBLY_REPAIR/PRINT/EyeTrace_R17_Plate_02_ABS_SLICED_HOLD.3mf`.
