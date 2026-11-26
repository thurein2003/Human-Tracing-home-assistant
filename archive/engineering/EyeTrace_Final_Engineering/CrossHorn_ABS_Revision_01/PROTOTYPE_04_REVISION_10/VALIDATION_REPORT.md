# Revision 10 — asymmetric short-arm width and 37 mm X axis

## Verification status
**CAD / mesh / slicer checks: PASS. Physical horn fit: UNVERIFIED.** This is a single ABS fit-test coupon; it is not a production drive component. Revision 09 and the production assembly remain untouched.

## Requested dimensional changes
- X-axis nominal span: **37.00 mm**.
- Left/right nominal reaches: **18.50 mm each**, equal and mirrored.
- Tip clearance: **0.10 mm per end**.
- X pocket reaches: **18.60 mm each**, total envelope **37.20 mm**.
- Bottom short-arm pocket (−Y): **4.40 mm wide**, increased by **1.00 mm total** from Revision 09's 3.40 mm.
- Upper short-arm pocket (+Y): **3.40 mm wide**, unchanged from Revision 09.
- Short-arm reaches remain **10.10 mm** each; rounded ends retained.
- Long-arm taper and rounded tips retained.

The saved FreeCAD document was reopened and sectioned at Y=+6.00 and −6.00 mm. The actual cavity walls are at X=±1.70 mm on the upper arm and X=±2.20 mm on the bottom arm, confirming widths of 3.40 and 4.40 mm respectively. A centerline section measures equal X pocket reaches of 18.60 mm.

## Center mount
- Front circular cavity: **Ø7.40 mm**, actual depth **3.20 mm** from the horn arm-seat plane at Z +2.10 mm to floor Z −1.10 mm.
- Backside recess: **Ø5.50 × 0.30 mm**.
- Separate center screw access: **Ø4.50 mm through**.
- Remaining center web: **0.80 mm**.
- Local underside reinforcement is retained from Revision 09; no ring-height change was made.

The dimensioned section is derived from the saved FreeCAD BRep, rather than the cutter's nominal height.

## Geometry and export validation
- FreeCAD 1.1.4 reopened model: valid, **one solid**.
- Native feature recompute tests: front and back depths independently changed cutter geometry and final BRep volume; original requested values were restored.
- STL: **6,800 triangles**, one connected solid, watertight; all 10,200 unique edges have exactly two incident faces.
- 3MF: valid archive, **one model object**, 6,800 triangles, watertight; all 10,200 edges have exactly two incident faces.
- Independent cross-sections of both STL and 3MF reproduce +Y width **3.40 mm**, −Y width **4.40 mm**, and front circular wall depth **3.20 mm**.
- K2 layout envelope is about **40 × 23 mm** (approximately 48 × 31 mm including 4 mm brim), within the 260 × 260 mm bed.

Detailed machine-readable results are in `reopen_parametric_validation.json`, `mesh_validation.json`, and `watertight_validation.json`.

## Creality Print slice
G-code: `SLICED_GCODE_FINAL/plate_1.gcode`.
- **36 layers** at 0.20 mm.
- Tree supports enabled, build-plate-only; one brim.
- Slicer estimate: **1.57 g ABS**, **15 min 12 sec** normal-mode time.
- Start temperatures: **255°C nozzle / 100°C bed**.

Inspect the support preview and print this single coupon. Test the actual white SG90 horn by hand for arm seating, hub seating, and retaining-screw access. Do not force the horn into the pocket. CAD and mesh checks do not establish physical fit.
