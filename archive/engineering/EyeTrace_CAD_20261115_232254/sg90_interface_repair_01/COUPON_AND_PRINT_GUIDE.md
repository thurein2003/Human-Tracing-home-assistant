# PETG coupons and print orientation

Print the five small pieces in coupons/ FIRST,100% scale in mm, using the intended PETG process. Choose temperatures/cooling from the filament/printer profile; none was tested here. These are diagnostics, not additional production mechanism parts.

1. SG90_EarMount_Coupon:2.5mm plate,23.3x12.8 window,27.2 pitch and1.9 plate holes for the proposed small fasteners. Check both actual cases, ear seating and holes. Thread leads separately. It does not certify full cage insertion, strain relief or the original thread type.
2. StarHorn_PositivePocket_Coupon: diameter42,2.2-deep profiled recess,1.8 roof and8mm central access. Same provisional star outline/0.25 side allowance as the carriers. Check both real stars, all arms and raised hubs. The five-arm shape is an estimate.
3. StarHorn_CaptiveCover_Coupon: actual tilt cover with captive M3 nut pockets. Pair with the pocket coupon, original detached horn and four M3x10 structural joints. Nominal grip5.5. Walls, not only friction, must stop relative rotation. Test gently off the servo; do not force its gearbox. Allowable torque and creep are unverified. The coupon pocket prints face-up; main-part supports may affect fit differently.
4. Camera_4Hole_Gauge_PROVISIONAL: thin plate with2.4 holes at configured28x28 pitch and central window. Gauge Y corresponds to camera verticalZ. Overlay only on safe PCB areas; never force M2 into smaller holes. Measure/regenerate if different. This gauge does not identify the camera or establish screw-length clearance.
5. PETG_Hole_Journal_Gauge: centersX5,13,21,29,37,45 atY6; diameters left-to-right1.9,2.4,3.3,5.0,5.2,5.4. Test actual screws and printed sleeve; record measured hole size/clearance. A printed gauge does not establish the PCB's hole diameter.

The14 mechanism STL files are separately bed-oriented: base/yoke/removable pillar upright; cradle on its right side; covers on broad horn-facing faces with nut pockets up; rails/spacers flat. Some yoke/cradle regions require supports. Keep scars out of profile, bearing, journal and nut faces. Nominally small running gaps and contact lands need real layer/tolerance checks.

PrintLayout.FCStd/prototype_print_layout.stl include all14 mechanism pieces with8mm packing gaps. No hardware, servo references, provisional stars or diagnostic coupons are included. Geometry fit does not guarantee that supports/brims/purge arrangements fit. Inspect each slicer layer before printing the mechanism.
