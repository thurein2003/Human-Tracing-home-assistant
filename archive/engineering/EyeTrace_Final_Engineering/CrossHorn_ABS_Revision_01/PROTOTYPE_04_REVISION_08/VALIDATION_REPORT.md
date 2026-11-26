# Revision 08 Validation Report

## Release status
**Fit-test coupon only. Physical horn fit remains UNVERIFIED.** This revision does not alter the pan/tilt production assembly.

## Requested center geometry
Measured from the modeled seating and rear reference faces in the final FreeCAD BRep:
- Front hub recess: **Ø7.40 mm × 3.20 mm total depth**.
- Backside recess: **Ø5.50 mm × 0.30 mm total depth**.
- Retaining-screw access: separate **Ø4.50 mm through-opening**.
- Remaining material web between the two recess floors: **0.80 mm**.
- Coupon base thickness: **3.80 mm**; local center reinforcement adds **0.50 mm**, so maximum local thickness is **4.30 mm**.
- Front-to-back recess radial separation: **0.95 mm**.

The front and back recesses are separate features; the through-opening is independent. No unintended through-cut was found.

## Parameter behavior
The saved FreeCAD document uses native parametric Part cylinders and Part cuts, with dimensions linked to a parameter object by expressions. Reopening the saved file and changing a parameter followed by recompute changed the cutter BRep and overall volume:
- Front depth changed 3.20 → 3.10 mm: cutter height became 3.10 mm; volume changed by **+2.710409 mm³**.
- Back depth changed 0.30 → 0.50 mm: cutter height became 0.50 mm; volume changed by **−1.570796 mm³**.
- Parameters were restored and saved at 3.20 / 0.30 mm. Reopened final model: valid shape, **1 solid**, web **0.80 mm**.

This verifies geometry recomputation after editing, rather than only updating displayed property values.

## Preserved coupon geometry
- Exactly one compact four-arm coupon.
- Equal X reaches: **17.60 mm each**, total X pocket span **35.20 mm**.
- Y reaches: **10.10 mm each**, total Y pocket span **20.20 mm**.
- Outer footprint: **38 × 23 mm**.
- Symmetric tapered long-arm profile and widened short-arm profile are retained.

## CAD and mesh checks
- FreeCAD shape: valid, one connected solid.
- FreeCAD volume: **1005.8353 mm³**.
- Bounding dimensions: **37.9996 × 22.9997 × 4.30 mm**.
- STL: **6,260 facets**, watertight/solid mesh.
- 3MF: package integrity checked; one model object with **6,260 triangles**, matching the exported mesh.
- K2 build volume: coupon and brim fit within the 260 × 260 mm bed.

## Slicer inspection
Sliced using the installed Creality Print command-line slicer (reported generator version V7.3.2.6412):
- G-code: `SLICED_GCODE/plate_1.gcode`
- Layer count: **22**.
- Slicer estimated material: **1.13 g ABS** (slicer-reported estimate).
- Slicer estimated time: **8 min 45 sec** (normal mode).
- Nozzle / bed start temperatures: **255°C / 100°C**.
- Brim: present.
- Support toolpaths: **none**; no `TYPE:Support` feature is present.
- G-code model bounds: X **111–149 mm**, Y **118.5–141.5 mm**, Z **0–4.3 mm**.

The slicer estimate is for the generated job and may vary with printer firmware, filament profile, and final machine settings. Review the project and first-layer preview in Creality Print before printing.

## Physical verification still required
Print this coupon in ABS, then test the actual white SG90 horn:
1. Seat the horn by hand without force; its arms should enter the rounded recess and the raised hub should bottom on its intended seating surface.
2. Confirm the retaining screw and screwdriver can reach the screw without the hub binding.
3. Confirm no rocking caused by the center hub or arm profile.
4. Record whether fit is tight, free, or loose; do not use this coupon as a structural drive part.

The 0.20 mm lateral fit assumptions and unmeasured horn profile details remain provisional. CAD and slicing validation do not establish physical fit.
