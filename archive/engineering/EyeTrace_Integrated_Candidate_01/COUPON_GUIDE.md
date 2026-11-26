# Small fit-test pieces
All eight individual STL/STEP files are in coupons, with FitTests.FCStd and FitTests_SingleBed.stl. Print individual tests first to minimize material. Keep 100% mm scale. Use the same PETG and calibrated settings intended for the assembly. Mesh checks passed; physical results are blank/unverified.

| Piece | Exact check | Success evidence required |
|---|---|---|
| SG90_EarMount_Coupon | 2.5 mm ledge, 23.3 x 12.8 window, 27.2 mm hole pitch, 1.9 mm holes | Both real cases enter; both ears seat flat; actual small screw passes without modifying original ears; nut and washer seat. This thin gauge does not test whole case height or cable path |
| StarHorn_PositivePocket_Coupon | 42 mm disk, 2.2 mm deep provisional five-arm pocket, 0.25 mm side allowance, 1.8 mm roof, 8 mm screw access | Detached original horn seats flat without force; arm outline/raised hubs clear; measurable play acceptable; pocket walls positively oppose rotation |
| StarHorn_CaptiveCover_Coupon | Actual tilt cover and captive M3 seats, used with pocket piece | Four M3 x 10 capture detached horn at nominal grip 5.5; original retaining screw head remains accessible. Do not test by forcing servo gearbox |
| PETG_Hole_Journal_Gauge | Holes at X5,13,21,29,37,45 / Y6: diameters 1.9,2.4,3.3,5.0,5.2,5.4 | Record as-printed sizes and sliding fits with actual fasteners and printed sleeve; no blanket whole-model scale correction |
| Camera_21x16_HoleCenter_Gauge | 30 x 25 x 1.5 gauge, four diameter2.4 holes on 21 x 16 centers | All four real camera holes align simultaneously without bending PCB. Gauge outline is not camera outline; its 8 mm center access is not lens clearance |
| Camera_Standoff_Test | Actual 5 mm OD, 3 mm tall, diameter2.4 bore | Check at each PCB hole for component/trace clearance and screw intrusion; confirm rear electronics clear plate at this standoff |
| PanJournal_Male_SizeTest | OD64 / ID60, height2 | Pair with female piece; check diameter/ovality and smooth rotation |
| PanJournal_Female_ClearanceTest | OD70.6 / ID64.6, height2 | Nominal radial gap0.3; record fit, rocking and friction. Thin coupons do not establish full-part distortion, load or creep |

The actual Tilt_Journal_FlangedSleeve STL is also small enough to print first with the hole gauge. Record both horn tests separately; original horns can differ. A visually plausible five-arm coupon is not evidence that the supplied original horn has this exact shape. If either profile fails, trace/measure the real outline and update both pocket and cover before exporting again.

Use measurements/physical_results.csv to record measured values, tools and test-print observations. No coupon alone verifies the camera cable sweep, payload capacity, tool access or long-term PETG behavior.
