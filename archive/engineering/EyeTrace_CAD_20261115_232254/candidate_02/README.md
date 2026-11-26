# Eye Trace — FreeCAD two-axis prototype

**Physical hardware fit NOT VALIDATED. This is a reviewable prototype, not a print-released functional assembly.**

Created with installed FreeCAD 1.1.4 using its Python/OpenCascade geometry engine. Start with [EyeTrace_Assembly.FCStd](EyeTrace_Assembly.FCStd), the colored assembly with separate printed and nominal hardware groups. [EyeTrace.FCStd](EyeTrace.FCStd) is the headless build snapshot. [assembly.step](assembly.step) exchanges the positioned assembly. Individual STEP and bed-oriented STL files are in [parts](parts/). The [single-bed STL](single_bed.stl) contains all seven printed parts, without the hardware.

![Actual FreeCAD assembly render](renders/assembly_isometric.png)

The pan axis is global Z through X=Y=0. The tilt axis is global X through Y=0, Z=78 mm, carried by the pan yoke. The original star horns are retained by printed sandwich clamps; M3 is used for structural fastening and the opposite idler. No printed splines are claimed to fit the servos. Servo retention uses printed caps. Camera retention is provisionally by straps.

## Verified digitally

| Printed part | Solid count | BRep valid |
|---|---:|---|
| Base | 1 | True |
| PanServoRetainer | 1 | True |
| TiltServoRetainer | 1 | True |
| PanYoke | 1 | True |
| TiltCameraCradle | 1 | True |
| PanHornClamp | 1 | True |
| TiltHornClamp | 1 | True |

All seven STL parts reload as one connected closed mesh apiece, without detected nonmanifold edges, self-intersections, or inconsistent face orientation. All seven STEP parts reload as one valid solid. The single-bed STL reloads as seven closed connected components with no detected self-intersections. Packed geometric dimensions: 215.5 x 170.0 x 75.0 mm, minimum packing gap 8 mm; within the standard K2 260 x 260 mm bed before slicer additions.

Motion check: 169 sampled poses, +/-60 degree pan in 10 degree steps and +/-30 degree tilt in 5 degree steps. 37856 pair checks, 0 detected positive-volume collisions in the tested set. Nominal M3 shanks, heads and nuts are included in the final motion audit. Common pan rotation is reused mathematically for internal pair checks. Face contact is permitted; collision threshold is 0.001 mm3. See [validation.json](checks/validation.json) for the actual pairs and results and [export_audit.json](checks/export_audit.json) for independent export checks.

No sampled collisions were detected. This does not establish continuous clearance or hardware fit.

## Limits and next measurements

The camera is an assumed envelope, not a manufacturer CAD model. Servo ears, strain relief, cables, actual horn hubs, screw threads, real tool access, optical field of view and IR light paths are not fully represented. No print, torque, strength, creep, cable-bend, fastener-locking or physical motion test has been performed. No mechanical stops are included. The camera dimensions and horn profile are critical blockers. Read [BUILD_AND_FIT.md](BUILD_AND_FIT.md) for measurements, hardware requirements, assembly steps and PETG slicing notes.

The native file is a positioned BRep assembly with separate component objects, not a native Assembly workbench joint solver. Kinematics are explicit rigid transforms about the documented axes. The generator is editable Python with dimension assumptions in code; parameters.json records selected assumptions and is not a complete live parameter driver.

## Reproduce and inspect

Preserved scripts in the parent folder: build_candidate_02.py, audit_candidate_02.py and render_candidate_02.FCMacro. Run with the installed `D:/App files/bin/python.exe`. The builder intentionally refuses to recreate an existing candidate_02 output folder; choose a NEW output path in a copied script for another run. Do not delete or overwrite earlier output to rerun it. The render macro produces real FreeCAD GUI views from the same geometry source. Source units and STL units are millimeters (STL itself has no unit metadata).

Earlier revisions are retained as design history and must not be selected for printing. Initial project and FreeCAD discovery are recorded in [INVENTORY.md](../INVENTORY.md).

More views: [front](renders/assembly_front.png), [right](renders/assembly_right.png), [top](renders/assembly_top.png), [pan60 / tilt30](renders/pose_pan60_tilt30.png), [exploded printed parts](renders/exploded_printed_parts.png), [single bed](renders/single_bed.png). A self-contained local gallery page is [REPORT.html](REPORT.html).
