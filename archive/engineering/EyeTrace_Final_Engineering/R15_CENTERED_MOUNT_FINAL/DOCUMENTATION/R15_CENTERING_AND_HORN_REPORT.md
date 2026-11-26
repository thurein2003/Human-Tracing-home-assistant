# R15 centered-mount / horn-standardization validation

Date: 2026-11-18. FreeCAD: 1.1.4. Creality Print: 7.2. Printer profile target: Creality K2, ABS, 0.4 mm nozzle, 0.20 mm layers. This revision is saved separately under `R15_CENTERED_MOUNT_FINAL`; prior revisions were not modified.

## Release status

**HOLD — do not use this as the final full-plate print release yet.** The internal motor mount was not shifted because geometric centering would break the verified servo mounting alignment. The new 13-part FreeCAD assembly and STL/STEP exports have passed geometry checks; the new full-plate 3MF project has not been sliced in Creality Print in this run. The base-only tree-support slice and bridge layers are included as evidence for the base feature only. This report does not certify a full 13-part print.

## 1. Internal motor-mount center and conflict

Measured from the actual base BREP (`Base_EarMount_ThrustSupport`):

| Datum | X (mm) | Y (mm) | Evidence |
|---|---:|---:|---|
| Circular base geometric center | 0.00 | 0.00 | Ø64 mm outer cylindrical face axis |
| Pan rotation axis | 0.00 | 0.00 | Pan rotor bore/axis datum |
| Pan SG90 output-axis line | 0.00 | 0.00 | Servo reference output boss and shaft cylinders |
| Internal rectangular mount bounds | −13.00…+24.00 | −9.00…+9.00 | BREP planar faces |
| Rectangular-mount geometric center | **+5.50** | 0.00 | Midpoint of BREP bounds |
| Servo tab-hole centers | −8.15 and +19.05 | 0.00 | BREP hole axes in base |
| Servo tab-hole midpoint | **+5.45** | 0.00 | From measured centers |

**Before:** mount center is (+5.50, 0.00) mm relative to circular center.  
**After:** unchanged at (+5.50, 0.00) mm; no mount geometry was moved.  
**Reason:** the tab-hole midpoint is +5.45 mm, only 0.05 mm from the mount center, while the pan output axis is at X=0. Moving the entire mount by −5.50 mm would misalign both tab holes by 5.50 mm. Moving the servo with it would shift the output axis 5.50 mm off the pan axis. The existing offset is therefore the support geometry for the eccentric SG90 body, not a harmless placement error. A true centered structural redesign would require changing the motor support/tab interface or servo orientation and then rechecking the shaft axis. No such geometry change was made.

The rectangular mount’s farthest corner from the housing axis is √(24²+9²)=25.632 mm. The base interior radius is 27.50 mm, giving a nominal radial housing clearance of 1.868 mm at that corner. This is a CAD clearance, not a printed tolerance result.

## 2. R15 cross-horn pocket standardization

Compared with the master BREP `CrossHorn_UltraMinimal_FitTest_04R15.FCStd`, both integrated drive cuts retain the validated R15 geometry. The source comparison in `FINAL_ALL_IN_ONE_R15/DOCUMENTATION/R15_DIMENSION_VERIFICATION.md` reports zero residual and zero unremoved target volume for both drive pockets. No printed drive component geometry was modified in this revision.

| Feature | R15 master | Pan yoke | Tilt cradle | Difference/status |
|---|---:|---:|---:|---|
| Nominal horn long span | 39.000 mm | 39.000 mm | 39.000 mm | 0; user-measured nominal |
| Pocket long envelope / reaches | 39.200 / 19.600 each | Same | Same | 0; CAD pass |
| Short-axis pocket envelope | 20.200 mm | Same | Same | 0; CAD pass |
| Pocket depth | 1.700 mm | Same | Same | 0; CAD pass |
| Center passage | Ø8.000 mm through | Same | Same | 0; CAD pass |
| Long root pocket width | 7.200 mm | Same | Same | 0; CAD pass |
| Long tip width / rounded radius | 4.7539 / 2.3769 mm | Same | Same | <0.001 mm; CAD pass |
| Upper short-arm pocket | 10.100 mm reach, 3.400 mm width | Same | Same | 0; CAD pass |
| Lower short-arm pocket | 10.100 mm reach, 4.400 mm width | Same | Same | 0; CAD pass |
| Underside | no outward boss | internal annular support land retained | internal annular support land retained | Datum preserved |

The user has confirmed Revision 15 passed physical horn fit testing. The integrated pocket geometry comparison is a CAD result; it does not prove spline/screw/servo-case compatibility independently.

## 3. Assembly placement and interference

The saved separate FreeCAD assembly copy restores the cross-horn placements against the actual pocket axes and returns the four camera PCB spacers to their four 21×14 mm positions. The previous 33.50 mm pan and 52.50 mm tilt gaps were artifacts of measuring those horn solids without their axis placements.

| Interface | CAD placement | Min. clearance | Intersection | Result |
|---|---|---:|---:|---|
| Pan horn → pan yoke | horn center at (0,0), plane at Z=35 mm | 0.09975 mm | 0 mm³ | CAD clearance pass |
| Tilt horn → tilt cradle | axis X through Y=0, Z=78 mm; center at X=−41 mm | 0.09975 mm | 0 mm³ | CAD clearance pass |
| Camera spacers → base | restored to X=±10.5, Z=69/83 mm | no overlap | 0 mm³ | Pass |
| Camera spacers → camera plate | faces meet at datum | 0 mm | 0 mm³ | Intended contact |
| Base → pan thrust ring | faces meet | 0 mm | 0 mm³ | Intended contact |
| Pan thrust ring → pan yoke | faces meet | 0 mm | 0 mm³ | Intended rotating interface |
| Yoke → idler pillar | faces meet | 0 mm | 0 mm³ | Intended support/contact |
| Pan yoke → pan horn cover | faces meet | 0 mm | 0 mm³ | Intended retainer contact |
| Tilt cradle → tilt horn cover | faces meet | 0 mm | 0 mm³ | Intended retainer contact |
| Tilt cradle → journal sleeve | faces meet | 0 mm | 0 mm³ | Intended bearing/journal contact |
| Tilt cradle → camera plate | faces meet | 0 mm | 0 mm³ | Intended attachment contact |

All 13 printable components reopened as valid FreeCAD solids (one solid each). Pairwise check found zero positive-volume intersections; listed zero-distance pairs are intended mating/attachment surfaces. The exact camera pattern remains 21 × 14 mm center-to-center. The servo body models still contain provisional dimensions; their shape labels are references, not manufacturer-specific verification.

## 4. Internal bridge and support

The base has a **23.3 mm** clear support span between the internal rails. The actual Creality Print 7.2 base-only V7 tree-auto slice showed tree branches beneath the bridge at layer Z=19.16 mm and Z=19.80 mm. The configured support top Z gap was 0.24 mm. Evidence is in `RENDERS/Base_V7_Bridge_Z19.16.png` and `RENDERS/Base_V7_Bridge_Z19.80.png`. Those images are from the base-only V7 slice, not the new 13-part 3-wall/20% project.

The newly generated full-plate candidate retains automatic tree support on the base, pan yoke, and tilt cradle, with build-plate-only support. Its exact support toolpaths and neighbor/brim footprints still need a completed Creality Print slice and preview inspection before the full-plate job is approved.

## 5. ABS consumption comparison

These are actual Creality Print estimates for the **base only**, not the full 13-part assembly:

| Base-only setting | Filament | Time | Notes |
|---|---:|---:|---|
| 3 walls, 10% gyroid | 32.30 g | 2 h 43 min | no support paths in this variant; bridge support not proven |
| 3 walls, 15% gyroid | 33.37 g | 2 h 49 min | no support paths in this variant |
| 3 walls, 20% gyroid | 34.36 g | 2 h 55 min | no support paths in this variant |
| 3 walls, 20% gyroid, tree auto | **35.79 g** | **3 h 08 min** | actual base-only tree support paths; support categories total 1.43 g |
| Earlier 4 walls, 35% gyroid | 41.06 g | 3 h 26 min | baseline estimate, lacked verified bridge supports |

For this load-bearing base, the recommended starting point is **3 walls / 20% gyroid / tree-auto localized to the base overhang, with the bridge support enabled**, because it is the highest tested infill among the requested options and has actual bridge support toolpaths. It saves 5.27 g (12.8%) versus the unsupported 4W/35% baseline estimate, but adds support over the unsupported 3W/20% setting. This is not a strength certification; loading, ABS warping, and support removal remain physical checks. A 10% option is lower material but is not selected for the motor-support base without load testing.

The new full-plate candidate uses Creality K2, Textured PEI, ABS, 255°C nozzle, 100°C textured bed, 0.20 mm layers, 3 walls, 20% gyroid, 5 mm brim, tree-auto supports. A dimensioned BREP-derived top-view schematic is saved as `RENDERS/Base_Mount_Offset_Dimension_Diagram.svg`. A fresh FreeCAD PNG render could not be captured in the current desktop session; the SVG is explicitly a dimensioned schematic, not a screenshot. Confirm actual filament-manufacturer temperature limits. **Full-plate grams/time remain unverified because that new project has not completed slicing in Creality Print during this run.**

## 6. Files and checks

- Editable assembly: `CAD/EyeTrace_R15_AxisAligned_Assembly_HOLD.FCStd`
- Complete STEP export, including reference solids: `CAD/EyeTrace_R15_AxisAligned_Assembly_HOLD.step`
- Standalone base: `CAD/R15_Base_OriginalMountGeometry.FCStd` and `CAD/R15_Base_OriginalMountGeometry.step`
- 13 individual printable STL meshes: `STL/` (one connected watertight mesh per part)
- Full 13-part ABS slicer project candidate: `EyeTrace_R15_ABS_3W20_TreeSupport_CANDIDATE.3mf`
- FreeCAD audit JSON: `CHECKS/R15_geometry_alignment_audit.json`
- STL/STEP mesh validation: `CHECKS/mesh_step_validation.json`, `CHECKS/step_reopen_validation.json`

`STL/` STL checks: each intended part is one solid mesh, one connected component. STEP reopen: all imported solids valid. The full 3MF has 13 build items and preserves the source project model entry; its geometry/layout derives from the earlier fixed 13-part layout. The new 3MF has not been sliced or approved.

## Remaining before full-plate print approval

1. Resolve whether to retain the existing +5.5 mm motor-body/mount centroid offset (recommended to preserve tab and shaft alignment) or authorize a redesigned centered support. Simply translating the current rectangle is incompatible.
2. Complete a real Creality Print slice of the new 3-wall/20% 3MF on K2 + Textured PEI + ABS; inspect all layers, support contacts, brims, and support clearances, then record full-plate filament/time.
3. Verify ABS settings against the selected filament's datasheet and confirm the actual K2 build surface.
4. Check camera/ribbon and the SG90 servo bodies/retaining hardware against the assembly references as applicable; STL/CAD fit is not physical verification.
5. Print and inspect the base for warp, bridge underside quality, support removal damage, screw-seat dimensions, and loaded pan movement.

**Release:** CAD interfaces and corrected placements: PASS. Centered-mount requirement: HOLD (conflicts with shaft/tab alignment). 3MF archive/layout: PASS for project integrity and unchanged 13-part model; complete slice/toolpaths: NOT VERIFIED. Full-plate print readiness: NOT APPROVED.


## Additional interface/export audit

- Servo-axis centerlines match the intended drive axes: pan at X=0, Y=0 about Z; tilt along X through Y=0, Z=78 mm. The correctly placed horns are concentric with these lines.
- The simplified servo/horn BREP pairs have 73.264 mm³ intersecting volume at the modeled hub/spline engagement region. This is intentional engagement in the proxy model, not an accurate spline-tooth Boolean. Exact spline geometry is not modeled. Physical fit testing for R15 was user-confirmed; actual spline flank clearance remains beyond CAD proof.
- The saved print STL root contains exactly 13 print-oriented meshes. All are watertight/solid and single-component, with Z-min=0. Their files are byte-identical to the previously validated source print STLs (13/13 SHA-256 matches).
- The new 3MF contains 13 build items. Its `3D/3dmodel.model` entry SHA-256 is identical to both the fixed layout source and the prior tree-support trial: `88c1300b285fa9f46ca87449c7491e9236042ce6d8fb37a3e7a970e17199efdc`. Only slicer settings were changed in the new project. Per-object auto tree support remains enabled on the base, pan yoke, and tilt cradle; other components remain support-disabled.
- The full-plate model geometry and placement are preserved from the fixed layout validation: 13 parts, inside 260×260 mm, zero detected component intersections, 16 mm minimum part gap and 5 mm minimum gap after configured brim widths. This is source-layout evidence; the modified candidate still requires a completed slicer run to verify generated support and brim footprints.

## Visualization note

`RENDERS/Base_Mount_Offset_Dimension_Diagram.svg` is the new dimensioned schematic derived from the measured base BREP. A fresh FreeCAD GUI PNG render could not be captured in this session (the GUI surface was blank), so no new image is represented as a screenshot. The bridge support images are actual slicer captures from the base-only V7 run; the 13-part project screenshot and final full-plate layer preview are not yet available.
