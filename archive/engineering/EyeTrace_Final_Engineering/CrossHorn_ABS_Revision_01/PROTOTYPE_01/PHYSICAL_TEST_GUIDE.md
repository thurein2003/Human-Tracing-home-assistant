# Cross-horn ABS prototype fit test 01

## Scope

This is a **provisional fit-test package**, not a production interface. It does not replace or modify the existing pan/tilt drive parts. The three pockets are test gauges for the real white SG90 horn.

## Print first

Open `Creality_Print_CrossHorn_ABS_FitTest_01.3mf` in Creality Print 7.2 and print the coupon bed in ABS. It contains three 43 x 27 mm coupons with 0.10, 0.20 and 0.30 mm **total lateral** pocket clearance. The raised dot count identifies the variant: one dot = 0.10, two = 0.20, three = 0.30 mm. No supports are needed; print flat, pocket face up. Use the 3MF's 0.20 mm layer, four-wall, 255 C nozzle, 100 C bed, 4 mm brim starting setup, subject to the ABS spool label and printer limits.

The coupon's 4.5 mm center access opening and 7.2 mm nominal hub recess are provisional assumptions. The 3MF is a slicer project, not sliced G-code; inspect the first layer and preview toolpaths in Creality Print before sending the job.

## Test with your hardware

1. Let the ABS coupons cool fully on the bed, then remove them without prying against the thin pocket walls. Clear only loose brim strings; do not file or drill the pocket before the first assessment.
2. Remove the white horn from the SG90 only if safe and use its original retaining screw as the reference hardware. Keep the servo unpowered and do not force the horn onto an output spline for this coupon test.
3. Orient the horn hub over the round center recess and the long pair over the long pocket. Lower it straight in by hand. Do not twist, lever, hammer, or tighten the servo screw to pull it into a tight pocket.
4. Record whether the plate sits flat, whether both long and short arms seat, any rocking, visible gaps, or local interference. Remove the horn vertically by hand.
5. Try the other two clearances and record the tightest coupon that seats without force and the loosest coupon's observable play. If no variant seats freely, stop and measure the actual profile; do not modify the servo horn.
6. Check access separately: pass the original retaining screw and the intended screwdriver through the center access opening without touching or binding on the pocket. Do not tighten a screw into this coupon; it has no verified threaded or nut-retention feature.
7. Photograph the best-fitting coupon with the horn seated from above and side, plus a caliper reading of any residual gap or rocking. Do not infer a production clearance solely from a hand-fit coupon.

## What this checks / does not check

- Checks: approximate rounded-cross envelope, hub recess entry, axial seating, and relative clearance across the three ABS variants.
- Does not check: servo spline engagement, torque strength, small horn-hole positions, fastener retention, full pan/tilt collisions, or production fit. No secondary holes are modeled because their actual positions are unknown.

## Measured versus provisional geometry

User-confirmed: horn long span 35 mm, short span 18 mm, raised hub diameter 7 mm; camera hole centers remain 21 x 14 mm.

Provisional model inputs: long/short arm widths 3.2/3.0 mm, centered hub, arm end radii 1.6/1.5 mm, horn plate thickness 1.5 mm, hub height 2.5 mm, center through access 4.5 mm, axial recess allowance 0.20 mm. The published SG90 Horn #3 drawing supports similar-horn values of 34.5 mm overall length, 6.9 mm hub diameter, 1.5 mm thickness, 2.5 mm hub height and typical 1.0 mm small holes; the drawing is not evidence that this clone matches. The drawing's overall length differs from your measured 35 mm, so the measured span controls. Do not use the provisional small-hole diameter to select a screw.

## Record results

Write down the chosen coupon dot count, fit (free / slight drag / will not seat), rocking/play, screw and driver access, ABS brand/profile, nozzle/bed temperatures, and attach top/side photos. Physical fit remains unverified until these results are recorded.
