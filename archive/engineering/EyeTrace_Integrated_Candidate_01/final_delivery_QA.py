from pathlib import Path
import json,hashlib,re,traceback
import FreeCAD as A
r=Path(__file__).resolve().parent
out={}
a=A.openDocument(str(r/'EyeTrace_Integrated_Assembly.FCStd'))
b=A.openDocument(str(r/'work_02/Integrated_Snapshot.FCStd'))
obs=[o for o in a.Objects if hasattr(o,'KinematicGroup')]
errs=[]
for o in obs:
 s=b.getObject(o.Name)
 if s is None:errs.append([o.Name,'missing'])
 else:
  v=o.Shape.cut(s.Shape).Volume+s.Shape.cut(o.Shape).Volume
  if v>0.001:errs.append([o.Name,v])
out['primary_vs_validated_snapshot']={'tagged_components':len(obs),'shape_changes':errs,'printed_parts':sum(bool(o.Printable) for o in obs)}
assert len(obs)==49 and not errs and sum(bool(o.Printable) for o in obs)==13
ex=A.openDocument(str(r/'EyeTrace_Exploded.FCStd'))
leaves=[o for o in ex.Objects if hasattr(o,'SourceComponent')]
out['exploded']={'leaf_features':len(leaves),'solids':sum(len(o.Shape.Solids) for o in leaves)}
assert out['exploded']['solids']==76
base=r.parent/'EyeTrace_CAD_20261115_232254'
old=json.loads((r/'work_02/checks/prior_artifacts_before.json').read_text())
changes=[]
for p,h in old.items():
 f=base/p
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=h:changes.append(p)
out['prior_artifact_preservation']={'files_checked':len(old),'changed_or_missing':changes}
assert not changes
report=(r/'REPORT.html').read_text(encoding='utf-8')
missing=[p for p in re.findall(r'(?:href|src)="([^"]+)"',report) if not (r/p).is_file()]
out['report_links']={'missing':missing}
assert not missing
out['exports']={'STL_parts':len(list((r/'parts').glob('*.stl'))),'STEP_parts':len(list((r/'parts').glob('*.step'))),'PNG_views':len(list((r/'renders').glob('*.png')))}
assert out['exports']=={'STL_parts':13,'STEP_parts':13,'PNG_views':11}
(r/'checks/final_delivery_QA.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
manifest=[]
for f in sorted(r.rglob('*')):
 if f.is_file() and f.name!='manifest.sha256':manifest.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(r).as_posix())
with (r/'manifest.sha256').open('x',encoding='utf-8') as f:f.write('\n'.join(manifest)+'\n')
print(json.dumps(out,indent=2));print('Manifest files:',len(manifest))
