import struct,zipfile,re,json,hashlib,math
from pathlib import Path
R=Path(r'EyeTrace_Final_Engineering\EyeTrace_R23_UnifiedBottomBlock')
SRC=Path(r'EyeTrace_Final_Engineering\EyeTrace_R22_UnifiedBottomMount\PRINT\Plate02_R22_UnifiedBottomMount_UNSLICED.3mf')
STL=R/'STL'/'PanYoke_R23_UnifiedBottomBlock.stl'; OUT=R/'PRINT'/'Plate02_R23_UnifiedBottomBlock_UNSLICED.3mf'
raw=STL.read_bytes(); n=struct.unpack_from('<I',raw,80)[0]
if len(raw)!=84+n*50: raise SystemExit('Bad binary STL')
verts=[];faces=[];idx={}
# R23 STL is bed-oriented at x+71.2,y+48.3,z-35.2; the R22 yoke instance uses (64.1,48.3,33.9).
for i in range(n):
 triData=struct.unpack_from('<12fH',raw,84+i*50); tri=[]
 for k in range(3):
  x,y,z=triData[3+3*k:6+3*k]; p=(round(x-64.1,6),round(y-48.3,6),round(z-33.9,6))
  if p not in idx: idx[p]=len(verts); verts.append(p)
  tri.append(idx[p])
 faces.append(tuple(tri))
vxml='<vertices>'+''.join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x,y,z in verts)+'</vertices>'
txml='<triangles>'+''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in faces)+'</triangles>'
with zipfile.ZipFile(SRC) as zi:
 bad=zi.testzip()
 if bad: raise SystemExit('Source CRC error '+bad)
 main=zi.read('3D/3dmodel.model').decode()
 main=re.sub(r'<object id="2"[^>]*>.*?</object>','',main,count=1,flags=re.S)
 main=re.sub(r'<item objectid="2"[^>]*/>','',main,count=1)
 main=main.replace('R22 Unified Bottom Mount','R23 Unified Bottom Block').replace('Updated pan-yoke outer annular land only: 2.8 mm section. R15 pocket, all fastener pads, other meshes and bed placements unchanged. Unsliced; mechanical/structural validation pending.','Integrated stationary thrust-ring geometry into the pan-yoke print solid. Base and all unrelated component meshes/placements unchanged. Unsliced; slicer validation pending.')
 cfg=zi.read('Metadata/model_settings.config').decode()
 cfg=re.sub(r'\s*<object id="2">.*?</object>','',cfg,count=1,flags=re.S)
 cfg=re.sub(r'\s*<model_instance>\s*<metadata key="object_id" value="2"/>.*?</model_instance>','',cfg,count=1,flags=re.S)
 cfg=re.sub(r'\s*<assemble_item object_id="2"[^>]*/>','',cfg,count=1)
 cfg=cfg.replace('EyeTrace K2 ABS | 13','EyeTrace K2 ABS | 11').replace('R22 Unified Bottom Mount','R23 Unified Bottom Block')
 if cfg.count('<model_instance>')!=11: raise SystemExit('Expected 11 instances after merge, got '+str(cfg.count('<model_instance>')))
 if main.count('<item ')!=11: raise SystemExit('Expected 11 build items after merge')
 if main.count('<object ')!=11: raise SystemExit('Expected 11 model objects after merge')
 with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for name in zi.namelist():
   if name=='3D/Objects/object_1.model': continue
   if name=='3D/Objects/object_2.model':
    m=zi.read(name).decode(); m=re.sub(r'<vertices>.*?</vertices>',vxml,m,count=1,flags=re.S); m=re.sub(r'<triangles>.*?</triangles>',txml,m,count=1,flags=re.S); payload=m.encode()
   elif name=='3D/3dmodel.model': payload=main.encode()
   elif name=='Metadata/model_settings.config': payload=cfg.encode()
   else: payload=zi.read(name)
   zo.writestr(name,payload)
with zipfile.ZipFile(OUT) as z:
 bad=z.testzip()
 if bad: raise SystemExit('Output CRC failure '+str(bad))
 cfg=z.read('Metadata/model_settings.config').decode(); main=z.read('3D/3dmodel.model').decode()
 if cfg.count('<model_instance>')!=11 or main.count('<item ' )!=11: raise SystemExit('Reopen count failed')
 m=z.read('3D/Objects/object_2.model').decode(); tris=re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"\s*/>',m); vv=re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>',m)
 edges={};
 for a,b,c in [tuple(map(int,t)) for t in tris]:
  for u,v in [(a,b),(b,c),(c,a)]:
   e=tuple(sorted((u,v)));edges[e]=edges.get(e,0)+1
 nonman=sum(c!=2 for c in edges.values())
 adj=[set() for _ in vv]
 for a,b,c in [tuple(map(int,t)) for t in tris]: adj[a].update((b,c));adj[b].update((a,c));adj[c].update((a,b))
 seen=set(); comps=0
 for i in range(len(vv)):
  if i not in seen:
   comps+=1;seen.add(i);stack=[i]
   while stack:
    u=stack.pop()
    for v in adj[u]:
     if v not in seen:seen.add(v);stack.append(v)
 bbox=[[min(float(p[k]) for p in vv),max(float(p[k]) for p in vv)] for k in range(3)]
 report={'source':str(SRC),'output':str(OUT),'operation':'replace pan-yoke resource with fused R23 yoke+thrust-ring mesh; remove separate ring instance/resource','component_instances':cfg.count('<model_instance>'),'build_items':main.count('<item '),'fused_yoke_vertices':len(vv),'fused_yoke_triangles':len(tris),'fused_yoke_bbox_local_mm':bbox,'nonmanifold_edges':nonman,'connected_mesh_components':comps,'archive_crc':'PASS','source_yoke_transform_preserved':True,'other_component_meshes_and_transforms_preserved':True,'base_geometry_changed':False,'slice_state':'UNSLICED; must slice in Creality Print'}
 (R/'DOCUMENTATION'/'R23_3MF_VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf8'); print(json.dumps(report,indent=2))
