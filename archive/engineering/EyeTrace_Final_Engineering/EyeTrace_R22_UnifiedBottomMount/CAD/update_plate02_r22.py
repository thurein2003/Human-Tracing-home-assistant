import re,struct,zipfile,json
from pathlib import Path
ROOT=Path(r'EyeTrace_Final_Engineering\EyeTrace_R22_UnifiedBottomMount')
src=Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate\PRINT\Plate02_R21_SingleMountPlate_SLICED_HOLD.3mf')
stl=ROOT/'STL'/'PanYoke_R22_UnifiedBottomMount.stl'
out=ROOT/'PRINT'/'Plate02_R22_UnifiedBottomMount_UNSLICED.3mf'
if out.exists():raise SystemExit('Refusing to overwrite '+str(out))
raw=stl.read_bytes(); n=struct.unpack_from('<I',raw,80)[0]
if len(raw)!=84+n*50:raise SystemExit('Invalid STL')
verts=[];faces=[];idx={}
for i in range(n):
 v=struct.unpack_from('<12fH',raw,84+i*50);tri=[]
 for k in range(3):
  # 3MF local coordinates; preserve original object placement at (64.1,48.3,33.9).
  x,y,z=v[3+3*k:6+3*k]
  p=(round(x-64.1,6),round(y-48.3,6),round(z-33.9,6))
  if p not in idx:idx[p]=len(verts);verts.append(p)
  tri.append(idx[p])
 faces.append(tuple(tri))
vxml='<vertices>'+''.join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x,y,z in verts)+'</vertices>'
txml='<triangles>'+''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in faces)+'</triangles>'
with zipfile.ZipFile(src) as zin:
 names=zin.namelist()
 if '3D/Objects/object_2.model' not in names:raise SystemExit('Expected yoke mesh resource absent')
 m=zin.read('3D/Objects/object_2.model').decode()
 if m.count('<vertices>')!=1 or m.count('<triangles>')!=1:raise SystemExit('Unexpected yoke mesh XML')
 m=re.sub(r'<vertices>.*?</vertices>',vxml,m,count=1,flags=re.S)
 m=re.sub(r'<triangles>.*?</triangles>',txml,m,count=1,flags=re.S)
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zout:
  for name in names:
   payload=m.encode() if name=='3D/Objects/object_2.model' else zin.read(name)
   if name=='3D/3dmodel.model':
    s=payload.decode().replace('R21 Single Mounting Plate','R22 Unified Bottom Mount').replace('R21 pan-yoke and open-frame retainer','R22 pan-yoke web reduced to 2.5 mm; thrust ring and retainer preserved')
    payload=s.encode()
   zout.writestr(name,payload)
with zipfile.ZipFile(out) as z:
 bad=z.testzip()
 if bad:raise SystemExit('ZIP CRC failure '+bad)
 settings=z.read('Metadata/model_settings.config').decode()
 if settings.count('<model_instance>')!=12:raise SystemExit('Object instance count changed')
 trans=re.search(r'<assemble_item object_id="4" instance_id="0" transform="([^"]+)"',settings)
 m=zipfile.ZipFile(out).read('3D/Objects/object_2.model').decode()
 if len(re.findall(r'<triangle ',m))!=n:raise SystemExit('Triangle count mismatch')
bbox=[[min(v[k] for v in verts),max(v[k] for v in verts)] for k in range(3)]
report={'source':str(src),'output':str(out),'replaced_component':'PanYoke_EarBracket_KeyedDrive mesh only','mesh_path':'3D/Objects/object_2.model','triangles':n,'vertices':len(verts),'local_bbox_mm':bbox,'component_instances':12,'placement_transform_unchanged':bool(trans),'archive_crc':'PASS','slice_state':'UNSLICED; must be sliced in Creality Print'}
(ROOT/'DOCUMENTATION'/'R22_3MF_REPLACEMENT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
