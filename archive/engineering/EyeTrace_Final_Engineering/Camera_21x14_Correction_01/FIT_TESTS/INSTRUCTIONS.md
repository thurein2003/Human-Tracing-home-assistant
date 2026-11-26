# Camera hole-pattern coupon — 21 × 14 mm

## Print first

Print `Camera_21x14_ABS_FitTest.3mf` (Creality Print project) or `Camera_Hole_Pattern_21x14_ABS.stl`. The project slices to 10 layers, about 1.35 g ABS and 8 min 34 s, with a 4 mm brim and no supports. Use 0.20 mm layers, 255 °C nozzle, 100 °C first-layer bed as the sliced starting point; confirm actual ABS manufacturer/printer settings.

The coupon is 29 × 22 × 2 mm with four 2.4 mm holes at X/Y = (±10.5, ±7) mm. Its only purpose is the 21 × 14 center pattern and access through the printed bores. It does not represent PCB size, lens clearance, rear-component clearance, board support, fastener strength, or the complete mounting plate.

## Prepare

- Let the coupon cool flat before measurement.
- Have the actual unpowered camera, digital calipers, and four smooth 2.0 mm nylon or polymer gauge pins. Do not start with metal screws.
- Keep the camera supported by its board edges. Do not rest the coupon on the lens, IR filter, soldered components, or ribbon connector.

## Test steps and PASS/FAIL

1. **Coupon dimensions:** measure hole centers. Use equal-diameter smooth pins and measure outer spans, then subtract the pin diameter. Target horizontal 21.00 mm and vertical 14.00 mm; proposed coupon screen is ±0.15 mm on each axis. Record actual values. A failure means recalibrate printer/material or report measurements before changing CAD.
2. **Coupon bore quality:** each 2.0 mm smooth gauge pin must pass a 2.4 mm printed bore without scraping or force. A failed bore is a print/process issue; do not drill the camera PCB.
3. **Camera pattern:** hold coupon parallel to the camera with visible clearance from the lens and components. Align pins through the coupon and the camera’s four holes without pushing, flexing, or clamping either part. All four align simultaneously and both measured center pitches are 21 × 14 mm within the measurement uncertainty: PASS. Any pin needs force, the PCB flexes, or one hole misses: FAIL. Stop immediately if the camera flexes or a pin contacts optics/components.
4. **Hardware:** only after step 3, verify the actual screw shank passes each PCB hole freely by hand. Confirm fastener head/nut clearance and inspect the rear. Do not assume M2 fit; do not use M3 in the camera holes. Any unmeasured rear region remains UNVERIFIED.
5. Record coupon ABS brand, nozzle/bed/layer settings, measured pitches, actual hole diameter, hardware tested, and photos of coupon and camera. Do not mark physical fit PASS until the actual camera has passed these non-forced checks.

The modelled rear-component envelope intersects two provisional camera screw models. If any component is near the four screws, stop and photograph both camera sides with a ruler/caliper in frame; do not shorten, bend, or force hardware based on this coupon.
