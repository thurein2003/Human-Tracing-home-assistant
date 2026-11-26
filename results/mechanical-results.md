# Mechanical results

FreeCAD 1.1.4 reopened the four selected native documents and all four promoted STL meshes. [Raw CAD readback](cad-readback.json).

| Mesh | Triangle count | Closed components | Envelope, mm |
| --- | ---: | ---: | --- |
| Corrected single bed | 35,348 | 13 | 217.097 × 218 × 67.175 |
| Camera hole coupon | 1,708 | 1 | 29 × 22 × 2 |
| Optimized diagnostic bed | 15,988 | 7 | 159.289 × 115.6 × 4.2 |
| ABS clearance-calibration bed | 18,148 | 20 | 241.284 × 206.294 × 6 |

The corrected FreeCAD camera coupon cylindrical axes confirm 21 × 14 mm spacing. Both corrected assemblies and the print layout contained zero invalid shape objects in this readback. Fresh STEP readback counted 76 valid solids for the assembly and 13 for the layout. All three promoted slicer containers passed CRC, and their build lists contain 13, one and one items respectively. [STEP and 3MF readback](format-readback.json). Archived motion sweeps report no unintended sampled moving-body intersections within their tested model scope. The estimated rear camera volume intersects its four modeled fastener envelopes, leaving physical fit open.

Historical corrected full-bed G-code recorded 124.33 g and 11 h 45 m 59 s. The earlier full fit bed recorded 12.06 g and 1 h 21 m 12 s. The corrected camera-only coupon records 1.35 g and 8 m 34 s. These are three distinct slicer estimates. See [manufacturing](../hardware/printing/manufacturing.md).

Physical dimensions, clearances, as-built revision, load capacity and print repeatability were not measured during archival.
