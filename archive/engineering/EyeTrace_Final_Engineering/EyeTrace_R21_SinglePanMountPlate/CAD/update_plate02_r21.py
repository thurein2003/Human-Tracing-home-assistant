import re, struct, zipfile, json
from pathlib import Path
ROOT=Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate')
src=Path(r'EyeTrace_Final_Engineering\EyeTrace_R20_UltraLowProfile\PRINT\Plate02_R20_LowProfile_Sliced_Candidate.3mf')
stl=ROOT/'STL'/'Pan_KeyedHorn_Cover_R21_OpenFrame.stl'
out=ROOT/'PRINT'/'Plate02_R21_SingleMountPlate_UNSLICED.3mf'
if out.exists(): raise SystemExit(f'Refusing to overwrite {out}')
data=stl.read_bytes()
if len(data)<84: raise SystemExit('Invalid binary STL')
n=struct.unpack_from('<I',data,80)[0]
if len(data)!=84+50*n: raise SystemExit('STL size/facet count mismatch')
verts=[]; faces=[]; index={}
for i in range(n):
 vals=struct.unpack_from('<12fH',data,84+i*50); tri=[]
 for k in range(3):
  x,y,z=vals[3+3*k:6+3*k]; p=(round(float(x),6),round(float(y),6),round(float(z)-2.1,6))
  if p not in index:index[p]=len(verts);verts.append(p)
  tri.append(index[p])
 faces.append(tuple(tri))
vxml='<vertices>'+''.join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x,y,z in verts)+'</vertices>'
txml='<triangles>'+''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in faces)+'</triangles>'
with zipfile.ZipFile(src,'r') as zin:
 names=zin.namelist()
 if '3D/Objects/object_4.model' not in names:raise SystemExit('Expected cover mesh object absent')
 model=zin.read('3D/Objects/object_4.model').decode()
 if model.count('<vertices>')!=1 or model.count('<triangles>')!=1:raise SystemExit('Unexpected source mesh XML')
 model=re.sub(r'<vertices>.*?</vertices>',vxml,model,count=1,flags=re.S)
 model=re.sub(r'<triangles>.*?</triangles>',txml,model,count=1,flags=re.S)
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  for name in names:zout.writestr(name,model.encode() if name=='3D/Objects/object_4.model' else zin.read(name))
with zipfile.ZipFile(out,'r') as z:
 bad=z.testzip()
 if bad:raise SystemExit('3MF CRC failure '+bad)
 m=z.read('3D/Objects/object_4.model').decode()
 if len(re.findall(r'<triangle ',m))!=n:raise SystemExit('Triangle count mismatch')
 settings=z.read('Metadata/model_settings.config').decode()
 count=len(re.findall(r'<model_instance>',settings))
 match=re.search(r'<assemble_item object_id="8" instance_id="0" transform="([^"]+)"',settings)
def rng(i):return [min(v[i] for v in verts),max(v[i] for v in verts)]
report={'source_3mf':str(src),'output_3mf':str(out),'replaced_mesh':'3D/Objects/object_4.model (Pan_KeyedHorn_Cover)','retained_component_instance_count':count,'replacement_stl_facets':n,'replacement_3mf_vertices':len(verts),'replacement_3mf_triangles':len(faces),'replacement_mesh_bbox_local_mm':[rng(0),rng(1),rng(2)],'cover_build_transform_unchanged':bool(match),'package_crc_test':'PASS','slicing_status':'UNSLICED; slicer inspection remains required'}
(ROOT/'DOCUMENTATION'/'3MF_REPLACEMENT_VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
