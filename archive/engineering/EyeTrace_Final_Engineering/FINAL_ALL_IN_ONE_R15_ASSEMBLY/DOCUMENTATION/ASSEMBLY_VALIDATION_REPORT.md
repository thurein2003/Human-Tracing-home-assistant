# R15 Assembly Validation Report

Date: 2026-11-18. Software: FreeCAD 1.1.4. Source geometry: `FINAL_ALL_IN_ONE_R15\CAD\EyeTrace_Final_Assembly_R15.FCStd`. No source file was modified.

## Release verdict

**ASSEMBLY VALIDATION: FAIL.** The editable document is generated and opens, and contains the 13 named printable BREP parts plus hardware/reference geometry. It is not an acceptable mechanically validated assembly because the saved-document motion audit reports coincident/penetrating camera spacers and base, while both provisional servo horns are far from the corresponding drive components. The render must not be read as proof of assembled interfaces.

**R15 geometry traceability: PROVISIONAL PASS.** Source dimensions are retained as reference properties: pan/tilt horn pockets 39.2 mm span (19.6 mm reach each), 20.2 mm short span, 1.7 mm pocket depth, Ø8.0 mm center opening; camera mounting centers 21 × 14 mm. Annular support lands are retained in the source BREP; this package does not modify the printable geometry. Exact pocket-to-assembly shape matching is not re-established by this task.

**Physical SG90/horn fit: UNVERIFIED.** Servo and four-arm horn references are explicitly provisional. No hardware dimensions/test print evidence has been supplied for this R15 fit.

## Assembly contents and functional roles

| Printable part | Intended function |
|---|---|
| Base_EarMount_ThrustSupport | Stationary base and pan-servo support |
| Pan_Replaceable_ThrustRing | Pan thrust surface |
| PanYoke_EarBracket_KeyedDrive | Pan rotor/yoke and horn pocket |
| Tilt_Removable_IdlerPillar | Opposite-side tilt pivot support |
| Pan_KeyedHorn_Cover | Pan horn retaining cover |
| TiltCradle_KeyedHorn_CameraFrame | Tilt cradle, camera frame, tilt horn pocket |
| Tilt_KeyedHorn_CaptiveCover | Tilt horn retainer |
| Tilt_Journal_FlangedSleeve | Opposite tilt journal sleeve |
| PCB_Spacer_Lower_Left/Right | Lower camera-board spacers |
| PCB_Spacer_Upper_Left/Right | Upper camera-board spacers |
| CameraPlate_Cut007 | Camera plate; 21 × 14 mm hole-center pattern |

The document also contains non-printable servo/horn/camera references, fasteners, and keep-out envelopes. Reference geometry must not be interpreted as hardware verification.

## Geometry and kinematics results

- Printed source BREP checks: 13 designated printable components; source audit reports each as one valid solid. The clean assembly document copied source BREP geometry without changing the shapes.
- Camera pattern: source parameter values are 21 mm horizontal × 14 mm vertical (nominal user-supplied centers).
- Pan axis datum recorded: vertical Z axis through (0,0).
- Tilt axis datum recorded: X axis through y=0, z=78 mm.
- Placement helper smoke test: PASS for transform math; combined pose pivot residual 1.46e-14 mm. This verifies arithmetic only, not a native FreeCAD joint solve or real mechanism movement.
- Native Assembly workbench joints/solver were not constructed. `KinematicGroup` is metadata, and `Set_Pan_Tilt_Angles.py` applies placements; no joint connectivity/DOF proof is made.
- Saved-document representative pose collision audit: FAIL. At neutral, it reports base-to-each-camera-spacer intersections of 22.667 mm³ and every spacer-to-spacer pair at 45.333 mm³. The same spacer-pair overlaps persist at all sampled poses (pan ±30°, tilt ±15°). These are unintended geometry-placement conflicts until independently reconciled against the source model and print STLs.
- Pan horn to pan yoke reported nearest separation: 33.500 mm; tilt horn to tilt cradle: 52.500 mm. The sampled horn shapes do not meet their drive pocket interfaces. Torque path therefore FAIL in the current assembled-coordinate document.
- Axis coaxiality and actual torque transfer: FAIL / not demonstrated, given the horn gaps above.
- No mechanical travel limits are asserted. Sampled angles are diagnostic poses only; physical motion is unverified.

## Print-layout document

`EyeTrace_R15_Print_Layout.FCStd` is a separate FreeCAD mesh document decoded from the exact fixed 3MF build objects. The source 3MF audit reports 13 intended printable meshes, each mesh solid, all at z=0, with overall bounds X=13..234 mm, Y=13..227.595 mm, Z≈0..77 mm, inside the 260 × 260 mm bed. This does not prove the operational assembly is mechanically valid. The per-object model transforms and mesh geometry were crosschecked to the fixed 3MF by the existing layout audit.

## Remaining blockers

1. Resolve source-shape versus object-placement semantics for every component, especially the four camera spacers; rerun exact pairwise tests on the final reopened FCStd.
2. Locate both horn models at the real servo output interfaces and prove engagement with the matching pan yoke and tilt cradle pockets without changing the verified R15 pocket geometry.
3. Establish native fixed/revolute joint connectivity or explicitly retain a transform-only study with no DOF claim.
4. Confirm horn, servo, camera envelope, fastener, and ribbon clearances from actual hardware measurements and physical fit tests.
5. Do not authorize a full mechanical print based on this assembly document.
