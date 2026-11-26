# Plate 02 blocker resolution — mechanical and slicer evidence

Date: 2026-11-18. Scope: Plate 02 only. Plate 01/base print and files were not opened, modified, or resliced.

## Tilt horn / two screw intersections

FreeCAD local BREP check on the repaired assembly reports 10.602875 mm³ common volume between `Tilt_OriginalStar_PROVISIONAL` and each of `TiltDrive_M3x10_2` and `_3`; minimum separation is effectively 0 mm. The same simplified horn proxy intersects the tilt servo output reference by 73.263511 mm³, which is expected at an output-engagement location.

The project contains no measured/scan-derived white horn BREP. It contains a single-solid `Tilt_OriginalStar_PROVISIONAL` reference and the physically fitted R15 coupon. The R15 master coupon has no secondary fastener-hole geometry/coordinates. Consequently the two screw overlaps are consistent with the proxy omitting the real horn holes, but they cannot be proven to be proxy-only; actual collision versus intended fastening engagement remains **UNVERIFIED**. No screw or carrier geometry was changed and no hole positions were invented. Physical horn hole centers and diameters (or a scaled top/underside photo with caliper references) are still needed to close this item.

## R15 pocket shape comparison

The R17 cleanup BREP audit compares both mapped carrier voids against the R15 master BREP, not just bounding boxes. Recorded difference volumes are:

| Interface | Extra void vs master | Missing master void | Result |
|---|---:|---:|---|
| Pan | 0.000 mm³ | 0.000 mm³ | Exact within the BREP Boolean check |
| Tilt | 0.000 mm³ | 0.000 mm³ | Exact within the BREP Boolean check |

Master profile dimensions: 39.2 × 20.2 mm envelope, 1.7 mm recess, Ø8.0 mm center bore. The repaired assembly uses the R17 tilt carrier and the selectively repaired pan carrier cut with the same master. The physically tested master coupon itself was not changed. This verifies the cavity shape comparison recorded by FreeCAD; it does not verify the user's particular horn axial stack or secondary screw-hole engagement.

## Static minimum distances (FreeCAD `distToShape`, mm)

| Pair | Common volume (mm³) | Minimum distance (mm) | Classification |
|---|---:|---:|---|
| Pan carrier / horn retainer | 0 | 0.200 | Clearance |
| Pan carrier / pan servo housing | 0 | 1.500 | Clearance; shaft/horn engagement checked separately |
| Pan carrier / base thrust support | 0 | 0.300 | Clearance |
| Pan carrier / pan thrust ring | 0 | 0.000 | Intended bearing/contact interface |
| Tilt carrier / tilt retainer | 0 | 0.000 | Intended mating/seating contact |
| Tilt carrier / tilt servo housing | 0 | 1.500 | Clearance; output engagement checked separately |
| Tilt carrier / idler pillar | 0 | 0.500 | Clearance |
| Tilt carrier / journal sleeve | 0 | 0.000 | Intended pivot/journal contact |
| Tilt horn proxy / screws 2 and 3 | 10.603 each | 0 | Unresolved proxy/hardware engagement |

No positive-volume intersection was found for these carrier-to-mate pairs except the explicitly noted proxy overlaps. Zero distance at the thrust ring, retainer seat, and journal is intentional contact, not a clearance.

## Motion diagnostic and limits

Diagnostic transforms of the pan carrier alone about the vertical axis and tilt carrier alone about the horizontal axis were sampled at −20°, −10°, 0°, +10°, +20°. Pan carrier-to-base-support minimum distance remained 0.300 mm at those samples; tilt carrier-to-servo-housing remained 1.500 mm. These are **limited local carrier checks**, not full assembly motion simulation: the project does not define intended travel limits or a native revolute-joint graph, and the diagnostic did not transform every rigidly attached component/cable as a mechanism. Intended travel clearance and servo-command limits therefore remain **HOLD**.

## Base and camera compatibility

The base was not altered. At nominal placement, the repaired pan carrier has 0.300 mm minimum distance to the checked base thrust support and zero common volume. This is local compatibility evidence only, not proof of free full-range rotation. Camera mounting remains the source nominal 21 × 14 mm hole pattern; no camera parts were changed.

## Creality Print slicing result

The installed executable is `D:\Creality Print 7.2\CrealityPrint.exe`; despite that directory/registry label, the actual sliced 3MF identifies Creality Print build **07.03.02.6412 (7.3.2.6412)** in `Metadata/slice_info.config`. The exact source Plate 02 3MF opened in that GUI with Creality K2, 0.4 mm nozzle, Textured PEI plate, and the ABS filament preset `EyeTrace ABS 255C K2 100C`.

Slicing completed successfully. Genuine Preview values displayed by the slicer:
- Filament: **94.26 g** (37.68 m)
- Estimated time: **10 h 21 min**
- Process metadata: 3 walls, 20% gyroid, 5 mm global outer brim, tree(auto)/tree_slim supports; pan yoke and tilt cradle support enabled, support-on-build-plate-only enabled for those carriers. Their model-level brim widths are 8 mm and 6 mm respectively.
- Profile temperatures: nozzle 255 °C, first layer 255 °C; bed/textured plate 100 °C first and subsequent layers; fan min 0%, max 15%.

The actual Preview screenshot shows sliced model paths and tree supports on the tall pan yoke and tilt cradle, as well as brim/toolpath paths. The screenshot was saved to `RENDERS/Plate02_Sliced_Toolpaths.png`. The preview was captured at the displayed upper Z=77.00 mm. An isolated layer-one screenshot and inspection of the critical pocket layers were not completed; therefore first-layer adhesion/collision and fine pocket-wall paths are not signed off. No print job was sent to the printer. (A Send-to-LAN dialog opened during UI navigation and was closed without sending.)

The completed sliced project was saved as a new 3MF and copied into this repair's `PRINT` folder. Source project and Plate 01 were not overwritten.

## Verdict

- Tilt R15 pocket BREP: **PASS** (zero extra/missing void in recorded direct comparison).
- Tilt horn-to-screw physical diagnosis: **UNVERIFIED** (simplified proxy has no measured mounting holes).
- Static carrier clearances: **PASS for measured local pairs**, with intentional contacts identified above.
- Full intended pan/tilt travel: **HOLD** (limits/joints/full rigid assemblies not defined or tested).
- Slicing: **PASS — slice completed**, 94.26 g, 10 h 21 min.
- Print readiness: **HOLD** until first-layer and critical horn-pocket layers are inspected and actual horn screw-hole engagement is resolved.
