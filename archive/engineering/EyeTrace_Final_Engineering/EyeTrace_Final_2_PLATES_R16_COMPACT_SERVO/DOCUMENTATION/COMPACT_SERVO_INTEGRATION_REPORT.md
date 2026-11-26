# Eye Trace R16 Compact Servo Integration — CAD Audit and Hold Report

Date: 2026-11-18. Audited with FreeCAD 1.1.4 against `EyeTrace_Final_2_PLATES_R15/CAD/EyeTrace_R15_Final_Assembly.FCStd` and its exact print layout sources. The R16 folder is a preserved, separate candidate snapshot. No geometry was changed because inspection found no verified unnecessary structural separation that can safely be removed from the evidence available.

## Verdict

**R16 COMPACT-SERVO REDESIGN: HOLD.** The two main printed drive carriers are already each single valid solids: the pan yoke includes its drive support and the tilt cradle includes its drive support. The separate pan and tilt covers are retainers; they preserve access to insert/remove the white horns and retaining screws. Fusing these covers to their carriers would obstruct that service path and was not justified.

The reference assembly shows both servo output axes coaxial with their respective horn pockets. The previous 33.50 mm pan and 52.50 mm tilt gap readings are documented as placement artifacts from measuring horn proxy objects before applying their placements. The actual R15 assembly audit reports 0.09975 mm minimum clearance between each correctly placed horn proxy and its pocket carrier, with zero intersection. It also reports 1.50 mm minimum body-to-carrier clearance for each servo proxy. These measurements describe different interfaces; the 1.50 mm is not an axial gap from spline tip to horn seat.

The servo reference geometry is explicitly provisional. It does not reliably establish spline projection, spline engagement length, horn underside-to-hub height, retaining screw engagement, or a physical shaft-tip-to-pocket-floor gap. No exact shaft-to-seat axial gap can responsibly be reported from this model. Do not close the 1.50 mm body clearance without hardware confirmation; doing so could create case interference.

## Measured R15 CAD values

| Check | Pan | Tilt | Status / meaning |
|---|---:|---:|---|
| Output axis to pocket axis offset | 0 mm | 0 mm | CAD coaxiality; pan axis Z at (0,0), tilt axis X through (Y=0,Z=78) |
| Horn proxy to carrier minimum distance | 0.09975 mm | 0.09975 mm | CAD pocket clearance reported by prior FreeCAD assembly check |
| Horn proxy/carrier positive-volume overlap | 0 mm³ | 0 mm³ | CAD check; does not prove actual shaft engagement |
| Servo proxy body to carrier minimum distance | 1.50 mm | 1.50 mm | BREP distance; model dimensions provisional |
| Body envelope in assembly coordinates | X −10.7…21.6, Y −6.1…6.1, Z 6.0…36.3 mm | X −70…−39.7, Y −6.1…6.1, Z 56.4…88.7 mm | Proxy geometry only |
| Main printed drive structure | `PanYoke_EarBracket_KeyedDrive` | `TiltCradle_KeyedHorn_CameraFrame` | Each one valid solid; support and drive interface are integrated |

The R15 horn profile remains the physical-test master: pocket envelope 39.2 × 20.2 mm, 1.7 mm depth, Ø8 mm center opening. Camera pattern remains 21 × 14 mm. The R16 snapshot did not alter them.

## Components and merging decision

- Pan: `PanYoke_EarBracket_KeyedDrive` is already one solid that combines the rotating yoke/support with its R15 pan horn pocket. `Pan_KeyedHorn_Cover` remains separate as the removable horn retainer.
- Tilt: `TiltCradle_KeyedHorn_CameraFrame` is already one solid that combines the camera cradle/support with its R15 tilt horn pocket. `Tilt_KeyedHorn_CaptiveCover` remains separate as the removable horn retainer.
- No stationary-to-rotating parts were fused.
- Printable inventory remains 13 unique parts (Plate 01: base, 1 part; Plate 02: remaining 12 parts). No parts were merged or duplicated.

## Compactness and material result

No geometry reduction was made, so **estimated ABS savings are 0 g / 0%** relative to the R15 geometry. The existing clearance is not evidence of an unnecessary vertical spacer. The two carrier solids already integrate their supports, and the split retainers enable horn servicing. A future compact revision should only reduce material after a measured physical stack-up proves surplus axial length and after the horn/screw remains installable.

## Essential physical measurements before changing the interface

With calipers, measure each actual SG90 independently:

1. Servo case/gearbox top seating datum to the highest spline tip, along the output axis (shaft projection).
2. Output boss height and diameter, from the same case datum.
3. Installed white horn underside seating face to its upper surface and to the raised center hub's highest point; measure hub protrusion on both sides if present.
4. Original retaining screw head height and usable thread engagement when the horn is seated.
5. With the horn seated on the spline and screw snugged, measure the axial stack from the servo mounting datum to the horn's structural seating face. Record pan and tilt separately because mounting orientations differ.

These establish whether any axial support distance is truly surplus. The CAD model's `SG90` labels do not make its provisional shaft geometry a measurement of the user's hardware.

## Two-plate print status

The R16 `PRINT` files are byte-for-byte copies of the R15 projects because there is no changed geometry to reslice. They are **not newly sliced R16 release jobs**. Existing slicer validation remains HOLD:

- Plate 01: 23.3 mm bridge support contact beneath the full span is not conclusively verified.
- Plate 02: existing completed slice reports a Z=0 layer-one path conflict between generated “Embossed text” and `Pan_KeyedHorn_Cover`.
- Existing estimates 34.53 g / 2 h 56 min for Plate 01 and 93.62 g / 10 h 21 min for Plate 02 are not released totals; Plate 02 has the conflict and ABS values still require confirmation against the spool data.

## Files and traceability

- `CAD/EyeTrace_R16_CompactServo_Assembly_HOLD.FCStd` — byte-identical R15 editable assembly snapshot; no modifications.
- `STL/` — 13 copied printable meshes, byte-identical to R15 source files.
- `PRINT/EyeTrace_R16_Plate_01_ABS_HOLD.3mf` and `PRINT/EyeTrace_R16_Plate_02_ABS_HOLD.3mf` — byte-identical R15 project copies, unsliced in this revision.
- `CHECKS/reference_geometry_audit.json` — direct FreeCAD 1.1.4 BREP metrics and cylindrical-surface locations from the assembly references.
- `RENDERS/Plate01_R15_Slice_Reference.png`, `RENDERS/Plate02_R15_Slice_Reference.png` — existing Creality Print screenshots, copied for context; not R16 slice evidence.

**Release:** R15 coaxiality/pocket clearances pass at CAD proxy level. Compacting/merging beyond the already integrated carriers is blocked pending physical axial stack measurements. Two-plate print readiness remains HOLD. No physical fit or load claim is made.

## Actual FreeCAD views

The following PNGs were rendered from the R16 FCStd in FreeCAD 1.1.4. The servo and horn solids are the assembly's provisional reference geometry, not scans or measured models of the user's hardware:

- `RENDERS/R16_Assembly_ActualCAD.png` — complete operational assembly.
- `RENDERS/R16_PanDrive_ActualCAD.png` — pan carrier, horn, servo proxy and retainer close-up.
- `RENDERS/R16_TiltDrive_ActualCAD.png` — tilt carrier, horn, servo proxy and retainer close-up.
- `RENDERS/R16_PanDrive_Section_ActualCAD.png` — actual BREP half-section through the pan axis and servo.
- `RENDERS/R16_TiltDrive_Section_ActualCAD.png` — actual BREP half-section through the tilt axis and servo.

Because the audit found no warranted geometry change, the section images are the current R15 configuration; there is no distinct “after” geometry. The R16 CAD/mesh/project copies are checksum-identical snapshots. A fabricated after-image would falsely imply that a redesign occurred.
