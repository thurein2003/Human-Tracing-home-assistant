import os,json,hashlib
import FreeCAD as A,Part
from FreeCAD import Vector as V
H=os.path.dirname(os.path.abspath(__file__));B=os.path.dirname(H);d=A.openDocument(os.path.join(H,'EyeTrace_Repair.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')]
def vol(a,b):
 aa,bb=a.BoundBox,b.BoundBox
 if any(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))<=1e-7 for t in ['X','Y','Z']):return 0
 return a.common(b).Volume
poses=[(pa,ta) for pa in [-62,62] for ta in [-32,32]]+[(0,-32),(0,32),(-62,0),(62,0)];events=[];count=0
for pa,ta in poses:
 ss={}
 for o in obs:
  s=o.Shape.copy()
  if o.KinematicGroup=='tilt':s.rotate(V(0,0,78),V(1,0,0),ta)
  if o.KinematicGroup!='fixed':s.rotate(V(),V(0,0,1),pa)
  ss[o.Name]=s
 for i,a in enumerate(obs):
  for b in obs[i+1:]:
   count+=1;v=vol(ss[a.Name],ss[b.Name])
   if v>.001:events.append({'pose':[pa,ta],'pair':[a.Name,b.Name],'volume':v})
json.dump({'poses':poses,'all_pairs_tested':count,'unintended':events,'cache_used':False,'scope':'Extra +/-2 degree guard for nominal pocket backlash only; not enlarged servo control limits or physical-clearance proof'},open(os.path.join(H,'checks','uncached_guard_poses.json'),'x'),indent=2)
assert not events,events[:5]
pairs=[('Pan ear bearing seat','Base_EarMount_ThrustSupport','PanServo_SG90_Reference'),('Tilt ear bearing seat','PanYoke_EarBracket_KeyedDrive','TiltServo_SG90_Reference'),('Pan captured nut clamp','PanDrive_M3x10_0','Pan_KeyedHorn_Cover'),('Tilt captured nut clamp','TiltDrive_M3x10_0','Tilt_KeyedHorn_CaptiveCover'),('Idler nut does not pinch wall','TiltIdler_M3x12','PanYoke_EarBracket_KeyedDrive'),('Idler nut bears sleeve','TiltIdler_M3x12','Tilt_Journal_FlangedSleeve'),('Idler washer bears cheek','TiltIdler_M3_Washer','TiltCradle_KeyedHorn_CameraFrame'),('Camera spacer touches PCB','PCB_Spacer_Lower_Left','PCB_Cut003'),('Camera spacer touches rail','PCB_Spacer_Lower_Left','Camera_SlidingRail_Lower'),('Camera nut bears rail','Camera_M2x12_Lower_Left','Camera_SlidingRail_Lower'),('Rail nut bears frame','RailMount_Lower_M3x10_0','TiltCradle_KeyedHorn_CameraFrame'),('Pan radial backup gap','Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive')]
ct=[]
for label,a,b in pairs:ct.append({'interface':label,'pair':[a,b],'distance_mm':d.getObject(a).Shape.distToShape(d.getObject(b).Shape)[0]})
json.dump(ct,open(os.path.join(H,'checks','actual_contact_clearance_distances.json'),'x'),indent=2)
assert ct[4]['distance_mm']>.25
for i in [0,1,2,3,5,6,7,8,9,10]:assert ct[i]['distance_mm']<1e-5,ct[i]
# Earlier artifacts remain byte-identical to their recorded manifests.
results=[]
for base in [B,os.path.join(B,'production_candidate_01'),os.path.join(B,'sg90_interface_audit_01'),os.path.join(B,'sg90_reference_revision_02')]:
 fn=os.path.join(base,'manifest.sha256');bad=[];n=0
 for line in open(fn):
  h,p=line.rstrip('\n').split('  ',1);n+=1
  if hashlib.sha256(open(os.path.join(base,p),'rb').read()).hexdigest()!=h:bad.append(p)
 results.append({'manifest':os.path.relpath(fn,B),'entries_checked':n,'changed':bad});assert not bad
json.dump(results,open(os.path.join(H,'checks','previous_artifact_preservation.json'),'x'),indent=2)
print('Guard pairs',count,'penetrations',len(events));print('CONTACTS',json.dumps(ct));print('Preservation',sum(x['entries_checked'] for x in results),'manifest entries unchanged')
