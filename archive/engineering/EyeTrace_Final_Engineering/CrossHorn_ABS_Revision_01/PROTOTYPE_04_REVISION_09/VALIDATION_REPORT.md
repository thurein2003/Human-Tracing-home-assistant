# Revision 09 — center recess correction and validation

## Verdict
**The actual Ø7.40 mm center cavity measures 3.20 mm vertically from the horn arm-seating surface to the cavity floor.** This is verified on the saved FreeCAD BRep, exported STL mesh, and 3MF model mesh. Physical horn fit remains **UNVERIFIED** until the ABS coupon is printed and checked with the actual horn.

This is one fit-test coupon. No production pan/tilt parts or earlier revisions were modified.

## Why Revision 08 looked like 1.00 mm
Revision 08's front cutter had a nominal height of 3.20 mm, but its upper 2.20 mm intersected air already removed by the cross-arm pocket. The actual horn arm-seat face was at Z +2.10 mm and the circular floor was at Z +1.10 mm. Their actual separation was therefore **1.00 mm**. Cutter height alone had concealed that condition.

Revision 09 starts the circular cavity at the actual arm-seat plane and places its floor at Z −1.10 mm:
- Upper horn arm-seat reference: **Z +2.10 mm**
- Ø7.40 mm circular cavity floor: **Z −1.10 mm**
- Direct vertical difference: **3.20 mm**

The center is reinforced only on the underside. A Ø10.20 mm local pad projects 2.20 mm below the coupon to provide a real cavity floor, the requested backside relief, and the 0.80 mm web. The surrounding coupon thickness and ring height were not increased. The resulting local Z span is 6.00 mm.

## Center dimensions
- Front cavity: **Ø7.40 × 3.20 mm**, measured from Z +2.10 to Z −1.10.
- Backside recess: **Ø5.50 × 0.30 mm**.
- Separate retaining-screw access: **Ø4.50 mm through**.
- Material web between the front and back recess floors: **0.80 mm**.
- Local underside support: **Ø10.20 mm**, projecting **2.20 mm** below the original coupon underside.
- Coupon footprint: approximately **38 × 23 mm**; maximum local Z span: **6.00 mm**.

## Independent geometry evidence
- Saved FreeCAD 1.1.4 document reopened successfully; final shape is valid and contains **one solid**.
- A fresh vertical BRep section at Y=0 intersects the circular wall at X=±3.70 mm from Z +2.10 to Z −1.10; measured vertical span **3.20 mm**.
- STL: **6,800 triangles**, closed solid mesh. The vertices on the Ø7.4 mm circular wall span **3.19999993 mm** (STL float precision).
- 3MF: valid ZIP package with **one model object** and the same **6,800 triangles**. Its circular wall spans **3.20 mm** after accounting for the bed-placement Z offset.
- Parametric edits were tested after reopening the saved FCStd: front depth 3.20→3.10 mm changed the actual cutter and BRep volume by +2.710409 mm³; rear depth 0.30→0.50 mm changed its cutter and volume by −1.570796 mm³. Values were restored to 3.20 / 0.30 mm; center web recomputed to 0.80 mm.
- X arm reaches remain symmetric at **±17.60 mm**; Y reaches remain **±10.10 mm**.

The dimensioned section, drawn from the final FreeCAD BRep section, is `CrossHorn_04R09_Center_Section.png`.

## Creality Print slice
Sliced with the installed Creality Print command-line slicer. G-code: `SLICED_GCODE_FINAL/plate_1.gcode`.
- **36 layers** at 0.20 mm.
- Slicer estimate: **1.52 g ABS**, **14 min 44 sec** normal-mode print time.
- Start temperatures: **255°C nozzle / 100°C bed**.
- Brim: **4 mm**.
- Tree supports are enabled and restricted to the build plate. G-code contains support feature paths beneath the locally raised underside/arm regions.
- 3MF bed-coordinate bounds: XY centered on the K2 bed; 38 × 23 mm model footprint (46 × 31 mm with the 4 mm brim), Z 0–6 mm. Fits the 260 × 260 × 260 mm K2 volume.

Open the 3MF in Creality Print and review the support preview before printing. Remove supports carefully without levering against the thin coupon.

## Physical check still required
Print this single ABS coupon and test the actual white SG90 horn by hand. Verify the horn arms seat without force, the raised hub enters the circular cavity to the intended shoulder, and the retaining screw remains accessible. This coupon is for fit testing only; it is not a structural drive part. CAD, mesh, and slicing checks do not establish physical fit.
