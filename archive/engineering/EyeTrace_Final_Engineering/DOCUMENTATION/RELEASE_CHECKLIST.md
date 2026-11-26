# Release checklist
PASS means completed evidence within its stated scope; PROVISIONAL means nominal CAD passes while actual hardware fit is unconfirmed; FAIL means a known defect; BLOCKED means required physical or external evidence is unavailable. Full requirement-by-requirement status is in REQUIREMENTS_STATUS.csv. No known unintended nominal-component penetration remains. Rear uncertainty overlaps are not physical-fit passes.

- [x] CAD VERIFIED ? saved nominal BReps open, all active solids valid, interfaces aligned, sampled all-pair motion passes, exports and mesh packing pass.
- [x] FIT-TEST READY ? separate small interface-test files validated, instructions supplied. This means ready for slicing/test fitting, not already physically printed or certified toolpaths.
- [ ] FULL-PRINT READY ? actual servo/horn fit, camera/component/connector clearances, cable sweep, hardware/tool compatibility and PETG bearing tests required; slicer/support preview also outstanding.
- [ ] PHYSICALLY VERIFIED ? assembled working hardware, safe powered travel, load and repeat-use results required.

Essential minimum physical evidence: ear/body coupon on both motors; paired positive-pocket/cover test on both original horns plus factory retaining screws; camera pattern gauge and real hole/PCB/component measurements; actual usable spacers at each camera hole; pan journal ring pair and actual tilt sleeve; real cable/connector sweep; camera mass/CoM and a conservative slow powered test. See FIT_TESTS/INSTRUCTIONS.md and REMAINING_PHYSICAL_FIT.md. User21x16 camera center spacing is already accepted and is not being replaced with PCB outside measurements.

Hardware beyond existing M3x10/plain nuts: nominal4 M1.6x8 screws,4 M1.6 nuts and4 small washers for ears; nominal4 M2x12 and4 M2 nuts for camera;1 M3x12,1 M3 locknut and1 M3 washer for idler. Small hardware remains conditional on real holes. Two correct original factory retaining screws are required; if missing obtain exact compatible originals rather than guess their threads. Base/host screws depend on host thickness.
