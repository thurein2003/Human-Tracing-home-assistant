# Cross-horn reference inspection and minimum measurements

## Reference-photo findings

The three JPEGs in `REFERENCES` show the actual white SG90 cross horn and printed interface tests. They establish shape/orientation only: a long opposing arm pair, a short opposing pair, rounded ends, a raised central hub, center retaining-screw opening, and rows of small arm holes. The photos do not include a ruler/caliper or a known-length item in the same plane. Perspective and rotation also prevent reliable scale extraction. Therefore no horn dimensions have been taken from the images.

The holes along the arms are not required for torque transfer in the new design. The recessed cross walls carry torque; the original servo retaining screw retains the horn axially. The small-hole array can be represented in the visual/reference horn model if its hole diameters and center coordinates are measured, but those details are not required to size the pocket.

The corrected source assembly’s camera parameter and BRep hole centers are 21 × 14 mm, but its plate object label still says “21x16mm HOLE CENTERS.” The new builder will relabel the separate candidate as 21 × 14; the source document is not edited.

## Actual old CAD drive interfaces

Audited in `CAD/EyeTrace_Final_Assembly.FCStd` and the corrected 21 × 14 native assembly. Both drive carriers currently use a provisional five-arm radial profile with arm angles 0°, 72°, 144°, 216°, 288°, arm length 12 mm, width 3.6 mm, and 4 mm hub radius. The profile is a simplified proxy, not the white cross horn.

- Pan drive carrier: `PanYoke_EarBracket_KeyedDrive`; axis at (0, 0, 35) mm, normal to XY. Legacy cavity depth 2.3 mm and radial clearance 0.25 mm. Old horn proxy to carrier gap measures 0.25 mm; cover contact is axial and does not establish torque engagement.
- Tilt drive carrier: `TiltCradle_KeyedHorn_CameraFrame`; axis at (-41, 0, 78) mm, normal to YZ. Legacy cavity depth 2.2 mm and radial clearance 0.25 mm. Old horn proxy to carrier gap measures 0.20 mm; captive-cover contact is axial.
- Existing nominal center access cuts are 8 mm diameter on pan and 7 mm on tilt. The new design must retain a coaxial opening large enough for the actual retaining screw head and the driver used.

These legacy profile dimensions come from the source CAD generator and document properties. They are not measurements of the white horn and are not reused as cross-horn dimensions.

## Essential caliper measurements

Use the white horn itself, remove it from the servo, and do not squeeze the plastic:

1. **Cross outline:** long-arm and short-arm tip-to-tip lengths; root and tip widths for each arm pair; and the rounded-end radius for each pair. Measure widths perpendicular to the arm. Measure root width just outside the center hub; measure tip width across the rounded end. Confirm the two opposing arms in each pair match; if they do not, the current generator needs individual dimensions for all four arms. If tip radius is difficult to measure, take a square-on top photo with a ruler/caliper in the horn plane.
2. **Axial stack and axis:** flat arm-plate thickness; raised hub outside diameter and height above the plate; center offset of the arm intersection from the raised hub (X/Y, expected near zero but must be confirmed); underside boss diameter and depth if the reverse side has a boss.
3. **Screw access:** center screw clearance-hole diameter; actual original servo screw head diameter and height; and the driver/bit outside diameter needed to reach it through the printed carrier.

These are the smallest inputs for the mating outline, hub relief, axis alignment, axial recess, and screw access. Fill corresponding fields in `CAD/cross_horn_measurements_template.json`. If no underside boss exists, leave both underside boss fields `null`. If you also want every small horn hole shown in the CAD model, measure each distinct hole diameter and its X/Y center from the hub center (X along the long arms); these holes are optional for the pocket and fit coupon.

## Fit and release sequence

After the dimensions are entered, the builder creates a parametric reference horn, cross pockets in both drive carriers, and five pocket coupons with 0.10/0.20/0.25/0.30/0.40 mm radial-clearance candidates. The 0.25 mm legacy value is included as a source-CAD control and as the provisional assembly candidate if no tested clearance is supplied. It is not a selected production tolerance.

Test the coupon with the actual horn and original retaining screw, without force. Record which clearance seats fully, has no visible rocking, and can be removed without bending the horn. Then inspect screw/driver access. The separate circular-clearance bed must also pass its ring and tilt-journal tests. Only after both coupon sets pass should the revised candidate motion/collision checks, STEP/STL exports, and slicer project be considered for full printing.
