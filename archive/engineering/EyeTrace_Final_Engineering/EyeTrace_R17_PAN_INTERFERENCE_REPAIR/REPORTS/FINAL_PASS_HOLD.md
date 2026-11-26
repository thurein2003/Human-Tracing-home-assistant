# R17 pan repair / print validation — PASS/HOLD

## Overall: HOLD — no repaired assembly or FINAL print jobs issued

R17's isolated pan and tilt negative pockets match the R15 master BREP: 39.2 × 20.2 mm envelope, 1.7 mm depth, Ø8.0 mm center opening. The integrated pan assembly fails: the new pan-carrier fill intersects the installed provisional horn (291.272 mm³), retainer cover (1,655.771 mm³), and four screws (4.017–8.413 mm³ each). Those same pairs had zero overlap in R16. Cause and exact added-material bounds are documented in `PAN_INTERFERENCE_ROOT_CAUSE.md`.

No safe repair was made because the broad fill erased functional cover/screw clearance, and the installed 4 mm-tall pan horn solid is explicitly provisional and cannot fit the 1.7 mm recess as modeled. Changing the tested R15 pocket or moving the servo/horn without measured axial horn data would be unjustified.

The output includes unchanged R17 source snapshots with HOLD names, not repaired deliverables. The camera plate remains the source 21 × 14 mm pattern. No assembly-wide motion sweep was completed; no native FreeCAD joints were found in the saved document.

Creality Print 7.2 was not available to slice these projects. The stored 3MF metadata identifies Creality Print 7.3.1.6378 and records a 70 °C first-layer bed setting. No actual bridge/support, brim, first-layer, or horn-pocket toolpaths were inspected. Actual filament consumption and print time are unavailable. The two jobs remain HOLD.

| Plate | Components | Slice result | ABS mass/time | Status |
|---|---:|---|---|---|
| Plate 01 (base) | 1 | Not sliced; 23.3 mm bridge support unverified | Not available | **HOLD** |
| Plate 02 | 12 | Not sliced; pan assembly clearance fails | Not available | **HOLD** |

All 13 STL mesh files in the snapshot reported closed solids in FreeCAD; both 3MF archives passed package integrity and preserve the 1+12 build allocation. These checks do not override the pan interference or substitute for slicing.
