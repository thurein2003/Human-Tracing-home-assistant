# Prototype 04 Revision 13 — Validation Report

## Change summary
- Starting point: preceding cross-horn fit-test revision; earlier revisions and production assembly were preserved.
- Replaced the former stepped Ø7.4/Ø5.5 center arrangement and underside Ø10.5 counterbore with a single Ø7.40 mm through-bore cutter. No Ø5.50 mm restriction or center shoulder remains.
- Preserved the local Ø12.50 mm underside support pad (2.20 mm deep), leaving a nominal 2.55 mm radial land from bore edge to pad perimeter.
- Symmetric long-axis nominal horn span: 39.00 mm, reaches 19.50 mm each side. The specified 0.10 mm clearance at each tip gives 19.60 mm pocket reaches and a 39.20 mm pocket envelope.
- Short-arm profile/widths carried forward unchanged from the prior revision.

## Actual CAD checks
- FreeCAD 1.1.4 recomputed and saved the editable model.
- `FinalCoupon`: valid shape, one solid; volume 1242.805 mm³; bounding box 42.000 × 23.000 × 6.000 mm.
- `ThroughBoreTool`: radius 3.700 mm, Ø7.400 mm; cutter spans Z = −2.200 to +4.800 mm, extending past both coupon faces (coupon Z = −2.200 to +3.800 mm).
- Vertical X-Z section at Y=0 shows cylindrical bore walls at X = ±3.700 mm from the underside to the horn-seat plane Z=+2.100 mm. Above that plane, the hole opens into the preserved horn-arm pocket. This is an open merge into a larger existing recess, not an inner restriction, shelf, or smaller bore. The final section shows no Ø5.50 mm step.
- FreeCAD parameter edit test changed ThroughDiameter to 7.30 mm and measured a different cutter diameter and solid volume; it then restored 7.40 mm and recomputed. The saved dimensions are geometry-derived, not property-label-only.

## Export checks
- STL: 5,126 triangles; every unique mesh edge has incidence 2 (closed manifold); one solid from the source BRep.
- 3MF: ZIP integrity passes; one model object; 5,126 triangles matching the STL.
- Envelope: 42 × 23 × 6 mm; within the Creality K2 260 × 260 × 260 mm build volume.
- Estimated net solid ABS mass is approximately 1.29 g using the CAD volume and 1.04 g/cm³ assumed density. This excludes brim, purge, and slicing/toolpath effects; it is not a slicer estimate.

## Slicer status
The installed Creality Print 7.2 CLI was invoked on the 3MF, but it exited without creating G-code or a sliced preview. Therefore layer toolpaths, support generation, print time, and slicer filament estimate remain unverified. The 3MF contains the inherited ABS profile: 0.20 mm layers, 2 walls, 0% infill, 255 °C nozzle, 100 °C bed, tree supports enabled/build-plate-only, and 4 mm brim. Open the 3MF in Creality Print and inspect the sliced preview before printing.

## Release status
CAD geometry/export validation: PASS. K2 dimensional envelope: PASS. Sliced toolpath inspection: UNVERIFIED. Physical fit of the actual white SG90 horn: UNVERIFIED until this coupon is printed and checked. This is a fit-test coupon only, not a production drive component.
