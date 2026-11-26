# Camera mounting audit
PASS nominal four-hole alignment: X offsets-10.5,+10.5mm, Z offsets-8,+8mm about pattern centerZ76, planeY nominal. Horizontal21mm and vertical16mm are USER-SUPPLIED NOMINAL CENTER DISTANCES. No official Raspberry Pi camera pattern has been substituted. Actual cylindrical centers in PCB and plate were tested directly, including independent parameter changes.

PCB outer38x38x1.6mm, hole diameter2.2mm, lens diameter14mm and10mm projection remain independent PROVISIONAL placeholders. Native properties and CAD/parameters.json keep them separate. Plate is56x32x3mm, four2.4mm PCB clearance holes,18mm nominal lens opening and four distinct M3 frame holes atX+/-24 andZ68/84. Plate mechanically seats on moving cradle frame and is secured by four M3x10 with nuts. Four separate3mm spacers support the PCB using conditionally sized M2x12 screws. Hardware must not pinch electronics or intrude into components.

The central lens opening offers2mm radial clearance only against the assumed14mm barrel. Real lens center, barrel, IR emitters/window, optical field, PCB components, rear connector and cable bend require evidence. Actual PCB outer extents and hole-to-edge offsets cannot be derived from21x16.

## Unresolved rear-component uncertainty
The inherited20x24.4x20mm box is not a measured component. It overlaps these nine pairs in the retained design. It has been converted to a live native parameterized box and has not been trimmed, hidden in collision tests or misclassified as intended hardware contact.

| Pair with rear uncertainty envelope | Overlap mm3 at recorded pose |
|---|---:|
|PCB_Spacer_Lower_Left / Camera_RearComponents_KEEP_OUT|17.9019|
|Camera_M2x12_Lower_Left / Camera_RearComponents_KEEP_OUT|13.0253|
|PCB_Spacer_Lower_Right / Camera_RearComponents_KEEP_OUT|17.9019|
|Camera_M2x12_Lower_Right / Camera_RearComponents_KEEP_OUT|13.0253|
|PCB_Spacer_Upper_Left / Camera_RearComponents_KEEP_OUT|17.9019|
|Camera_M2x12_Upper_Left / Camera_RearComponents_KEEP_OUT|13.0253|
|PCB_Spacer_Upper_Right / Camera_RearComponents_KEEP_OUT|17.9019|
|Camera_M2x12_Upper_Right / Camera_RearComponents_KEEP_OUT|13.0253|
|CameraPlate_Cut007 / Camera_RearComponents_KEEP_OUT|423.4214|

These are BLOCKED clearance decisions, not proven material collisions and not software clearance passes. Cutting a plate window alone cannot guarantee clearance around unknown rear components at the four standoffs and screw ends. Actual footprints/heights are required; then update the rear envelope/standoff/interface design and rerun all tests. No software-resolvable nominal-component penetration remains.

Camera module removal/installation was checked at six approach distances with its four frame screws removed. Front M2 and M3 driver paths and a6mm rear nut-tool envelope on the detached module also pass. Rear-nut access is obtained before mounting the camera module to the cradle.

A20mm wide,1mm thick,18mm long flat ribbon space reservation is checked in all poses. It is not the actual cable or connector and does not establish a full flex loop. No real minimum bend radius or cable strain is known.

CAD/parameters.json now includes camera_standoff_height_mm, camera_standoff_outer_diameter_mm, camera_plate_hole_diameter_mm and camera_mount_screw_length_mm. Regeneration moves PCB/lens/rear datum and rebuilds all four spacers and camera screw/nut stacks together. Changing a native standoff property alone is not a complete mechanical revision. Camera pitch stays21x16.
