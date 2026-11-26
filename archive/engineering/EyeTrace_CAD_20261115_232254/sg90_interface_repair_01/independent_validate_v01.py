# Independent validator: opens saved native geometry; does not import or execute the CAD builder.
import os,sys,json,math
import FreeCAD as A,Part,MeshPart
from FreeCAD import Vector as V
H=os.path.dirname(os.path.abspath(__file__));R=os.path.join(H,sys.argv[1] if len(sys.argv)>1 else 'work_05')
d=A.openDocument(os.path.join(R,'EyeTrace_Repair.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable];groups={o.Name:o.KinematicGroup for o in obs}
assert len(obs)==47 and len(parts)==13
checks={};critical=[]
def save(n,x):json.dump(x,open(os.path.join(R,'checks',n+'.json'),'x'),indent=2)
def volume(a,b):
 aa,bb=a.BoundBox,b.BoundBox
 if any(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))<=1e-7 for t in ['X','Y','Z']):return 0.
 return a.common(b).Volume
# Canonicalized motors must be the same geometry, not just share labels.
panP=A.Placement(V(0,0,6),A.Rotation(V(0,0,1),90));tiltP=A.Placement(V(-70,0,78),A.Rotation(V(0,1,0),V(0,0,1),V(1,0,0),'ZXY'))
def transform(s,p):q=s.copy();q.Placement=p.multiply(q.Placement);return q
p=transform(d.getObject('PanServo_SG90_Reference').Shape,panP.inverse());t=transform(d.getObject('TiltServo_SG90_Reference').Shape,tiltP.inverse());delta=p.cut(t).Volume+t.cut(p).Volume
alignment={'motor_canonical_symmetric_difference_mm3':delta,'pan_axis':[0,0,1],'pan_axis_point':[0,0,0],'tilt_axis':[1,0,0],'tilt_axis_point':[0,0,78],'references_identical':delta<.001,'idler_wall_diameter':5.2,'idler_sleeve_diameter':5.,'radial_clearance':.1,'sleeve_end_x':39.3,'wall_end_x':39.,'nut_to_wall_axial_clearance':.3,'flange_rear_x':36.3,'wall_front_x':36.5,'flange_wall_clearance':.2}
assert delta<.001
save('independent_alignment',alignment)
# Native camera expressions are exercised, including hardware; restore before assembly testing.
pr=d.getObject('RepairParameters');orig=(pr.CameraPitchX.Value,pr.CameraPitchZ.Value); trials=[]
for px,pz in [(20,20),(20,32),(32,20),(32,32),(28,28)]:
 pr.CameraPitchX=px;pr.CameraPitchZ=pz;d.recompute();err=[]
 pcb=[o for o in obs if o.TypeId=='Part::Cut'][0];centers=set()
 for f in pcb.Shape.Faces:
  s=f.Surface
  if type(s).__name__=='Cylinder' and abs(s.Radius-1.1)<1e-6:centers.add((round(s.Center.x,5),round(s.Center.z,5)))
 expected={(sx*px/2,76+sz*pz/2) for sx in [-1,1] for sz in [-1,1]}
 if centers!=expected:err.append('PCB hole centers')
 for row,sg in [('Lower',-1),('Upper',1)]:
  zz=76+sg*pz/2
  for n in ['Camera_SlidingRail_'+row]+['RailMount_'+row+'_M3x10_'+str(i) for i in [0,1]]:
   bb=d.getObject(n).Shape.BoundBox
   if abs((bb.ZMin+bb.ZMax)/2-zz)>1e-6:err.append(n)
  for col,sx in [('Left',-1),('Right',1)]:
   for n in ['PCB_Spacer_'+row+'_'+col,'Camera_M2x12_'+row+'_'+col]:
    bb=d.getObject(n).Shape.BoundBox
    if abs((bb.XMin+bb.XMax)/2-sx*px/2)>1e-6 or abs((bb.ZMin+bb.ZMax)/2-zz)>1e-6:err.append(n)
 conflicts=[];keep=d.getObject('Camera_RearComponents_KEEP_OUT').Shape
 for o in obs:
  if o.Name.startswith(('PCB_Spacer','Camera_M2')):
   v=volume(o.Shape,keep)
   if v>.001:conflicts.append({'component':o.Name,'volume':v})
 trials.append({'pitch':[px,pz],'live_expression_errors':err,'provisional_rear_keepout_conflicts':conflicts,'note':'Range is mechanical adjustability, not proof of a real camera board/components.'})
 assert not err
pr.CameraPitchX=orig[0];pr.CameraPitchZ=orig[1];d.recompute();save('camera_parameter_trials',trials)
# Positive torque path: relative horn/carrier rotation, not friction assumptions.
engagement=[]
for horn,carrier,point,axis in [('Pan_OriginalStar_PROVISIONAL','PanYoke_EarBracket_KeyedDrive',V(),V(0,0,1)),('Tilt_OriginalStar_PROVISIONAL','TiltCradle_KeyedHorn_CameraFrame',V(0,0,78),V(1,0,0))]:
 data=[]
 for ang in [-5,-3,-2,-1,0,1,2,3,5]:
  h=d.getObject(horn).Shape.copy();h.rotate(point,axis,ang);v=volume(h,d.getObject(carrier).Shape);data.append({'relative_angle_deg':ang,'engagement_probe_volume_mm3':v})
 ok=any(x['relative_angle_deg']<0 and x['engagement_probe_volume_mm3']>.001 for x in data) and any(x['relative_angle_deg']>0 and x['engagement_probe_volume_mm3']>.001 for x in data)
 engagement.append({'horn':horn,'carrier':carrier,'positive_wall_drive_both_directions':ok,'classification':'DESIGNED ENGAGEMENT probe only, not an operating assembly pose or stress proof','samples':data})
 assert ok
save('positive_horn_drive',engagement)
# Staged insertion/removal: fasteners/horns removed. Real flexible leads must be threaded separately.
install=[]
for name,targets,axis in [('PanServo_SG90_Reference',['Base_EarMount_ThrustSupport','Pan_Replaceable_ThrustRing'],V(0,0,1)),('TiltServo_SG90_Reference',['Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive'],V(1,0,0))]:
 fails=[]
 for dist in [0,.25,1,2,5,10,15,20,25,30,40]:
  s=d.getObject(name).Shape.copy();s.translate(axis*dist)
  for n in targets:
   v=volume(s,d.getObject(n).Shape)
   if v>.001:fails.append({'translation':dist,'target':n,'volume':v})
 install.append({'motor':name,'removed_subassemblies':'pan yoke removed for pan; cradle/horn removed for tilt; ear screws removed','samples':11,'unintended':fails,'wire_scope':'Rigid case/ears/boss only; flexible cable insertion and connector size unverified'})
 if fails:critical.append(name+' insertion')
save('installation_removal',install)
# Service tool envelopes and explicit disassembly stages.
def cy(r,h,p,ax):return Part.makeCylinder(r,h,V(*p),V(*ax))
cam_remove={o.Name for o in obs if o.Name.startswith(('Camera_M2','PCB_Spacer','Camera_Rear','Camera_Lens','Camera_Wire')) or o.TypeId=='Part::Cut'}
access=[]
def tooltest(label,tool,targets,procedure):
 fails=[]
 for o in targets:
  v=volume(tool,o.Shape)
  if v>.001:fails.append({'component':o.Name,'volume':v})
 access.append({'test':label,'procedure':procedure,'unintended':fails})
 if fails:critical.append(label)
for i,x in enumerate([-8.15,19.05]):tooltest('Pan ear screw '+str(i),cy(1.6,40,(x,0,26.5),(0,0,1)),[d.getObject(n) for n in ['Base_EarMount_ThrustSupport','PanServo_SG90_Reference']],'Yoke/horn removed; small nuts captive; driver diameter3.2 from above')
for i,z in enumerate([58.95,86.15]):tooltest('Tilt ear screw '+str(i),cy(1.6,55,(-49.5,0,z),(1,0,0)),[d.getObject(n) for n in ['PanYoke_EarBracket_KeyedDrive','TiltServo_SG90_Reference']],'Cradle/horn removed; small nuts captive; driver diameter3.2 from fork side')
tooltest('Original pan retaining screw',cy(2.5,80,(0,0,38),(0,0,1)),[o for o in obs if o.Name not in cam_remove and o.Name!='PanOriginalScrew_PROVISIONAL'],'Camera/lead removed; retained cradle has diameter6 service hole; driver diameter5')
exclude=cam_remove|{'TiltOriginalScrew_PROVISIONAL','TiltIdler_M3x12','TiltIdler_M3_Washer','Tilt_Journal_FlangedSleeve'}
tooltest('Original tilt retaining screw',cy(2.5,85,(-38,0,78),(1,0,0)),[o for o in obs if o.Name not in exclude],'Power off, support cradle, remove idler bolt/washer/sleeve; through-axis diameter5.2 access; driver diameter5')
for i,(y,z) in enumerate([(15,78),(-15,78),(0,93),(0,63)]):
 n='TiltDrive_M3x10_'+str(i);tool=cy(2.5,30,(-34,y,z),(1,0,0)).fuse(cy(5.5,20,(-4,y,z),(1,0,0)))
 tooltest(n+' service',tool,[o for o in obs if o.Name not in cam_remove|{n}],'Camera removed; internal stubby tool length50, bit diameter5, body diameter11; final approach envelope only')
for i,(x,y) in enumerate([(18,0),(-18,0),(0,18),(0,-18)]):
 n='PanDrive_M3x10_'+str(i);tooltest(n+' service',cy(2.5,50,(x,y,42),(0,0,1)),[o for o in obs if o.KinematicGroup!='tilt' and o.Name!=n],'Tilt cradle/camera removed; driver diameter5 from top; captive nuts below')
save('screw_access',access)
print('PRE-MOTION critical:',critical,flush=True)
# All pairs, no overlap exemption. Cache only mathematically invariant relative configurations.
cache={};events=[];pairtests=0;posetests=0
poses=[(pa,ta) for pa in range(-60,61,10) for ta in range(-30,31,5)]+[(17.5,-12.5),(-37.5,22.5),(53.25,27.25)]
for pa,ta in poses:
 posetests+=1;shapes={}
 for o in obs:
  s=o.Shape.copy();g=o.KinematicGroup
  if g=='tilt':s.rotate(V(0,0,78),V(1,0,0),ta)
  if g!='fixed':s.rotate(V(),V(0,0,1),pa)
  shapes[o.Name]=s
 for i,a in enumerate(obs):
  for b in obs[i+1:]:
   pairtests+=1;ga,gb=a.KinematicGroup,b.KinematicGroup
   rel=(0,0) if ga==gb else ((0,ta) if 'fixed' not in [ga,gb] else (pa,ta if 'tilt' in [ga,gb] else 0))
   key=(a.Name,b.Name,rel)
   if key not in cache:cache[key]=volume(shapes[a.Name],shapes[b.Name])
   if cache[key]>.001:events.append({'pose':[pa,ta],'pair':[a.Name,b.Name],'volume_mm3':cache[key],'classification':'UNINTENDED penetration'})
save('independent_motion',{'poses':posetests,'pair_tests':pairtests,'unique_relative_tests':len(cache),'all_component_pairs_included':True,'positive_overlap_whitelist':[],'unintended_instances':len(events),'events':events,'limits':'Discrete operating poses and nominal exit keep-outs; not continuous motion, spline, flexible cable-loop, stress or physical-fit proof.'})
meshes={}
for o in parts:
 m=MeshPart.meshFromShape(Shape=o.Shape,LinearDeflection=.08,AngularDeflection=.15,Relative=False)
 meshes[o.Name]={'brep_valid':o.Shape.isValid(),'solid_count':len(o.Shape.Solids),'mesh_closed':m.isSolid(),'mesh_components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'inconsistent_normals':m.hasNonUniformOrientedFacets()}
 if not(o.Shape.isValid() and len(o.Shape.Solids)==1 and m.isSolid() and m.countComponents()==1 and not m.hasNonManifolds() and not m.hasSelfIntersections() and not m.hasNonUniformOrientedFacets()):critical.append(o.Name+' mesh')
save('independent_print_geometry',meshes)
summary={'critical_software_failures':critical,'motion_penetrations':len(events),'positive_horn_drive':[x['positive_wall_drive_both_directions'] for x in engagement],'physical_fit':'UNVERIFIED','native_components':len(obs),'printed_components':len(parts),'independent_of_builder':'Validator imports no builder code; opens saved native BRep and native expressions.'}
save('independent_validation_summary',summary)
print(json.dumps(summary),flush=True);print('MOTION pair tests',pairtests,'unique',len(cache),'collision pairs',sorted(set(tuple(x['pair']) for x in events)),flush=True)
