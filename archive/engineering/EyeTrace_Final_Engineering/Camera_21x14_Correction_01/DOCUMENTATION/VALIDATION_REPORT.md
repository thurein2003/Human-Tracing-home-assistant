# 21 × 14 correction validation

## Results

- FreeCAD 1.1.4 assembly: 80 document objects, 49 kinematic shapes, 13 printable components; invalid solids: 0.
- Camera bore centers: (±10.5, 69/83) mm in X/Z; horizontal pitch 21 mm, vertical pitch 14 mm.
- Camera plate: one valid solid, 56 × 3 × 32 mm; independent 32 mm height parameter. PCB envelope remains 38 × 1.6 × 38 mm.
- STEP readback: full assembly valid (76 exported solids), camera plate valid (1 solid), print layout valid (13 solids).
- Full project: 13 model meshes and 13 build items; each exported model mesh is a closed component. Combined bed STL reopens as 13 closed components.
- Full-bed toolpath: 599 layers; 124.33 g; 11 h 45 m 59 s; 255 °C nozzle and 100 °C first-layer bed from actual G-code. Extrusion bounds, including brim/support, are X=6.644…228.788 mm and Y=6.644…234.439 mm, within the 260 × 260 mm bed.
- Supports: tree slim enabled for Base_EarMount_ThrustSupport, PanYoke_EarBracket_KeyedDrive, and TiltCradle_KeyedHorn_CameraFrame; disabled on other parts, including the camera plate. The G-code contains support toolpaths on supported components and no support paths for the camera coupon.
- Camera coupon toolpath: 10 layers; 1.35 g; 8 min 34 s; 255 °C nozzle, 100 °C bed; 4 mm brim, supports off. Extrusion bounds X=116.972…153.028 mm and Y=93.972…123.028 mm.
- Native assembly solver: 0 before/after simulation. Grounded base, two revolute joints, two intended rotational DOF. Pan-only, tilt-only, and combined simulations each regenerated 52 frames; independent-axis checks passed.
- Collision sampling: pan 91 positions at 2° from −90° to +90°; tilt 61 positions at 1° from −30° to +30°; opposite pivot 61 positions; simultaneous grid 91 positions. No unintended moving-body overlaps detected.

## Known CAD clearance issue / uncertainty

The estimated rear-camera envelope intersects all four modeled camera fastener assemblies by approximately 13.03 mm³ each. The envelope is provisional and not actual measured electronics. Treat rear-component clearance as BLOCKED pending a safe physical inspection/measurement. The camera holes and PCB dimensions are not physically verified by the slicer or CAD solver.

The lens envelope clears the plate by 5.016 mm in the current model. The modeled PCB reference is 3 mm from the plate. The cable reservation has 18.09 mm minimum neutral distance to the cradle and 18.40 mm to the plate; actual ribbon bending and strain relief remain unverified.

The complete machine output and source inputs are in `../CHECKS/SLICE_FULL/` and `../CHECKS/SLICE_CAMERA/`. Re-open the `.3mf` project in Creality Print before printing; G-code estimates depend on the configured printer/material and do not establish ABS process success or physical fit.

Physical fit: **UNVERIFIED**. Do not start the full assembly print until the corrected coupon and actual-camera clearance review pass.

