# Eye Trace R16 two-plate print validation

Date: 2026-11-18
Candidate: EyeTrace_R16_PRINT_READY_CANDIDATE
Input: EyeTrace_Final_2_PLATES_R16_COMPACT_SERVO
Slicer: Creality Print application launched from D:\Creality Print 7.2\CrealityPrint.exe. The 3MF generator metadata identifies build V7.3.1.6378; this version/build discrepancy is retained as a record.

## Release summary

| Plate | Result | Components | Sliced estimate | Main finding |
|---|---|---:|---:|---|
| 01 | **HOLD** | 1 base housing | 34.53 g; 2 h 56 min | Slice completes, but actual support paths beneath the 23.3 mm internal bridge are not verified. |
| 02 | **PASS for slicer/layout check; HOLD for final ABS release** | 12 | 93.48 g; 10 h 19 min | Slice completes with no reported layer-one path conflict; first-layer preview shows separated part/brim regions. Manufacturer-specific ABS validation remains unavailable. |
| Total | **HOLD** | **13 unique intended parts** | **128.01 g; 13 h 15 min** | Plate 01 bridge support is the print-blocking issue. |

The estimates are the slicer outputs for these exact projects, not measured print consumption or wall-clock guarantees.

## Project and geometry preservation

- Candidate projects: PRINT/Plate_01_ABS_HOLD.3mf and PRINT/Plate_02_ABS_HOLD.3mf. The HOLD names are intentional.
- Both candidate 3MF archives pass ZIP integrity checks.
- The 3D/3dmodel.model entry is byte-identical to its corresponding R16 source 3MF in both candidates. Only project/process metadata and plate display naming were changed while preparing the candidate settings.
- Plate 01 contains one build item; Plate 02 contains twelve. Across the two source models there are 13 component wrappers, with one intended component on Plate 01 and twelve on Plate 02. No component was merged or duplicated.
- Candidate model SHA-256: Plate 01 699df8febfb4a228ba038dadb9a369be2e0b46266f2fbeba775fc2a293d191ab; Plate 02 753b6f101827dea39cedde7d96b01cda50045ddf8f3cfea4a64025af5c0f8701.
- No CAD geometry, R15 horn interface geometry, 21 × 14 mm camera mounting pattern, servo alignment, or separate horn retainers were edited by this validation work. Model-byte identity confirms the plate meshes match the R16 source 3MFs. It does not establish physical servo engagement.

## Slicer configuration

Both projects load with Creality K2, 0.4 mm nozzle, Textured PEI Plate, ABS filament profile, 255 °C nozzle, 100 °C textured-plate bed, 0.20 mm layers, 3 walls, 20% infill, tree(auto) supports, 40° support threshold, build-plate-only support, and 5 mm brim. These values are the candidate project configuration and fall within the user-provided ABS starting ranges. The exact filament manufacturer and its datasheet were not supplied, so nozzle/bed compatibility with the specific ABS spool and K2 surface is **not independently confirmed**.

## Plate 01 — circular base

- Slice completed; 226 layers and 36.6 mm displayed total height.
- Slicer estimate: 34.53 g, 2 h 56 min.
- At the inspected bridge-region layer band around Z=19.2–19.8 mm, the rectangular internal structure is visible in the toolpath preview. The line-type totals for the entire base show 0.17 g Support, 0.01 g Support interface, and 0.00 g Support transition; Bridge is 0.03 g total and Internal Bridge is 1.47 g total.
- These aggregate totals and the viewed region do not prove a localized support/interface is actually beneath the complete 23.3 mm bridge with a suitable interface gap. The displayed preview does not make that support contact auditable; the tiny total support/interface values are insufficient evidence for the requested support.
- Mounting-hole openings appear unobstructed in the sampled layer view, but that does not cure the support-verification failure.
- **Verdict: HOLD.** Do not print Plate 01 until localized support paths under the bridge and their interface gap are visibly confirmed in the actual sliced layers.

## Plate 02 — remaining components

- Exact 3MF loaded and slicing completed. Slicer estimate: 93.48 g, 10 h 19 min.
- The object list contains twelve printable parts: thrust ring, pan yoke ear-bracket, tilt idler pillar, pan horn cover, tilt cradle, tilt horn cover, tilt journal sleeve, four PCB spacers, and camera plate.
- The previous reported layer-one Embossed text versus Pan_KeyedHorn_Cover path conflict did not recur in the completed slice. No slice error or path-conflict dialog appeared.
- The lowest available range capture shows Z=0.20–2.40 mm (the slicer range control would not collapse to one 0.20 mm layer). Separate brim/object regions are visible in that low-layer band; tree support is present around the tall cradle. No brim overlap is visible in the captured band. This is visual evidence for the initial layers, not a single-layer-only screenshot or metrology-grade clearance proof for every support point.
- Precision features remain represented in the sliced model; a successful slice does not prove dimensional accuracy after ABS shrinkage.
- **Verdict: PASS for slicer/layout check. HOLD for final ABS print release** pending the specific filament datasheet/process confirmation and the project's Plate 01 release blocker.

## Genuine slicer screenshots

Saved under RENDERS/ from the running Creality Print window:

- Plate01_ABS_Sliced_Overview.png — completed base slice and estimate.
- Plate01_Bridge_Bounded.png, Plate01_Bridge_LowerLayer.png, Plate01_Bridge_LineTypes.png — bridge-region slices and support line-type totals.
- Plate02_Sliced_Complete.png — completed 12-part slice, supports, brim, and estimate.
- Plate02_FirstLayer_Only.png — first-layer toolpaths and footprints.

## Required next action

Plate 01 needs a localized support enforcer or another slicer-supported means of generating support beneath the bridge. Reslice, then inspect the actual layers immediately below and above the underside: confirm support reaches the bridge while holes and fit surfaces remain clear, and document the actual support Z gap. Keep Plate 01 named HOLD unless that is verified. Confirm the ABS spool manufacturer's allowed nozzle/bed temperatures and the K2 Textured PEI compatibility before final print approval.

## Physical verification boundary

These results validate slicer loading and the toolpaths visible in the cited screenshots only. No physical fit, servo/horn torque engagement, ABS dimensional fit, or completed print is certified by this report.


## Plate 01 separate support trial

A separate file, CHECKS/Plate_01_ABS_SupportTrial_Internal.3mf, was created without editing any part mesh. The first trial did not override object-level support metadata and reproduced the original support result, so it is not used. A second trial changed both process and object-level settings to conventional 
ormal(auto) support with support allowed from internal surfaces. Creality Print sliced that trial at **37.01 g / 3 h 10 min**, with **2.28 g Support**, **0.26 g Support interface**, and **0.12 g Support transition**. These paths increased material but did not provide an unambiguous view that the interface lies directly beneath the full 23.3 mm bridge. The isolated support view shows generated support near the internal structure, but the contact location and gap cannot be conclusively matched to the complete bridge underside from the available view. This trial is **not approved** and does not replace the Plate 01 HOLD project. Screenshot: RENDERS/Plate01_InternalTrial_Z19_8.png and RENDERS/Plate01_InternalTrial_Z19_2.png (actual UI selections display the same sampled layer because Creality Print's range handle could not be independently set to both exact bounds); RENDERS/Plate01_SupportOnly_Zoom.png and RENDERS/Plate01_InternalTrial_SliceProgress.png.

The Plate 02 lowest-layer screenshot RENDERS/Plate02_FirstLayer_Only.png covers Z=0.20–2.40 mm; it is not a strict single-layer image. The playback-step field can select an individual toolpath step, but not produce a complete simultaneous first-layer overview. The completed slice still contains no layer-one conflict warning.
