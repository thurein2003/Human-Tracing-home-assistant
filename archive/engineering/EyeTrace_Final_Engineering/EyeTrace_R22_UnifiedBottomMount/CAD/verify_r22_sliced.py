import zipfile,re,json,hashlib,math
from pathlib import Path
root=Path(r'EyeTrace_Final_Engineering\EyeTrace_R22_UnifiedBottomMount')
files=[root/'PRINT'/'Plate02_R22_UnifiedBottomMount_UNSLICED.3mf',root/'PRINT'/'Plate02_R22_UnifiedBottomMount_SLICED_HOLD.3mf']
def inspect(p):
 with zipfile.ZipFile(p) as z:
  bad=z.testzip();cfg=z.read('Metadata/model_settings.config').decode(); rows=[]
  for n in z.namelist():
   if n.startswith('3D/Objects/') and n.endswith('.model'):
    t=z.read(n).decode(errors='ignore'); verts=re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>',t); tris=re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"\s*/>',t)
    if verts: rows.append({'name':n,'v':len(verts),'t':len(tris),'hash':hashlib.sha256((str(verts)+str(tris)).encode()).hexdigest(),'bbox':[[min(float(v[k]) for v in verts),max(float(v[k]) for v in verts)] for k in range(3)]})
  return {'file':str(p),'crc':'PASS' if bad is None else bad,'instances':cfg.count('<model_instance>'),'mesh_count':len(rows),'meshes':rows}
a,b=map(inspect,files);out={'unsliced':a,'sliced':b,'sliced_profile_estimate':'83.53 g, 9 h 31 min (Creality Print preview)','slicer_warning':'Pan_KeyedHorn_Cover floating cantilever warning; requires support/reorientation review'}
(root/'DOCUMENTATION'/'R22_SLICED_3MF_REOPEN_CHECK.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
