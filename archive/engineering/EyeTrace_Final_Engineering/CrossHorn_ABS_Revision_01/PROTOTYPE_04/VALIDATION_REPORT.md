# Prototype 04 — Ultra-minimal ABS horn fit gauge

**Status: CAD/mesh verified; actual horn fit and sliced mass unverified. Fit-test only, not a structural part.** Prototype 03, Revision 02 and all production assembly files remain unchanged.

## Deliverables

- `CrossHorn_UltraMinimal_FitTest_04.FCStd` — editable FreeCAD solid with parameter properties
- `CrossHorn_UltraMinimal_FitTest_04.stl`
- `CrossHorn_UltraMinimal_FitTest_04.3mf` — Creality Print K2 project
- `CrossHorn_UltraMinimal_FitTest_04_Top.png` and `CrossHorn_UltraMinimal_FitTest_04_Isometric.png` — actual FreeCAD viewport images
- `parameters.json`, `build_prototype_04.FCMacro`, and `package_prototype_04_3mf.py`
- `geometry_validation.json`, `fcstd_reopen_validation.json`, and `validation_results.json`
- `SLICER_QA/Slicing_Attempt.md`

## Gauge geometry

The horn cavity profile is carried forward from Prototype 03 Revision 02: tapered, rounded, unequal long arms; widened short arms; the same provisional 1.25 mm hub offset; and a separate Ø4.5 mm center retaining-screw access opening. The user supplied nominal dimensions remain 35 mm long span, 18 mm short-span baseline, and 7 mm hub. The 18 mm baseline is extended 1.0 mm at both short-arm ends; the pocket is 20.2 mm including 0.20 mm total lateral clearance.

The outer boundary is a rounded cross following the pocket with a nominal **1.4 mm wall**. Overall height is **3.7 mm**. Arm pockets are **1.7 mm deep**, leaving **2.0 mm** of floor beneath the horn arms. The center hub recess is **Ø7.4 × 2.7 mm deep**, leaving a distinct **1.0 mm floor** beneath the hub seat. The separate retaining-screw access bore passes through by design; the rest of the hub seat floor remains intact. This reproduces the Horn #3 drawing's 1.5 mm plate / 2.5 mm total hub-height relationship as provisional geometry while retaining your nominal Ø7 mm hub measurement.

The CAD part is 38.0 × 23.0 × 3.7 mm. With the configured 4 mm brim allowance it occupies approximately 46.0 × 31.0 mm, within the Creality K2 260 × 260 × 260 mm build volume. The gauge is oriented flat on its base, pocket upward. Its open pockets and vertical walls have no designed overhangs; supports are disabled. Walls are 1.4 mm nominal, equivalent to 3.5 × a 0.4 mm line width; the slicer may vary actual line placement. The continuous floor prints as solid bottom layers; sparse infill is set to 0%.

## Validation results

- FreeCAD 1.1.4 reopened the saved FCStd: **valid BRep, one solid**, volume **965.52 mm³**.
- Exported STL: **5,120 facets**, FreeCAD mesh reports solid/watertight; dimensions match the BRep.
- 3MF archive CRC is valid, has one printable mesh object, and its **5,120 triangles** match the STL.
- Hub floor 1.0 mm; arm floor 2.0 mm; the center access bore is the only intentional through-opening.
- K2 bed fit passes with the configured brim envelope.

The chosen printable settings are **ABS, 0.20 mm layers, 2 walls, 0% sparse infill, supports off, 4 mm brim, 255 °C nozzle, 100 °C bed**. Confirm temperature limits and range against the actual filament spool and printer before slicing.

## Filament comparison — actual sliced values unavailable

Prototype 03 Revision 02 BRep volume is 1,750.89 mm³; Prototype 04 is 965.52 mm³, a **44.9% CAD solid-volume reduction**. This is a geometry comparison only; it is **not** a measured filament reduction. The projects also use different wall and infill settings, so volume ratio cannot predict sliced mass accurately.

I attempted the Creality Print 7.2 documented CLI slice on both projects. The local executable opened a GUI process but produced no G-code, slice log, or filament/time metadata. Consequently, actual sliced filament mass, print time, and percentage material savings versus Prototype 03 are **NOT VERIFIED** and are intentionally not estimated here. See `SLICER_QA/Slicing_Attempt.md` for details. No G-code is included.

## Physical verification

The actual white horn has not been tested in this gauge. With the horn unforced, verify that all four arms descend into the cavity, the long arms follow the tapered ends, both short arms clear their extended pockets, and the raised hub enters the circular seat without bottoming. Check the horn lies flat on the arm seating floor, the retaining screw remains accessible, and the horn lifts out without prying. Record gaps, rocking, insertion force, and any print defects before changing dimensions.

Arm widths, end radii, local contour, hub offset, hub height and screw/tool access remain provisional because the actual horn was not dimensioned at those locations. This fit gauge does not validate torque transfer or production strength.
