# R18 Circular Mount Correction 01

## Release status

**CAD geometry: PASS for the edited BREP and exported carrier mesh.**  
**Plate 02 package: HOLD.** The 3MF package and STL topology validate, but a Creality Print slice/toolpath review was not completed. The two supplied reference screenshots were not present as local files during this work, and the FreeCAD GUI render macro did not produce comparison images. Therefore no screenshot-to-screenshot match is claimed.

## Component and source

The corrected component is `PanYoke_EarBracket_KeyedDrive`. The editable source for the repair was the compact R17 FreeCAD BREP at `EyeTrace_Plate02_Compact_Carrier_Test/CAD/EyeTrace_CompactCarrier_Candidate.FCStd`. The current R18 lightweight CAD and Plate 02 project were preserved in `BACKUP/` before this revision. Plate 01 was not edited.

The compact R17 BREP was used as the geometric reference because the two requested image files were unavailable locally. This avoids deriving dimensions from screenshot pixels. The R18 relief was rebuilt as a corner-only web lightening cut, with a Ø46 mm cylindrical keepout about the pivot axis. This keeps the original curved pivot cut (CAD radius 20.1 mm) and its surrounding central region outside the relief cutter.

## Restored/retained circular-mount geometry

Measured from the source CAD geometry, not the screenshots:

| Feature | CAD value | Result |
|---|---:|---|
| Outer circular land radius | 35.3 mm | Preserved |
| Inner circular counterbore radius | 32.3 mm | Preserved |
| Counterbore axial interval | Z 33–37 mm | Preserved |
| Main circular land axial interval | Z 33–41 mm | Preserved |
| Central shaft opening | Ø8.0 mm | Preserved |
| Four mount-hole centers | X/Y = (±18, ±18) mm in the source local layout | Preserved |
| Curved pivot-relief radius | 20.1 mm | Preserved; Ø46 mm keepout used during local web relief |
| Bounding box | X −58.2…44.0, Y −35.3…35.3, Z 35.2…103.0 mm | Unchanged |

The redesigned upper web relief is limited to Y −20…20 mm and Z 45…99 mm with 3 mm corner radii. The web is 2.5 mm through the relieved panel regions; the source 8 mm perimeter rails remain. It removes 3,342.159 mm³ (8.021% of the compact source yoke). Overall height did not change.

The ring, counterbore, shaft opening and mount holes are below the relief window and were not touched by the Boolean. The pivot relief and central region were protected by the keepout. The source and output retain one valid solid.

## Deliverables

- Editable assembly: `CAD/EyeTrace_R18_CircularMount_Correction_01.FCStd`
- Corrected carrier STEP: `CAD/PanYoke_CircularMount_R18C1.step`
- Corrected carrier STL: `STL/PanYoke_CircularMount_R18C1.stl`
- Updated 12-part Plate 02 project: `PRINT/Plate02_R18_CircularMount_Correction_01.3mf`
- Combined bed STL: `PRINT/Plate02_R18_CircularMount_Correction_01.stl`
- Geometry extraction: `DOCUMENTATION/r18c1_geometry.json`
- Package validation script/results: `DOCUMENTATION/validate_r18c1_package.py`

## Validation completed

- FreeCAD 1.1.4 BREP: valid, one solid; output volume 38,324.180 mm³.
- Carrier bounds: unchanged from source.
- Corrected carrier STL: 48,384 facets; triangle-edge incidence check reports zero open or nonmanifold edges.
- All 12 supplied component STLs: binary size checks pass and triangle-edge incidence reports zero open/nonmanifold edges for each.
- 3MF: ZIP CRC check passes; 12 build items and 12 unique component names are present exactly once. These are the 12 Plate 02 parts; the circular base/Plate 01 is not included.
- Camera plate remains the unchanged `CameraPlate_21x14` mesh. Its nominal 21 × 14 mm pattern was not regenerated or modified.
- No part geometry other than the pan yoke was replaced in the 3MF.

## Not verified / HOLD items

- No actual Creality Print slice or layer preview was produced in this run. The 3MF is a project package, not evidence of sliced supports/toolpaths or print readiness.
- No new actual CAD screenshot was captured. The local FreeCAD GUI macro remained running without producing images; no substitute render is presented as a genuine screenshot.
- Exact match to the user's first reference image cannot be confirmed until those image files are available. The restored profile follows the original compact R17 CAD geometry.
- Mechanical clearances and physical SG90/horn fit are not certified by this focused geometry repair.

**Recommendation: keep this revision on HOLD for printing until the exact project is opened and sliced in Creality Print and the circular mount is visually checked against the supplied reference image.**
