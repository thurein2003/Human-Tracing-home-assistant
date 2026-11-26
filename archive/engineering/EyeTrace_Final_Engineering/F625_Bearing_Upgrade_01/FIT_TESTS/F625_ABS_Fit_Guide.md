# F625 ABS fit coupon: test guide

## Print this first

Print `F625_ABS_Fit_Coupon_r02.stl` only. It is a single 90 × 44 × 8.4 mm coupon with the bearing-seat axis vertical, matching the revised pillar's recommended print orientation.

The seats, left to right, are nominal **16.0, 16.1, 16.2 and 16.3 mm**. Each has the same nominal 18.2 mm flange recess, 1.1 mm deep. The three small rings on the second row have **12.5, 13.5 and 14.5 mm** central openings; these check the retainer's overlap on the bearing outer race versus clearance to the inner-race face.

## Hardware to prepare

- One actual F625 ZZ bearing (the same physical bearing intended for the mechanism)
- The actual proposed 5 mm shaft or 4.95 mm OD / 3.2 mm ID metal adapter sleeve
- Actual M3×16 screw, M3 nut and approximately 6 mm OD washer for the pivot clamp stack
- Calipers; optional 0.05/0.10/0.15 mm feeler gauges

The 2× M3×10 cap screws and 2× M3 nuts for the retainer are already represented in the existing hardware set; use the real parts during the pillar dry-fit after the coupon passes.

## Print setup

Use ABS and the settings in `SLICER/F625_K2_ABS_Start_Settings.json`: 0.20 mm layer height, 4 walls, 35% gyroid, 255°C nozzle and 100°C bed as starting values, subject to the filament label and K2 limits. Print flat, with the seat bores vertical; no supports should be needed. Use a 6 mm brim for ABS adhesion. The seat sizes are calibration choices; do not scale the whole part.

## Measurable pass/fail

1. **Outer race seat fit:** Try the bearing in all four pockets. PASS when it seats to the shoulder using finger pressure, has no visible tilt/rock, and can be removed without tools. Record the selected ID. FAIL if it must be hammered, cracks the coupon, sits proud by more than 0.1 mm, or rocks visibly.
2. **Flange seat:** PASS when the flange lays flat on its shoulder without rocking or bending; target visible axial gap at the shoulder is ≤0.1 mm. FAIL if the flange binds at the counterbore or is distorted.
3. **Adapter through bearing:** PASS when the actual sleeve/shaft passes through the actual bearing and turns smoothly by fingers with no binding or obvious eccentricity. FAIL if forced, loose enough to wobble visibly, or if it damages the shield.
4. **Retainer race isolation:** Place each aperture ring over the bearing face in turn. PASS when at least 0.5 mm radial overlap remains on the outer race and the ring does not touch the inner race or ZZ shield; the inner race must turn freely with the ring in place. FAIL if the ring rubs the inner race/shield, cannot retain the outer race, or adds drag.
5. **Axial preload:** With the chosen retainer concept and sleeve/washer stack hand-tight, PASS when the outer race remains seated without squeeze and the inner race turns freely. If measuring endplay, target 0.10–0.20 mm at the outer race before the cap arrests it. Do not tighten until the inner and outer race faces have been identified.

The coupon's open pockets are a dimensional screen. The final pillar seat is a through-seat and will still need a dry-fit with the retainer cap before printing the remaining parts.

## If a test fails, send only these measurements/photos

- Bearing maker/marking and close photo of both faces with a ruler/calipers in frame
- Measured OD, bore, total width, flange OD and flange width
- The failed coupon pocket size and how far the bearing sits proud/recessed
- Measured OD/ID/length of the proposed adapter sleeve
- A side photo of the actual bearing face showing inner-race OD and the shield clearance
- Which retainer aperture rubs, and whether drag begins before or after tightening
