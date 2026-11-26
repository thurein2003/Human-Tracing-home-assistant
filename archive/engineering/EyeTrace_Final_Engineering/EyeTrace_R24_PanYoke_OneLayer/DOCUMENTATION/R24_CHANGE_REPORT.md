# R24 Pan-yoke bottom mounting correction

## Scope

Starting from `EyeTrace_R23_UnifiedBottomBlock.FCStd`, changed only `PanYoke_EarBracket_KeyedDrive`. `Base_EarMount_ThrustSupport` (printed Plate 01), `TiltCradle_KeyedHorn_CameraFrame`, the other component shapes, and assembly placements were preserved.

## Geometry change

The R23 yoke has a circular lower land at Z=35.2–37.7 mm and the rectangular mounting web begins at Z=37.0 mm. Their coincident footprint created local doubled material. The trim was limited to the part of the lower land directly beneath the measured upper plate footprint. The circular land outside that footprint and the existing base-contact regions were retained.

The rectangular web remains 2.5 mm thick (Z=37.0–39.5 mm). Local 4.0 mm screw-boss regions were retained. Representative local column measurements (before ? after):

| XY (mm) | R23 height (mm) | R24 height (mm) | Interpretation |
|---|---:|---:|---|
| (30, 20) | 5.8 | 4.0 | Lower overlapping land removed; boss retained |
| (32, 20) | 5.8 | 4.0 | Lower overlapping land removed; boss retained |
| (34, 20) | 5.8 | 4.0 | Lower overlapping land removed; boss retained |
| (33, 15) | 2.5 | 2.5 | Plate web unchanged |
| (40, 20) | 2.5 | 2.5 | Plate web unchanged |
| (31, 15) | 2.5 | 2.5 | Circular land outside plate footprint unchanged |

The four-millimeter result at the boss probes is a retained local boss, not a uniform plate thickness. This is a CAD geometry correction; strength and physical fit have not been physically tested.

## Validation

- R24 yoke: valid BREP, one solid; volume 27,840.3253 mm³.
- Removed from the R23 yoke: 155.5124 mm³.
- Geometry at and above Z=37 mm: symmetric difference 0 mm³.
- R15 shaft/horn core: symmetric difference 0 mm³.
- Plate 01/yoke positive-volume intersection: 0 mm³.
- Existing base-contact probe columns retained.
- Plate 01 and tilt cradle shapes were checked unchanged.
- Exported STL reopened in FreeCAD as a solid mesh: 126,522 facets, one connected component, zero nonmanifold edges.
- Updated Plate 02 3MF reopens with 11 build items and 11 instances; CRC passes. Only the yoke mesh resource was replaced. Its triangles match the exported STL within 0.00005 mm coordinate precision. All other 3MF resources and placements are unchanged.
- No new Creality Print slicing was performed. The 3MF is an unsliced project and is not a print-release approval.

## Output files

- `CAD/EyeTrace_R24_PanYoke_OneLayer.FCStd`
- `CAD/PanYoke_R24_OneLayer.step`
- `CAD/EyeTrace_R24_Assembly.step`
- `STL/PanYoke_R24_OneLayer.stl`
- `PRINT/Plate02_R24_PanYoke_OneLayer_UNSLICED.3mf`
- Validation evidence: `R24_GEOMETRY_VALIDATION.json`, `R24_LOCAL_THICKNESS_COMPARISON.json`, `R24_REOPEN_VALIDATION.json`, `R24_INDEPENDENT_EXPORT_CHECK.json`, and `R24_3MF_VALIDATION.json`.

## Status

Geometry/export checks: PASS. Physical mating/strength: unverified. Slicer/toolpath validation: not performed; slice this 3MF in Creality Print before printing.
