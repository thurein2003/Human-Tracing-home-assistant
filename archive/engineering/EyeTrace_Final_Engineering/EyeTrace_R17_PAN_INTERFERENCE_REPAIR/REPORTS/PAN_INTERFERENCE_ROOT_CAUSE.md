# R17 pan interference — cause and disposition

## Result

**HOLD — no geometry repair applied.** The actual R15 pocket remains an isolated exact match, but the R17 pan carrier does not clear the installed modeled horn, cover, and screws. Current R17 assembly and print files in this folder are source snapshots renamed HOLD; they are not repaired outputs.

## Reproduction and cause

The R16 source carrier and its corresponding modeled pan horn, retainer cover, and four M3 drive screw solids have zero BREP common volume. R17 retains the same component placements, but its rebuild changes the carrier shape. The FreeCAD macro cuts the full Ø41.0 × 3.8 mm local cylinder from the carrier, then fuses a solid circular disk with the R15 cross pocket removed. The added-material delta is 3,501.396 mm³, with global bounds X/Y ±20.5 mm and Z 33.0–36.8 mm.

That broad fill overwrites clearance volume used by the surrounding hardware. New R17 common volumes are:

| Pair | R16 | R17 | New overlap |
|---|---:|---:|---:|
| Pan carrier / provisional four-arm horn | 0 | 291.272 mm³ | 291.272 mm³ |
| Pan carrier / retainer cover | 0 | 1,655.771 mm³ | 1,655.771 mm³ |
| Pan carrier / each of two screws | 0 | 4.017 mm³ | 4.017 mm³ each |
| Pan carrier / each of two other screws | 0 | 8.413 mm³ | 8.413 mm³ each |

The overlap locations are contained within the added-material region. The servo body itself has zero overlap with the added material. Thus the measured cause is the carrier Boolean construction, not a moved servo or axis placement. The cover and screw overlaps show that some of the R16 surrounding voids are functional clearance and cannot be indiscriminately filled as “legacy slots.”

The horn intersection is with `Pan_OriginalStar_PROVISIONAL`, a simplified solid whose current envelope is 39 × 20 mm in plan and 4.0 mm tall. The master seat is only 1.7 mm deep. The actual white horn passed its separate R15 coupon test, so this simplified assembled horn solid is not a trustworthy axial fit model. The drawing/profile match in plan does not resolve its axial shape or installed seating datum.

## Why no repair was issued

A safe repair must preserve both (a) the tested R15 pocket and (b) actual clearance for the installed cover, screw heads, and real horn. The broad circular fill fails (b). Moving the servo or horn would conceal a carrier defect and would alter axis/retaining-screw alignment without evidence. Cutting the R15 pocket deeper or wider would change the physically tested interface. The current CAD does not supply verified white-horn arm thickness and two-sided hub protrusion sufficient to replace the provisional 4 mm horn solid with a faithful axial envelope. I therefore stopped without modifying the validated R15 interface or issuing a falsely passing assembly.

## Tilt status

The tilt carrier's newly added material had zero BREP intersection with its listed horn, retainer cover, four screws, and tilt servo in this limited check. This does not constitute a complete pairwise clearance or motion validation.

## Minimum physical data to resolve the horn proxy

With calipers, measure the real white horn:

1. Arm plate thickness at a straight section, away from the raised hub.
2. Hub protrusion from the arm plane on the servo-facing side.
3. Hub protrusion from the arm plane on the opposite side.
4. Which face seats against the printed carrier, and the distance from that seating face to the horn's servo-output engagement datum (a side-on photo beside the caliper helps).

The cover and screw positions are already available in CAD; their overlap is caused by the new fill. Any redesigned counterbore/relief must be checked in CAD against those existing solids and then in Creality Print.
