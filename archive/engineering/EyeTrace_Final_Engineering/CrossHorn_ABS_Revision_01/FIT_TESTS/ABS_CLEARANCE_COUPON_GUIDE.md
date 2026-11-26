# ABS circular clearance calibration

Print `ABS_Circular_Clearance_Calibration_Bed.stl` flat on the K2 bed. It contains the same-size male and female pan rings at five labeled gaps, and five tilt journal/bore pairs. This is a calibration job only; it does not replace the existing complete assembly print.

## Coupon key and required hardware

| Mark | Feature | Nominal candidate | Use |
|---|---|---:|---|
| PAN C1 | 64.0 OD male / 64.1 ID female | 0.10 mm diametral gap | Tightest test; do not force |
| PAN C2 | 64.0 / 64.2 mm | 0.20 mm diametral gap | Tight candidate |
| PAN C3 | 64.0 / 64.3 mm | 0.30 mm diametral gap | Intermediate |
| PAN C4 | 64.0 / 64.4 mm | 0.40 mm diametral gap | Loose candidate |
| PAN C5 | 64.0 / 64.6 mm | 0.60 mm diametral gap | Existing CAD control |
| TILT T1–T5 | 5.00 mm journal plug with 5.05/5.10/5.15/5.20/5.30 mm bore blocks | 0.05–0.30 mm diametral gap | 5.20 mm is current CAD control |

One through-hole on the pan tab denotes C1, continuing to five holes for C5. Tilt blocks use one through-edge notch for T1 through five for T5. Identifiers also appear in individual STL filenames. The rings are not a bearing race and do not reproduce axial retention or loaded deflection.

No servo, horn, camera, screw, nut, or F625 bearing is needed for this clearance-only print. Use a digital caliper (0.01 mm display resolution preferred), a marker, and the actual assembly parts for follow-up checks.

## ABS starting profile

- Project profile: 0.20 mm layers, 4 walls, 100% infill, no supports, 4 mm outer-only brim. The parts are small clearance gauges; dense infill keeps the thin annular sections dimensionally consistent.
- ABS temperature must follow the filament maker and K2 limits; use the already calibrated ABS profile. A reasonable starting window is 250–260 °C nozzle and 100–110 °C bed if the spool and printer permit it.
- Print flat, no supports. The Creality project uses a 4 mm outer-only brim to avoid filling the narrow mating gap; remove it before measurement.
- Keep the printer enclosed and use the filament maker's ventilation guidance.
- Do not apply XY compensation until this calibration has been measured. Do not globally scale the assembly.

## Physical checks and pass criteria

1. Let the coupons cool fully to room temperature. Remove brim and strings without sanding the circular mating faces.
2. Measure each male OD and female ID in at least two perpendicular directions. Record both values and ovality (largest minus smallest). If a coupon is visibly warped, cracked, or oval by more than 0.15 mm, mark that variant invalid and fix the print process before using its result.
3. Try each matched pair by hand. Do not twist with pliers or press it in a vise. PASS for the pan candidate: it seats without force, rotates through a full turn by fingertip without catching, and has no obvious rocking when held at the rim. Record the gap and any perceptible play. FAIL if it binds, needs force, cracks, or has visible rocking; select another candidate and test in the actual assembly before release.
4. Pass the 5.00 mm tilt plug through each matching block. PASS for a candidate: it moves through by hand and rotates without binding. Then test the actual journal and pillar after assembly; the gauge alone cannot establish loaded-axis wobble.
5. Select a final clearance only after the ring and journal are installed in the actual printed structure and checked through the complete intended motion. Repeat the test after the structure has cooled and remained assembled for 24 hours to observe ABS creep/relaxation.

Report the printer/profile, spool brand/type, measured ID/OD at each direction, chosen variant, rotation feel, wobble, and any binding. Photos of caliper readings and the assembled interface are the minimum evidence if no variant passes.
