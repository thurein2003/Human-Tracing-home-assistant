import os,json,csv,html
import FreeCAD as A
H=os.path.dirname(os.path.abspath(__file__))
def read(n):return open(os.path.join(H,n),encoding='utf-8').read()
def write(n,t):
 with open(os.path.join(H,n),'x',encoding='utf-8') as f:f.write(t)
m=json.loads(read('checks/independent_motion.json'));g=json.loads(read('checks/uncached_guard_poses.json'));e=json.loads(read('checks/export_and_layout_audit.json'))
assert m['unintended_instances']==0 and not g['unintended']
collision=f'''# Collision, motion and assembly validation

independent_validate_v02.py opens the SAVED native model and imports no builder code. It checks native expressions, canonical motor identity, component pairs, installation paths, screw envelopes and printed meshes. This is independent software validation, not physical certification.

- {m['poses']} operating poses:169 grid poses over pan +/-60deg in10deg steps and tilt +/-30deg in5deg steps, plus three off-grid poses. {m['pair_tests']} component-pair tests, {m['unique_relative_tests']} unique relative checks, ZERO unintended positive-volume intersections.
- Eight extra uncached guard poses at nominal boundaries extended by2deg: {g['all_pairs_tested']} more all-pair tests, ZERO unintended intersections. Combined: {m['pair_tests']+g['all_pairs_tested']} pair checks across180 poses. Guard poses are geometry tests for modeled free play, not expanded control limits for actual servos.
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
'''
write('COLLISION_AND_MOTION.md',collision)
remaining='''# Remaining physical verification — HOLD

Use measurements/essential_hardware_results.csv. Only data not established by the available evidence are requested. Exact product drawings/SKUs can substitute where they demonstrably describe the actual units. No actual camera photos or measured values were supplied; resolution and focal length do not identify a mounting pattern.

- [ ] E1/E2: confirm BOTH SG90 ear pitch/diameter, seating height/thickness and body/boss/output envelopes. Try the ear coupon without forcing the original ears.
- [ ] H1/H2: confirm BOTH original star outlines, web/raised hubs and seated horn/center-screw access. Use a measured trace or coupon results. The current five-arm outline is provisional, not an SG90 standard. Do not print replacement spline horns from these references.
- [ ] C1/C2: establish all four camera holes, PCB thickness/outline, rear components and lens/IR/connector keep-outs. Default28mm is not evidence. The mechanical travel is20–32mm, but the placeholder rear box conflicts at20x20. Use actual data and revalidate after changes.
- [ ] Obtain the extra fasteners in hardware_BOM.csv and confirm purchased dimensions. Existing M3 stock alone is insufficient.
- [ ] P1: print the five fit-test pieces first in intended PETG/nozzle/profile. Record as-printed sizes and fit before finishing. Check captured nuts, star wall engagement/play and journal freedom. Main-part support finish may differ from coupon finish.
- [ ] W1: route the actual leads/plugs with slack through both axes. Nominal exit keep-outs do not prove full flexible-loop behavior or connector passage.
- [ ] Review slicer supports/brims, bearing faces, profile pockets, journal and nut seats. The complete bed is a geometric prototype layout, not verified G-code.
- [ ] L1: assemble and verify idler locknut clamp without wall binding; measure actual payload mass/center and test support, friction/backlash, creep and conservative powered duty. Calibrate real servo travel. No mechanical end stops or rated strength/bearing proof are supplied.

Until these pass, physical compatibility and production readiness remain UNVERIFIED. The proposed parts and fasteners are mechanically modeled; actual hardware validation has not occurred.
'''
write('REMAINING_PHYSICAL_VERIFICATION.md',remaining)
coupons='''# PETG coupons and print orientation

Print the five small pieces in coupons/ FIRST,100% scale in mm, using the intended PETG process. Choose temperatures/cooling from the filament/printer profile; none was tested here. These are diagnostics, not additional production mechanism parts.

1. SG90_EarMount_Coupon:2.5mm plate,23.3x12.8 window,27.2 pitch and1.9 plate holes for the proposed small fasteners. Check both actual cases, ear seating and holes. Thread leads separately. It does not certify full cage insertion, strain relief or the original thread type.
2. StarHorn_PositivePocket_Coupon: diameter42,2.2-deep profiled recess,1.8 roof and8mm central access. Same provisional star outline/0.25 side allowance as the carriers. Check both real stars, all arms and raised hubs. The five-arm shape is an estimate.
3. StarHorn_CaptiveCover_Coupon: actual tilt cover with captive M3 nut pockets. Pair with the pocket coupon, original detached horn and four M3x10 structural joints. Nominal grip5.5. Walls, not only friction, must stop relative rotation. Test gently off the servo; do not force its gearbox. Allowable torque and creep are unverified. The coupon pocket prints face-up; main-part supports may affect fit differently.
4. Camera_4Hole_Gauge_PROVISIONAL: thin plate with2.4 holes at configured28x28 pitch and central window. Gauge Y corresponds to camera verticalZ. Overlay only on safe PCB areas; never force M2 into smaller holes. Measure/regenerate if different. This gauge does not identify the camera or establish screw-length clearance.
5. PETG_Hole_Journal_Gauge: centersX5,13,21,29,37,45 atY6; diameters left-to-right1.9,2.4,3.3,5.0,5.2,5.4. Test actual screws and printed sleeve; record measured hole size/clearance. A printed gauge does not establish the PCB's hole diameter.

The14 mechanism STL files are separately bed-oriented: base/yoke/removable pillar upright; cradle on its right side; covers on broad horn-facing faces with nut pockets up; rails/spacers flat. Some yoke/cradle regions require supports. Keep scars out of profile, bearing, journal and nut faces. Nominally small running gaps and contact lands need real layer/tolerance checks.

PrintLayout.FCStd/prototype_print_layout.stl include all14 mechanism pieces with8mm packing gaps. No hardware, servo references, provisional stars or diagnostic coupons are included. Geometry fit does not guarantee that supports/brims/purge arrangements fit. Inspect each slicer layer before printing the mechanism.
'''
write('COUPON_AND_PRINT_GUIDE.md',coupons)
# Test co-moving compound contents once: no hidden internal positive overlap.
d=A.openDocument(os.path.join(H,'EyeTrace_Repair.FCStd'));intern=[]
for o in d.Objects:
 if hasattr(o,'KinematicGroup') and len(o.Shape.Solids)>1:
  solids=o.Shape.Solids
  for i,a in enumerate(solids):
   for j,b in enumerate(solids[i+1:],i+1):
    v=a.common(b).Volume;intern.append({'component':o.Name,'solid_indices':[i,j],'common_volume_mm3':v});assert v<.001
write('checks/internal_compound_solids.json',json.dumps({'pairs':len(intern),'results':intern,'scope':'Suppressed threads; simplified designed engagement, not actual thread-fit proof'},indent=2))
# Report selects corrected detail views; earlier blank/raw renders remain traceable.
gallery=[('assembled_opaque','Complete nominal assembly; camera geometry is provisional'),('assembled_front','Four-hole PCB attachment; actual camera unmeasured'),('assembled_transparent','Both motor references and original-star proxies'),('pose_pan60_tilt30','Actual BRep pose: pan60 / tilt30'),('pan_positive_star_pocket_v2','Positive arm-wall profile, provisional star outline'),('tilt_positive_star_pocket','Tilt profiled carrier and captured cover'),('pan_ear_installation_v2','Pan ear mounting and small fasteners'),('tilt_ear_installation','Tilt ear mounting, cradle removed for access'),('camera_mount_rear','Adjustable rails and separate PCB spacers'),('tilt_retaining_screw_service','Idler/pillar removed for original screw access'),('complete_print_layout_v2','All14 printable mechanism components'),('fit_coupons_v2','Five diagnostic coupon pieces')]
rows=list(csv.reader(open(os.path.join(H,'dimensional_audit.csv'),encoding='utf-8')))
htmltable='<table>'+''.join('<tr>'+''.join(('<th>' if i==0 else '<td>')+html.escape(x)+('</th>' if i==0 else '</td>') for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eye Trace SG90 interface repair01</title><style>body{font:16px/1.55 system-ui;max-width:1250px;margin:30px auto;padding:20px;color:#193247;background:#f5f7f9}header,section,figure{background:white;padding:22px;margin:20px 0}header{border-left:7px solid #b9511c}.hold{color:#9d3f14;font-weight:bold}img{max-width:100%;height:auto}td,th{border:1px solid #b8c7d4;padding:8px;text-align:left}table{border-collapse:collapse}pre{white-space:pre-wrap;font:inherit}a{color:#155c86}</style><header><h1>Eye Trace — SG90 interface repair01</h1><p class="hold">Physical fit UNVERIFIED — not production-ready</p><p>Positive star pockets, ear-mounted motors, removable right journal support, pan bearing support and adjustable four-hole PCB rails.14 printable parts,50 tagged components. No user camera photograph or measured hardware dimensions were supplied.</p><p><a href="EyeTrace_Repair_Assembly.FCStd">Editable FreeCAD assembly</a> · <a href="EyeTrace_Assembly.step">STEP assembly</a> · <a href="prototype_print_layout.stl">Prototype bed STL</a> · <a href="coupons/coupon_layout.stl">Fit-test bed STL</a></p><p><a href="ASSEMBLY_AND_FASTENERS.md">Assembly/BOM</a> · <a href="COLLISION_AND_MOTION.md">Collision/motion</a> · <a href="REMAINING_PHYSICAL_VERIFICATION.md">Remaining checks</a> · <a href="measurements/essential_hardware_results.csv">Measurement/results form</a></p></header>'+''.join('<figure><img loading="lazy" src="renders/'+n+'.png"><figcaption>'+html.escape(c)+'</figcaption></figure>' for n,c in gallery)+'<section><h2>Dimensional audit</h2>'+htmltable+'</section>'+''.join('<section><h2>'+html.escape(title)+'</h2><pre>'+html.escape(text)+'</pre></section>' for title,text in [('Validation',collision),('Assembly and fasteners',read('ASSEMBLY_AND_FASTENERS.md')),('Remaining physical verification',remaining),('Coupons and printing',coupons)])+'</html>'
write('REPORT.html',page)
write('STATUS.json',json.dumps({'overall_status':'HOLD: physical verification required','software_nominal_configuration':'PASS tested geometry, motions and assembly paths','printed_parts':14,'tagged_components':50,'step_solids':77,'operating_poses':m['poses'],'operating_pair_tests':m['pair_tests'],'guard_poses':len(g['poses']),'uncached_guard_pairs':g['all_pairs_tested'],'internal_compound_pairs':len(intern),'physical_fit':'UNVERIFIED','camera_pitch_default_mm':[28,28],'required_extra_hardware':True,'audit_authority':'../sg90_interface_audit_01'},indent=2))
write('renders/report_selection.json',json.dumps(gallery,indent=2))
print('Report and verification checklists saved; internal compound pairs:',len(intern))
