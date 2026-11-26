# Engineering validation ? release HOLD
Date: 2026-11-16. Actual FreeCAD 1.1.4 geometry and Python interface used. Independent validator opens saved native geometry and imports no builder. Evidence is in checks/*.json. No physical print or hardware measurements were fabricated.

## Integration and provenance
The reviewed camera_mount_21x16_01 native assembly already incorporated repaired structure. Retained reference motors match sg90_reference_revision_02 BReps exactly; retained mounting structure matches sg90_interface_repair_01. Camera plate and frame use the reviewed 21 x 16 correction. See integration_provenance.json. Both motor cases, ears, open ear holes, bosses, smooth shaft envelopes and wire exits are present. Original star-horn profiles and retaining screws are explicitly provisional. No exact spline is asserted.

## Results
| Check | Result | Scope / limit |
|---|---|---|
| Nominal solids | PASS | 13 printed single solids; full STEP valid, 76 reference/component solids, 49 tagged components |
| Reference consistency | PASS | Both servo references match corrected source, not model labels alone |
| Servo body and tab alignment | PASS nominal / hardware UNVERIFIED | Both motor installation paths and ear fastener axes checked; source tolerances unpublished |
| Horn / output interface | PASS nominal mechanism / physical UNVERIFIED | Both horns and output proxies included in ordinary pair checks; smooth socket is not spline-fit evidence |
| Positive torque transfer | PASS proxy geometry | Pocket walls engage by +/-2 degrees; free at +/-1 degree. Diagnostic relative-rotation penetration is designed engagement, not a collision exemption or load rating |
| Camera center pattern | PASS nominal | Four actual cylindrical centers match 21 horizontal x 16 vertical mm; user nominal, not PCB outside size |
| Camera plate-to-cradle | PASS nominal | Four separate M3 joints join plate to frame; seated contacts and bolts checked |
| Pivot coaxiality | PASS nominal | Tilt idler bore radius 2.6, sleeve radius 2.5; coaxial with drive axis |
| Hardware and access | PASS stated stages | Actual nut seats and nominal grips checked; staged driver envelopes, motor/cradle/pillar/camera installation paths checked |
| Motion interference | PASS nominal components | 180 poses, 211680 pair tests, 39918 unique relative tests; zero unintended nominal penetrations |
| Rear camera components | UNVERIFIED ? HOLD | Nine pair conflicts with unmeasured rear-component uncertainty box; retained and reported, not dismissed |
| Lens clearance | PASS nominal only | 18 mm opening / 14 mm assumed lens gives 2 mm radial margin; real lens/IR field and component envelopes unknown |
| Cable routing | UNVERIFIED | 20 x 1 x 18 mm flat ribbon reservation tested as solid; actual connector, bend radius, slack and changing flexible shape unknown |
| Individual meshes | PASS | All 13 watertight, manifold, correctly oriented, no detected self-intersections; vertex-to-native surface <0.01 mm |
| STEP / STL consistency | PASS | STEP symmetric differences <0.001 mm3; full assembly STEP volume error 6.12e-10 mm3 |
| Single-bed layout | PASS geometric packing | 13 parts, 197 x 192.6 x 77 mm, minimum gap 8 mm, within nominal 260 mm K2 bed with 10 mm margins; slicing/support/brim clearance still required |
| Coupons | PASS mesh geometry | Eight valid standalone fit-test pieces; no physical results yet |

## Motion and contact classification
Main grid: pan -60..60 degrees in 10-degree steps and tilt -30..30 in 5-degree steps (169 poses), plus three off-grid and eight guard poses at +/-62 and +/-32. Guard checks do not extend allowed servo commands. Exact BRep intersections are used for overlapping bounds; invariant relative transforms are cached. Penetration reporting threshold: 0.001 mm3. Discrete sampling is not a continuous swept-volume proof.

All relevant component pairs, including original horns, output envelopes, motor bodies and retaining-screw proxies, participate. No positive-overlap whitelist. Zero-distance intended contacts include ear seats, nut seats, camera frame/plate and PCB/spacer interfaces. Designed engagement is separately probed at the horn pocket walls. Unmeasured rear-envelope overlaps are classified UNVERIFIED, not intended material contact. See independent_motion.json for exact conflicting pairs and volumes.

## Support and fastening limits
Pan uses a replaceable 1 mm thrust annulus at radii 27.5..32 mm and a radial backup gap of 0.3 mm. It reduces nominal unsupported load paths but is not a rated bearing. The factory horn retains torque/axial functions; permissible load and PETG wear/creep remain unknown. Tilt has a second support via a flanged sleeve: nominal radial gap 0.1 mm, flange clearance 0.2 mm, sleeve projects 0.3 mm beyond wall. The idler nut clamps the sleeve, not the rotating wall. No stress, torque, thermal creep or fatigue certification is claimed.

M3 x 10 is used only in compatible structural joints. Ear mounts provisionally use M1.6 hardware; camera holes provisionally use M2. These require real hole measurements. Factory horn retaining screws are the originals, not M3 replacements. Thread helices and clamp preload are not modeled.

## Numerical tolerances versus physical tolerances
Geometric comparison thresholds are computational criteria, not hardware manufacturing tolerances. Manufacturer servo dimensional tolerances were not published in the consulted source. PETG clearances are design allowances to test, not verified printer accuracy. User-supplied camera spacing is nominal without a supplied tolerance.

## Release decision
Software-resolvable nominal integration is complete. Full production printing is HOLD pending camera rear clearance resolution, actual horn/case fit evidence, suitable fasteners, cable sweep and printed journal/interface results. See REMAINING_PHYSICAL_FIT.md. No physical-fit PASS is issued.
