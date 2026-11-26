from pathlib import Path
import json
import FreeCAD as A,Part
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')]
def overlap(a,b):
 aa,bb=a.BoundBox,b.BoundBox
 if any(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))<=1e-7 for t in ['X','Y','Z']):return 0
 return a.common(b).Volume
out=[]
def probe(label,start,direction,targets,diameter=None):
 dia=diameter or (3 if 'M2' in label else 5);tool=Part.makeCylinder(dia/2,35,V(*start),V(*direction));hits=[{'name':o.Name,'volume':overlap(tool,o.Shape)} for o in targets if overlap(tool,o.Shape)>.001];assert not hits,(label,hits);out.append({'interface':label,'tool_diameter_mm':dia,'unintended':hits})
for o in obs:
 if o.Name.startswith('Camera_M2'):
  b=o.Shape.BoundBox;x=(b.XMin+b.XMax)/2;z=(b.ZMin+b.ZMax)/2
  probe(o.Name+' front driver',(x,-34,z),(0,-1,0),[v for v in obs if v!=o]);probe(o.Name+' rear socket bit - camera module removed',(x,-22.8,z),(0,1,0),[v for v in obs if v.Name in ['PCB_Cut003','CameraPlate_Cut007'] or v.Name.startswith('PCB_Spacer')],6)
 if o.Name.startswith('RailMount_'):
  b=o.Shape.BoundBox;x=(b.XMin+b.XMax)/2;z=(b.ZMin+b.ZMax)/2;probe(o.Name+' front driver',(x,-30.4,z),(0,-1,0),[v for v in obs if v!=o])
for x in [-32,32]:
 for y in [-27,27]:probe('Base host screw approach BEFORE yoke installation '+str((x,y)),(x,y,4),(0,0,1),[o for o in obs if o.KinematicGroup=='fixed'])
(r/'TESTS/results/additional_tool_access.json').write_text(json.dumps({'probes':out,'scope':'Camera rear nuts accessed with complete module removed; Rear M2 socket envelope diameter6; actual tool and finger access still physical checks. Two base corners are obstructed in the completed assembly: secure base before yoke installation, remove upper assembly for host-screw service. No host fastener size inferred.'},indent=2))
print('Camera and base driver approach checks:',len(out),'PASS')
