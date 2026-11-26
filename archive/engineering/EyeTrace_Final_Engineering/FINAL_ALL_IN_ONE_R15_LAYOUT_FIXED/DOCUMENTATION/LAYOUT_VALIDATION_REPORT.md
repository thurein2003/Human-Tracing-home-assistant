# R15 Fixed Build-Plate Layout Validation

**Status:** Geometry and placement validation PASS. Slicer toolpath validation UNVERIFIED. Physical SG90 horn fit remains UNVERIFIED.

## Output

- 3MF: `EyeTrace_K2_ABS_All_In_One_R15_Fixed.3mf`
- Individual STL files: `STL/` (13 parts)
- Build-plate image: `RENDERS/EyeTrace_R15_Fixed_Build_Plate.png`
- Machine-readable placement checks: `CHECKS/layout_validation.json`
- Exact exported-3MF pairwise intersection results: `CHECKS/actual_pairwise_mesh_intersections.json`

The original R15 files were not modified. This new 3MF changes placement only; meshes were translated without scaling, remeshing, or simplification. Individual STL files are byte-identical copies of the source part STLs.

## Parts on plate

1. Base_EarMount_ThrustSupport
2. Pan_Replaceable_ThrustRing
3. PanYoke_EarBracket_KeyedDrive
4. Tilt_Removable_IdlerPillar
5. Pan_KeyedHorn_Cover
6. TiltCradle_KeyedHorn_CameraFrame
7. Tilt_KeyedHorn_CaptiveCover
8. Tilt_Journal_FlangedSleeve
9. PCB_Spacer_Lower_Left
10. PCB_Spacer_Lower_Right
11. PCB_Spacer_Upper_Left
12. PCB_Spacer_Upper_Right
13. CameraPlate_21x14

## Geometry and placement checks

| Check | Result |
|---|---|
| 3MF archive reopened and parsed | PASS |
| Mesh objects / build items | 13 / 13 |
| Components compared against source STL facets | PASS, all 13; maximum inverse-translation vertex deviation < 0.000000071 mm |
| Individual mesh closure / positive volume | PASS, carried from source meshes without facet edits |
| Connected mesh component count | PASS, one per each of 13 meshes |
| Transformed 3D mesh-pair checks | PASS, 78 pairs; zero detected intersections |
| XY part-to-part minimum clearance | 16.0 mm |
| Minimum remaining gap after configured brim widths | 5.0 mm |
| Overall XYZ bounds | X 13.0–234.0 mm; Y 13.0–227.5953 mm; Z 0–77.0 mm |
| Inside 260 × 260 mm bed | PASS |
| All object bottoms at Z=0 | PASS |
| Accidental floating / buried / inverted placements | None indicated by the exported mesh bounds and placement checks |

The minimum 5.0 mm post-brim spacing is based on configured brim widths: base 6 mm, pan yoke 8 mm, tilt cradle 6 mm, idler pillar 6 mm, and 5 mm for the other parts. It is not a slicer-generated support-envelope measurement.

## Preserved mechanical geometry

All 13 object meshes match the original verified individual STL facets after reversing only their rigid placement translations. The layout operation does not alter geometry. The source validation records the specified R15 interface invariants: 39.2 mm horn-pocket envelope (19.6 mm reaches each side), 20.2 mm short-axis span, 1.7 mm arm recess, Ø8 mm center opening, and camera-hole spacing 21 × 14 mm. This task verifies preservation by unchanged component mesh facets; it does not independently certify the physical horn interface.

## Supports and print preparation

The 3MF carries the existing slicer settings: tree-slim support enabled for the base, pan yoke, and tilt cradle; supports disabled for the other parts. Brim widths are as listed above. The 3MF itself contains the part meshes; support structures are slicer-generated and therefore are not included in mesh intersection or XY-spacing checks. Confirm support branches do not land on functional interfaces in Creality Print preview before printing.

## Slicer inspection limitation

Creality Print 7.2 was available and the repaired project opened with all 13 components. A reliable completed slice/Preview capture could not be obtained in this session. Therefore:

- Actual ABS filament mass: **not verified**
- Estimated print time: **not verified**
- Layer-by-layer toolpaths, generated support footprints, first-layer contact, and support collisions: **not verified**

Open the provided 3MF in Creality Print 7.2, select the Creality K2 and the intended ABS profile, slice the plate, inspect Preview at all layers, then verify the displayed mass/time and support contact before printing.

## Release note

The repaired 3MF passes exported-geometry and bed-placement validation and contains no detected component intersections. It is **not slicer-validated for printing** until the actual toolpath preview and support footprints are inspected. The R15 SG90 cross-horn physical fit remains unverified; this layout repair does not change that status.
