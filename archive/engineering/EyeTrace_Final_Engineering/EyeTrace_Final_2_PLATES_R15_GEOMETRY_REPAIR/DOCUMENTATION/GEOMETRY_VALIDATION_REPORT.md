# Eye Trace R15 — Horn Interface Geometry Audit

Date: 2026-11-18  
Audited with: FreeCAD 1.1.4  
Scope: pan yoke and tilt cradle horn interfaces in the exact current two-plate candidate.

## Verdict

**No confirmed horn-pocket defect was found. No geometry was changed.** The irregular strips/discontinuities in the preview are consistent with small STL facets along rounded surfaces and seam/edge rendering, plus the intentional annular support land around the center bore. The FreeCAD BREP and exported meshes do not show broken pocket walls, disconnected fragments, or invalid solids.

The suspicious features are not all identical: the pan yoke includes a small intentional annular support land and therefore has a nonzero Boolean overlap with the full master cutter body. At the actual cross-pocket profile, the land does not intrude into the arms. It is retained as designed and must not be removed as a false-positive repair.

## Exact inputs and preservation

- Current two-plate assembly: `CAD/EyeTrace_R15_Final_Assembly.FCStd`
- Plate 01: `PRINT/EyeTrace_R15_Plate_01_ABS.3mf`
- Plate 02: `PRINT/EyeTrace_R15_Plate_02_ABS.3mf`
- Master: `CrossHorn_ABS_Revision_01/PROTOTYPE_04_REVISION_15/CrossHorn_UltraMinimal_FitTest_04R15.FCStd`, object `ArmPocketTool`
- Component meshes: the 13 STLs in `STL/`

The assembly FCStd, both 3MFs, and all 13 STL files were copied without geometry edits. SHA-256 checks show the output copies match the source files byte-for-byte. The current assembly FCStd also matches the CAD document used by the independent BREP audit (SHA-256 `6478270E7489880B4334A943E9ED04091CFA5233CA26E9786D9E25C240401092`).

## Identified components and source files

| Interface | Exact component | Source FreeCAD object | Exported mesh |
|---|---|---|---|
| Pan drive | `PanYoke_EarBracket_KeyedDrive` | Same-named object in `CAD/EyeTrace_R15_Final_Assembly.FCStd` | `STL/PanYoke_EarBracket_KeyedDrive.stl` |
| Tilt drive | `TiltCradle_KeyedHorn_CameraFrame` | Same-named object in `CAD/EyeTrace_R15_Final_Assembly.FCStd` | `STL/TiltCradle_KeyedHorn_CameraFrame.stl` |

Both parts appear on Plate 02. Plate 01 contains the base housing and does not contain either suspect horn interface.

## Reference geometry and comparison

The master BREP is valid and one solid. Its cutter bounds are 39.2 × 20.2 × 1.7 mm; the nominal profile reaches are ±19.6 mm and ±10.1 mm, and the central through-opening is Ø8 mm. The source R15 profile has the symmetric tapered long arms, rounded ends, and widened short arms. The documented support land around the center is concentric at Ø9.2/Ø8.0 mm and lies within the carrier's seating region; it is not an underside boss.

Using the documented component coordinate transforms, the master cutter bounds are:

- Pan yoke: X −19.6…+19.6, Y −10.1…+10.1, Z 35.1…36.8 mm.
- Tilt cradle: X −41.0…−39.3, Y −10.1…+10.1, Z 58.4…97.6 mm.

The R15 master profile was compared to both actual carrier BREPs at 4,315 interior profile samples per interface on a 0.25 mm grid at local Z=2.95 mm. **Both interfaces had 0 of 4,315 sampled points inside carrier material.** The cross-shaped pocket profile is clear at the sampled section.

The exact Boolean common volume between the full master cutter and pan carrier is 13.0525 mm³ (two small solids); the tilt common volume is 0 mm³. The pan common is the intentional annular support land around the center bore, not an arm-pocket remnant. Do not interpret that full-volume Boolean test alone as an arm cavity defect. The sampled arm profile and section render show no arm intrusion. This annular land provides the documented center support; its physical horn seating remains subject to hardware fit, not this geometry audit.

### CAD and mesh checks

| Metric | Pan yoke | Tilt cradle |
|---|---:|---:|
| FreeCAD BREP | Valid; 1 solid | Valid; 1 solid |
| BREP volume | 42,345.8261 mm³ | 24,528.2897 mm³ |
| BREP faces / edges | 152 / 457 | 146 / 434 |
| BREP faces <0.01 mm² | 0 | 0 |
| BREP edges <0.05 mm | 0 | 0 |
| STL facets | 9,942 | 9,108 |
| FreeCAD `Mesh.isSolid()` / components | True / 1 | True / 1 |
| Faceted mesh volume | 42,340.8807 mm³ | 24,526.2621 mm³ |
| Mesh-to-BREP volume delta | 0.01168% | 0.00827% |

The source BREP has no tiny sliver faces by the stated thresholds. STL tessellation does contain small triangles on curved edges (minimum facet area about 0.000284 mm²; minimum edge about 0.02775 mm), which is expected from mesh approximation and can appear as thin strips or uneven lines in a slicer preview. The meshes are closed/solid and each is one connected component. No disconnected internal islands were found.

## Defect checklist

| Suspected issue | Result |
|---|---|
| Broken/disconnected pocket wall | Not found |
| BREP self-intersection / invalid shape | Not found; both valid single solids |
| Boolean sliver faces in pocket | Not found in BREP; zero faces below 0.01 mm² |
| Unexpected arm-pocket rib | Not found in sampled pocket profile |
| Incomplete long/short arm subtraction | Not found in 0.25 mm occupancy comparison |
| Center material | Intentional annular support land; pan cutter common 13.0525 mm³ is localized there |
| STL disconnected fragments | Not found; each mesh reports solid and one component |
| Preview-only line/facet artifacts | Likely at rounded edges/seams; mesh facets account for fine visual segmentation |

## Screenshots and evidence

CAD-derived, dimensioned profile-inspection renders (green = actual carrier is void at sample locations; dashed orange = R15 master profile):

- Pan top/profile: `RENDERS/PanYoke_EarBracket_KeyedDrive_R15_Top_Section.png`
- Pan underside/profile: `RENDERS/PanYoke_EarBracket_KeyedDrive_R15_Bottom_Section.png`
- Tilt top/profile: `RENDERS/TiltCradle_KeyedHorn_CameraFrame_R15_Top_Section.png`
- Tilt underside/profile: `RENDERS/TiltCradle_KeyedHorn_CameraFrame_R15_Bottom_Section.png`
- Combined source comparison: `RENDERS/R15_Interface_Section_Comparison.svg`

Existing Creality Print previews, copied from the current two-plate project:

- `RENDERS/Plate01_Existing_Sliced_Preview.png`
- `RENDERS/Plate01_Existing_Bridge_Layer.png`
- `RENDERS/Plate02_Existing_Sliced_Preview.png`

The profile renders are generated from FreeCAD BREP occupancy checks, not screenshots of the FreeCAD GUI. The Creality images are slicer screenshots from the existing plate slices.

## Slicer / release status

This audit did not change geometry, so it did not create a new slice. The exact existing 3MF plate projects and their previous Creality Print evidence are preserved. Their outstanding print blockers remain:

- Plate 01: support contact under the full 23.3 mm internal bridge remains **unverified** from the captured toolpath view.
- Plate 02: the prior completed slice reported a layer-1 Z=0 path conflict between generated “Embossed text” and `Pan_KeyedHorn_Cover`.

Accordingly, this audit does **not** approve either plate for printing. The horn geometry is CAD-verified against the master profile at the sampled section, but physical horn seating/fit is a separate physical condition.

## Output contents

- `CAD/EyeTrace_R15_Final_Assembly.FCStd` — unchanged copy of current assembly
- `PRINT/EyeTrace_R15_Plate_01_ABS.3mf` and `PRINT/EyeTrace_R15_Plate_02_ABS.3mf` — unchanged copies
- `STL/` — 13 unchanged component STLs
- `CHECKS/fresh_brep_audit.json` — FreeCAD BREP/STL metrics and exact cutter intersection
- `CHECKS/pocket_grid_comparison.json` — 0.25 mm profile occupancy test
- `CHECKS/cutter_transform_probe.json` — cutter placements and common volume
- `RENDERS/` — CAD-derived interface comparisons and existing slicer previews

**Disposition:** Geometry repair not warranted. Both arm pockets PASS the sampled R15 profile comparison; no physical fit claim is made. Plate print readiness remains HOLD for the separate slicer issues above.
