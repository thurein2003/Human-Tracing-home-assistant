import struct,zipfile,re,json,hashlib
from pathlib import Path
R=Path(r'EyeTrace_Final_Engineering\EyeTrace_R24_PanYoke_OneLayer'); S=R/'STL'/'PanYoke_R24_OneLayer.stl'; Z=R/'PRINT'/'Plate02_R24_PanYoke_OneLayer_UNSLICED.3mf'; SRC=Path(r'EyeTrace_Final_Engineering\EyeTrace_R23_UnifiedBottomBlock\PRINT\Plate02_R23_UnifiedBottomBlock_IMPORTFIX_UNSLICED.3mf')
b=S.read_bytes(); n=struct.unpack_from('<I',b,80)[0]; expected=[]; verts=[]; faces=[]; idx={}; edgecounts={}; bbox=[[float('inf'),float('-inf')] for _ in range(3)]
for i in range(n):
 d=struct.unpack_from('<12fH',b,84+i*50); tri=[]
 for k in range(3):
  p=tuple(round(float(d[3+3*k+j]),4) for j in range(3)); expected.append((p[0]-64.1,p[1]-48.3,p[2]-33.9))
  for j,v in enumerate(p):bbox[j][0]=min(bbox[j][0],v);bbox[j][1]=max(bbox[j][1],v)
  if p not in idx:idx[p]=len(verts);verts.append(p)
  tri.append(idx[p])
 faces.append(tuple(tri))
 for u,v in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:e=tuple(sorted((u,v)));edgecounts[e]=edgecounts.get(e,0)+1
nonman=sum(c!=2 for c in edgecounts.values()); adj=[set() for _ in verts]
for a,c,d in faces:adj[a].update((c,d));adj[c].update((a,d));adj[d].update((a,c))
seen=set(); comps=0
for i in range(len(verts)):
 if i not in seen:
  comps+=1;seen.add(i);stack=[i]
  while stack:
   q=stack.pop()
   for j in adj[q]:
    if j not in seen:seen.add(j);stack.append(j)
with zipfile.ZipFile(SRC) as a,zipfile.ZipFile(Z) as z:
 if z.testzip():raise SystemExit('3MF CRC failure')
 m=z.read('3D/Objects/object_2.model').decode(); vv=[tuple(map(float,x)) for x in re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>',m)]; ff=[tuple(map(int,x)) for x in re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"\s*/>',m)]
 if len(ff)!=n:raise SystemExit('3MF triangle count differs from STL')
 maxerr=0.0
 for ti,face in enumerate(ff):
  for corner,vi in enumerate(face):
   got=vv[vi]; exp=expected[ti*3+corner]; maxerr=max(maxerr,max(abs(got[j]-exp[j]) for j in range(3)))
 if maxerr>0.0001:raise SystemExit(f'STL/3MF transformed coordinate delta too large: {maxerr}')
 main=z.read('3D/3dmodel.model').decode(); cfg=z.read('Metadata/model_settings.config').decode(); changed=[]
 for nm in a.namelist():
  if nm not in z.namelist():changed.append(nm);continue
  if nm in ('3D/Objects/object_2.model','3D/3dmodel.model'):continue
  if hashlib.sha256(a.read(nm)).digest()!=hashlib.sha256(z.read(nm)).digest():changed.append(nm)
 report={'stl_path':str(S),'stl_facets':n,'unique_vertices':len(verts),'nonmanifold_edges':nonman,'connected_components':comps,'bed_bbox_mm':bbox,'3mf_path':str(Z),'crc':'PASS','build_items':main.count('<item '),'stl_3mf_triangles_same_order':True,'maximum_coordinate_delta_mm':maxerr,'other_3mf_archive_resources_modified':changed,'replacement_scope':'PanYoke mesh only'}
 if nonman or comps!=1 or changed or main.count('<item ')!=11 or cfg.count('<model_instance>')!=11:raise SystemExit(json.dumps(report,indent=2))
 (R/'DOCUMENTATION'/'R24_INDEPENDENT_EXPORT_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))

