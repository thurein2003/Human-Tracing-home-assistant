import os,json,csv,shutil
H=os.path.dirname(os.path.abspath(__file__));B=os.path.dirname(H)
s=json.load(open(os.path.join(H,'checks','independent_validation_summary.json')));assert not s['critical_software_failures'] and s['motion_penetrations']==0
E=json.load(open(os.path.join(H,'checks','export_and_layout_audit.json')))
def write(n,t):
 with open(os.path.join(H,n),'x',encoding='utf-8') as f:f.write(t)
def table(n,head,rows):
 with open(os.path.join(H,n),'x',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
shutil.copy2(os.path.join(B,'sg90_interface_audit_01','AUDIT.md'),os.path.join(H,'measurements','authoritative_audit_baseline.md'))
shutil.copy2(os.path.join(B,'sg90_reference_revision_02','dimension_comparison_with_tolerances.csv'),os.path.join(H,'measurements','servo_reference_source_ledger.csv'))
write('ATTRIBUTION.md',open(os.path.join(B,'sg90_reference_revision_02','ATTRIBUTION.md')).read()+'\n\nRepair additions: ear mounts, positive star-profile carriers, captive covers, removable idler pillar, thrust/journal supports and adjustable four-hole PCB rails. Servo reference dimensions remain unverified for the actual clones. Source audit sg90_interface_audit_01 is authoritative. Prior files are unchanged. No manufacturer endorsement or spline-fit claim is made.\n')
rows=[
('Servo main case L/W/H','22.7 /12.2 /22.7','TowerPro B/D plus Juan Fenoy native case height','Published nominal + community detail','CAD consistent; physical clone fit UNVERIFIED'),
('Shoulder/output top from base','27 /30.3','TowerPro C/A drawing; headline29 conflicts','Datum interpretation/conflicting sources','Actual seated height UNVERIFIED'),
('Ear span/bottom/thickness','32.3 /15.9 /2.5','TowerPro E + community native placement','Nominal/community','UNVERIFIED for clones'),
('Ear pitch/hole/open slot','27.2 /2.0 /1.3','Community native geometry','Community reference','M3 NOT suitable for modeled ear holes'),
('Output center from near end','5.9','Community native geometry','Community reference','UNVERIFIED for clones'),
('Output/bore envelope','diameter5 /diameter1.7','Community bounds, smooth envelopes only','LOW for physical mating','Spline teeth NOT modeled; thread fit UNVERIFIED'),
('Wire notch W/H/elevation','3.6 /1.2 /4.5','Community native sketch','Community reference','Actual strain relief/connector UNVERIFIED'),
('Original star profile','5 arms, length12,width3.6,hub diameter8,web2','Inherited PROVISIONAL outline; configurable arrays','LOW, no measured horn trace','Actual profile fit UNVERIFIED'),
('Original retaining screw envelope','diameter1.6,head3.5x1,length5','PROVISIONAL visualization, not a thread specification','LOW','Retain original screws; physical seating UNVERIFIED'),
('Positive horn pocket','0.25 side clearance,2.2 depth','Printed design choice','CAD verified against provisional outline','Positive wall engagement PASS; physical fit/strength UNVERIFIED'),
('Horn pocket free play','No contact at +/-1deg; wall probe contact at +/-2deg','Independent relative-rotation test','CAD verified','Actual backlash/torque UNVERIFIED'),
('Pan thrust/radial support','thrust ring r27.5..32,thickness1; radial gap0.3','Printed design and actual CAD distances','CAD verified','Bearing load, wear, creep UNVERIFIED'),
('Tilt journal','sleeve OD5,bore5.2,radial gap0.1','Actual saved cylindrical surfaces','CAD verified','PETG running fit UNVERIFIED'),
('Idler anti-pinching gaps','flange-to-wall0.2,nut-to-wall0.3','Actual geometry and distance check','CAD verified','Compressed physical stack UNVERIFIED'),
('Idler bolt','M3x12,grip6.8,nut4,projection1.2','Selected nominal hardware','Requires extra bolt/washer/locknut','CAD contact PASS; actual hardware fit UNVERIFIED'),
('Ear fasteners','M1.6x8,grip5.5,nut1.3,projection1.2','Selected nominal hardware, conditional on ear holes','Extra hardware required','Not M3; physical fit UNVERIFIED'),
('Drive fasteners','8xM3x10,grip5.5,nut2.4,projection2.1','Selected nominal hardware/design stack','CAD contact verified','Physical hardware/PETG fit UNVERIFIED'),
('Removable pillar/rail fasteners','6xM3x10,grip6,nut2.4,projection1.6','Design stack','CAD contact verified','Physical hardware/PETG fit UNVERIFIED'),
('Camera PCB/holes','38x38x1.6,diameter2.2','PROVISIONAL layout, no user camera photograph/dimensions','LOW','Actual PCB UNVERIFIED'),
('Camera hole pitch','Default28x28; mechanical travel20..32 X/Z','PROVISIONAL default, live native expressions','LOW for actual board','Only default28 full-assembly validation; actual pitch UNVERIFIED'),
('Camera standoff/rear keep-out','spacers3; rear keep-out20x24.4x20','PROVISIONAL layout','LOW','Real components/IR emitters UNVERIFIED'),
('Camera PCB fasteners','M2x12,grip7.6,nut1.6,projection2.8','Selected nominal hardware','Additional hardware required','Only if real holes permit M2'),
('Complete prototype layout','237x192.6x77,minimum gap8','Native/STL read-back and packing','CAD verified','Slicer supports/brims and actual printing pending')]
table('dimensional_audit.csv',['Interface','Nominal mm unless stated','Source','Confidence','Status'],rows)
md='| Interface | Nominal CAD | Source/confidence | Status |\n|---|---|---|---|\n'+'\n'.join('| '+' | '.join([r[0],r[1],r[2]+'; '+r[3],r[4]])+' |' for r in rows)
write('DIMENSIONAL_AUDIT.md','# Dimensional audit — physical fit unverified\n\n'+md+'\n\nNo manufacturing tolerance was established for the actual SG90 clones, original horns or camera. Source disagreements are not tolerance bands. CAD intersection threshold0.001mm3 and STL comparison threshold0.01mm are numerical validation limits, not physical dimensional accuracy. See measurements/servo_reference_source_ledger.csv for original source details and measurements/authoritative_audit_baseline.md for the unchanged authoritative audit. No actual camera photograph or measured camera dimensions were supplied.\n')
bom=[('M3x10 structural screws',14,'Stock described; quantity/head size to confirm','4 pan,4 tilt,4 rail,2 pillar'),('M3 plain nuts',14,'Stock described; quantity/dimensions to confirm','Drive/pillar captive pockets and rail joints'),('M3x12 idler screw',1,'Additional hardware required','Longer than supplied x10 for locking stack'),('M3 nylon-insert locknut,nominal height4',1,'Additional hardware required','Idler locking'),('M3 washer,OD7/ID3.3/thickness0.5',1,'Additional hardware required','Around right service bore'),('M1.6x8 cap screws',4,'Additional hardware, conditional on real ear holes','Never force M3 into servo ears'),('M1.6 nuts,AF3.2/height1.3',4,'Additional hardware','Captive ledge nuts'),('M1.6 washers,OD4/ID1.8/thickness0.5',4,'Additional hardware','Across original ear slots'),('M2x12 screws',4,'Additional hardware, conditional on real PCB holes','Camera four-hole attachment'),('M2 nuts,AF4/height1.6',4,'Additional hardware','PCB rails'),('Original servo-specific horn screws',2,'Availability and size to confirm','Keep factory screws, thread unspecified'),('Base-to-host fasteners','As needed','External support dependent','Four3.4mm base holes; length depends on host thickness')]
table('hardware_BOM.csv',['Hardware','Quantity','Availability/status','Use'],bom)
readme='''# Eye Trace SG90 interface repair01 — physical verification pending

Start with REPORT.html and EyeTrace_Repair_Assembly.FCStd. This continues the existing project using sg90_interface_audit_01 as the authoritative baseline. All previous candidates/audits are preserved. This is NOT production-ready.

The repair supplies two consistent drawing/community-based SG90 references with ears/holes/bosses/wire exits; small-fastener ear mounts; positive star-profile carriers with accessible original screws; a removable right pillar; a replaceable journal sleeve with non-pinching locking stack; pan thrust/radial support; and an adjustable four-hole PCB interface. Clone fit, original horn outlines, actual camera geometry and physical performance remain unverified.

## Files

- EyeTrace_Repair_Assembly.FCStd: colored editable component assembly with live camera pitch properties. EyeTrace_Repair.FCStd is the geometry snapshot. This is a positioned BRep assembly with scripted rigid kinematics, not a native Assembly-workbench joint solver.
- EyeTrace_Assembly.step: full50-component/77-solid assembly, including separate hardware solids.
- parts/:14 printed STL/STEP components. PrintLayout.FCStd and prototype_print_layout.stl contain all14 packed parts, no motors/horns/hardware and no diagnostic coupons.
- coupons/:five small diagnostic pieces, native layout, STL and STEP files. Print these first.
- DIMENSIONAL_AUDIT.md and dimensional_audit.csv: sources, confidence and separate CAD/physical status.
- COLLISION_AND_MOTION.md and checks/: independent native-file checks, motion/contact classification, installation/service tests, mesh/export evidence.
- ASSEMBLY_AND_FASTENERS.md and hardware_BOM.csv: sequence and required additional hardware. The supplied M3 stock alone is insufficient.
- REMAINING_PHYSICAL_VERIFICATION.md and measurements/essential_hardware_results.csv: essential missing measurements/results.
- COUPON_AND_PRINT_GUIDE.md: diagnostic use, print orientation and limitations.

## Edits and history

In the native document, edit RepairParameters.CameraPitchX/CameraPitchZ over the mechanical20–32mm range. PCB holes, rails, spacers and fasteners are expression-linked. The camera is a provisional38mm PCB, not identified hardware. Check rear components as well as pitch: the placeholder keep-out conflicts at20x20; only default28x28 has full motion/export validation. Regenerate exports after edits; existing STLs do not update automatically.

Builders preserve existing targets. Regenerate using build_repair_v09.py with a NEW work-folder name and optional parameter JSON; run independent_validate_v02.py on it; use export_repair_v03.py work_folder new_export_folder. Other servo/horn stack dimensions need coordinated code/parameter changes when actual measurements differ. A changed horn thickness is not fixed by relabeling the model.

Earlier repair attempts remain in work_*/ and archived_packages/. Use only the CURRENT top-level deliverables for review. Previous candidates and authoritative audit remain byte-identical to their recorded checksums. Sources/attribution are in ATTRIBUTION.md and measurements/servo_reference_source_ledger.csv. No exact spline teeth were invented.
'''
write('README.md',readme)
assembly='''# Assembly and fasteners — nominal reference only

Use hardware_BOM.csv. There are14 printed components and50 tagged CAD components. Extra small fasteners and a longer locking idler joint are REQUIRED; do not assume the provided M3 screws fit original servo ears/horn holes or the PCB.

Nominal hardware sources: [M1.6 cap screws](https://www.accu.co.uk/api/product-datasheet?id=3038), [small nuts](https://www.reliance.co.uk/wp-content/uploads/2023/01/Reliance-Precision-RG36-Issue-B3-Section-13-Machine-Screws.pdf), [M3 locknut](https://www.hardwarespecialty.com/Product/1497955). Confirm purchased head/nut/washer dimensions. Original retaining screws remain original; the CAD screw envelope is not a thread specification.

1. Measure real hardware and test coupons. Establish a physical neutral appropriate to the actual servo/controller. CAD zero does not establish safe servo commands.
2. Load small M1.6 nuts in base/yoke ledge pockets. Insert the pan servo from above, feed its cable separately, and fasten original ears using small screws and washers. It is ear-mounted, not squeezed by body caps.
3. Fit the replaceable thrust ring on its three clearance locating pins. Load four M3 nuts in the pan cover, put it over the shaft, then fit the original star and original center screw. Lower the yoke's profile onto the star and fit four M3x10 screws from above. Profile walls transmit torque; the cover retains the horn axially. Nominal pocket depth2.2 versus web2 gives0.2 axial allowance, so friction is not the only drive mechanism.
4. Leave the right pillar OFF. Insert the tilt motor from inside the fork toward the left through the full ear-passage opening and secure its ears with two small screw/washer joints. Its referenced2mm holes are not M3 holes.
5. Load the four M3 nuts in the tilt cover, fit cover and original star/center screw. With camera PCB and tilt-drive screws removed, slide the cradle from the right onto the keyed horn. This axial insertion requires the removable pillar. Fit four M3x10 screws from inside the fork into the captured cover nuts.
6. Seat the flanged sleeve in the right cheek. Slide the separate right pillar from the right over the projecting sleeve, onto its base pad. Align on the sleeve and fasten two M3x10 foot screws to captive nuts. Add M3 washer, M3x12 idler bolt and locknut. The sleeve gives0.2 flange clearance and0.3 nut clearance to the wall; tightening must clamp the ROTATING sleeve stack, not pinch the stationary wall. Check this physically because PETG compression can change gaps.
7. Fit both camera rails with four M3x10 joints; adjust row spacing in the frame slots. Place four separate3mm spacers at the actual PCB holes and use correctly sized camera screws through rail slots. Configured M2x12/28mm pitch are provisional. Do not force M2 into smaller PCB holes or let screw tips touch rear components.
8. Fit the actual camera/lens/IR assembly only after keep-outs are checked. Route real leads with slack through both axes, then verify slow unpowered movement before gradual powered testing. No mechanical end stops are included.

## Service stages checked in CAD

- Pan ear screws: yoke/horn removed, diameter3.2 driver from above. Tilt ears: cradle/horn removed, diameter3.2 driver from fork side. Small nuts remain captive.
- Pan original center screw: camera/lead removed as needed, diameter5 driver through the cradle's diameter6 service hole and yoke opening.
- Tilt original center screw: power off/support cradle, remove idler bolt/washer and two-bolt pillar, then sleeve. Diameter5 driver reaches the original screw through the coaxial5.2mm cheek bore. Reinstall all journal parts afterward.
- Tilt drive screws: camera removed, neutral pose; tested internal tool length50 with diameter5 bit section and diameter11 body. Pan drive screws: tilt cradle/camera removed, driver from above.
- Pillar screws: cradle neutral, diameter5 long shaft, handle above fixture.

These are sampled rigid assembly and final tool-approach envelopes. Actual hand/tool insertion sweeps, flexible cable threading and connector passage are physical checks. The cradle/right-pillar assembly path is explicitly tested, not inferred from collision-free operating poses.

## Loading

The new printed pan thrust ring/radial backup transfers load toward the base; the retained horn still supplies torque and axial retention. This is not a rated bearing. Tilt uses the removable pillar and journal sleeve, with threads kept away from the stationary bore. Payload mass/center of mass, PETG strength/friction/creep/wear, backlash and servo duty cycle remain unverified. Stall torque does not establish bearing reaction or continuous capability.
'''
write('ASSEMBLY_AND_FASTENERS.md',assembly)
measure=[('E1','Both servo ears','Hole pitch/diameter, underside height and thickness','27.2/2.0/15.9/2.5 reference; confirm selected M1.6'),('E2','Both servo envelopes','Max case/boss dimensions, axis offset and seated horn plane relative ears','Reference is not clone certified'),('H1','Both original stars','Measured outline/arm count, web and raised-hub dimensions OR trace and coupon fit','Five-arm profile is provisional'),('H2','Original center screws','Correct originals present; seated horn height and screw-head/tool access','No spline-tooth measurement needed for external printed carrier'),('C1','Camera mounting face','Both hole-center pitches, each hole diameter, PCB outline/thickness','Current28x28/diameter2.2/38x38x1.6 unmeasured'),('C2','Camera keep-outs','Rear components, standoff space, lens/IR/connector positions and screw intrusion limit','Actual camera photograph/drawing helpful; none supplied'),('W1','Real cables','Plug passage/exit positions and bend/slack throughout movement','Only nominal exit envelopes checked'),('P1','PETG coupons','As-printed sizes, nut seats, positive profile/play and journal fit','CAD gaps are not manufacturing tolerances'),('L1','Payload test','Actual mass/center of mass, friction/backlash and warm duty behavior','No material/bearing/servo load approval')]
table('measurements/essential_hardware_results.csv',['ID','Hardware/test','Essential data/result','Reason','Pan/unit A','Tilt/unit B','Camera/shared'],[list(r)+['','',''] for r in measure])
print('Core documents, source ledger and hardware/result tables saved.')
