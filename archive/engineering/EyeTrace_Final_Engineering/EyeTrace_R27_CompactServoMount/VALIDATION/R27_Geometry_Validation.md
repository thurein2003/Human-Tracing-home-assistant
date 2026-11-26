# Eye Trace R27 compact servo mount

The R26 STL came from the R25 FreeCAD assembly. R27 modifies only its `TiltCradle_KeyedHorn_CameraFrame` solid. Assembly coordinates and the inherited print orientation are retained.

| Measurement | R26 | R27 |
| --- | --- | --- |
| Circular outer flange | Ø42 mm | Removed |
| Ordinary mounting web, six measured sections | 8.0 mm | 2.5 mm |
| Nominal compact web plan around the frame root | — | 33 × 38.5 mm, plus short root transition and local seats |
| Overall mount body depth away from the frame root | 8.0 mm | 7.0 mm at the localized screw seats |
| Full end-region envelope including the frame root | 8.0 mm | 8.0 mm |
| Material section area at 0.05 mm from the original mounting datum | 1,096.73 mm² | 395.61 mm² |
| Cradle volume | 24,742.03 mm³ | 19,686.93 mm³ |

The remaining rib follows the keyed horn pocket and four original fastener positions. The shaft center remains at assembly Y=0 and Z=78 mm. The horn-cover mating datum remains at X=−41 mm. The pocket retains its 1.7 mm depth, the central service bore remains Ø8 mm, and the four Ø3.3 mm through-bores retain their bearing seats. The local head pockets provide at least Ø5.6 × 3.0 mm of clear head space, with the original screws and nuts in their original locations. The separate horn cover remains part of the source assembly and the K2 job contains the revised cradle only.

The FreeCAD shape recomputed as one valid solid and passed the BREP check. The unmodified upper frame, camera rails, all other part shapes and placements, the 21 × 14 mm camera pattern, and Plate 01 were verified against the source. The STEP reimport matched the revised solid. The STL reopened as one watertight mesh, and its triangles match the editable K2 project.

At neutral, the CAD model shows 1.50 mm clearance to the SG90 body and approximately 0.10 mm to the provisional horn. The relocated surfaces introduce zero interference at neutral or at the 15 tested tilt angles through ±45°. The original horn engagement was reproduced at every tested relative horn angle in both directions. Physical horn fit, servo travel, and printed strength remain unverified.

Creality Print 7.3.2.6412 completed the ABS slice for the K2 with a 0.4 mm nozzle, textured PEI, and automatic tree supports. It estimated 3 h 43 min and 31.39 g for 616 layers. The separate sliced package passed CRC and the embedded G-code checksum. The editable project is the plain .3mf file.

The rear close-up comparison uses a single camera for both solids. Its direction was reconstructed from the R26 Creality screenshot, included separately as a reference crop.

The machine-readable measurements and export hashes are in [R27_Geometry_Validation.json](R27_Geometry_Validation.json).
