# Validation and release record — CrossHorn ABS Revision 01

## Results completed in software

| Check | Result | Evidence / scope |
|---|---|---|
| FreeCAD version / coupon generation | PASS | FreeCAD 1.1.4; `ABS_Clearance_Calibration.FCStd`; 20 valid solid coupon objects |
| Pan-ring calibration pair | PASS (CAD intent only) | Source BRep: 64.0 mm male OD, 64.6 mm female ID; coupon candidates test diametral gaps 0.10, 0.20, 0.30, 0.40 and 0.60 mm |
| Tilt journal coupon | PASS (CAD intent only) | 5.00 mm journal plugs with 5.05, 5.10, 5.15, 5.20 and 5.30 mm bores; 5.20 mm is the current source control |
| STL binary structure / manifold edge test | PASS | 21 meshes checked (bed + 20 individual files); every mesh edge occurs twice; zero boundary/nonmanifold edges |
| Coupon component interference | PASS | FreeCAD checked the 10 bounding-box-overlap pairs among 20 coupon solids; zero solid intersections |
| K2 bed envelope | PASS | Bed STL extents 241.284 × 206.294 × 6.0 mm, within 260 × 260 × 260 mm; minimum 18.6 mm side margin on X |
| Camera pattern | PRESERVED | Source correction parameter file specifies 21 × 14 mm center spacing, separate from provisional 38 × 38 × 1.6 mm PCB envelope |
| Existing native assembly solve/connectivity | PASS (source revision only) | Recomputed unmodified corrected 21 × 14 native assembly: solver return 0; one grounded base, four fixed joints, two revolute joints; all seven rigid bodies connected; 90 solid objects valid |
| Stored native motion simulations | PASS (source revision only) | Pan, tilt and combined simulations each regenerated to 52 frames. Pan-only peak sample: 59.8816° with pan stator fixed; tilt-only: 24.9507° with pan rotor and tilt stator fixed; combined sample: pan 44.9112°, relative tilt 19.9605° |
| Camera hole centers in assembly | PASS | BRep centers X = ±10.5 mm and Z = 69/83 mm; measured pitch 21 × 14 mm |
| Existing star-horn profile | FAIL for actual hardware compatibility / UNVERIFIED torque fit | Five-arm proxy remains in the source only: five 72° arms, nominal length 12 mm, width 3.6 mm, hub radius 4 mm; pan and tilt carriers retain legacy star cavities |
| Creality Print project package | PASS (package structure/settings) | One bed object, 18,148 mesh triangles; 0.20 mm layers, 255/100 °C start temperatures, 4 walls, 100% infill, support disabled, 4 mm outer-only brim |
| Creality sliced toolpath | NOT VERIFIED | Project package passed structural/settings checks; no new G-code/toolpath inspection was completed in this revision |
| Cross-horn model/pocket | BLOCKED_PENDING_MEASUREMENT | Three photos establish shape only. The builder exits before writing geometry while 17 essential dimensions and confirmation of opposing-arm symmetry are missing |
| Revised cross-horn assembly, motion, collision and STEP | NOT GENERATED | Native simulation revalidation above applies only to the original star-proxy CAD. New assembly/motion/collision/STEP must follow measured horn geometry |
| ABS physical fit | UNVERIFIED | Coupons have not been printed/tested in this work |

## Release stage

- CAD VERIFIED: **PARTIAL for clearance coupons and the unmodified 21 × 14 native assembly check**; cross-horn mechanism is not verified.
- FIT-TEST READY: **YES for circular joint clearance coupon**. Cross-horn test is blocked until essential horn/screw dimensions are supplied.
- FULL-PRINT READY: **NO CHANGE / NOT APPROVED**. Existing full print project was not changed.
- PHYSICALLY VERIFIED: **NO**.

No motion, strength, cross-horn torque-transfer, or final ABS clearance claim is made. After measurements, update horn and pocket geometry in this separate revision, create and pass the horn coupon, then rerun assembly solver, torque path, full-range collisions, exports, and slicing before considering a full print.

The image in `RENDERS/ABS_clearance_coupon_top_render.png` is a top orthographic projection of the actual FreeCAD BRep edges. It is a coupon visualization, not an assembled mechanism screenshot. Detailed native simulation evidence is in `CHECKS/native_21x14_motion_revalidation.json`.
