from pathlib import Path
import json,math
import FreeCAD as A,Part
from FreeCAD import Vector as V
r=Path(__file__).resolve().parent;base=r.parent.parent;d=A.openDocument(str(base/'CAD/EyeTrace_Final_Assembly.FCStd'));names=['Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive','TiltCradle_KeyedHorn_CameraFrame','Tilt_Removable_IdlerPillar'];out={}
for name in names:
 o=d.getObject(name);rows=[]
 for ax,angle in [('Y',0),('Y',45),('Y',90),('Y',135),('Y',180),('Y',225),('Y',270),('X',90),('X',270)]:
  s=o.Shape.copy();s.rotate(V(),V(0,1,0) if ax=='Y' else V(1,0,0),angle);bb=s.BoundBox;s.translate(V(-bb.XMin,-bb.YMin,-bb.ZMin));bb=s.BoundBox;vs,ts=s.tessellate(.15);areas={str(a):0. for a in [30,40,45,50]};bedarea=0
  for a,b,c in ts:
   p,q,t=vs[a],vs[b],vs[c];n=(q-p).cross(t-p)
   if n.Length<1e-8:continue
   if max(p.z,q.z,t.z)<.001:bedarea+=n.Length/2
   if min(p.z,q.z,t.z)<.01:continue
   for threshold in [30,40,45,50]:
    if n.z/n.Length < -math.cos(math.radians(threshold))-.00001:areas[str(threshold)]+=n.Length/2
  rows.append({'axis':ax,'angle':angle,'dims':[bb.XLength,bb.YLength,bb.ZLength],'downward_area_by_surface_angle_mm2':areas,'bed_contact_area_mm2':bedarea})
 out[name]=rows
 print(name,[(x['axis']+str(x['angle']),round(x['downward_area_by_surface_angle_mm2']['40'],1),round(x['bed_contact_area_mm2'],1),[round(i,1) for i in x['dims']]) for x in rows])
(r/'CHECKS/orientation_candidates.json').write_text(json.dumps(out,indent=2))
