# Assembly and fasteners — nominal reference only

Use hardware_BOM.csv. There are14 printed components and50 tagged CAD components. Extra small fasteners and a longer locking idler joint are REQUIRED; do not assume the provided M3 screws fit original servo ears/horn holes or the PCB.

Nominal hardware sources: [M1.6 cap screws](https://www.accu.co.uk/api/product-datasheet?id=3038), [small nuts](https://www.reliance.co.uk/wp-content/uploads/2023/01/Reliance-Precision-RG36-Issue-B3-Section-13-Machine-Screws.pdf), [M3 locknut](https://www.hardwarespecialty.com/Product/1497955). Confirm purchased head/nut/washer dimensions. Original retaining screws remain original; the CAD screw envelope is not a thread specification.

1. Measure real hardware and test coupons. Establish a physical neutral appropriate to the actual servo/controller. CAD zero does not establish safe servo commands.
2. Load small M1.6 nuts in base/yoke ledge pockets. Insert the pan servo from above, feed its cable separately, and fasten original ears using small screws and washers. It is ear-mounted, not squeezed by body caps.
3. Fit the replaceable thrust ring on its three clearance locating pins. Load four M3 nuts in the pan cover, put it over the shaft, then fit the original star and original center screw. Lower the yoke's profile onto the star and fit four M3x10 screws from above. Profile walls transmit torque; the cover retains the horn axially. Nominal pocket depth2.2 versus web2 gives0.2 axial allowance, so friction is not the only drive mechanism.
4. Leave the right pillar OFF. Insert the tilt motor from inside the fork toward the left through the full ear-passage opening and secure its ears with two small screw/washer joints. Its referenced2mm holes are not M3 holes.
5. Load the four M3 nuts in the tilt cover, fit cover and original star/center screw. With camera PCB and tilt-drive screws removed, slide the cradle from the right onto the keyed horn. This axial insertion requires the removable pillar. Fit four M3x10 screws from inside the fork into the captured cover nuts.
6. Seat the flanged sleeve in the right cheek. Slide the separate right pillar from the right over the projecting sleeve, onto its base pad. Align on the sleeve and fasten two M3x10 foot screws to captive nuts. Add M3 washer, M3x12 idler bolt and locknut. The sleeve gives0.2 flange clearance and0.3 nut clearance to the wall; tightening must clamp the ROTATING sleeve stack, not pinch the stationary wall. Check this physically because PETG compression can change gaps.
7. Fit both camera rails with four M3x10 joints; adjust row spacing in the frame slots. Place four separate3mm spacers at the actual PCB holes and use correctly sized camera screws through rail slots. Configured M2x12/28mm pitch are provisional. Do not force M2 into smaller PCB holes or let screw tips touch rear components.
8. Fit the actual camera/lens/IR assembly only after keep-outs are checked. Route real leads with slack through both axes, then verify slow unpowered movement before gradual powered testing. No mechanical end stops are included.

## Service stages checked in CAD

- Pan ear screws: yoke/horn removed, diameter3.2 driver from above. Tilt ears: cradle/horn removed, diameter3.2 driver from fork side. Small nuts remain captive.
- Pan original center screw: camera/lead removed as needed, diameter5 driver through the cradle's diameter6 service hole and yoke opening.
- Tilt original center screw: power off/support cradle, remove idler bolt/washer and two-bolt pillar, then sleeve. Diameter5 driver reaches the original screw through the coaxial5.2mm cheek bore. Reinstall all journal parts afterward.
- Tilt drive screws: camera removed, neutral pose; tested internal tool length50 with diameter5 bit section and diameter11 body. Pan drive screws: tilt cradle/camera removed, driver from above.
- Pillar screws: cradle neutral, diameter5 long shaft, handle above fixture.

These are sampled rigid assembly and final tool-approach envelopes. Actual hand/tool insertion sweeps, flexible cable threading and connector passage are physical checks. The cradle/right-pillar assembly path is explicitly tested, not inferred from collision-free operating poses.

## Loading

The new printed pan thrust ring/radial backup transfers load toward the base; the retained horn still supplies torque and axial retention. This is not a rated bearing. Tilt uses the removable pillar and journal sleeve, with threads kept away from the stationary bore. Payload mass/center of mass, PETG strength/friction/creep/wear, backlash and servo duty cycle remain unverified. Stall torque does not establish bearing reaction or continuous capability.
