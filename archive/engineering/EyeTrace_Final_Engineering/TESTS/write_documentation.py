from pathlib import Path
import json,csv,html,re
from PIL import Image
r=Path('EyeTrace_Final_Engineering');doc=r/'DOCUMENTATION';checks=r/'TESTS/results';motion=json.loads((checks/'nominal_validation/checks/independent_motion.json').read_text());exp=json.loads((checks/'export_mesh_layout.json').read_text());loads=json.loads((checks/'strength_load_assessment.json').read_text())
def put(n,t): (r/n).write_text(t.strip()+'\n',encoding='utf-8')
# Pack animation from real rendered frames only, no synthetic geometry or decorative image generation.
frames=[]
for p in sorted((r/'RENDERS').glob('motion_[0-9][0-9].png')):
 im=Image.open(p).convert('RGB');im.thumbnail((960,720));frames.append(im.copy())
assert len(frames)==17
frames[0].save(r/'RENDERS/validated_CAD_motion.gif',save_all=True,append_images=frames[1:],duration=250,loop=0)
put('RENDERS/motion.html','''<!doctype html><meta charset="utf-8"><title>Eye Trace real CAD motion</title><style>body{font:18px system-ui;max-width:1000px;margin:auto}img{width:100%}</style><h1>Actual FreeCAD motion frames</h1><p>Rigid CAD geometry: validated sampled positions. Cable flex, physical fit and real servo calibration remain unverified.</p><img src="validated_CAD_motion.gif" alt="Rendered CAD motion animation"><p><a href="motion_frames.json">Frame angles</a></p>''')
put('DOCUMENTATION/REVISION_SELECTION.md','''# Source revision audit and integration decision
Seven actual native FreeCAD documents were opened: candidate_02, production_candidate_01, sg90_interface_audit_01, sg90_interface_repair_01, sg90_reference_revision_02, camera_mount_21x16_01 (reviewed) and EyeTrace_Integrated_Candidate_01. See TESTS/results/revision_native_audit.json for component BReps, validity, bounds and checksums; feature_traceability.csv maps every final tagged component to exact matching source geometry. Filename age alone was not used.

The integrated candidate is the most complete nominal assembly: corrected SG90 bodies match reference_revision_02, repaired base/yoke/covers/pillar/journal match repair_01, and camera plate/cradle match the reviewed21x16 camera revision. The integrated flat ribbon reservation is explicitly provisional. Older simplified motors and obsolete camera rails were not reintroduced. Final active assembly has49 tagged components,13 printed components and76 solid leaves including compound hardware and labeled reference spaces. Hidden native Boolean tools/history are not duplicated manufactured parts.

The final mechanical BReps match the integrated source within0.001mm3 symmetric difference. This is intentional preservation of reviewed geometry, not a claim that every source was physically validated. Added final engineering work includes rebuildable horn profiles/pockets, a live parameterized rear-camera envelope, finer all-pair motion tests, additional camera/base tool checks, actual servo dimension extraction, load/mass/section/overhang screening, reduced coupons, portable generation and complete final documentation.

All previous files are preserved and checked against743 source SHA256 entries. Local archives: tochatgpt.zip exists and was inventoried without extraction or execution. EyeTrace_Integrated_Candidate_01.zip was not found. Full project inventory and archive member inventory are included. No actual camera photograph or clone-specific drawing was established as evidence; the21x16 hole spacing comes from the user.

Retained printed functions: base mounts pan ears and supports thrust ring; ring is replaceable wear surface; yoke is pan-driven carrier and tilt-ear bracket; removable pillar allows cradle assembly/service; two captive covers retain original horns; cradle supplies positive tilt drive and camera frame; sleeve separates idler threads from bearing wall; plate supplies exact four-hole interface; four spacers support PCB. Reducing these without evidence would compromise independent wear replacement, disassembly or PCB support. Four equal spacers are required quantities, not redundant geometry.
''')
put('DOCUMENTATION/SERVO_COMPATIBILITY_AUDIT.md','''# SG90 compatibility audit
| Dimension | Both actual CAD models mm | Source / confidence | Status |
|---|---:|---|---|
| Main case length x width |22.7 x12.2|BRep section at localZ5; TowerPro nominal body dimensions with detailed community datum|PASS CAD / PROVISIONAL clone fit|
| Main case height |22.7|Juan Fenoy reference detailed case|PROVISIONAL|
| Entire case/ears/output bounding dimensions |32.3 x12.2 x30.3|Actual canonical BRep bounds, both references|PASS CAD / PROVISIONAL hardware|
| Ear bottom / thickness |15.9 /2.5|Community native geometry; manufacturer datumF ambiguous|PROVISIONAL|
| Ear hole pitch / diameter / open slot |27.2 /2.0 /1.3|Community drawing/native model|PROVISIONAL|
| Output shoulder / top above base |27 /30.3|Manufacturer dimension labels; headline29 conflicts with detailed datum|PROVISIONAL|
| Axis from near case end |5.9|Canonical section and community output datum|PROVISIONAL|
| Gear boss diameter / height |12.2 /4.3|Manufacturer width plus community height datum|PROVISIONAL|
| Output smooth envelope diameter / height |5 /3.3|Rounded community envelope; no exact tooth shape|PROVISIONAL; not spline dimensions|
| Wire exit notch W/H/base height |3.6 /1.2 /4.5|Community native sketch|PROVISIONAL|

Both references are consistent SG90-sized geometry, with ears, holes, bosses, smooth outputs and wire exits. They are not MG90S/MG995 replacements. Canonical BRep comparison is below0.001mm3; actual dimensions/cylinder surfaces are in TESTS/results/actual_servo_dimensions.json. Manufacturer tolerances were not published; no dimensional tolerance or clone equivalence is inferred. See DIMENSIONAL_AUDIT.csv and historical_servo_dimension_comparison.csv for full sources and low-confidence details.

Original star-horn proxy: five arms at0/72/144/216/288 degrees,12mm tip lengths,3.6mm widths,2mm web,8mm hub diameter. None was measured on the user's original horns. Socket and retaining-screw proxies are not thread or spline specifications. Exact spline teeth are not modeled. Preserve original horn-to-servo pairing and original factory retaining screws; M3 is never assumed to fit the horn.

Both original horns are axially captured by covers and four M3 structural joints, with0.25mm nominal side allowance and2.2mm pocket depth. Proxy engagement probes show free at+/-1 degree and positive wall engagement by+/-2 degrees. This demonstrates a plausible positive torque path in the modeled profile, not measured backlash, load capacity or physical fit. Both horn and output/screw reference solids were included in all-pair interference tests; no positive-overlap whitelist.

Both motor installation/removal routes, original ear seating, ear bolt axes and staged retaining-screw tool paths were checked. Ear mounts provisionally require M1.6x8 with small nuts/washers, conditional on measured original holes. M3 stock is for structural joints only. The small ear coupon and two-piece positive horn coupon are essential before full printing.
''')
conflicts=motion['unverified_rear_envelope_conflicts']
ct='\n'.join('|'+ ' / '.join(x['pair'])+'|'+f"{x['volume_mm3']:.4f}"+'|' for x in conflicts)
put('DOCUMENTATION/CAMERA_MOUNTING_AUDIT.md','''# Camera mounting audit
PASS nominal four-hole alignment: X offsets-10.5,+10.5mm, Z offsets-8,+8mm about pattern centerZ76, planeY nominal. Horizontal21mm and vertical16mm are USER-SUPPLIED NOMINAL CENTER DISTANCES. No official Raspberry Pi camera pattern has been substituted. Actual cylindrical centers in PCB and plate were tested directly, including independent parameter changes.

PCB outer38x38x1.6mm, hole diameter2.2mm, lens diameter14mm and10mm projection remain independent PROVISIONAL placeholders. Native properties and CAD/parameters.json keep them separate. Plate is56x32x3mm, four2.4mm PCB clearance holes,18mm nominal lens opening and four distinct M3 frame holes atX+/-24 andZ68/84. Plate mechanically seats on moving cradle frame and is secured by four M3x10 with nuts. Four separate3mm spacers support the PCB using conditionally sized M2x12 screws. Hardware must not pinch electronics or intrude into components.

The central lens opening offers2mm radial clearance only against the assumed14mm barrel. Real lens center, barrel, IR emitters/window, optical field, PCB components, rear connector and cable bend require evidence. Actual PCB outer extents and hole-to-edge offsets cannot be derived from21x16.

## Unresolved rear-component uncertainty
The inherited20x24.4x20mm box is not a measured component. It overlaps these nine pairs in the retained design. It has been converted to a live native parameterized box and has not been trimmed, hidden in collision tests or misclassified as intended hardware contact.

| Pair with rear uncertainty envelope | Overlap mm3 at recorded pose |
|---|---:|
'''+ct+'''

These are BLOCKED clearance decisions, not proven material collisions and not software clearance passes. Cutting a plate window alone cannot guarantee clearance around unknown rear components at the four standoffs and screw ends. Actual footprints/heights are required; then update the rear envelope/standoff/interface design and rerun all tests. No software-resolvable nominal-component penetration remains.

Camera module removal/installation was checked at six approach distances with its four frame screws removed. Front M2 and M3 driver paths and a6mm rear nut-tool envelope on the detached module also pass. Rear-nut access is obtained before mounting the camera module to the cradle.

A20mm wide,1mm thick,18mm long flat ribbon space reservation is checked in all poses. It is not the actual cable or connector and does not establish a full flex loop. No real minimum bend radius or cable strain is known.
''')
put('DOCUMENTATION/MOTION_VALIDATION.md',f'''# Motion and collision validation
PASS nominal components: {motion['poses']} distinct sampled poses, {motion['pair_tests']} component-pair checks, {motion['unique_relative_tests']} unique relative-transform checks; zero unintended nominal-component penetrations. Nine rear uncertainty conflicts remain BLOCKED as explained in CAMERA_MOUNTING_AUDIT.md.

All49 tagged components participate: both motor housings/ears/bosses/output envelopes, original horn proxies, covers, factory screw proxies, all structural/camera fastener solids, PCB, lens, frame, pillar, sleeve and cable reservations. No positive penetration whitelist. Compounds also receive internal-solid pair checks.

Main grid: pan-60..60 and tilt-30..30 in2.5-degree increments (1225 combinations). Additional off-grid and one-degree-spaced guard positions near+/-60..62 and+/-30..32 produce1266 distinct poses. Both independent axes and simultaneous motion are included. Exact BRep volume is computed after bounding-box screening; only invariant relative transforms are cached. Reporting threshold0.001mm3. Numerical thresholds are not hardware tolerances. This discrete sampling is not a continuous swept-volume guarantee.

Proposed initial command window: pan+/-55deg, tilt+/-25deg relative to a physically established neutral. This gives5-degree margin inside the main tested envelope; actual cable/servo limits can be smaller. Guard positions are not an expanded command range. No full180-degree travel is claimed. CAD zeros are not guaranteed electrical neutral PWM values. There are no newly certified external hard stops; original servo internal stops and exact electrical endpoints remain unknown. Never use a gearbox stop as a calibration force limit.

Contact classes: zero-distance ear seats, nut seats, spacer/PCB and plate/frame contacts are intentional bearing/fastening contacts; horn pocket wall drive is separately probed as designed engagement; unintended nominal penetration is a FAIL; rear-box overlap is unverified possible camera material, explicitly retained as BLOCKED. No coincident smooth shaft/socket geometry establishes physical spline engagement.

17-frame motion GIF and source images in RENDERS use positions on the tested grid. They show rigid CAD motion only. True cable bend, connector strain, backlash, wear and powered repeatability require physical checks.
''')
lt='\n'.join(f"|{x['camera_mass_assumption_g']}|{x['tilt_max_static_gravity_Nm']:.4f}|{x['tilt_demand_2xgravity_plus_accel_cable_Nm']:.4f}|{x['pan_demand_friction_accel_cable_Nm']:.4f}|{'Within' if x['tilt_within_assumed_budget'] else 'EXCEEDS'} assumed tilt budget|" for x in loads['camera_sensitivity'])
put('DOCUMENTATION/STRENGTH_AND_LOAD_ASSESSMENT.md','''# Strength and load assessment — screening, not certification
TowerPro publishes1.8kgf cm stall torque at4.8V: https://towerpro.com.tw/product/sg90-analog/ . Converted nominal stall torque is0.17652Nm. Stall torque is not a continuous working rating, and it does not certify the user's clones. An analyst-selected25% working budget is0.04413Nm; it is a conservative screening assumption, not a manufacturer guarantee.

Mass/center estimates use actual CAD volumes and volume-weighted solid centroids. Printed parts are treated as100% solid PETG at1.27g/cm3 (illustrative Prusament material: https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf); nominal steel7.85g/cm3, horn nylon1.15g/cm3, SG90 mass9g. Solid printed mass bound is173.2g before supports/brim, not slicer filament consumption. Actual filament density, infill distribution, hardware masses and camera mass are unknown.

Assumed camera/lens combined mass10/25/50g at[0,-33,76]mm. Gravity torque is summed about tiltX atZ78 and maximized at0.5-degree samples within+/-30deg. Slow acceleration assumption1rad/s2 with conservative bounding-radius inertia. Tilt demand=2*maximum gravity+I*acceleration+0.005Nm cable allowance. Pan demand=mu*weight*radius+I*acceleration+0.005Nm, assuming mu0.30 and30mm effective thrust radius. A worse cable or bearing friction can exceed these assumptions.

|Camera assumption g|Tilt static Nm|Tilt screened demand Nm|Pan screened demand Nm|Assessment|
|---:|---:|---:|---:|---|
'''+lt+'''

At25g camera assumption: tilt moving mass82.47g, pan moving mass169.06g; neutral tilt CoM[-7.20,-15.40,73.78]mm. Pan neutral eccentricity13.02mm creates0.0216Nm overturning moment under gravity. The annular support has27.5/32mm radii; mean thrust pressure0.00197MPa is an area average, not peak pressure. Clearance/compliance can create partial contact and transfer residual moment into horn/shaft; no shaft bearing load rating was found. At50g the tilt screening budget is exceeded. No measured payload rating is issued.

Opposite tilt support nominal reaction at25g is about0.345N, giving projected pressure0.0276MPa on assumed5mm x2.5mm journal area. This simple rigid two-support split excludes bracket flexibility and dynamic loads. Sleeve/nut clamp separation is geometrically checked; a real freely turning journal and secure retaining nut remain test items.

Representative weak-axis PETG plate-strip calculation:2N at20mm lever,20mm effective width,2.5mm thickness and assumed1000MPa effective modulus yields1.92MPa bending stress and0.205mm deflection. This is a sensitivity example, not peak stress in the actual fork or FEA. Actual layer adhesion, local notches, bridges, print defects, nut preload and time/temperature creep are excluded. No numerical factor of safety or fatigue certification is claimed from generic PETG properties.

Retain the thrust wear ring, opposite pivot and removable pillar. Avoid heavier cameras or cable tension until measured. Verify low-speed operation without stalls, bracket deflection, settling/vibration, backlash, fastener loosening, bearing wear and creep under intended duty/temperature. Rebalance or revise only using actual camera mass/CoM evidence; arbitrary thickening raises servo inertia and material use.
''')
# Correct carried-forward location references and add the new service finding.
p=doc/'ASSEMBLY_INSTRUCTIONS.md';s=p.read_text(encoding='utf-8');s=s.replace('renders/exploded.png','../RENDERS/exploded.png');s=s.replace('1. Confirm both actual','1. Secure the base to its host BEFORE fitting the rotating yoke: two host-screw driver approaches are obstructed by the completed upper assembly. Remove upper assembly for base-screw service. Host fasteners depend on host thickness and are additional to the bench BOM. Confirm both actual');s+='\nCamera front tool paths and a6mm rear nut-tool envelope were checked; assemble PCB/spacers/plate as a detached module before fixing it to the cradle. Native tool checks do not establish hand clearance or actual wrench dimensions.\n';p.write_text(s,encoding='utf-8')
put('FIT_TESTS/INSTRUCTIONS.md','''# Minimal interface-test bed
Seven pieces cover four interface classes. Print these before the full bed; no physical results have been supplied. All STL units mm, scale100%, PETG,0.4mm nozzle,0.2mm target layers. Use the same calibrated material/profile as intended for the assembly. FitTests_K2_Bed.stl is the separate test layout, not the full assembly bed.

1. SG90_EarMount_Coupon: thin2.5mm mounting ledge with23.3x12.8mm body window,27.2mm hole pitch and1.9mm holes. Check BOTH actual servos enter, original ears seat flat, and candidate M1.6 hardware/nuts/washers align without modifying factory holes. It does not test whole-case height or cable routing.
2. StarHorn_PositivePocket_Coupon plus StarHorn_CaptiveCover_Coupon: test BOTH detached original horns. Nominal five-arm outline is provisional. Pocket must seat without force and positively oppose torque after acceptable lash; four M3x10 retain it at nominal5.5mm grip. Check raised hub, web and factory screw-head access. Do not use powered gearbox or force spline engagement. Covers alone are not acceptable friction-only torque transfer.
3. Camera_21x16_HoleCenter_Gauge: simultaneously align all four real PCB holes to21mm horizontal x16mm vertical centers without bending the PCB. Gauge holes2.4mm are not evidence of actual camera hole diameter. Gauge outline30x25 and central8mm access hole are not PCB/lens dimensions. Check actual selected small screws separately.
4. PanJournal_Male_SizeTest and PanJournal_Female_ClearanceTest:2mm tall complete-diameter rings, maleOD64 and femaleID64.6, nominal0.3mm radial gap. Check ovality, friction and rocking. Full diameter is necessary; thin rings do not prove full printed bracket distortion/creep.
5. Tilt_Journal_FlangedSleeve: the ACTUAL usable assembly part is on the bed, not a redundant coupon. Check its3.2mm nominal bolt bore and5mm journal against the mating5.2mm CAD bore; test actual M3 shank and print the small pillar/bore area only if needed after these results. No separate throwaway hole gauge or standoff copy is included. The four required PCB spacers are already tiny usable parts in STL/individual and can be printed first for rear-component footprint checks.

Record dimensions and results in ../DOCUMENTATION/physical_results.csv. Deburr minimally and record finishing. A failed horn outline requires a scaled trace or measured profile update in CAD/parameters.json; regenerate both carrier pockets/horns and the corresponding coupon before proceeding. After any edit rerun the full validation, not just export meshes. Parameterized uncertainty is not a physical fit PASS.
''')
put('DOCUMENTATION/PETG_PRINTING_GUIDE.md','''# PETG manufacturing guide
Creality K2 nominal volume260x260x260mm,0.4mm nozzle, target0.2mm layer. Print geometry is oriented/seated atZ0. STL/individual contains exactly13 required printed components. Combined STL/EyeTrace_Final_K2_SingleBed.stl occupies197x192.6x77mm, minimum8mm gaps and verified10mm bed margins. No hardware/camera/keepouts enter either printing bed.

Untested starting recipe: four walls, five top/bottom layers,40% gyroid in large base/yoke/cradle;100% in covers, ring, sleeve, spacers and fit tests. Small thin walls may fit fewer perimeter tracks; use calibrated variable-width paths rather than forcing four lines into0.9mm. Use the filament maker's temperatures/drying/adhesion guidance and the actual K2 PETG profile; brand is unknown. No arbitrary whole-model scaling.

Actual BRep section probes: base4mm; ring1mm; cover webs1.5mm; pillar2.5mm; camera frame/plate3mm; sleeve radial wall0.9mm; PCB spacer radial wall1.3mm. See wall_section_probes.json. These are directed local sections, not a global minimum-wall certificate. At0.2mm layers,1.5mm webs and1.1mm sleeve flange can be quantized differently by the slicer; inspect layer preview or use local/adaptive layer heights. Axial capture clearances are small and must be tested.

Mesh-normal overhang screening is in FDM_overhang_screen.json. Review supports especially under base ear ledges, yoke cavities, cradle/cover roofs and horizontal holes. Thin spacers/sleeve should be oriented as exported. Keep thrust faces, journals, hex seats and horn-drive walls free from support damage. Inspect accessible support removal; PETG interfaces can fuse. A bare geometric overhang is not automatically a FAIL if support can be printed and removed.

Use modest brims on small-footprint parts if needed.8mm gaps accommodate two3mm brims with2mm remaining gap, but supports and purge lines/towers must be reviewed separately. Check slicer retains all13 disconnected volumes and four spacers. Material estimate173.2g is100%-solid geometry bound before supports, not a sliced estimate;40% infill does not make total mass40% because shells remain solid.

Installed Creality Print was discovered and local CLI attempts recorded in TESTS/results/slicer_attempt. Underscore options were rejected; hyphenated options opened the GUI route and produced no G-code before the controlled session was closed. Its official repository documents CLI support and a matching argv/GUI issue: https://github.com/CrealityOfficial/CrealityPrint/issues/634 . Therefore toolpath/support preview is BLOCKED in this automation environment; no sliced-print success is claimed. No files were sent to a printer. Local profile references and machine-readable starting settings are included; actual filament and support settings still need slicer preview before full print.
''')
put('DOCUMENTATION/PRINT_SETTINGS.md','See PETG_PRINTING_GUIDE.md for final settings, wall sections, support review and recorded local slicer limitation.')
# Fix relative source links in copied attribution; original source files remain at workspace sibling.
p=doc/'ATTRIBUTION_AND_SOURCES.md';s=p.read_text(encoding='utf-8').replace('measurements/historical_servo_dimension_comparison.csv','historical_servo_dimension_comparison.csv').replace('../EyeTrace_CAD_20261115_232254','../../EyeTrace_CAD_20261115_232254');s+='\nFinal revision changes: live rear-camera envelope and rebuildable horn/pocket parameters; default component BReps preserved. Manufacturer stall torque and PETG density sources are cited in STRENGTH_AND_LOAD_ASSESSMENT.md.\n';p.write_text(s,encoding='utf-8')
p=doc/'REMAINING_PHYSICAL_FIT.md';s=p.read_text(encoding='utf-8').replace('measurements/measurement_checklist.svg','measurement_checklist.svg').replace('COUPON_GUIDE.md','../FIT_TESTS/INSTRUCTIONS.md').replace('measurements/physical_results.csv','physical_results.csv').replace('from8smallcoupons','from the seven-piece fit bed');s+='\nFull-print toolpath preview was not completed because installed Creality Print did not run its CLI slice path. See PETG_PRINTING_GUIDE.md. A25g camera assumption passed the stated load budget;50g did not. Measure actual mass/CoM rather than treating either as the hardware specification. Secure base to host before upper assembly installation.\n';p.write_text(s,encoding='utf-8')
put('CAD/printing_start_parameters.json',json.dumps({'printer':'Creality K2','bed_mm':[260,260,260],'nozzle_mm':.4,'layer_height_mm':.2,'wall_loops':4,'top_shell_layers':5,'bottom_shell_layers':5,'sparse_infill_density_percent':40,'sparse_infill_pattern':'gyroid','small_parts_infill_percent':100,'scale_percent':100,'supports':'Review local overhang report and actual slicer preview','temperatures':'Use actual filament maker profile; unknown brand','toolpath_validation':'BLOCKED installed CLI did not produce slice; not print-certified'},indent=2))
print('Final audit, manufacturing, assembly and fit-test documentation plus real-CAD GIF created')
