# Prototype 04 Revision 07 — Deeper front center recess

## Status
One provisional ABS fit-test coupon. CAD and export checks passed. The raised hub of the actual white SG90 horn has not been physically checked; fit remains **UNVERIFIED**. This coupon is not approved as a structural drive part.

## Revision 07 geometry
- Front center circular recess: **Ø7.4 mm × 3.2 mm deep** (depth increased from 2.7 mm).
- Rear center circular recess: **Ø5.5 mm × 0.8 mm deep**, unchanged.
- Separate retaining-screw access: **Ø4.5 mm through**, unchanged.
- Center web between recess floors: **0.8 mm**.
- To preserve the 0.8 mm web, the local center pad rise was increased by **0.5 mm**, from 0.5 to **1.0 mm total above the surrounding 3.8 mm body**. The local Ø10.2 mm pad is the only thickened region; coupon maximum thickness is **4.8 mm**. The front recess floor remains at z=1.6 mm and the rear recess floor at z=0.8 mm.
- The through screw access remains separate from both circular recesses.
- Exactly one connected ultra-minimal coupon is present.

The 3.2 mm recess gives CAD depth beyond the published similar-horn hub-height reference, but the actual clone's raised hub height and underside shape are not established by that drawing. The coupon must be tried with the real horn before any fit claim.

## Preserved arm geometry
- X pocket reaches: **17.60 mm / 17.60 mm**, total 35.20 mm.
- Y pocket reaches: **10.10 mm / 10.10 mm**, total 20.20 mm.
- Symmetric tapered X arms and rounded ends retained; Y dimensions unchanged.
- Outer envelope: **38.00 × 23.00 × 4.80 mm**. The higher local center pad accounts for the Z increase; the rest of the coupon remains 3.8 mm thick.

## Validation
- FreeCAD 1.1.4 saved-document reopen: **PASS** — valid shape, one solid, volume 1018.964 mm³; bbox 38 × 23 × 4.8 mm.
- Reopened dimensions: **PASS** — front Ø7.4 × 3.2 mm; rear Ø5.5 × 0.8 mm; web 0.8 mm; separate Ø4.5 mm screw access; arm reaches unchanged.
- STL: **PASS** — 6,260 facets; FreeCAD mesh reports a closed solid (`isSolid()` true).
- 3MF: **PASS** — archive CRC valid, one object, 6,260 embedded triangles matching the STL.
- K2 bed footprint: **PASS** — 38 × 23 mm within 260 × 260 mm.
- Sliced toolpath: **NOT INSPECTED** — 3MF contains starting ABS settings (0.20 mm layer, 2 walls, 0% infill, supports off, 4 mm brim, 255 °C nozzle, 100 °C bed). Check the actual Creality Print preview and filament/printer limits before printing.
- Physical horn fit and retaining-screw access: **UNVERIFIED** pending an ABS coupon test with the actual horn and screw.

## Images
- `CrossHorn_UltraMinimal_FitTest_04R07_Top_Dimensioned.png` — top projection generated from FreeCAD BRep edges.
- `CrossHorn_UltraMinimal_FitTest_04R07_Section.png` — diagonal FreeCAD BRep section through the stepped center recesses, with depths and center web annotated.

## Files
- `CrossHorn_UltraMinimal_FitTest_04R07.FCStd` — editable FreeCAD model
- `CrossHorn_UltraMinimal_FitTest_04R07.stl` — single coupon
- `CrossHorn_UltraMinimal_FitTest_04R07.3mf` — one-object Creality Print project
- `VALIDATION_REPORT.md`, `geometry_validation.json`, `reopen_validation.json`, `export_validation.json`, `parameters.json`

Earlier revisions and the production assembly were not modified.
