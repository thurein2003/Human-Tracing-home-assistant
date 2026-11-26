# Prototype 04 Revision 06 — Symmetric X arms

## Status
One provisional, ultra-minimal ABS fit-test coupon. The symmetric X dimensions are implemented and CAD-validated. The white SG90 horn has not been fitted to this revision; physical compatibility remains **UNVERIFIED**. This is not a production torque-transfer component.

## Revision changes from Revision 05
- X-axis nominal reaches are now **17.50 mm on both sides**, measured from hub/pattern center to rounded tip.
- Pocket reaches are **17.60 mm on both sides**, adding 0.10 mm end allowance per side (0.20 mm total across the span).
- X pocket span is **35.20 mm**.
- The X arms are mirrored across the Y-axis: same root width, same tip width, same taper angle, and same rounded-end radius.
- The Horn #3 unequal 16.0/18.5 mm long-reach references are not used to set Revision 06 arm lengths. The latest user instruction supersedes them.
- Symmetric taper is provisionally 7.15 degrees, the arithmetic mean of the prior 6.3 and 8.0 degree profile references; this affects width only, not the arm reaches. Resulting modeled pocket root width is 7.20 mm and both pocket tip widths are 5.00475 mm.

## Retained dimensions
- +Y pocket reach: **10.10 mm**.
- −Y pocket reach: **10.10 mm**.
- Y pocket span: **20.20 mm**. The 18.0 mm baseline is extended 1.0 mm at each end and has 0.10 mm tip allowance per side.
- Front recess: **Ø7.4 mm × 2.7 mm deep**.
- Rear recess: **Ø5.5 mm × 0.8 mm deep**.
- Center retaining-screw access: **Ø4.5 mm through**.
- Local center reinforcement is retained: Ø10.2 mm pad, +0.5 mm local height. The center web is 0.8 mm; general coupon thickness is 3.8 mm and local maximum is 4.3 mm.

## Extents and print layout
- Pocket envelope: **35.20 × 20.20 mm** (X × Y).
- Overall coupon extents: **38.00 × 23.00 × 4.30 mm** (X × Y × Z); 4.30 mm is the local center-pad maximum.
- One connected coupon only; fits within the Creality K2 260 × 260 × 260 mm build volume.
- 3MF starting settings: ABS, 0.20 mm layers, 2 walls, 0% infill, supports off, 4 mm brim, 255 °C nozzle, 100 °C bed. Confirm against filament/printer limits and inspect the slicer's actual Preview before printing. No sliced toolpath was examined in this revision.

## Validation results
- FreeCAD 1.1.4 reopened saved FCStd: **PASS** — one valid solid; volume 1015.460 mm³; bbox 38.00 × 23.00 × 4.30 mm.
- Reopened feature parameters: **PASS** — X nominal reaches 17.50/17.50 mm; X pocket reaches 17.60/17.60 mm; Y pocket reaches 10.10/10.10 mm; long tip widths are equal at 5.00475 mm; center recesses/access match specified values.
- FreeCAD STL mesh: **PASS** — 6,260 facets; `isSolid()` true.
- 3MF integrity: **PASS** — ZIP CRC valid; one object; embedded triangle count 6,260, matching the STL.
- Single printable item and bed footprint: **PASS** — one coupon, 38 × 23 mm footprint.
- Physical horn profile/clearance/seat: **UNVERIFIED**. Actual print and hand fit with the real white horn are required.

## Dimensioned view
`CrossHorn_UltraMinimal_FitTest_04R06_Top_Dimensioned.png` is generated from horizontal-edge projections of the Revision 06 FreeCAD BRep. It labels all four center-to-tip pocket reaches and both axis spans.

## Deliverables
- `CrossHorn_UltraMinimal_FitTest_04R06.FCStd` — editable FreeCAD model
- `CrossHorn_UltraMinimal_FitTest_04R06.stl` — single coupon
- `CrossHorn_UltraMinimal_FitTest_04R06.3mf` — one-object Creality Print project
- `CrossHorn_UltraMinimal_FitTest_04R06_Top_Dimensioned.png` — dimensioned top projection
- `build_prototype_04_revision_06.FCMacro`, `package_prototype_04_revision_06_3mf.py`, `parameters.json`, `geometry_validation.json`, and `reopen_validation.json`

Revision 05 and all earlier revisions and the production pan/tilt assembly were left unchanged.
