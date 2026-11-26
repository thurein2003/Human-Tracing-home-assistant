# Eye Trace R30 flat mounting plate

R30 removes the four topside bosses and the raised horn-pocket ridge from the R29 tilt cradle. The mount-to-frame transition ends before the nearest fastener land. The vertical frame, camera mount, Plate 01 and all existing component geometries and placements are preserved.

| Verification | Result |
| --- | --- |
| Ordinary thickness at eight locations | 2.50 mm |
| Flat upper and lower planes on the mounting web | Assembly X=−38.50 mm and X=−41.00 mm |
| Raised material in the mounting area above the top plane or below the bottom plane | 0 mm³ |
| Fastener holes | Four Ø3.30 mm bores, with the inherited centers |
| Central driver opening | Ø8.00 mm, centered on the existing shaft |
| Material removed from R29 | 512.55 mm³ |

The recessed SG90 key geometry and mating height are identical to R29. The 1.7 mm key recess leaves a 0.8 mm floor at the two mounting holes along the long horn axis. Those are the locations requiring load distribution. In CAD, a flat metal washer with a 3.3 mm bore, 8 mm outside diameter and 1.5 mm thickness spans the pocket edges with 12.81 mm² of full-thickness plate support under each of those two washers.

Use a 1.5 mm spacer washer under each existing M3 screw head to take up the gap left by removal of the bosses. The four virtual washers seated against both the flat plate and existing heads with zero positive-volume interference. This preserves the original 2.4 mm modeled screw-to-nut engagement. The delivered CAD retains the original hardware references, and the print project contains the cradle only. Physical horn fit and clamping strength have not been tested.

FreeCAD verified one valid solid, exact keyed engagement against the inherited provisional horn, and zero interference at neutral and at 19 sampled tilt poses from −45° to +45°, including the spacer washer envelopes. The STEP reimport matched the revised solid. The STL reopened as one watertight mesh, and the flat-face areas recovered from its triangles match the CAD. The Creality K2 project contains the exact STL mesh. Creality Print completed the ABS slice with tree supports and estimated 3 h 30 min and 29.08 g. The delivered 3MF is the editable project.

The matched screenshots show the mounting plate from above and from the low side. The upper camera plate is clipped out of the top views so the mounting-hole lands can be inspected.

[Detailed geometry and export checks](R30_Geometry_Validation.json)
