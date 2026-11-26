# Prototype 04 Revision 15 — Underside Boss Removed

## Geometry change
Revision 15 starts from Revision 14. The local underside reinforcement boss (Ø12.5 mm × 2.2 mm projection) has been removed entirely. The underside is now the body’s flush plane at Z=0.00 mm. The FreeCAD feature tree contains no center reinforcement/pad feature. The upper cross-shaped horn recess and short-arm geometry remain unchanged.

The center opening remains a concentric Ø8.00 mm through-hole (radius 4.00 mm). Its cutter passes from Z=0.00 to Z=4.80 mm through the 3.80 mm coupon body. It opens into the upper horn-arm recess at its seating plane; no smaller internal bore, shelf, or ring is present.

## CAD validation
- FreeCAD 1.1.4 recompute: valid single connected solid.
- Coupon bounds: 42.000 × 23.000 × 3.800 mm; volume: 1052.125 mm³.
- Actual underside geometry: flush at Z=0.00 mm; no raised central boss.
- Actual cylinder cutter: Ø8.00 mm, centered at X=Y=0.
- Section at Y=0 confirms the bore walls at X=±4.00 mm up to the horn-seat plane Z=+2.10 mm, then the cavity opens into the preserved upper cross pocket.
- X-axis remains symmetric: nominal reach 19.50 mm per side, nominal span 39.00 mm; pocket span 39.20 mm. Short arm pockets remain +Y width 3.40 mm and −Y width 4.40 mm.
- FreeCAD recompute test changed the bore parameter and measured a resulting geometry/volume change, then restored Ø8.00 mm.

## Export validation
- STL: 4,282 triangles; all unique edges have incidence 2 (watertight closed manifold).
- STL bottom rim vertices measure radius 3.999995–4.000006 mm (mesh precision), confirming Ø8.00 mm.
- 3MF: valid archive, one object, triangle count matches STL; model Z range is 0.00–3.80 mm, so its underside is placed on the build plane.
- Build envelope: 42 × 23 × 3.8 mm, within Creality K2 volume.
- Estimated net ABS mass: 1.09 g using 1.04 g/cm³ assumed density; brim/purge/slicer overhead excluded. No sliced estimate is claimed.

## Physical status
This remains a fit-test coupon. The actual horn fit is unverified until printed and tested. Inspect the sliced preview in Creality Print before printing.
