# R21 Double Mounting Plate Repair

**Status: MECHANICAL GEOMETRY CANDIDATE — PRINT HOLD**

## Change scope

The two horizontal layers were separate FreeCAD components: the pan yoke (PanYoke_EarBracket_KeyedDrive) and its removable lower horn retainer (Pan_KeyedHorn_Cover). The lower cover has a real retention/support role, so it was not deleted. Its broad plate material was replaced by four connected radial support arms, a narrow annular bridge around the center access, and the four existing screw-pad regions. This leaves the yoke as the only broad mounting plate.

Only Pan_KeyedHorn_Cover geometry changed. Plate 01, the pan yoke, servo references and positions, camera components, and all other component BREP shapes remain unchanged. The R20 file set remains preserved.

## Measured CAD results

| Check | Result |
|---|---:|
| Original lower cover volume | 3022.479 mm³ |
| Revised retainer volume | 1271.111 mm³ |
| Removed material | 1751.368 mm³ (57.94%) |
| Revised retainer BREP | Valid, 1 connected solid |
| Retainer Z envelope | 30.8–35.0 mm (4.2 mm local stack envelope retained) |
| Yoke-to-retainer gap | 0.200 mm |
| Horn-proxy-to-retainer | 0 mm separation, 0 mm³ penetration (intended contact) |
| Four Ø3.2 mm screw-clearance probes | 0 mm³ obstruction at all four existing centers |
| Yoke BREP change | 0 mm³ |
| Revised STL | 8362 facets; watertight; 1 connected component |
| Revised print-bed envelope | 47.60 × 47.60 × 4.20 mm |

The R20 yoke carries the main mounting surface. Its sampled annular land is 2.8 mm thick; localized boss/structure sections remain 4.0 mm. I did not thin the yoke or its screw bosses because that would change the functional mounting component beyond removal of the redundant broad lower plate.

## Plate 02 3MF verification

The R21 project retains all 12 source component instances and their existing placements/settings. Only the Pan_KeyedHorn_Cover mesh resource was replaced. Creality Print opened and sliced the exact R21 project. The saved slice retains the same vertex and triangle counts and face connectivity as the candidate mesh; the maximum coordinate difference after slicer serialization is 0.000579 mm. The saved 3MF passes its archive CRC check, and the replacement mesh has no non-manifold edges and one connected component.

Slicer result: **83.71 g, 9 h 30 min**. Creality Print warns that the pan cover has a floating cantilever while support is disabled. Therefore this plate is **HOLD** until that warning is addressed and the support/toolpaths are reviewed. This work did not enable or tune supports because the requested change was limited to the mounting plate geometry.

## Physical limits

The servo horn model remains a simplified proxy. Zero proxy overlap is a CAD result, not proof that the actual servo horn, retaining screw, or printed ABS retainer fits or carries load. No physical strength or fit claim is made.

## Files

- Assembly: CAD/EyeTrace_R21_SinglePanMountPlate.FCStd
- Changed component STEP: CAD/Pan_KeyedHorn_Cover_R21_OpenFrame.step
- Changed component STL: STL/Pan_KeyedHorn_Cover_R21_OpenFrame.stl
- Plate project before slicing: PRINT/Plate02_R21_SingleMountPlate_UNSLICED.3mf
- Sliced project, not released for printing: PRINT/Plate02_R21_SingleMountPlate_SLICED_HOLD.3mf
- FreeCAD view: SCREENSHOTS/R21_OneMountingPlate_Isometric.png
- Creality Print sliced preview: SCREENSHOTS/R21_CrealityPrint_Sliced.png
- Geometry and mesh checks: DOCUMENTATION/DOUBLE_PLATE_REPAIR_GEOMETRY.json, DOCUMENTATION/3MF_REOPEN_MESH_VERIFICATION.json, and DOCUMENTATION/ASSEMBLY_CHANGE_SCOPE_CHECK.json

