# Eye Trace — CrossHorn ABS Revision 01

This is a separate engineering workspace. It preserves the prior 21 × 14 mm camera revision and prior full-print projects.

## What is ready

- FreeCAD-generated editable circular-clearance coupon document and per-feature STLs.
- A complete ABS calibration-bed STL and a Creality Print project based on the existing K2 ABS coupon profile.
- CAD-derived BRep top projection and automated mesh/K2 bed-size results.
- Inspected white cross-horn reference photos, a measurement template/checklist, and a measurement-gated cross-horn CAD builder.
- A fresh solver/connectivity/native-motion revalidation of the unmodified 21 × 14 assembly.

## What is blocked

The three photos in `REFERENCES` confirm the white four-arm cross shape but have no scale, so no cross-horn dimensions are inferred. The actual measured cross-horn solid, recessed drive pockets, fit-test STL, revised drive parts, updated assembly/STEP, and new motion/collision results are still blocked. The checklist is in `DOCUMENTATION/CROSS_HORN_REFERENCE_AND_MEASUREMENTS.md`. The builder in `CAD/build_cross_horn_revision.py` reports missing dimensions and exits without writing geometry until the required values are entered.

The existing star-horn assembly remains the source design and has not been edited or promoted. The full ABS print project remains unchanged. Camera pattern stays 21 × 14 mm.

## Start here

Open `Creality_Print/EyeTrace_ABS_Circular_Clearance_Calibration.3mf` in Creality Print for the pan and tilt circular-clearance calibration job. Instructions are in `FIT_TESTS/ABS_CLEARANCE_COUPON_GUIDE.md`. This job is not a full mechanism print and does not test the cross horn.
