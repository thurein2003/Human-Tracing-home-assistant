# R15 geometric verification — exact final 3MF

**Scope:** read-only comparison of the exact R15 FreeCAD source and `FINAL_ALL_IN_ONE_R15/EyeTrace_K2_ABS_All_In_One_R15.3mf`. No source CAD, final CAD, STL, 3MF, or prior validation file was changed. This report and supplemental section/audit evidence were added separately.

## Verdict

| Check | Result | Evidence |
|---|---|---|
| Pan yoke horn pocket profile | **PASS — CAD profile only** | R15 BREP cutter is fully cleared from the prepared pan-yoke volume where it intersects the carrier; 0.000 mm³ residual material and 0.000 mm³ unremoved target volume. The exact 3MF pan mesh matches its placed STL mesh to sub-micron numerical precision. |
| Tilt cradle horn pocket profile | **PASS — CAD profile only** | Same comparison for tilt cradle; 0.000 mm³ residual and unremoved target volume. The exact 3MF tilt mesh matches its placed STL mesh to sub-micron numerical precision. |
| Ø8 center opening | **PASS — CAD geometry** | Ø8.00 mm cylinder probe has 0 mm³ solid intrusion along both drive axes; no smaller bore restriction is modeled. The cross recess merges with the bore at its face by design. |
| No protruding underside boss | **PASS — CAD datum check** | The restored annular land is inside the original counterbore envelope and begins flush at the carrier interface face; it does not extend outward past the face datum. It is an added internal support land and differs from the flat coupon underside. |
| Camera mounting pattern | **PASS — 3MF geometry** | Hole centers are (−10.5,69), (−10.5,83), (10.5,69), (10.5,83) mm in the assembly’s X/Z plane: exactly 21 × 14 mm center-to-center. The camera plate mesh is unchanged apart from placement translation. |
| Exact 3MF build-plate non-overlap | **FAIL** | Actual object meshes in the specified 3MF have surface intersections for three separate printable-part pairs. See “3MF placement/collision finding.” |
| Physical horn/servo fit | **UNVERIFIED** | The R15 test coupon has not been physically tested with the actual horn; servo spline and retaining screw fit are not established by these CAD comparisons. |

Therefore, the **horn-pocket cuts match the R15 BREP**, but the exact supplied 3MF is **not a valid non-overlapping single-bed layout**, and the CAD interfaces are not physically approved. Do not print the all-in-one 3MF as a bed job in its current state.

## R15 source geometry measured from BREP

Source file: `CrossHorn_ABS_Revision_01/PROTOTYPE_04_REVISION_15/CrossHorn_UltraMinimal_FitTest_04R15.FCStd`, object `ArmPocketTool` and final coupon solid. Measurements below are millimeters. “Nominal horn” dimensions are user-confirmed/profile inputs; the larger pocket dimensions include the R15 clearance/extension.

| Feature | R15 source BREP measurement | Pan integrated pocket | Tilt integrated pocket | Difference |
|---|---:|---:|---:|---:|
| Nominal long-axis span | 39.000; equal nominal reaches 19.500 / 19.500 | Same | Same | 0.000 nominal |
| Pocket long-axis envelope | 39.200; reaches −19.600 / +19.600 | 39.200 | 39.200 | 0.000 |
| Long arm root width | 7.200 total pocket width (7.000 provisional profile + 0.200 total clearance) | Same BREP cutter | Same BREP cutter | 0.000 |
| Long arm tip width at rounded-cap center | 4.7539; equal on both sides | Same BREP cutter | Same BREP cutter | <0.001 |
| Long rounded-end radius | 2.3769 | Same | Same | <0.001 |
| Taper | Symmetric; 7.15° profile construction value; section width at X=10 is 5.7797 | Same | Same | 0.000 from source tool |
| Upper short arm (+Y) | Reach 10.100; width 3.400; end radius 1.700 | Same | Same | 0.000 |
| Lower short arm (−Y) | Reach 10.100; width 4.400; end radius 2.200 | Same | Same | 0.000 |
| Short-axis pocket envelope | 20.200 total | 20.200 | 20.200 | 0.000 |
| Recess depth | 1.700 | 1.700 tool depth | 1.700 tool depth | 0.000 |
| Center passage | Ø8.000 continuous through coupon thickness (3.800) | Ø8.000 clear along pan axis | Ø8.000 clear along tilt axis | 0.000 nominal |
| Inner circular step / smaller restriction | None in the Ø8 passage | None detected in bore probe | None detected in bore probe | None |
| Underside boss | None on coupon | No outward projection past the carrier datum; internal annular land remains | No outward projection past the carrier datum; internal annular land remains | See below |

The source BREP is one valid solid. Its measured cutter bounds are X = −19.600…+19.600, Y = −10.100…+10.100, and Z = 2.100…3.800. The short arms are constant-width rounded-ended arms, not tapered. The X arms are mirrored. The nominal 39 mm horn span is distinct from the 39.2 mm pocket envelope.

### Integrated geometry and tolerance comparison

The actual final assembly solids were sectioned and compared with the source cutter transformed to the pan and tilt axes. The source-tool region that intersects the original/prepared carrier was fully removed in each final carrier: pan target volume 221.892701 mm³, tilt target volume 244.188359 mm³; both had 0.000000 mm³ residual and 0.000000 mm³ missing removal. The smaller values than the 461.656735 mm³ full cutter are because portions of the cutter lie outside the original carrier envelope, not because the cutter was scaled. The Boolean comparison tolerance is FreeCAD/OpenCascade’s geometric kernel tolerance; it does not represent printer accuracy.

Actual profile sections measure the left/right long-arm tip width as 4.7539 / 4.7539 mm and the upper/lower short-arm widths as 3.4000 / 4.4000 mm. The long-arm section width at X=10 is 5.7797 mm. A section near the long-arm root, X=2.5, is 6.8449 mm; the root value of 7.200 mm is the extrapolated BREP taper intercept, where the orthogonal short-arm junction obscures the root boundary in a direct section.

The pan and tilt carriers preserve a concentric Ø9.20/Ø8.00 annular support land (outer radius 4.600, bore radius 4.000). It refills the older Ø8.50 counterbore and lies inward from the original interface datum: pan spans Z=35.000…37.300 with the outer face at Z=35.000; tilt spans X=−41.000…−38.800 with the outer face at X=−41.000. Thus this is a recessed/flush support feature, not a boss projecting outward. It is an additional internal land absent from the minimal R15 coupon profile.

CAD nominal clearance between the modeled horn profile and carrier walls is approximately 0.10 mm per side (0.20 mm total where specified). No exact clone-horn spline, horn-hole fastener pattern, or physical ABS fit has been validated.

## Section views

The image below is generated from actual FreeCAD BREP section edges at the source coupon and both final carrier interfaces. The dashed outline is the R15 source section transformed to each carrier’s local axis; the solid outline is the final carrier section.

![FreeCAD BREP section comparison](../RENDERS/R15_Interface_Section_Comparison.svg)

Raw section points and geometry measurements are in `CHECKS/r15_actual_section_edges.json` and `CHECKS/r15_exact_geometry_comparison.json`.

## Exact 3MF checks and layout failure

The 3MF mesh objects for pan yoke and tilt cradle have the expected triangle counts (9,942 and 9,108). Their vertex sets match their bed-component STL meshes to approximately 0.000001 mm; bidirectional face-centroid-to-triangle checks report maximum deviations below 0.000001 mm. The 3MF camera-plate mesh has the same 3,828 triangles and 1,898 vertices as the placed camera-plate STL after accounting for a rigid translation of +45.000 mm X and +16.000 mm Y. That translation preserves the 21 × 14 hole pattern.

However, the actual 3MF mesh vertices—not the earlier `bed_components` STL positions—give overall bounds X=10…224 mm, Y=10.004…230 mm, Z≈0…77 mm. They fit inside the K2’s 260 × 260 mm XY envelope, but FreeCAD mesh-surface intersection checks find:

- `Base_EarMount_ThrustSupport` × `PanYoke_EarBracket_KeyedDrive`: **1,019 intersecting facets**
- `Pan_KeyedHorn_Cover` × `TiltCradle_KeyedHorn_CameraFrame`: **4,315 intersecting facets**
- `TiltCradle_KeyedHorn_CameraFrame` × `Tilt_KeyedHorn_CaptiveCover`: **12,271 intersecting facets**

These are separate printable parts, so those crossings are not acceptable as a one-bed arrangement. The earlier layout screenshot and `3mf_package_validation.json` describe different placed component geometry and do not validate the exact 3MF’s build objects. The exact R15 3MF therefore fails the all-in-one print-layout check even though the requested geometry is on the bed.

## Camera check

The 3MF camera plate is object `CameraPlate_21x14`; it remains 56 × 32 mm in envelope in the 3MF mesh and differs from its placed STL only by the translation above. The FreeCAD mounting-hole centers are exactly (±10.5, ±7.0) mm relative to pattern center, i.e. 21.000 × 14.000 mm center-to-center. PCB outside envelope remains a separate parameter.

## Final conclusion

- The two **R15 cross-pocket cuts match their source BREP** within CAD-kernel tolerance.
- The Ø8 mm passage and 21 × 14 mm camera pattern pass CAD geometry checks.
- A flush annular support land is present around each Ø8 bore; it does not project outward beyond the original carrier face.
- The exact all-in-one 3MF has three printable-part mesh intersections and is **not ready to print as a single bed**.
- Physical horn fit remains **unverified** until the R15 coupon is tested with the actual white SG90 horn. No physical compatibility or production approval is claimed.
