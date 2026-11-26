import zipfile,xml.etree.ElementTree as ET,json,hashlib
from pathlib import Path
root=Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate\PRINT')
files=[root/'Plate02_R21_SingleMountPlate_UNSLICED.3mf',root/'Plate02_R21_SingleMountPlate_SLICED_HOLD.3mf']
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def model(path):
 with zipfile.ZipFile(path) as z:
  bad=z.testzip()
  candidates=[n for n in z.namelist() if n.startswith('3D/Objects/') and n.endswith('.model')]
  found=None
  for name in candidates:
   tree=ET.fromstring(z.read(name)); obj=tree.find('.//c:object[@id="7"]/c:mesh',ns)
   if obj is not None: found=(name,obj);break
  if not found:raise RuntimeError(f'cover object id7 missing: {path}')
  name,m=found
  vs=[(float(v.attrib['x']),float(v.attrib['y']),float(v.attrib['z'])) for v in m.find('c:vertices',ns)]
  fs=[(int(t.attrib['v1']),int(t.attrib['v2']),int(t.attrib['v3'])) for t in m.find('c:triangles',ns)]
  edges={}
  for a,b,c in fs:
   for u,v in [(a,b),(b,c),(c,a)]:
    e=tuple(sorted((u,v)));edges[e]=edges.get(e,0)+1
  badedges=sum(1 for n in edges.values() if n!=2)
  # graph connected-components by shared triangle vertices
  adj=[set() for _ in vs]
  for a,b,c in fs:
   adj[a].update((b,c));adj[b].update((a,c));adj[c].update((a,b))
  seen=set();cc=0
  for i in range(len(vs)):
   if i not in seen:
    cc+=1;stack=[i];seen.add(i)
    while stack:
     j=stack.pop()
     for k in adj[j]:
      if k not in seen:seen.add(k);stack.append(k)
  bbox=[[min(p[i] for p in vs),max(p[i] for p in vs)] for i in range(3)]
  s=z.read('Metadata/model_settings.config').decode()
  instances=s.count('<model_instance>')
  return {'file':str(path),'crc':bad or 'PASS','mesh_path':name,'vertices':len(vs),'triangles':len(fs),'bbox_local':bbox,'nonmanifold_edges':badedges,'connected_components':cc,'instances':instances,'mesh_sha256':hashlib.sha256(json.dumps([vs,fs],separators=(',',':')).encode()).hexdigest(),'mesh':(vs,fs)}
a=model(files[0]);b=model(files[1]); same=a['mesh_sha256']==b['mesh_sha256']
out={'unsliced':{k:v for k,v in a.items() if k!='mesh'},'sliced':{k:v for k,v in b.items() if k!='mesh'},'replacement_mesh_identical_after_slicing':same}
(Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate\DOCUMENTATION')/'3MF_REOPEN_MESH_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
