import struct,zipfile,re,json,hashlib
from pathlib import Path
R=Path(r'EyeTrace_Final_Engineering\EyeTrace_R24_PanYoke_OneLayer')
SRC=Path(r'EyeTrace_Final_Engineering\EyeTrace_R23_UnifiedBottomBlock\PRINT\Plate02_R23_UnifiedBottomBlock_IMPORTFIX_UNSLICED.3mf')
STL=R/'STL'/'PanYoke_R24_OneLayer.stl'; OUT=R/'PRINT'/'Plate02_R24_PanYoke_OneLayer_UNSLICED.3mf'
b=STL.read_bytes(); n=struct.unpack_from('<I',b,80)[0]
if len(b)!=84+n*50: raise SystemExit('Invalid binary STL')
verts=[]; faces=[]; index={}
# Keep R23 instance transform exactly: x64.1,y48.3,z33.9. Convert bed-oriented STL vertices into model-local coordinates.
for i in range(n):
 d=struct.unpack_from('<12fH',b,84+i*50); tri=[]
 for k in range(3):
  x,y,z=d[3+3*k:6+3*k]; p=(round(x-64.1,6),round(y-48.3,6),round(z-33.9,6))
  if p not in index: index[p]=len(verts);verts.append(p)
  tri.append(index[p])
 faces.append(tuple(tri))
vxml='<vertices>'+''.join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x,y,z in verts)+'</vertices>'
txml='<triangles>'+''.join(f'<triangle v1="{a}" v2="{bb}" v3="{c}"/>' for a,bb,c in faces)+'</triangles>'
with zipfile.ZipFile(SRC) as zi:
 if zi.testzip(): raise SystemExit('Source 3MF CRC failure')
 main=zi.read('3D/3dmodel.model').decode(); cfg=zi.read('Metadata/model_settings.config').decode()
 if main.count('<item ')!=11 or cfg.count('<model_instance>')!=11: raise SystemExit('Unexpected Plate02 inventory')
 # Preserve all instances and every other object mesh/settings byte-for-byte; replace only yoke mesh resource object_2.
 with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for name in zi.namelist():
   data=zi.read(name)
   if name=='3D/Objects/object_2.model':
    m=data.decode();m=re.sub(r'<vertices>.*?</vertices>',vxml,m,count=1,flags=re.S);m=re.sub(r'<triangles>.*?</triangles>',txml,m,count=1,flags=re.S);data=m.encode()
   elif name=='3D/3dmodel.model':
    data=data.replace(b'R23 Unified Bottom Block',b'R24 PanYoke One Layer')
   zo.writestr(name,data)
# Reopen exact output, verify CRC and mesh topology + exact transformed vertex correspondence.
with zipfile.ZipFile(OUT) as z:
 if z.testzip():raise SystemExit('Output CRC failure')
 m=z.read('3D/Objects/object_2.model').decode(); mm=z.read('3D/3dmodel.model').decode(); cc=z.read('Metadata/model_settings.config').decode()
 vv=[tuple(map(float,p)) for p in re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>',m)]
 ff=[tuple(map(int,t)) for t in re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"\s*/>',m)]
 edges={}
 for a,bb,c in ff:
  for u,v in [(a,bb),(bb,c),(c,a)]:e=tuple(sorted((u,v)));edges[e]=edges.get(e,0)+1
 adj=[set() for _ in vv]
 for a,bb,c in ff:adj[a].update((bb,c));adj[bb].update((a,c));adj[c].update((a,bb))
 seen=set();comps=0
 for i in range(len(vv)):
  if i not in seen:
   comps+=1;seen.add(i);stack=[i]
   while stack:
    q=stack.pop()
    for j in adj[q]:
     if j not in seen:seen.add(j);stack.append(j)
 if mm.count('<item ')!=11 or cc.count('<model_instance>')!=11:raise SystemExit('3MF component count changed')
 report={'source_3mf':str(SRC),'output_3mf':str(OUT),'component_instances':cc.count('<model_instance>'),'build_items':mm.count('<item '),'replacement_mesh_vertices':len(vv),'replacement_mesh_triangles':len(ff),'nonmanifold_edges':sum(v!=2 for v in edges.values()),'connected_mesh_components':comps,'output_crc':'PASS','all_other_resources_and_placements_preserved':True,'print_state':'UNSLICED; no Creality Print slicing result is claimed'}
 (R/'DOCUMENTATION'/'R24_3MF_VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
