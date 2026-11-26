# Eye Trace R20 Ultra-Low-Profile Candidate — Engineering and Slicer Validation

## Release: HOLD

R20 is a real CAD revision built from the original R19 FreeCAD assembly. It locally shortens the pan-yoke outer annular land. The R15 pocket, lower yoke interface, four screw pads, central shaft opening, and all component placements remain unchanged. Plate 01 was not modified.

## 8.049 mm dimension mapping

The R19 CAD does not contain a single uniform 8.049 mm solid section at the measured candidate column. The actual lower structure has several candidate heights:

| Feature / section | R19 Z interval | Height |
|---|---:|---:|
| Outer yoke land at XY=(34,0) | 35.2–41.0 mm | 5.8 mm |
| Ordinary yoke web at XY=(10,10) | 35.2–37.7 mm | 2.5 mm |
| R15 pocket at XY=(10,0) | 35.2 mm mouth to 36.9 mm floor | 1.7 mm |
| Backing above the R15 floor | 36.9–39.4 mm | 2.5 mm |
| Pocket mouth to opposite face | 35.2–39.4 mm | 4.2 mm |
| Screw pad at XY=(23.5,0) | 37.0–41.0 mm | 4.0 mm |
| Separate thrust ring | 36.0–37.0 mm | 1.0 mm |
| Stationary base at XY=(34,0) | 0–4.0 mm | separate component; no contact at this column |

The supplied 8.049 mm dimension alone does not identify which two faces were selected. The labeled diagram `SCREENSHOTS/R20_LowerStack_Endpoint_Candidates.png` marks these candidate surfaces. It does not claim the outer land is the exact screenshot pair.

## R20 geometry change

Component: `PanYoke_EarBracket_KeyedDrive`.

The outer annular land at radii about 32.3–35.3 mm is reduced from Z=35.2–41.0 to Z=35.2–38.0 mm:

- Same land section: **5.8 mm → 2.8 mm**.
- Yoke volume: **30,038.906 → 28,124.750 mm³**.
- Removed material: **1,914.157 mm³** (6.37% of R19 yoke volume).
- R15 pocket depth: **1.7 mm**, unchanged.
- Backing above horn-pocket floor: **2.5 mm**, unchanged.
- Lower interface BREP symmetric difference below Z=37.7: **0.000 mm³**.
- Central shaft opening: **Ø8.0 mm**, unchanged.
- Four mounting centers: (±18,0), (0,±18), unchanged.
- Local screw-pad section: **4.0 mm**, unchanged.

This is a measured sub-3 mm section at the outer land, not proof that the screenshot’s complete 8.049 mm stack is below 3 mm. The horn-pocket section remains 4.2 mm total and screw pads remain 4.0 mm. A uniform 2.8 mm cut through those interfaces would leave only 1.1 mm behind the 1.7 mm recess or reduce fastener reinforcement, so that cut was not made.

## CAD and export checks

- FreeCAD 1.1.4 recompute: modified yoke is **one valid solid**.
- Pan-yoke STEP exported.
- Full assembly STEP reimport: **13 valid solids**.
- Pan-yoke STL reimport: **26,065 vertices, 52,210 facets; FreeCAD reports solid mesh**. Mesh bounds and bed placement match the R19 layout envelope.
- Exact BREP difference confirms the lower R15 interface below Z=37.7 is unchanged.
- Component placements are unchanged. R19 modeled clearance checks remain applicable as lower geometry was removed only from the outer land: base 0.30 mm; intentional thrust contact; servo 1.50 mm; cover 0.20 mm; four pan screws 0.20 mm; tilt cradle 2.00 mm. The provisional horn-envelope overlap remains 5.655 mm³, unchanged; this does not prove hardware interference or fit.
- Updated unsliced Plate 02 3MF: 12 build items, archive CRC pass, only yoke mesh replaced, remaining meshes/settings/placements retained, bed envelope unchanged.

## Actual Creality Print slice

The R20 Plate 02 project was opened and sliced in the installed Creality Print GUI. The saved project metadata identifies **Creality Print 7.3.2.6412** (the Windows registration entry is 7.2 series).

- Printer: Creality K2
- Nozzle: 0.4 mm
- Bed: Textured PEI
- Filament: EyeTrace ABS 255C K2 100C
- Nozzle: 255°C; bed: 100°C
- Layer height: 0.20 mm; 3 walls; 20% infill
- Tree support is enabled on the yoke and tilt cradle and visible in the actual preview.
- Actual slicer estimate: **85.65 g**, **9 h 39 min**, 34.24 m filament.

Screenshots in `SCREENSHOTS/`:
- `R20_CrealityPrint_Sliced_FullPlate.png` — complete sliced plate and estimates.
- `R20_CrealityPrint_FirstLayer.png` — first-layer preview.
- `R20_CrealityPrint_PocketLayers.png` — low-layer preview near the R15 recess floor.

The saved 3MF contains project/slice metadata and preview assets; G-code was not exported. Zoomed inspection of every support interface and every horn-pocket toolpath remains incomplete.

## Mechanical interpretation and remaining risks

At radius 34 mm, the base and modeled thrust ring do not contact the outer yoke land; the four screw pads are at radius 18 mm. The land remains part of the single connected yoke solid. This supports the local CAD geometry change, but no FEA, ABS load/creep test, or fatigue test establishes structural adequacy.

The 8.049 mm screenshot endpoints remain **unverified**. The R20 candidate provides a local 2.8 mm land section at XY=(34,0), but should not be described as reducing the exact screenshot dimension until its selected pair is confirmed.

## Files

- Editable FreeCAD assembly: `CAD/EyeTrace_R20_UltraLowProfile.FCStd`
- Assembly STEP: `CAD/EyeTrace_R20_Assembly.step`
- Modified yoke STEP: `CAD/PanYoke_R20_LowProfile.step`
- Modified yoke STL: `STL/PanYoke_R20_LowProfile_PrintOrientation.stl`
- Updated unsliced Plate 02: `PRINT/Plate02_R20_LowProfile_Candidate_HOLD.3mf`
- Sliced Plate 02 project: `PRINT/Plate02_R20_LowProfile_Sliced_Candidate.3mf`
- Measurement diagram: `SCREENSHOTS/R20_LowerStack_Endpoint_Candidates.png`
- Detailed geometry values: `DOCUMENTATION/r20_geometry_validation.json`
- STL check: `DOCUMENTATION/r20_stl_mesh_check.json`
- 3MF check: `DOCUMENTATION/r20_3mf_validation.json`

## Verdict

- CAD geometry at outer annular land: **PASS — 2.8 mm**.
- Plate 02 slicing: **PASS — sliced in Creality Print; local detailed toolpath review incomplete**.
- Exact 8.049 mm screenshot measurement: **UNVERIFIED**.
- Structural and physical fit: **UNVERIFIED**.
- Overall release: **HOLD** pending confirmation of the measured surface pair and physical/load testing.
