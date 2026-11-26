# Prototype 03 Revision 02 — Horn #3 profile fit coupon

**Release status: provisional fit-test coupon only. Physical fit is UNVERIFIED.** No production pan/tilt parts, assembly files, or earlier prototypes were changed.

## Files

- Editable FreeCAD: `CrossHorn_Horn3_FitTest_03R02.FCStd`
- STL: `CrossHorn_Horn3_FitTest_03R02.stl`
- Creality Print project: `CrossHorn_Horn3_FitTest_03R02.3mf`
- FreeCAD viewport screenshots: `CrossHorn_Horn3_FitTest_03R02_Top.png`, `CrossHorn_Horn3_FitTest_03R02_Isometric.png`
- Visual comparison: `CrossHorn_Horn3_Profile_Comparison.png`
- Parameter source: `parameters.json`; generation macro: `build_prototype_03_revision_02.FCMacro`

## Reference comparison and dimensional choices

The cited Auselectronics Direct SG90 drawing is available at [TA0132 SG90 servo and horn drawings](https://www.auselectronicsdirect.com.au/assets/brochures/TA0132.pdf). Page 4 is the servo-body drawing; page 5 shows Horn #3. The downloaded source and rendered pages are retained in this folder. The body drawing is not used to set the removable horn hub dimensions.

The top-view CAD profile was visually compared against the actual white horn photo in `REFERENCES/download.jpg` and the Horn #3 page. Both show a four-arm unequal cross, rounded tips, broad-to-narrow long arms and unequal long reaches. The photograph and drawing are shown side-by-side in the comparison image; image scale/perspective was not used to infer physical dimensions.

| Feature | Revision 02 value | Provenance / confidence |
|---|---:|---|
| Long overall span | 35.0 mm user measurement | Confirmed nominal by user; actual measurement tolerance not supplied |
| Short span baseline | 18.0 mm user measurement | Confirmed nominal by user |
| Horn center hub | 7.0 mm user measurement | Confirmed nominal by user; distinct from servo shaft/boss |
| Horn #3 long reach either side of hub | 16.0 / 18.5 mm on drawing (34.5 mm total); normalized to 16.25 / 18.75 mm to preserve user 35 mm span | Published similar-horn drawing; provisional offset X = -1.25 mm |
| Horn #3 short span | 16.3 mm drawing; not substituted for user's 18 mm | Reference only |
| Long arm taper angles | 6.3° / 8.0° on drawing, interpreted as total width-convergence angles | Profile guidance; interpretation provisional |
| Long root width | 7.0 mm nominal estimate; 7.2 mm pocket | Scaled/profile estimate, not a dimension explicitly called out on the drawing |
| Long tip widths | CAD pocket 5.406 / 4.565 mm | Derived from the provisional root estimate, arm reaches and interpreted drawing angles |
| Short arm width | 3.2 mm nominal profile estimate; 3.4 mm pocket | Provisional scaled drawing/profile estimate; wider than Prototype 01's 3.0 mm assumption |
| Lateral pocket clearance | 0.20 mm total | User target; CAD parameter, not ABS process compensation validation |
| Short pocket end extension | +1.0 mm each end from 18 mm baseline; pocket span 20.2 mm including 0.20 mm clearance | User requirement plus nominal allowance |
| Hub recess | Ø7.4 × 2.7 mm deep | Provisional; Ø7.0 hub supplied by user and +0.4 diametral recess allowance retained |
| Separate screw access | Ø4.5 mm through | Carried forward as provisional driver/retaining-screw access; not horn spline or shaft geometry |
| Base / floor | 4.2 mm base; 1.5 mm under hub, 2.5 mm under arms | CAD-measured; floor intentionally not pierced except separate center access bore |
| Perimeter | Approximately 2.7 mm around recess | Rounded-cross envelope expansion; local perimeter varies at arm intersections |

**All arm widths, radii, local contour, hub offset, hub depth and screw-access size remain PROVISIONAL.** The published page 5 also depicts a 6.9 mm horn hub and 2.5 mm raised height; these are reference values only. User's measured 7.0 mm hub supersedes 6.9 mm. The 2.7 mm recess depth follows 2.5 mm reference height plus 0.2 mm provisional axial allowance. No secondary horn holes are modeled because their positions were not measured.

## CAD and mesh validation

- FreeCAD 1.1.4 generated the coupon; FreeCADCmd independently reopened the saved FCStd and verified one valid BRep solid; BRep volume **1750.89 mm³**.
- The exported STL contains **5120 facets**; FreeCAD reports the mesh as solid/watertight.
- 3MF ZIP CRC passes, contains exactly one printable mesh object and has the same **5120 triangles** as the STL.
- Bounding box: **40.60 × 25.60 × 4.20 mm**. With 4 mm brim allowance: **48.60 × 33.60 mm**, within the Creality K2 260 × 260 × 260 mm volume.
- Blind hub recess leaves **1.50 mm** floor; arm pocket leaves **2.50 mm**. Center access hole remains a separate through-feature.
- The coupon is one continuous solid with no detached geometry. Flat base on bed, pocket upward; supports disabled.

Full machine slicing is not confirmed. Creality Print 7.2 is installed, but this run did not produce or inspect sliced layers/G-code. Open the 3MF, slice it, and inspect the first layer, perimeter, pocket floors and center opening before printing.

## ABS project starting settings

0.20 mm layers, 3 walls, 12% gyroid infill, supports off, 4 mm outer brim, 255 °C nozzle and 100 °C bed. Verify these against the filament maker's range and printer configuration. The brim can be reduced after an adhesion calibration; do not scale the complete model for ABS shrinkage without measured calibration.

## Consumption and time estimates (not slicer output)

Prototype 01 reference: three coupons, combined CAD volume 12,892.95 mm³; prior project used 100% infill and 4 walls. At assumed ABS density 1.04 g/cm³, estimated mass is **13.41 g**. Prototype 03 Revision 02 BRep volume is 1750.89 mm³. With a broad 55–80% effective material fraction for 12% infill plus walls/top/bottom, estimated mass is **1.00–1.46 g**, or about **89.1–92.5% less** than the three-coupon Prototype 01 package.

Estimated time uses 2.5 mm³/s effective flow plus 5 minutes handling/travel overhead: **91 minutes** for Prototype 01 versus **11–14 minutes** for this coupon. These are rough geometry-based estimates only; actual filament and time remain unknown until sliced in Creality Print.

## Physical test / remaining verification

Use the actual white horn, centered on the separate hub recess. It should sit fully into the rounded tapered pocket without force, show no arm interference or forced bending, allow the hub to seat without bottoming, and leave the original retaining screw accessible through the separate opening. Remove it by hand without prying the horn. Record arm gaps, rocking, insertion feel and whether any ABS strings need cleanup; do not sand the horn or enlarge the coupon before recording the result.

If it fails, provide a straight-down photo of the horn alongside a ruler/calipers and measure: (1) long-arm width at the root and 2–3 distances toward each tip, (2) short-arm width, (3) hub outer diameter and height above the horn plate, (4) long and short end reach from the hub center, including center offset, and (5) retaining-screw head diameter / screwdriver access requirement. Production pan/tilt drive parts remain untouched pending coupon fit.
