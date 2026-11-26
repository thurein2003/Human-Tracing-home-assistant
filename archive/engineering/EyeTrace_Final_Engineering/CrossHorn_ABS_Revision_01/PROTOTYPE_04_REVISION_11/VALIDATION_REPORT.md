# Revision 11 — underside SG90 clearance enlargement

## Status
**CAD, mesh, and slicer validation: PASS. Physical servo fit: UNVERIFIED.** This is one ABS fit-test coupon only. The production pan/tilt assembly and all previous revisions remain unchanged.

## Underside opening inspection and correction
Revision 10's underside opening measured **Ø5.50 mm** in its CAD feature and section. The requested +5.00 mm total change gives a new opening of **Ø10.50 mm**.

That opening would be 0.15 mm larger per side than Revision 10's Ø10.20 mm underside support land. Revision 11 locally increases only that land to **Ø12.50 mm**, leaving a **1.00 mm radial rim** around the Ø10.50 mm opening. This avoids cutting the opening beyond the local support footprint. The resulting BRep remains one valid solid, and the section retains the 0.80 mm center web. This is a fit-test geometry check, not a structural or torque certification.

## Measured dimensions from final geometry
- Back/underside servo-clearance recess: **Ø10.50 × 0.30 mm**; section wall at X=±5.25 mm, Z=−2.20 to −1.90 mm.
- Local underside support land: **Ø12.50 mm**; radial rim around clearance pocket **1.00 mm** per side.
- Front horn recess is independent and unchanged: **Ø7.40 × 3.20 mm**.
- Front/back center web: **0.80 mm**.
- Separate retaining-screw access: **Ø4.50 mm through**.
- Front and backside recess tools have separate FreeCAD parameters and recompute independently.

The dimensioned underside section was generated from the final FreeCAD BRep: `CrossHorn_04R11_Underside_Section.png`.

## Geometry/export validation
- FreeCAD 1.1.4 file reopened successfully; final body is valid and has **one solid**.
- Actual BRep section measures the underside recess diameter at **10.50 mm**, depth **0.30 mm**, support land Ø12.50 mm, and radial rim 1.00 mm.
- The same section measures the front recess at Ø7.40 × 3.20 mm and the center web at 0.80 mm.
- STL mesh: **6,806 triangles**, watertight; all 10,209 unique mesh edges have exactly two incident faces.
- 3MF: valid archive, **one model object**, 6,806 triangles, watertight; all 10,209 edges have exactly two incident faces.
- Independent STL and 3MF mesh vertex sections reproduce both circular diameters and depths.
- Coupon footprint is approximately **40 × 23 mm**; with its 4 mm brim it fits on the K2's 260 × 260 mm build plate.

The larger shallow underside clearance does not intersect the front recess or retaining-screw passage. It does leave a relatively thin 0.80 mm center web and 1.00 mm radial support rim; assess the actual printed coupon gently. No load-bearing use is approved from these CAD checks.

## Creality Print toolpath check
G-code: `SLICED_GCODE_FINAL/plate_1.gcode`.
- **36 layers**, 0.20 mm.
- Tree supports restricted to the build plate; one brim.
- Slicer estimate: **1.55 g ABS**, **14 min 52 sec** normal-mode time.
- Start temperatures: **255°C nozzle / 100°C bed**.
- The 3MF contains one coupon. Review the support preview before printing.

Print this coupon and check the actual SG90 mounting area by hand without forcing it. Confirm the underside clears the servo housing/mounting area and that the front horn recess, screw access, and center web remain intact. Physical compatibility is not yet verified.
