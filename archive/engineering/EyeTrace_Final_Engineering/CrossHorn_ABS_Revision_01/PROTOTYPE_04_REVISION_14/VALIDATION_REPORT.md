# Prototype 04 Revision 14 — Validation Report

## Revision changes
- Source: Revision 13. Prior revisions and the production pan-and-tilt assembly were not modified.
- Center bore parameter and actual FreeCAD cutter diameter: Ø8.00 mm, radius 4.00 mm, concentric with the horn center.
- A single cylindrical cutter spans Z = −2.20 to +4.80 mm, beyond the coupon faces at Z = −2.20 and +3.80 mm. No Ø5.50 mm restriction or stepped center feature is modeled.
- The bore joins the existing horn-arm pocket above the horn-seat plane (Z=+2.10 mm); this makes the top opening locally open into that pocket. The section shows no smaller bore or shelf.
- X-axis nominal horn span remains 39.00 mm with equal 19.50 mm reaches; pocket envelope remains 39.20 mm. Short-arm geometry is carried forward unchanged.
- Local Ø12.50 mm support pad remains 2.20 mm deep. Radial land from Ø8 bore edge to pad perimeter is 2.25 mm.

## FreeCAD geometry verification
- FreeCAD 1.1.4 recompute: valid, single connected solid.
- Actual through-cylinder X/Y dimensions: 8.00 × 8.00 mm (radius 4.00 mm); center at X=Y=0. Full cutter extends through the coupon thickness.
- Actual saved-solid section at Y=0 shows the bore walls at X=−4.00 and +4.00 mm through the coupon material up to the arm-pocket seat plane. The horn pocket then opens around the bore; there is no internal narrowing or Ø5.50 shoulder.
- Parametric recompute test altered ThroughDiameter to 7.30 mm and measured a changed cutter and final volume, then restored 8.00 mm. Geometry changed, not just the displayed property.
- Final solid volume: 1211.522 mm³; bounds: 42.000 × 23.000 × 6.000 mm.

## STL and 3MF
- STL: 5,128 triangles; all unique mesh edges have incidence 2 (closed manifold).
- 3MF: valid ZIP archive, exactly one object, 5,128 triangles matching the STL.
- Fit-test envelope is within the Creality K2 260 × 260 × 260 mm build volume.
- Approximate net ABS mass: 1.26 g using 1.04 g/cm³ assumed density; this excludes brim, purge and slicer overhead.

## Physical and slicer status
This is one fit-test coupon only. Actual horn fit remains physically unverified. Review the 3MF in Creality Print and inspect its sliced preview before printing; no slicer toolpath/print-time estimate is asserted here.
