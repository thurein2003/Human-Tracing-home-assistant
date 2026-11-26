from pathlib import Path
import json,hashlib,re,zipfile,math
import FreeCAD as A,Part,Mesh
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];root=r.parent;out={}
for p in list((r/'CAD').glob('*.py'))+list((r/'TESTS').glob('*.py')):compile(p.read_bytes(),str(p),'exec')
d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable]
assert len(obs)==49 and len(parts)==13
invalid=[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()];assert not invalid
out['native']={'opens':True,'invalid_geometric_features':invalid,'components':len(obs),'printable_parts':len(parts),'component_solids':sum(len(o.Shape.Solids) for o in obs)}
pr=d.getObject('RepairParameters');expected=[(-10.5,-8),(-10.5,8),(10.5,-8),(10.5,8)]
def centers(o,radius):return sorted(set((round(f.Surface.Center.x,6),round(f.Surface.Center.z-76,6)) for f in o.Shape.Faces if type(f.Surface).__name__=='Cylinder' and abs(f.Surface.Radius-radius)<1e-6 and abs(f.Surface.Axis.y)>.999))
assert centers(d.getObject('PCB_Cut003'),pr.CameraPCBMountHoleDiameter.Value/2)==expected and centers(d.getObject('CameraPlate_Cut007'),pr.CameraPlateHoleDiameter.Value/2)==expected
out['camera_center_pattern_mm']=[21,16]
# Independent reopened full STEP comparison of every solid, not just total volume.
step=Part.read(str(r/'CAD/EyeTrace_Final_Assembly.step'));assert step.isValid();remaining=list(step.Solids);worst=0
for o in obs:
 for solid in o.Shape.Solids:
  b=solid.BoundBox;matches=[]
  for j,s in enumerate(remaining):
   c=s.BoundBox;err=max(abs(getattr(b,k)-getattr(c,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
   if err<1e-4 and abs(s.Volume-solid.Volume)<.001:matches.append(j)
  assert matches,('STEP solid missing',o.Name)
  i=matches[0];s=remaining.pop(i);delta=solid.cut(s).Volume+s.cut(solid).Volume;worst=max(worst,delta);assert delta<.001,(o.Name,delta)
assert not remaining
out['STEP']={'solid_count':len(step.Solids),'all_solids_match_native':True,'max_solid_symmetric_difference_mm3':worst}
stls=list((r/'STL/individual').glob('*.stl'));assert len(stls)==13;meshqa={}
for o in parts:
 path=r/'STL/individual'/(o.PrintFileName+'.stl');m=Mesh.Mesh(str(path));assert m.isSolid() and m.countComponents()==1 and not m.hasNonManifolds() and not m.hasSelfIntersections() and not m.hasNonUniformOrientedFacets();meshqa[o.PrintFileName]={'reopened':True,'watertight':True}
out['individual_meshes']=meshqa
for path,num in [(r/'STL/EyeTrace_Final_K2_SingleBed.stl',13),(r/'FIT_TESTS/FitTests_K2_Bed.stl',7)]:
 m=Mesh.Mesh(str(path));b=m.BoundBox;assert m.isSolid() and m.countComponents()==num and b.XMin>=0 and b.YMin>=0 and b.ZMin>=-1e-5 and b.XMax<=260 and b.YMax<=260 and b.ZMax<=260
 out[path.name]={'components':m.countComponents(),'bounds_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'watertight':True}
# Exact counts of modeled purchased fastener sets versus BOM.
counts={n:sum(o.Name.startswith(p) for o in obs) for n,p in [('pan_M3x10','PanDrive_'),('tilt_M3x10','TiltDrive_'),('camera_frame_M3x10','RailMount_'),('pillar_M3x10','IdlerPillar_'),('camera_M2','Camera_M2'),('pan_ear_M1p6','PanEar_'),('tilt_ear_M1p6','TiltEar_')]}
assert list(counts.values())==[4,4,4,2,4,2,2];out['modeled_fastener_counts']=counts
ex=A.openDocument(str(r/'CAD/EyeTrace_Exploded_Rendered.FCStd'));leaves=[o for o in ex.Objects if hasattr(o,'SourceComponent')];assert len(leaves)==76;out['exploded_solid_count']=len(leaves)
# Check every HTML image/file link in the delivered self-contained report.
missing=[]
for p in [r/'REPORT.html',r/'RENDERS/motion.html']:
 for target in re.findall(r'(?:href|src)="([^"]+)"',p.read_text(encoding='utf-8')):
  if not target.startswith(('https:','http:','#')) and not (p.parent/target).is_file():missing.append(str(p)+':'+target)
assert not missing;out['report_missing_links']=missing
baseline=json.loads((r/'TESTS/results/source_checksums_before.json').read_text());changed=[]
for rel,h in baseline.items():
 p=root/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:changed.append(rel)
assert not changed;out['preservation']={'prior_files_checked':len(baseline),'changed_or_missing':changed}
archives=json.loads((r/'TESTS/results/archive_inventory.json').read_text());out['source_archive_CRC']={}
for z in archives:
 with zipfile.ZipFile(root/z['path']) as f:bad=f.testzip();assert bad is None;out['source_archive_CRC'][z['path']]='PASS'
# Geometry hash locks reports/screenshots to unchanged retained nominal BReps, with final motion evidence.
summary=json.loads((r/'TESTS/results/final_validation/checks/independent_validation_summary.json').read_text());assert not summary['critical_software_failures'] and summary['motion_penetrations']==0
out['final_motion_summary']=summary;out['source_preserved_nominal_geometry']=json.loads((r/'TESTS/results/final_generation.json').read_text())['default_source_shape_differences_mm3']=={}
assert out['source_preserved_nominal_geometry']
qa=json.loads((r/'RENDERS/render_QA.json').read_text());out['CAD_PNG_views']=len(qa['images']);assert len(qa['images'])==31
out['release']='CAD VERIFIED within nominal scope; FIT-TEST READY; FULL PRINT BLOCKED; PHYSICAL FIT UNVERIFIED'
(r/'TESTS/results/final_delivery_QA.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'CAD':out['native'],'STEP':out['STEP'],'camera_pattern':out['camera_center_pattern_mm'],'source_preservation':out['preservation'],'PNG_views':out['CAD_PNG_views'],'release':out['release']},indent=2))
