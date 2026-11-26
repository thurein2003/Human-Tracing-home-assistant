from pathlib import Path
import json
import FreeCAD as A,Part
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'));data={}
placements={'PanServo_SG90_Reference':A.Placement(V(0,0,6),A.Rotation(V(0,0,1),90)),'TiltServo_SG90_Reference':A.Placement(V(-70,0,78),A.Rotation(V(0,1,0),V(0,0,1),V(1,0,0),'ZXY'))}
for name,pl in placements.items():
 s=d.getObject(name).Shape.copy();s.Placement=pl.inverse().multiply(s.Placement);b=s.BoundBox
 sections={}
 for z in [5,16.5,24,28]:
  sec=s.section(Part.makePlane(100,100,V(-50,-50,z)));bb=sec.BoundBox;sections[str(z)]={'XY_extents_mm':[bb.XLength,bb.YLength],'bounds_mm':[bb.XMin,bb.YMin,bb.XMax,bb.YMax]}
 cylinders=[]
 for f in s.Faces:
  c=f.Surface
  if type(c).__name__=='Cylinder':
   bb=f.BoundBox;cylinders.append({'diameter_mm':round(2*c.Radius,6),'axis':[round(c.Axis.x,6),round(c.Axis.y,6),round(c.Axis.z,6)],'center':[round(c.Center.x,6),round(c.Center.y,6),round(c.Center.z,6)],'Z_extent_mm':[round(bb.ZMin,6),round(bb.ZMax,6)]})
 data[name]={'canonical_extents_mm':[b.XLength,b.YLength,b.ZLength],'XY_sections_at_case_height_mm':sections,'cylinder_surfaces':cylinders}
assert all(abs(a-b)<1e-6 for a,b in zip(data['PanServo_SG90_Reference']['canonical_extents_mm'],data['TiltServo_SG90_Reference']['canonical_extents_mm']))
(r/'TESTS/results/actual_servo_dimensions.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:{'extents':v['canonical_extents_mm'],'case_section5':v['XY_sections_at_case_height_mm']['5']} for k,v in data.items()},indent=2))
