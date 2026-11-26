# Prototype 02 fit correction 01

**Status: SOFTWARE-VALIDATED FIT-TEST COUPON; PHYSICAL FIT UNVERIFIED.** This revision contains one coupon. Prototype 01, prior Prototype 02 files, and the full pan/tilt assembly were not modified.

## Selected geometry

| Feature | Selected CAD dimension | Status |
|---|---:|---|
| Horn nominal long span | 35.0 mm | User-confirmed reference |
| Horn nominal short span | 18.0 mm | User-confirmed reference |
| Long pocket span | 35.2 mm | 35 mm + 0.20 mm total lateral allowance |
| Long-arm root width | 7.7 mm | Provisional: 7.5 mm profile + clearance |
| Long-arm tip width | 5.2 mm | Provisional: 5.0 mm profile + clearance |
| Long-arm rounded end radius | 2.6 mm | Provisional: 2.5 mm profile + 0.10 mm per side |
| Short-pocket span | 20.2 mm | 18 mm baseline + 1 mm at each end + 0.20 mm allowance |
| Short-arm root width | 7.2 mm | Provisional; widened 0.5 mm per side beyond failed Prototype 02 |
| Short-arm tip width | 6.2 mm | Provisional; widened 0.5 mm per side beyond failed Prototype 02 |
| Short-arm end radius | 3.1 mm | Provisional rounded tip, equal to half the selected tip width |
| Horn nominal hub diameter | 7.0 mm | User-confirmed reference |
| Hub recess diameter | 7.4 mm | User-requested provisional seat; 0.4 mm diametral clearance |
| Hub recess depth | 2.7 mm | Provisional, independently adjustable in generator parameters |
| Retaining-screw/driver access | 4.5 mm | Retained from previous coupon; separate from hub recess |

The latest available local test photos (`REFERENCES\3cd0d0fa-0738-49df-ab6d-14f760c752b4.jpg` and `REFERENCES\download (1).jpg`) were used for shape guidance only. They have no reliable scale. Arm widths, end radii, exact hub centering, hub projection, horn thickness, screw-head size, and screwdriver envelope are unmeasured. Widths and end radii above are provisional model choices, not measurements extracted from photos.

Short-arm pocket span is deliberately 20.2 mm even though the horn baseline is 18 mm: this reflects the requested 1.0 mm extension at each end and 0.20 mm total allowance. The added short-arm width is a separate provisional step: +0.5 mm per side beyond the failed Prototype 02 width, in addition to the baseline 0.20 mm total clearance.

## Software validation

- FreeCAD 1.1.4 reopened the FCStd: one valid BRep solid.
- STEP reopens as one valid solid.
- STL reopens as a watertight solid mesh: 3,080 facets.
- Coupon bounding box: 43 x 27 x 4.35 mm; within the K2 260 x 260 x 260 mm build volume.
- 3MF archive integrity passes; exactly one model object with 3,080 triangles matching the STL.
- ABS starting settings copied from Prototype 01: 0.20 mm layer, 4 walls, 255 C nozzle, 100 C bed, 4 mm brim, supports off. Follow the filament manufacturer's range and inspect first layer/toolpaths.

Creality Print 7.2 is installed and the 3MF project is prepared. This run did not produce or inspect a sliced layer preview or G-code; the project settings and 3MF integrity checks are not slicer-toolpath validation.

## Physical test

Test with the actual white horn, unpowered and without forcing it into the pocket. Confirm the rounded long arms sit fully in the tapered recess, the short arms seat in the widened extended recess, the 7 mm hub enters the 7.4 mm recess without bottoming, and the original screw plus screwdriver pass through the separate 4.5 mm access. Note rocking, gaps, and removal force. Do not use the screw to pull a tight horn into the coupon.

Do not transfer this geometry into the production pan/tilt parts until the coupon passes. If it still fails, measure actual long/short arm widths at root and tip, each arm-tip distance from the hub center, raised-hub projection, and retaining-screw head/driver dimensions with calipers.
