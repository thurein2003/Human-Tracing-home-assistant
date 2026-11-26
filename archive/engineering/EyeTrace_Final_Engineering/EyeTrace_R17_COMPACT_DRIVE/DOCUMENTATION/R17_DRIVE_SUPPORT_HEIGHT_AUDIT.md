# Eye Trace R17 drive-support height audit

Date: 2026-11-18
Source CAD: EyeTrace_Final_2_PLATES_R16_COMPACT_SERVO
Status: **HOLD — no height reduction made.**

## Findings from FreeCAD 1.1.4 geometry

The source FCStd was opened with FreeCAD 1.1.4 and measured as BREP. The pan and tilt carrier objects are each valid, single-solid shapes. The alleged 8 mm is solid geometry, not an empty air gap or a separate spacer. The current project message did not include the referenced annotated screenshots, so the exact highlighted edge could not be mapped from the images; the two likely drive-support sections in the actual carriers are measured below.

| Drive | CAD component | Measured section | Geometric role |
|---|---|---:|---|
| Pan | PanYoke_EarBracket_KeyedDrive | 8.000 mm between X=−51.000 and X=−43.000 mm on the vertical drive/support web; the circular carrier also has an 8.000 mm overall Z envelope from Z=33.000 to Z=41.000 mm, with an intermediate annular face at Z=37.000 mm | Integral material joining the R15 drive carrier to its upright support and providing the circular carrier/backing surfaces. The disk is stepped; the full 8 mm is not an open separation. |
| Tilt | TiltCradle_KeyedHorn_CameraFrame | 8.000 mm between the horn-side face X=−41.000 mm and rear face X=−33.000 mm | Integral drive plate thickness connecting the horn interface to the rectangular cradle/support. |

PanYoke_EarBracket_KeyedDrive: bounding box X=−58.2…44.0, Y=−35.3…35.3, Z=33.0…103.0 mm; volume 42,345.826 mm³; 1 valid solid. Its large planar web faces lie at X=−51 and X=−43 mm. The circular region has outer planes at Z=33 and Z=41 mm and a stepped annular surface at Z=37 mm.

TiltCradle_KeyedHorn_CameraFrame: bounding box X=−41…36, Y=−24.4…21, Z=54…99 mm; volume 24,528.290 mm³; 1 valid solid. The horn-side drive face is at X=−41 mm and its rear support face at X=−33 mm, giving 8 mm axial thickness.

The removable pan and tilt horn retainers remain separate. Neither stationary nor rotating parts were fused. The R15 pocket and shaft/horn design were not changed. Camera mounting pattern remains the source CAD’s 21 × 14 mm. Thirteen printable source meshes are copied unchanged.

## Why a safe minimum cannot be selected from this CAD

The 8 mm regions are load-bearing connection sections, not unused stand-off space. The carrier pocket is 1.7 mm deep and has an Ø8 mm through-opening; that opening removes the central ligament, while the surrounding pocket walls transmit horn torque into the yoke/cradle. Thinning the back of these sections would reduce the wall supporting that torque path and could alter the contact/backing faces. Thinning from the horn face would alter the accepted R15 seating plane and engagement. On the pan side, reducing the circular carrier thickness also changes its stepped annular support stack.

CAD alone does not provide a validated ABS strength/load case, fatigue/creep allowance, or real servo/horn axial stack. Therefore no minimum safe reduced thickness can be certified. Keeping 8 mm is the only defensible geometry-preserving result from current evidence; this is not a structural strength certification.

To authorize a later reduction, measure pan and tilt hardware separately: (1) servo mounting datum to output spline tip; (2) installed horn underside to the top of its hub and screw head; (3) horn seating-face to the adjoining printed support face in the assembled position; and (4) clearance to adjacent stationary surfaces through manual travel. Record caliper resolution and the actual ABS process. A load/deflection requirement is also needed to establish a strength-based minimum.

## Assembly and preserved geometry checks

- Pan and tilt carrier BREP: PASS, one valid solid each.
- R15 pocket features: retained from the source geometry; 39.2 × 20.2 mm envelope, 1.7 mm recess, Ø8 mm center opening. No geometry was rewritten. The exploratory motion screen is recorded in CHECKS/R17_motion_probe.json and is not treated as a validated motion result.
- 21 × 14 mm camera hole pattern: preserved by byte-identical CAD snapshot and component mesh copies.
- Pan/tilt alignment: prior R16 FreeCAD audit reports coincident CAD proxy axes; this R17 snapshot introduces no change. No new physical fit or movement-range certification is implied.
- Motion/interference: an exploratory FreeCAD transform screen sampled pan and tilt at −15°, −10°, −5°, 0°, +5°, +10°, and +15°. It is **inconclusive/HOLD**, not a collision-free pass: the source document contains hardware reference objects still at the global origin (for example Camera_M2x12_* bounds X=−2…2, Y≈±2.31, Z=−2…12 mm and RailMount_* bounds Z≈±3.18 mm), so the full assembly transform/joint placement cannot be safely inferred from object names. The probe reports overlaps that include intended horn/shaft engagement and mispositioned reference hardware. No travel range is approved. Axis-line transverse offsets remain 0 mm in the CAD proxy data; actual shaft seating and movement need proper component placements and hardware checks.

## R17 files

- CAD/EyeTrace_R17_DriveSupport_Audit_HOLD.FCStd — byte-identical copy of the R16 source assembly; audit-only snapshot, not a shortened redesign.
- STL/ — all 13 R16 printable STLs copied unchanged.
- PRINT/Plate_01_ABS_HOLD.3mf and PRINT/Plate_02_ABS_HOLD.3mf — copies of the latest R16 ABS candidate projects; both remain HOLD. Plate 01 bridge-support contact is still unverified. Plate 02 previously sliced at 93.48 g / 10 h 19 min without the old layer-one conflict. The current ABS spool manufacturer settings remain unconfirmed.
- RENDERS/R17_*_SameGeometry.png — actual FreeCAD section and drive views from the byte-identical R16 geometry, copied for traceability; no after-change image is presented.
- CHECKS/r17_geometry_audit.json — direct FreeCAD BREP dimensions and validity.
- CHECKS/R17_SHA256.json — checksums for the R17 assembly, all STLs, and both 3MF projects.

## Release decision

**R17 geometry reduction: NOT APPROVED.** The 8 mm sections are solid support/drive material. An exact safe minimum is **UNVERIFIED** without physical axial-stack measurements and a specified structural load criterion. No shortening was made; the R15 interfaces, shaft alignment, retainers, and camera pattern remain unchanged. Both print projects remain HOLD as indicated by their filenames.
