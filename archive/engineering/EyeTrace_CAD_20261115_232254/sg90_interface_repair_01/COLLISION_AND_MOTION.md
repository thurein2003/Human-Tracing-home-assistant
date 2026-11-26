# Collision, motion and assembly validation

independent_validate_v02.py opens the SAVED native model and imports no builder code. It checks native expressions, canonical motor identity, component pairs, installation paths, screw envelopes and printed meshes. This is independent software validation, not physical certification.

- 172 operating poses:169 grid poses over pan +/-60deg in10deg steps and tilt +/-30deg in5deg steps, plus three off-grid poses. 210700 component-pair tests, 38854 unique relative checks, ZERO unintended positive-volume intersections.
- Eight extra uncached guard poses at nominal boundaries extended by2deg: 9800 more all-pair tests, ZERO unintended intersections. Combined: 220500 pair checks across180 poses. Guard poses are geometry tests for modeled free play, not expanded control limits for actual servos.
- All50 tagged components are included: both motors, star proxies, original-screw proxies, printed parts, hardware, camera and three nominal wire-exit envelopes. There is NO positive-overlap whitelist. Exact BRep common volume is checked when bounding boxes overlap; threshold0.001mm3.
- Same-frame pairs are rotation-invariant. Pan/tilt relative pairs depend on tilt, fixed/pan on pan, fixed/tilt on both. Results are reused only under these invariances. Guard checks use no cache. This is discrete coverage, not a continuous sweep proof.

## Contact and engagement classification

INTENDED CONTACT/CLEARANCE includes thrust faces, ear ledges, nut/washer seats, spacer/PCB faces and journal running gaps. Actual CAD distances are in checks/actual_contact_clearance_distances.json. The idler nut has0.3mm wall clearance while bearing on the sleeve, rather than pinching the wall. The journal's radial clearance is0.1mm; pan radial backup gap0.3mm. These are nominal CAD gaps, not verified PETG tolerances.

DESIGNED ENGAGEMENT includes the original spline/thread functions (not modeled as exact teeth/threads), captured nut flats and external star walls. A separate geometric probe rotates each star RELATIVE to its carrier: no contact at1deg, wall engagement by2deg in both directions for the provisional outline. Deliberate probe penetration tests the positive torque path; it is not an operating-pose exemption or strength proof. During operating poses the carrier and horn rotate together.

UNINTENDED PENETRATION is any modeled operating pair with common volume over0.001mm3. None were detected for the released default configuration. Real spline/tooth flanks, flexible cable loops, deformation and unmeasured parts are not accurately represented, so physical mating remains UNVERIFIED. Internal co-moving nut/shank/washer solid pairs are checked separately; their thread geometry is suppressed.

## Assembly and service

The staged checks cover both motor insertions, cradle lateral insertion onto the keyed horn with the right pillar removed, and right-pillar insertion over the flanged sleeve. This closes an assembly-path problem that collision-free operating poses alone did not establish. See checks/installation_removal.json.

Tool checks use explicit disassembly stages. Small servo screws require yoke/cradle removal; the original tilt screw requires supporting the cradle and removing the idler/pillar/sleeve. The specified bit/handle envelopes have clear final approach paths. Actual hand/tool insertion sweeps and flexible lead threading remain physical checks. See checks/screw_access.json.

The native camera was tested at20/20,20/32,32/20,32/32 and28/28mm pitch. Holes, rails, spacers and fasteners all follow. The provisional rear component box conflicts with20/20. Only default28/28 has the full motion/export validation. A real camera may need a changed keep-out or larger frame; changing native pitch requires revalidation and fresh exports.

## Exports and print layout

All14 printed BReps are valid single solids. Individual STL read-backs are closed, single-component, consistently oriented, manifold and without detected self-intersections. STEP parts were compared to native shapes by symmetric difference. Every STL vertex was checked against its oriented native surface within0.01mm. This is numerical serialization validation, not a full Hausdorff/manufacturing-accuracy proof.

The full STEP has77 solids and agrees with the component volume sum. The prototype bed has14 closed components, dimensions237x192.6x77mm and minimum packing gap8mm, within the nominal260x260 K2 bed before slicer additions. Supports/brims/purge exclusions and actual printing remain to be checked. Five diagnostic pieces have separate native/STEP/STL outputs and a validated coupon layout.
