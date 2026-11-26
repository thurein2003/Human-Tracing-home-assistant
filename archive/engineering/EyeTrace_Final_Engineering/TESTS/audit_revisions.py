from pathlib import Path
import json,csv,hashlib
import FreeCAD as A
r=Path(__file__).resolve().parents[1];workspace=r.parent;b=workspace/'EyeTrace_CAD_20261115_232254'
paths={'candidate_02':b/'candidate_02/EyeTrace_Assembly.FCStd','production_candidate_01':b/'production_candidate_01/EyeTrace_Assembly.FCStd','sg90_interface_audit_01':b/'sg90_interface_audit_01/SG90_Audit_Hold.FCStd','sg90_interface_repair_01':b/'sg90_interface_repair_01/EyeTrace_Repair_Assembly.FCStd','sg90_reference_revision_02':b/'sg90_reference_revision_02/EyeTrace_SG90_Reference_01.FCStd','camera_mount_21x16_01':b/'camera_mount_21x16_01/validated/EyeTrace_Camera_21x16_Reviewed.FCStd','integrated':workspace/'EyeTrace_Integrated_Candidate_01/EyeTrace_Integrated_Assembly.FCStd'}
report={};docs={}
for tag,p in paths.items():
 if not p.exists():report[tag]={'exists':False};continue
 d=A.openDocument(str(p));docs[tag]=d;items=[]
 for o in d.Objects:
  if hasattr(o,'Shape') and not o.Shape.isNull():
   bb=o.Shape.BoundBox
   items.append({'name':o.Name,'label':o.Label,'type':o.TypeId,'valid':o.Shape.isValid(),'solids':len(o.Shape.Solids),'volume_mm3':o.Shape.Volume,'bounds_mm':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'tagged':hasattr(o,'KinematicGroup'),'printable':bool(getattr(o,'Printable',False))})
 report[tag]={'path':str(p.relative_to(workspace)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'objects':len(d.Objects),'geometric_features':items,'invalid_features':[o['name'] for o in items if not o['valid']]}
print('Opened',len(docs),'actual FreeCAD documents. Version',A.Version()[:3])
final=docs['integrated'];trace=[]
for o in [o for o in final.Objects if hasattr(o,'KinematicGroup')]:
 matches=[]
 for tag,d in docs.items():
  if tag=='integrated':continue
  other=d.getObject(o.Name)
  if other and hasattr(other,'Shape') and not other.Shape.isNull():
   try:
    delta=o.Shape.cut(other.Shape).Volume+other.Shape.cut(o.Shape).Volume
    if delta<.001:matches.append(tag+':'+other.Name)
   except Exception:pass
 # SG90 canonical source object names differ.
 if 'Servo_SG90' in o.Name:
  q=docs['sg90_reference_revision_02'].getObject(o.Name.replace('_SG90_Reference','_ASSUMED'));delta=o.Shape.cut(q.Shape).Volume+q.Shape.cut(o.Shape).Volume
  assert delta<.001;matches.append('sg90_reference_revision_02:'+q.Name)
 trace.append([o.Name,o.Label,'PRINT' if o.Printable else 'REFERENCE',o.KinematicGroup,'; '.join(matches) or 'Integrated ribbon reservation; inspect source change',o.Shape.isValid()])
(r/'TESTS/results/revision_native_audit.json').write_text(json.dumps(report,indent=2))
with (r/'DOCUMENTATION/feature_traceability.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['Component','Function label','Manufacturing role','Frame','Exact matching prior BRep sources (<0.001mm3)','Native valid']);w.writerows(trace)
p=final.getObject('RepairParameters')
props={n:(getattr(p,n).Value if hasattr(getattr(p,n),'Value') else str(getattr(p,n))) for n in p.PropertiesList if n not in ['ExpressionEngine','Label','Label2','Visibility']}
(r/'TESTS/results/native_parameter_inventory.json').write_text(json.dumps(props,indent=2))
for o in final.Objects:
 if hasattr(o,'KinematicGroup') and ('Camera' in o.Name or 'PCB_' in o.Name or 'OriginalStar' in o.Name):
  print(o.Name,o.TypeId,[round(v,2) for v in [o.Shape.BoundBox.XMin,o.Shape.BoundBox.YMin,o.Shape.BoundBox.ZMin,o.Shape.BoundBox.XMax,o.Shape.BoundBox.YMax,o.Shape.BoundBox.ZMax]])
