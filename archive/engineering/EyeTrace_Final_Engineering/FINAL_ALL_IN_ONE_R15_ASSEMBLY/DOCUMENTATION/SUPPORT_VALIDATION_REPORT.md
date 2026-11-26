# ABS Support Validation Report

Date: 2026-11-18. Slicer: Creality Print 7.2. Printer profile: Creality K2, 260 × 260 mm. Material tile shown as ABS; nozzle 255 °C and bed 100 °C, 0.20 mm layers, four walls, 35% infill, 5 mm global brim with per-part overrides. Confirm exact filament manufacturer limits before a production job.

## Files and geometry preservation

- Input: `FINAL_ALL_IN_ONE_R15_LAYOUT_FIXED\EyeTrace_K2_ABS_All_In_One_R15_Fixed.3mf`.
- Support trial: `EyeTrace_R15_ABS_AutoTree_SupportTrial.3mf` in the output folder. Only slicer support metadata was changed; printable mesh geometry was kept identical.
- The fixed layout contains 13 intended components. Mesh/layout audit reports all are solid, rest at z=0 and fit within the 260 × 260 mm plate (overall X=13..234 mm, Y=13..227.595 mm). The closest 3D part spacing and expanded support/brim footprints were not exhaustively computed from G-code paths.

## Actual sliced support result

The fixed 3MF originally marked support enabled on Base, PanYoke and TiltCradle while selecting `tree(manual)` without manual supports. The slice preview showed no support paths, so those flags alone were ineffective.

A separate trial used automatic tree supports, build-plate-only, slim style on those three parts. The actual Creality Print sliced preview showed tree-support, support-interface and support-transition toolpaths. Screenshot: `RENDERS\EyeTrace_R15_Support_Preview.png`.

| Slicer estimate | Result |
|---|---:|
| Total time | 14 h 13 min |
| Total filament | 140.83 g (56.30 m) |
| Support | 22.37 g, 2 h 08 min |
| Support interface | 1.69 g, 17 min 10 s |
| Support transition | 1.59 g, 14 min 50 s |
| Support categories combined | 25.65 g, about 2 h 40 min |
| Brim | 1.52 g, 14 min 15 s |

The estimates are slicer estimates, not measured consumption or elapsed time.

## Inspection and unresolved print risks

- Actual layer/toolpath preview was inspected. Tree supports are visible under the pan yoke and tilt cradle; the 3MF's originally absent support paths are corrected in the separate trial.
- The preview does not establish removal force, interface scarring, or final fit. Support is visible in open regions; precision surfaces and hidden cavities still require layer-by-layer review before printing.
- No slicer warning was observed in the captured preview, but support/brim-to-neighbor minimum XY clearance was not analytically extracted from every toolpath. Do not treat visual inspection as a quantified clearance proof.
- Important slicer profile mismatch: the interface showed a process preset name containing “PETG” while the filament tile/settings showed ABS. Confirm and save a genuine ABS process preset before printing; do not rely only on the filament tile.
- Creality Print supports were checked for three parts only. Supports were not enabled for the other ten parts in this support trial. Their actual needs should be judged from the model orientation and sliced layers; avoid support inside horn pockets, camera holes, pivot bores, nut traps, and precision lands.
- Mechanical assembly validation has failed (see assembly report); a successful print slice is not a mechanical release.
- Physical SG90 horn fit remains unverified. No full assembly production release is made.

## Release status

**Support toolpaths: slicer-preview verified for the three auto-tree-supported parts only.**

**Complete ABS print package: NOT RELEASED.** Confirm the ABS process preset, review all 13 parts at layer level and their support footprints, and resolve assembly failures before a complete print.
