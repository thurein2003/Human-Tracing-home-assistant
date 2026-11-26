# Eye Trace R18 lightweight candidate

**Release state: HOLD — geometry candidate only; not sliced and not approved for printing.** Plate 01 and its geometry/files were not modified. The R18 assembly is a separate copy based on the compact-carrier R17 candidate; backups of the R17 assembly and compact-carrier source are in `BACKUP`.

## What changed

Only `PanYoke_EarBracket_KeyedDrive` was redesigned. The R17 upright web was one 8.0 mm-thick slab between X=−51.0 and X=−43.0 mm; it was not two separate fused walls. A rounded side relief (R=3 mm) was cut into its broad central span, leaving a continuous 2.5 mm web from X=−51.0 to X=−48.5 mm in Y=−18…+18 mm and Z=45…99 mm. The original 8 mm thickness remains locally at the perimeter: 6 mm-wide side rails and 4 mm top/bottom rails. This is a single thin web with perimeter reinforcement, not a double wall.

The cut is subtractive and does not change the yoke placement, screw-hole axes, pan axis, tilt axis, or lower circular carrier. The lower R15 region (Z≤41.001 mm) has a BREP symmetric-difference volume of 0.0 mm³ against the input compact R17 carrier. The Ø8 mm center opening, 39.2 × 20.2 mm R15 interface, and 1.7 mm pocket remain unchanged. The removable pan retainer remains a separate part. The tilt cradle, idler pillar, SG90 references, camera plate, spacers, and other parts are unchanged.

## Dimensions and volume

| Measure | R17 full source | Immediate compact input | R18 |
|---|---:|---:|---:|
| Pan-yoke overall Z height | 70.0 mm (Z=33…103) | 67.8 mm (Z=35.2…103) | 67.8 mm |
| Upright web full height | 62.0 mm (Z=41…103) | 62.0 mm | 62.0 mm |
| Main web thickness | 8.0 mm | 8.0 mm | 2.5 mm in relieved panel; 8.0 mm perimeter rails remain |
| Pan-yoke BREP volume | 43,453.582 mm³ | 41,666.340 mm³ | 36,613.826 mm³ |

R18 removes **5,052.513 mm³** (5.053 cm³, 12.13%) from the immediate compact input yoke. Relative to the un-compacted R17 source, the total reduction is 6,839.756 mm³ (15.74%), including the earlier 2.2 mm lower-carrier reduction. At an assumed ABS density of 1.04 g/cm³, the immediate R18 volume change corresponds to about 5.25 g of fully solid ABS equivalent; this is not a slicer filament estimate. Actual print mass/time savings are not measured.

No additional vertical height was removed in R18. The preceding compact-carrier revision already reduced overall height by 2.2 mm versus the full R17 source. The R18 upright still spans 62 mm. I retained that height because the assembly has no documented operating limits or validated load criterion to establish a safe top-edge trim.

## CAD and export validation

- FreeCAD 1.1.4: R18 assembly recomputed and reopened; modified pan yoke is valid, one connected solid.
- STEP: independently reimported; valid, one solid; volume 36,613.826 mm³ and bbox X=−58.2…44.0, Y=−35.3…35.3, Z=35.2…103 mm.
- STL: 35,546 triangles; edge-incidence check found zero edges with other than two incident triangles. Bbox X=13…115.2, Y=13.004…83.596, Z=0…67.8 mm in the existing Plate 02 orientation.
- All 49 non-target component features checked against the compact source retain the same shape volume and bounding box; no non-target feature differences were found. The two assembly group shapes naturally reflect the changed yoke.
- R15 lower drive region: symmetric difference 0.0 mm³.
- Camera plate component unchanged; nominal camera pattern remains 21 × 14 mm center-to-center.
- The 12 Plate 02 STLs and combined bed STL passed closed-edge incidence checks. The 3MF ZIP CRC and XML checks passed; it has 12 build items. All bounds are on the 260 × 260 mm K2 bed, at Z=0, with no XY bounding-box overlaps. Minimum XY envelope gap is 16 mm. This is not a check of sliced supports or brim paths.

## Assembly clearance and motion screen

Static BREP checks after the cut found zero positive-volume intersections for the yoke against the modeled tilt servo, tilt cradle, idler pillar, removable cover, base, thrust ring, and four pan-drive screws. Measured model distances: 2.0 mm to tilt cradle, 0.2 mm to pan cover, 0.3 mm to base support, and 0.2 mm to each pan-drive screw. The modeled thrust-ring contact is intentional. The yoke-to-tilt-servo and yoke-to-idler-pillar distances are 0 mm with zero positive-volume intersection (touching/contact in the CAD model), not a physical fit confirmation.

Exploratory transforms on the R18 assembly checked pan −90°…+90° at 5° (37 samples), tilt −45°…+45° at 5° (19 samples), and 49 combined pan/tilt grid states. The pan and tilt sweeps show only the known 73.264 mm³ simplified horn/output engagement overlap. The simultaneous grid found no positive intersections against the stationary base and pan-servo references. These are discrete CAD screens, not validated SG90 limits or a continuous sweep. The CAD does not specify safe movement limits; provisional lens/cable and camera fastener keep-outs are not reliable physical geometry.

Unresolved model overlaps remain: pan horn proxy/carrier 5.655 mm³, and tilt horn proxy/two screws 10.603 mm³ each. Actual white-horn thickness, raised hub dimensions, horn-hole coordinates, and installed shaft/screw stack are not documented. Do not interpret proxy overlaps as proven physical collisions or verified engagement.

## Plate 02 project and slicing

`PRINT\Plate02_R18_K2.3mf` retains the source project's K2/ABS settings metadata: 0.4 mm nozzle, 0.20 mm layer height, 255 °C nozzle, 100 °C plate entries, three walls, 20% gyroid, tree-auto supports, and 5 mm general brim. The pan object retains its existing object-level brim setting. The exact project was launched through the installed Creality Print executable, but the process produced no usable active slicer window/title in this session and no slice job completed. Therefore I could not confirm the GUI loaded this exact project, and first-layer paths, support contact, support/brim spacing, small features, and R15 pocket toolpaths have not been inspected. No actual filament estimate or print time is available. Do not print this candidate until it is sliced and reviewed in Creality Print with the intended ABS/build-surface profile.

## Remaining risks and release

- The 2.5 mm main web is a CAD thickness target, not an ABS strength/fatigue/creep certification. No load case, deflection target, or FEA was supplied.
- Height beyond the prior 2.2 mm compact-carrier reduction is unchanged.
- Real SG90/horn fit and torque transfer remain unverified by this CAD operation.
- Horn/screw and cable/lens details remain provisional.
- Actual slicer wall generation, supports, adhesion, filament mass, and time remain unverified.

**R18 CAD geometry: PASS for shape validity, target web thickness, preserved R15 region, and non-target component preservation.**

**Mechanical release: HOLD pending load/fit evidence. Print release: HOLD pending actual Creality Print slicing and toolpath inspection.**

