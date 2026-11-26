# Prototype 04 Revision 05 — Four-arm length reconciliation

## Release status
**Documented provisional fit-test geometry; physical horn fit is unverified.** The four arm lengths and references are now documented. This remains a coupon, not a production torque-transfer part. Inspect the 3MF preview before printing; physical fit still requires the real horn.

## Current CAD arm lengths (Revision 04, before this revision)
Measurements are from the CAD hub/pattern center to the extreme rounded tip of each pocket, read from the feature construction parameters:

| Top view arm | CAD pocket center-to-tip | Corresponding horn nominal used |
|---|---:|---:|
| Long −X (left) | 16.35 mm | 16.25 mm |
| Long +X (right) | 18.85 mm | 18.75 mm |
| Short +Y (upper) | 10.10 mm | 10.00 mm |
| Short −Y (lower) | 10.10 mm | 10.00 mm |

Revision 04 already had these dimensions geometrically, but the -1.25 mm hub offset and the drawing-to-user span adjustment were not explicit or traceable. Revision 05 makes them explicit in the FreeCAD parameters and validation data; the shape itself is unchanged from Revision 04.

## Long-arm reference and reconciliation
The user-measured long-axis overall span is **35.0 mm**, and the user-measured hub diameter is **7.0 mm**. The cited SG90 Horn #3 drawing gives unequal center-to-end reaches of **16.0 mm** and **18.5 mm**, summing to **34.5 mm**. To match the user's 35.0 mm total while preserving the drawing's 2.5 mm asymmetry, the CAD nominal horn reaches add **0.25 mm to each drawing reach**, giving **16.25 mm** and **18.75 mm** (sum 35.0 mm). The coupon pocket adds 0.10 mm at each end, corresponding to 0.20 mm total lengthwise clearance, giving pocket reaches **16.35 mm** and **18.85 mm** and pocket span **35.20 mm**.

The drawing is a reference for a similar Horn #3, not proof of clone geometry. The user's photographs show the white four-arm horn and its unequal long/short arm arrangement, but have perspective/no scale and cannot resolve these lengths independently or establish which long tip maps to +X/−X. Left/right is the CAD top-view naming; orient the actual horn during the physical test accordingly.

## Short-arm reference and requested extension
The user's 18.0 mm short-span measurement supersedes the drawing's 16.3 mm short span. The previous Prototype 01 had an 18.0 mm short-axis baseline. The requested +1.0 mm extension at each end gives a 20.0 mm nominal pocket span: **10.0 mm from center to each tip**. Applying the same 0.20 mm total fit clearance adds 0.10 mm per tip, so the CAD pocket reaches are **10.10 mm each** and pocket span is **20.20 mm**. This extension is a fit-test adjustment, not an assertion that the physical horn itself is 20 mm wide.

## Final Revision 05 dimensions
- Arm pocket reaches: 16.35, 18.85, 10.10, 10.10 mm from the pattern center (−X, +X, +Y, −Y).
- Nominal horn reaches represented: 16.25, 18.75, 10.00, 10.00 mm (the short values include the requested 1 mm per-end gauge extension).
- Pattern/pocket envelope: **35.20 × 20.20 mm**.
- Overall outer coupon extents: **38.00 × 23.00 × 4.30 mm**. The 4.30 mm maximum is the local center pad; the general body is 3.80 mm thick.
- Center dimensions retained: front recess Ø7.4 × 2.7 mm; rear recess Ø5.5 × 0.8 mm; retaining-screw access Ø4.5 mm through; center web 0.8 mm.
- Wide tapered long arms, rounded tips, widened short arms and local center pad retained.

## Validation evidence
- FreeCAD 1.1.4 saved-document reopen: **PASS** — valid BRep, one solid, volume 1013.656 mm³, bounding box 38.00 × 23.00 × 4.30 mm. Reopened custom properties match all four nominal and pocket reaches and the specified recesses.
- Generated mesh: **PASS** — 6,260 facets; FreeCAD mesh `isSolid()` true.
- 3MF package: **PASS** — ZIP CRC valid, one model object, embedded triangle count matches the STL's 6,260 facets.
- K2 bed: **PASS** — 38 × 23 mm part footprint is within 260 × 260 mm.
- Actual ABS sliced toolpath: **NOT INSPECTED**. 3MF stores starting settings (0.20 mm layer, 2 walls, 0% infill, supports off, 4 mm brim, 255 °C nozzle, 100 °C bed); verify these against the filament/printer profile and inspect Preview.
- Physical fit: **UNVERIFIED**. No physical test of the Revision 05 coupon is represented here.

## Images
`CrossHorn_UltraMinimal_FitTest_04R05_Top_Dimensioned.png` is a dimensioned top view based on the actual FreeCAD viewport image for Revision 04. Revision 05's reopened BRep and mesh have the same dimensions and geometry; Revision 05's FreeCAD model explicitly records the reconciled parameters. The image identifies each center-to-tip reach and distinguishes nominal horn reach from pocket allowance.

## Files
- `CrossHorn_UltraMinimal_FitTest_04R05.FCStd` — editable FreeCAD document
- `CrossHorn_UltraMinimal_FitTest_04R05.stl` — one coupon
- `CrossHorn_UltraMinimal_FitTest_04R05.3mf` — one-object ABS fit-test project
- `CrossHorn_UltraMinimal_FitTest_04R05_Top_Dimensioned.png` — dimensioned top view
- `geometry_validation.json`, `parameters.json`, `reopen_validation.json` — parameters and check evidence

Earlier revisions and the production pan/tilt assembly were not modified.
