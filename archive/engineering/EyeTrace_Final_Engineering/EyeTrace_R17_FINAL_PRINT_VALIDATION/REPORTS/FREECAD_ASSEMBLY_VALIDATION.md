# FreeCAD assembly validation — R17 final print check

## Verdict: HOLD

FreeCAD 1.1.4 reopened the saved R17 assembly. Both modified carrier BREPs are valid, one-solid shapes, and their isolated pocket voids match the Revision 15 master. The assembled pan interface fails clearance because the R17 material restoration creates new solid intersections.

### Interface geometry

| Carrier | Extra R15-pocket void | Missing R15-pocket void | Envelope | Depth | Center hole |
|---|---:|---:|---:|---:|---:|
| Pan yoke | 0.000 mm³ | 0.000 mm³ | 39.2 × 20.2 mm | 1.7 mm | Ø8.0 mm |
| Tilt cradle | 0.000 mm³ | 0.000 mm³ | 39.2 × 20.2 mm | 1.7 mm | Ø8.0 mm |

Four independent Ø3.3 mm retainer bores remain. Pocket-profile matching is a geometry comparison only and does not establish an installed horn fit.

### New pan intersections vs R16

| Pair | R16 common volume | R17 common volume |
|---|---:|---:|
| Pan carrier / modeled cross horn | 0 | 291.272 mm³ |
| Pan carrier / retainer cover | 0 | 1,655.771 mm³ |
| Pan carrier / each of two M3 drive screws | 0 | 4.017 mm³ |
| Pan carrier / each of two M3 drive screws | 0 | 8.413 mm³ |

These are BREP common volumes, not assumed fastening contact. They show that the restored R17 pan seat occupies space used by the modeled horn, cover, and fasteners. **The pan assembly fails; do not print or assemble this pan yoke.** Tilt added material had zero common volume with its listed horn, cover, four drive screws, and servo in this limited local check; this is not a full tilt clearance or motion pass.

### Alignment and motion

The source document reopened with 54 objects and valid top-level/group shapes. No native Joint, Ground, or simulation objects were found in the saved document. The local seat-axis profile comparison passed, but a full assembly axis-coaxiality audit, all-pair interference sweep, service-access check, and pan/tilt representative motion simulation were not completed. Those items remain **UNVERIFIED**.

The camera mounting plate was carried through unchanged and retains the nominal 21 × 14 mm center spacing. This run did not independently remeasure the physical camera or validate its cable envelope.

Detailed data: `ASSEMBLY_PAIR_INTERFERENCE.json`; source placements and BREP checks are in the R17 cleanup folder.
