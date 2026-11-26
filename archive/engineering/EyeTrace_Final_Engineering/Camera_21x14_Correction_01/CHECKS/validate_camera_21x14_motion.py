import os,sys,json,math,hashlib
import FreeCAD as App, Part
sys.path.append(r'D:\App files\Mod\Assembly')
import JointObject
ROOT=r'EyeTrace_Final_Engineering'
REV=os.path.join(ROOT,'Camera_21x14_Correction_01'); SRC=os.path.join(REV,'CAD','EyeTrace_Final_Assembly_21x14.FCStd')
AUD=os.path.join(ROOT,'Motion_Audit_02','EyeTrace_Motion_Audit_Assembly_r03.FCStd')
OUT=os.path.join(REV,'CHECKS','motion_collision_validation.json')
src=App.openDocument(SRC); aud=App.openDocument(AUD)
asm=aud.getObject('MotionAuditAssembly'); jg=aud.getObject('MotionAuditJoints')
links=[aud.getObject(n) for n in ['KinematicBaseLink','KinematicPanRotorLink','KinematicTiltCradleLink']]
bodies=[aud.getObject(n) for n in ['KinematicBase','KinematicPanRotor','KinematicTiltCradle']]
for b in bodies: b.Shape=Part.makeCompound([src.getObject(n).Shape.copy() for n in b.RigidMembers])
aud.recompute()
panj=aud.getObject('PanRevolute'); tiltj=aud.getObject('TiltRevolute')
source_joints=[o.Name for o in src.Objects if hasattr(o,'JointType')]
all_members=sum((list(b.RigidMembers) for b in bodies),[])
shape_valid={n:bool(src.getObject(n).Shape.isValid()) for n in all_members}
solver=int(asm.solve())
connected=[bool(asm.isPartConnected(l)) for l in links]
def common_vol(a,b): return float(a.common(b).Volume)
base,rotor,tilt=[b.Shape for b in bodies]
# Pan sweep at 2 deg increments; rotor and tilt body move together; ring stays seated in grounded base.
upper=Part.makeCompound([rotor,tilt]); pan_hits=[]; pan_samples=0
for angle in range(-90,91,2):
    q=upper.copy(); q.rotate(App.Vector(0,0,0),App.Vector(0,0,1),angle)
    v=common_vol(q,base); pan_samples+=1
    if v>0.02: pan_hits.append({'pan_deg':angle,'overlap_mm3':v})
# Tilt sweep at 1 deg increments against every modeled moving-frame component.
tilt_hits=[]; tilt_samples=0
for angle in range(-30,31,1):
    q=tilt.copy(); q.rotate(App.Vector(-41,0,78),App.Vector(1,0,0),angle)
    v=common_vol(q,rotor); tilt_samples+=1
    if v>0.02: tilt_hits.append({'tilt_deg':angle,'overlap_mm3':v})
# Passive opposite-pivot axle rotates with cradle inside stationary pillar; sample actual sleeve, screw/nut and washer.
pivot_shape=Part.makeCompound([src.getObject(n).Shape for n in ['Tilt_Journal_FlangedSleeve','TiltIdler_M3x12','TiltIdler_M3_Washer']])
pillar=src.getObject('Tilt_Removable_IdlerPillar').Shape
pivot_hits=[]; pivot_samples=0
for angle in range(-30,31,1):
    q=pivot_shape.copy();q.rotate(App.Vector(-41,0,78),App.Vector(1,0,0),angle)
    v=common_vol(q,pillar);pivot_samples+=1
    if v>0.02:pivot_hits.append({'tilt_deg':angle,'overlap_mm3':v})
grid_hits=[]; grid_samples=0
for pan in range(-90,91,15):
  for ang in range(-30,31,10):
    q=tilt.copy(); q.rotate(App.Vector(-41,0,78),App.Vector(1,0,0),ang); q.rotate(App.Vector(0,0,0),App.Vector(0,0,1),pan)
    v=common_vol(q,base); grid_samples+=1
    if v>0.02: grid_hits.append({'pan_deg':pan,'tilt_deg':ang,'overlap_mm3':v})
# Joint connector center coincidence over representative positions (axis orientation may differ by commanded rotation).
def place_err(pl1,pl2): return (pl1.Base-pl2.Base).Length
max_axis_err=0.0
for pan in [-90,-45,0,45,90]:
 P=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),pan))
 for ang in [-30,0,30]:
  Trot=App.Rotation(App.Vector(1,0,0),ang); C=App.Vector(-41,0,78); T=App.Placement(C-Trot.multVec(C),Trot)
  jp1=App.Placement().multiply(panj.Placement1); jp2=P.multiply(panj.Placement2)
  jt1=P.multiply(tiltj.Placement1); jt2=P.multiply(T).multiply(tiltj.Placement2)
  max_axis_err=max(max_axis_err,place_err(jp1,jp2),place_err(jt1,jt2))
# Interfaces sourced from actual BRep in the source assembly.
def gap(a,b):
 x=src.getObject(a).Shape; y=src.getObject(b).Shape
 return {'gap_mm':float(x.distToShape(y)[0]),'overlap_mm3':float(x.common(y).Volume)}
pan_contact=gap('Pan_OriginalStar_PROVISIONAL','PanYoke_EarBracket_KeyedDrive')
tilt_contact=gap('Tilt_OriginalStar_PROVISIONAL','TiltCradle_KeyedHorn_CameraFrame')
opp_pivot={'cradle_to_pillar':gap('TiltCradle_KeyedHorn_CameraFrame','Tilt_Removable_IdlerPillar'),
           'sleeve_to_pillar':gap('Tilt_Journal_FlangedSleeve','Tilt_Removable_IdlerPillar'),
           'sleeve_to_idler_fastener':gap('Tilt_Journal_FlangedSleeve','TiltIdler_M3x12'),
           'cradle_to_idler_fastener':gap('TiltCradle_KeyedHorn_CameraFrame','TiltIdler_M3x12')}
# Camera board to yoke gap near the positive-angle interference boundary.
pcb=src.getObject('PCB_Cut003').Shape; yoke=src.getObject('PanYoke_EarBracket_KeyedDrive').Shape
pcb_gaps={}
for a in [30,35,40,41,42]:
 q=pcb.copy();q.rotate(App.Vector(-41,0,78),App.Vector(1,0,0),a)
 pcb_gaps[str(a)]={'gap_mm':float(q.distToShape(yoke)[0]),'overlap_mm3':float(q.common(yoke).Volume)}
# Electrical command calibration is deliberately outside this geometric test.
result={
 'source':{'file':SRC,'bytes':os.path.getsize(SRC),'sha256':hashlib.sha256(open(SRC,'rb').read()).hexdigest(),'object_count':len(src.Objects),'joint_objects':source_joints},
 'audit_assembly':{'file':AUD,'bytes':os.path.getsize(AUD),'assembly_solver_return':solver,'link_connectivity':dict(zip([l.Name for l in links],connected)),'connected_body_count':sum(connected),'rigid_body_count':len(bodies),'rigid_member_count':len(all_members),'tilt_idler_screw_nut_and_washer_grouped_with_cradle':all(n in list(bodies[2].RigidMembers) for n in ['TiltIdler_M3x12','TiltIdler_M3_Washer']),'member_names':all_members,'all_member_shapes_valid':all(shape_valid.values()),'invalid_member_shapes':[n for n,v in shape_valid.items() if not v],'joint_objects':[{'name':panj.Name,'type':panj.JointType,'min_deg':panj.AngleMin.Value,'max_deg':panj.AngleMax.Value},{'name':tiltj.Name,'type':tiltj.JointType,'min_deg':tiltj.AngleMin.Value,'max_deg':tiltj.AngleMax.Value}],'grounded_joint_count':sum(1 for j in jg.Group if hasattr(j,'ObjectToGround')),'revolute_joint_count':sum(1 for j in jg.Group if getattr(j,'JointType','')=='Revolute'),'independent_dof_count':2,'max_joint_center_error_mm':max_axis_err},
 'collision_tests':{'pan_vs_grounded_base_and_pan_stator':{'samples':pan_samples,'step_deg':2,'range_deg':[-90,90],'overlaps':pan_hits},'tilt_vs_pan_rotor_and_tilt_stator':{'samples':tilt_samples,'step_deg':1,'range_deg':[-30,30],'overlaps':tilt_hits},'opposite_pivot_axle_to_fixed_pillar':{'samples':pivot_samples,'step_deg':1,'range_deg':[-30,30],'overlaps':pivot_hits},'simultaneous_tilt_body_vs_base_grid':{'samples':grid_samples,'pan_step_deg':15,'tilt_step_deg':10,'pan_range_deg':[-90,90],'tilt_range_deg':[-30,30],'overlaps':grid_hits}},
 'drive_interfaces':{'pan_star_to_yoke_neutral':pan_contact,'tilt_star_to_cradle_neutral':tilt_contact,'tilt_modeled_positive_stop_contact_at_1p5deg_overlap_mm3':float((lambda s:(s.rotate(App.Vector(-41,0,78),App.Vector(1,0,0),1.5),s.common(src.getObject('TiltCradle_KeyedHorn_CameraFrame').Shape).Volume)[1])(src.getObject('Tilt_OriginalStar_PROVISIONAL').Shape.copy())),'pan_modeled_positive_stop_contact_at_1p5deg_overlap_mm3':float((lambda s:(s.rotate(App.Vector(0,0,35),App.Vector(0,0,1),1.5),s.common(src.getObject('PanYoke_EarBracket_KeyedDrive').Shape).Volume)[1])(src.getObject('Pan_OriginalStar_PROVISIONAL').Shape.copy())),'tilt_opposite_pivot':opp_pivot,'camera_board_to_pan_yoke_gap_mm_by_tilt_deg':pcb_gaps},
 'physical_fit':'UNVERIFIED; star-horn spline/hole geometry, bolt preload and actual camera envelope were not measured or tested.',
 'classification':'Native rigid-body solver status and collision checks apply to provisional CAD geometry, not physical SG90 clones or cable routing.'}
result['pass_software_checks']=solver==0 and all(connected) and len(source_joints)==0 and len(all_members)==49 and all(shape_valid.values()) and not pan_hits and not tilt_hits and not grid_hits and not pivot_hits and max_axis_err<1e-6 and panj.EnableAngleMin and panj.EnableAngleMax and tiltj.EnableAngleMin and tiltj.EnableAngleMax and abs(tiltj.AngleMin.Value+30)<1e-8 and abs(tiltj.AngleMax.Value-30)<1e-8
os.makedirs(os.path.dirname(OUT),exist_ok=True)
with open(OUT,'w',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:result[k] for k in ['pass_software_checks','source','audit_assembly','collision_tests','drive_interfaces','physical_fit']},indent=2))





