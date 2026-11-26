# Cross horn and ABS pivot correction — revision 01

## Release status

- Existing 21 × 14 mm camera pitch: **preserved as source geometry**. The source parameter file reports hole centers at (±10.5, ±7.0) mm. No camera geometry was altered in this coupon-only increment.
- Pan/tilt cross-horn geometry: **PROVISIONAL / BLOCKED** pending caliper dimensions. Three reference photographs are present and confirm shape/orientation only; they have no known scale. The old star-shaped proxies remain in the untouched source assembly and are not reused as cross geometry.
- Pan ring and tilt journal: **calibration coupon generated; production clearance remains UNVERIFIED** until printed ABS pieces are measured and tested.
- Native assembly/motion: **independently revalidated on the unmodified 21 × 14 source**; it still contains the obsolete five-arm horn proxies. No cross-horn assembly was promoted. Existing production and ABS projects remain unchanged.
- Physical fit: **UNVERIFIED**.

## CAD-derived pivot interfaces

The source assembly contains a 64.0 mm OD pan thrust ring and a 64.6 mm ID mating circular surface in the yoke. This is an intended pair in the CAD; nominal diametral clearance is 0.60 mm (0.30 mm radial). The existing 2 mm ring coupon is only a local fit gauge and does not model the full part's stiffness, roundness, retention, or load.

The opposite tilt journal is modeled at 5.00 mm OD in a 5.20 mm support bore: 0.20 mm diametral / 0.10 mm radial clearance. The new gauge includes bores from 5.05 to 5.30 mm with 5.20 mm as the source-geometry control. The coupons are calibration choices, not a declared ABS shrinkage correction.

ABS shrinkage is printer-, filament-, orientation-, and process-dependent. Do not scale the assembly. Measure the printed coupon dimensions and choose the tightest candidate that rotates without binding and has acceptable wobble after the actual components are assembled.

## Cross-horn dimensions needed

The minimum fit-test inputs and exact caliper procedure are in [CROSS_HORN_REFERENCE_AND_MEASUREMENTS.md](CROSS_HORN_REFERENCE_AND_MEASUREMENTS.md). Essential dimensions are the long/short arm tip spans and root/tip widths, rounded tip radii, plate thickness, raised hub diameter/height, center screw clearance, original screw head dimensions, and driver access diameter. Measure an underside boss only if present. Arm-hole coordinates are optional for torque fit; the cross-arm pocket transfers torque positively and the original retaining screw provides axial retention.

No dimension is inferred from the photos. The parameter-gated builder is [build_cross_horn_revision.py](../CAD/build_cross_horn_revision.py); it refuses to write CAD while required values are missing.

## F625 ZZ assessment

The bearing is not integrated by this revision. Manufacturer nominal dimensions are 5 mm bore, 16 mm OD, 5 mm width, 18 mm flange OD and 1 mm flange thickness. The actual bearing lot and the printed bearing seat/shaft remain unmeasured. The existing second-side journal already supports the tilt axis, so the bearing is optional until a hand-turn/side-load comparison demonstrates a useful reduction in friction or shaft loading. Do not clamp the inner and outer races together. Any bearing option needs a separate seat/retention coupon and a supported concentric 5 mm shaft or adapter.

Sources: [JTEKT F625 ZZ](https://www.jtekt.co.jp/products/bearing/en/p/detail/?ClassKey=010-020-020&pno=F625+ZZ), [NSK F625ZZ](https://www.nsk.com/engineering/f625zz-esm-md-wf.html). Manufacturer nominal data; confirm actual bearing with calipers before designing its seat.
