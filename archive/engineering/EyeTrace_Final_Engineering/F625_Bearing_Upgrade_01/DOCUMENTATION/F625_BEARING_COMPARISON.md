# F625 bearing upgrade: engineering comparison

## Recommendation

**Optional and mechanically plausible; not required for basic operation.** An F625 ZZ at the opposite tilt pivot can replace the current printed plain journal and provide a rolling radial support opposite the SG90 output. That should reduce journal sliding friction and wear, and may reduce the radial load carried by the servo output. The existing journal already provides a second-side support, so the upgrade does not add a new support point; it replaces the journal interface with a bearing.

The likely benefit is smoother, lower-friction support, not a need for the bearing's load capacity. For a lightweight camera with intermittent motion, the existing journal may be adequate and is simpler and more tolerant of print variation. The bearing version adds a large seat, a precision sleeve/shaft requirement, axial race-isolation details, and ABS fit calibration. Print the coupon first and adopt the upgrade only if it fits freely and improves hand motion without binding.

## Bearing specification and confidence

| Dimension / property | Nominal value | Source confidence | Actual item status |
|---|---:|---|---|
| Bore `d` | 5 mm | High: NSK and Koyo/JTEKT catalog | Unmeasured; bearing maker/clearance variant unknown |
| Outside diameter `D` | 16 mm | High: both catalogs | Unmeasured |
| Width `B` | 5 mm | High: both catalogs | Unmeasured |
| Flange diameter `D1/D1,2` | 18 mm | High: both catalogs | Unmeasured |
| Flange width `C1/C1,2` | 1 mm | High: NSK and Koyo/JTEKT catalog | Unmeasured |
| Minimum chamfer radius | 0.3 mm | High: NSK and Koyo/JTEKT catalog | Not checked on user's bearing |
| Dynamic/static load ratings | NSK 1.91 kN / 0.67 kN; Koyo 2.15 kN / 0.67 kN | High for the named manufacturer's listed variant | Do not infer the user's bearing maker/variant from the marking alone |
| Inner race outside diameter and exact race-face widths | Not specified on the cited summary drawing | Not established | Must inspect the actual bearing face to select the retainer aperture/contact land |
| Bore/OD tolerance and radial clearance class | Variant-dependent; numeric tolerance not provided on the consulted product pages | Unverified | Measure the actual bearing; coupon determines ABS seat allowance |

Manufacturer references: [NSK F625ZZ series](https://www.nsk.com/eu-en/engineering/products/bearings/ball-bearings/deep-groove-ball-bearings/extra-small-ball-bearings-and-miniature-ball-bearings-metric-series-with-flamge/f625zz-esm-md-wf.html) and [Koyo/JTEKT F625 ZZ](https://www.jtekt.co.jp/products/bearing/en/p/detail/?ClassKey=010-020-020&pno=F625+ZZ). NSK notes that product images are representations and may differ from the actual product. These sources confirm the nominal dimensions; they do not measure the user's bearing.

## Existing pivot and load path

The source geometry has the tilt axis parallel to X, through `y=0, z=78 mm`; the servo-driven pivot is at `x=-41 mm` and the opposite support is near `x=35.5 mm`. The source idler pillar contains an approximately 5.2 mm cylindrical journal feature. Its sleeve is nominally 5.0 mm OD, with about 0.1 mm radial clearance in CAD. The sleeve and M3 idler hardware were grouped with the moving cradle in the kinematic assembly; the pillar is fixed to the pan rotor.

Thus, the existing load path is camera/cradle → plain sleeve → pillar → pan rotor. The other end is supported at the SG90 output/horn. The bearing alternative keeps that same two-support arrangement and the same tilt axis.

## r02 bearing arrangement

- Modified pillar has an axial through-seat for the bearing barrel: nominal CAD diameter 16.2 mm, with an 18.2 mm × 1.1 mm flange counterbore. These are provisional ABS dimensions, not manufacturer tolerances.
- The bearing is positioned at `x=36..41 mm` on the `y=0, z=78 mm` axis; its flange faces the cradle side and seats at `x≈36 mm`.
- Bearing insertion/removal is from the outboard `+X` side. Removing the two M3 retainer screws releases the cap; the bearing then slides out toward `+X`.
- A separate removable cap surrounds the outer race at the outboard side. It has a 13.0 mm central relief and a designed nominal 0.15 mm axial clearance to avoid pinching the outer race. The 13.0 mm relief is provisional because the actual inner-race face diameter is not specified by the catalog summary; the coupon offers 12.5, 13.5 and 14.5 mm alternatives.
- A nonprinted precision sleeve, nominal CAD 4.95 mm OD × 3.2 mm ID × 8 mm long, spans the cradle hub and bearing bore. A modeled M3×16 pivot screw, washer and nut clamp the cradle/adapter/inner-race stack. Buy the longer screw if the existing hardware does not reach.
- The outer race is held by the pillar seat, flange shoulder and removable cap. The inner race is clamped through the centered sleeve and washer/nut stack. The bearing internals are not modeled, and contact on the actual inner-race land must be verified by hand. The CAD envelope cannot prove that the physical shields or races are untouched.
- The bearing does not add a native solver joint. The existing tilt revolute remains the only modeled tilt DOF; bearing rotation is internal to the hardware. This avoids adding a redundant second revolute constraint.

## CAD and export verification

The alternative is in `CAD/EyeTrace_F625_Alternative_r02.FCStd`; the original final assembly and earlier F625 draft are preserved. The r02 assembly has one grounded body, four Fixed joints, two Revolute joints, and three saved native simulations. FreeCAD 1.1.4 reopened it and returned solver code 0.

- Pan sweep: 91 samples from −90° to +90° at 2° steps; no modeled interpenetrations.
- Tilt sweep: 61 samples from −30° to +30° at 1° steps; no modeled interpenetrations among the moving body, bearing envelope, pillar and cap.
- Combined pan/tilt collision grid: 91 samples; no modeled interpenetrations.
- Native simulations generated 52 frames each. Pan-only moves pan about 59.88° at the checked quarter-cycle while relative tilt remains 0°; tilt-only moves relative tilt about 24.95° while pan remains 0°; combined motion moves about 44.91° pan and 19.96° relative tilt at the check frame.
- The modified pillar, cap and fit coupon are valid single solids. Their r02 STL meshes were reopened by a binary STL audit: all are finite, watertight, and have every mesh edge shared by exactly two triangles.
- The STEP export reopens as 82 valid solids.
- Print-orientation bounding boxes: pillar 57 × 57 × 16 mm; retainer 34 × 28 × 8.85 mm; coupon 90 × 44 × 8.4 mm. All fit the K2's 260 × 260 mm bed.

These are CAD checks. They do not certify the actual bearing fit, race isolation, ABS strength/creep, camera load, or physical motion.

## Remaining checks before using the bearing version

1. Measure the actual bearing bore, barrel OD, total width, flange OD and flange width with calipers; inspect for flange damage and identify any maker/clearance suffix.
2. Use the coupon to select the seat diameter that lets the bearing seat fully by hand without rocking or hammering. Confirm the flange seats flat and is not distorted.
3. Select the retainer relief ring that overlaps the outer race while clearing the actual inner race face. With the cap fitted, turn the inner race/adapter by hand and verify the cap adds no drag.
4. Fit the actual 5 mm adapter sleeve through the bearing and the cradle hub. Confirm free rotation without binding or perceptible eccentricity. The 4.95 mm model value is a fit allowance to test, not a guaranteed shaft tolerance.
5. Tighten the M3×16 axle fastener and retainer screws, then recheck that the outer race remains free of clamp preload and that the cradle turns freely.
6. Hand-sweep the complete mount unpowered through its intended range and check the camera, servo horn, cable, bearing cap and fasteners.

**Status: FIT-TEST REQUIRED. Physical compatibility is unverified. Do not full-print or install this alternative until these checks pass.**
