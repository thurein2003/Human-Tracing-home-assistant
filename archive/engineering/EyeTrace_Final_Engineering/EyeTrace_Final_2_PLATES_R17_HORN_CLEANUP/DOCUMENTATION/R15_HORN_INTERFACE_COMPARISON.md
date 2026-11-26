# R15 horn-interface comparison — R17 cleanup

## Verdict

| Interface | Result |
|---|---|
| Pan yoke | **PASS — exact R15 pocket void in CAD** |
| Tilt cradle | **PASS — exact R15 pocket void in CAD** |
| Center opening | **PASS — Ø8.0 mm in the R15 profile** |
| Camera mounting pattern | **PASS — untouched source component retains 21 × 14 mm nominal centers** |

This is a CAD geometry result. It does not establish physical fit of the newly integrated carriers, and it is not a slicer or print-readiness approval.

## Reference and method

Master: `CrossHorn_ABS_Revision_01/PROTOTYPE_04_REVISION_15/CrossHorn_UltraMinimal_FitTest_04R15.FCStd`.

The pan and tilt carrier solids were rebuilt in FreeCAD 1.1.4 from their editable R16 assembly geometry. The previous horn-seat region was cut back to a circular Ø41.0 mm local seating land, then the exact master BREP horn negative was subtracted at the corresponding output face. Four existing retainer-screw bores (Ø3.3 mm) and the master Ø8.0 mm center opening were maintained as distinct openings. The master coupon was not changed.

Comparison used the actual BREP voids in the mapped local seat coordinates, not labels or bounding boxes alone. Difference volumes within the R15 horn-pocket envelope:

| Feature | Pan | Tilt |
|---|---:|---:|
| Unwanted extra void vs R15 | 0.000 mm³ | 0.000 mm³ |
| Missing R15 void | 0.000 mm³ | 0.000 mm³ |
| Pocket envelope | 39.2 × 20.2 mm | 39.2 × 20.2 mm |
| Recess depth | 1.7 mm | 1.7 mm |
| Center opening | Ø8.0 mm | Ø8.0 mm |
| Independent retainer bores | 4 × Ø3.3 mm | 4 × Ø3.3 mm |

The earlier geometry had additional void inside the R15 comparison envelope (approximately 892.461 mm³ pan and 148.415 mm³ tilt). These were obsolete slot/cutout regions, not part of the R15 horn shape. The rebuilt seat removes those extra cuts while retaining the documented retainer bores.

## Geometry and exports

Both rebuilt carrier BREPs are valid single solids. The final mesh exports are closed solids. The two updated 3MF files each contain 13 mesh resources and 13 component resources; their build lists contain one plate object and twelve plate objects respectively (13 components total). Other component meshes and project settings were retained from the source two-plate projects. The camera plate was not edited.

The after top views are orthographic drawings generated from the saved BREP edges. The section images are BREP-derived section edge drawings; they are not screenshots captured from the FreeCAD GUI. Existing “Before” images are the source FreeCAD views.

- Pan top: `../RENDERS/After_Pan_Interface_BREP_View.png`
- Pan section: `../RENDERS/After_Pan_Interface_BREP_Section.png`
- Tilt top: `../RENDERS/After_Tilt_Interface_BREP_View.png`
- Tilt section: `../RENDERS/After_Tilt_Interface_BREP_Section.png`

## Limits

No new assembly-wide motion or interference sweep was run. No Creality Print slicing or support/brim inspection was performed for these updated 3MFs. Both plate projects therefore remain **HOLD** pending slicer verification. Physical fit of the integrated pan and tilt interfaces is not established by this BREP comparison.
