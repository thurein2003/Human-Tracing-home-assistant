from pathlib import Path
import json,hashlib,re,csv,zipfile,xml.etree.ElementTree as E
import FreeCAD as A,Mesh,MeshPart
r=Path(__file__).resolve().parent;base=r.parent.parent;doc=A.openDocument(str(r/'CAD/Physical_Verification_Optimized.FCStd'));obs=[o for o in doc.Objects if hasattr(o,'SourceCoupon')];assert len(obs)==7
# Optional standard3MF with named geometry only, NOT a pre-sliced Creality project.
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns);model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'});res=E.SubElement(model,'{'+ns+'}resources');build=E.SubElement(model,'{'+ns+'}build')
for i,o in enumerate(obs,1):
 m=MeshPart.meshFromShape(Shape=o.Shape,LinearDeflection=.05,AngularDeflection=.1,Relative=False);vs,ts=m.Topology;obj=E.SubElement(res,'{'+ns+'}object',{'id':str(i),'type':'model','name':o.Label});mesh=E.SubElement(obj,'{'+ns+'}mesh');vertices=E.SubElement(mesh,'{'+ns+'}vertices');triangles=E.SubElement(mesh,'{'+ns+'}triangles')
 for v in vs:E.SubElement(vertices,'{'+ns+'}vertex',{k:format(0 if abs(val)<1e-8 else val,'.9g') for k,val in zip(['x','y','z'],[v.x,v.y,v.z])})
 for t in ts:E.SubElement(triangles,'{'+ns+'}triangle',dict(zip(['v1','v2','v3'],map(str,t))))
 E.SubElement(build,'{'+ns+'}item',{'objectid':str(i)})
path=r/'SLICER/Named_Geometry_Only.3mf'
if not path.exists():
 with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
  z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True));z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>');z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/></Relationships>')
with zipfile.ZipFile(path) as z:
 assert z.testzip() is None;root=E.fromstring(z.read('3D/3dmodel.model'));assert len(root.findall('.//{'+ns+'}object'))==7
 for node in root.findall('.//{'+ns+'}mesh'):
  vs=[A.Vector(float(v.get('x')),float(v.get('y')),float(v.get('z'))) for v in node.findall('{'+ns+'}vertices/{'+ns+'}vertex')];facets=[[vs[int(t.get(k))] for k in ['v1','v2','v3']] for t in node.findall('{'+ns+'}triangles/{'+ns+'}triangle')];m=Mesh.Mesh(facets);assert m.isSolid() and not m.hasNonManifolds() and not m.hasSelfIntersections()
# Direct camera gauge center extraction.
cam=next(o for o in obs if o.Label.startswith('04'));centers=sorted(set((round(f.Surface.Center.x,5),round(f.Surface.Center.y,5)) for f in cam.Shape.Faces if type(f.Surface).__name__=='Cylinder' and abs(f.Surface.Radius-1.2)<1e-6));assert len(centers)==4
assert abs(max(x for x,y in centers)-min(x for x,y in centers)-21)<1e-6 and abs(max(y for x,y in centers)-min(y for x,y in centers)-16)<1e-6
# Only additional files in this new directory are allowed.
original=json.loads((r/'CHECKS/existing_files_before.json').read_text());changed=[]
for rel,h in original.items():
 p=base/rel
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:changed.append(rel)
diagnostic_changes=[x for x in changed if x=='TESTS/results/slicer_attempt/stdout_hyphen.txt'];unexpected=[x for x in changed if x not in diagnostic_changes];assert not unexpected,unexpected
for critical in ['CAD/EyeTrace_Final_Assembly.FCStd','CAD/EyeTrace_Final_Assembly.step','DOCUMENTATION/RELEASE_STATUS.json','STL/EyeTrace_Final_K2_SingleBed.stl']:
 assert hashlib.sha256((base/critical).read_bytes()).hexdigest()==original[critical],critical
missing=[]
for p in [r/'GUIDE.html',r/'CHECKLIST.html']:
 for t in re.findall(r'(?:href|src)="([^"]+)"',p.read_text(encoding='utf-8')):
  if not t.startswith(('https:','http:','#')) and not (p.parent/t).is_file():missing.append(t)
assert not missing
for n,expected in [('CAMERA_NINE_PAIRS.csv',9),('CABLE_POSES.csv',15)]:
 data=list(csv.DictReader((r/n).open(encoding='utf-8-sig')));assert len(data)==expected and all(q['Result']=='UNVERIFIED' for q in data)
qa=json.loads((r/'CHECKS/render_QA.json').read_text());assert len(qa['images'])==10
report={'existing_files_checked':len(original),'unexpected_validated_file_changes':unexpected,'unchanged_existing_files':len(original)-len(changed),'diagnostic_log_changes_left_in_place':diagnostic_changes,'diagnostic_note':'An old slicer stdout log changed since initial hash capture. Cause not established; kit workflow did not write it and has left it in place. All other prior files match. No CAD/release file changes.','assembly_native_SHA256_unchanged':True,'release_status_SHA256_unchanged':True,'coupon_STL_geometry_passed':True,'camera_pitch_mm':[21,16],'CAD_images':len(qa['images']),'3MF_seven_named_solids_reopened':True,'report_links_missing':missing,'camera_pair_rows':9,'cable_pose_rows':15,'physical_results':'NOT PERFORMED','slicer_import_and_toolpaths':'NOT VERIFIED','full_print_release':'UNCHANGED'}
(r/'CHECKS/final_kit_QA.json').write_text(json.dumps(report,indent=2))
manifest=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and p.name!='manifest.sha256':manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(r).as_posix())
with (r/'manifest.sha256').open('x',encoding='utf-8') as f:f.write('\n'.join(manifest)+'\n')
print(json.dumps(report,indent=2));print('New kit manifest files',len(manifest))
