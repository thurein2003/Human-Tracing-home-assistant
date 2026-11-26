from pathlib import Path
import json,math
import FreeCAD as A,Part
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'))
def chord(name,p,axis):
 line=Part.makeLine(V(*p)-V(*axis)*100,V(*p)+V(*axis)*100);section=d.getObject(name).Shape.common(line);return sorted(round(e.Length,6) for e in section.Edges)
probes=[('Base plate','Base_EarMount_ThrustSupport',(36,30,2),(0,0,1)),('Base thrust wall radial','Base_EarMount_ThrustSupport',(30,0,20),(1,0,0)),('Replaceable thrust ring','Pan_Replaceable_ThrustRing',(29,1,36.5),(0,0,1)),('Pan cover web','Pan_KeyedHorn_Cover',(10,3,34.25),(0,0,1)),('Tilt cover web','Tilt_KeyedHorn_CaptiveCover',(-42,8,8+78),(1,0,0)),('Right pillar wall','Tilt_Removable_IdlerPillar',(37.5,10,70),(1,0,0)),('Camera frame vertical rail','TiltCradle_KeyedHorn_CameraFrame',(-24,-23,76),(0,1,0)),('Camera plate','CameraPlate_Cut007',(20,-26,76),(0,1,0)),('Tilt sleeve radial wall','Tilt_Journal_FlangedSleeve',(38,2,78),(0,1,0)),('PCB standoff radial wall','PCB_Spacer_Lower_Left',(-10.5,-29,68),(1,0,0))]
rows=[]
for label,name,p,ax in probes:rows.append({'feature':label,'component':name,'probe_center_mm':p,'direction':ax,'material_chords_mm':chord(name,p,ax)})
assert all(x['material_chords_mm'] for x in rows),rows
(r/'TESTS/results/wall_section_probes.json').write_text(json.dumps({'method':'Actual BRep common with directed line; all material segments reported, not an exhaustive global minimum-wall proof','probes':rows},indent=2))
print(json.dumps(rows,indent=2))
