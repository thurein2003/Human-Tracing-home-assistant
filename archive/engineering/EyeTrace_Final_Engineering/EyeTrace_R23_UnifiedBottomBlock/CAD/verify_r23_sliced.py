import zipfile,re,json,hashlib
from pathlib import Path
R=Path(r'EyeTrace_Final_Engineering\EyeTrace_R23_UnifiedBottomBlock')
p=R/'PRINT'/'Plate02_R23_UnifiedBottomBlock_SLICED_HOLD.3mf'
with zipfile.ZipFile(p) as z:
 bad=z.testzip(); cfg=z.read('Metadata/model_settings.config').decode(); model=z.read('3D/3dmodel.model').decode(); rel=z.read('3D/_rels/3dmodel.model.rels').decode()
 rows=[]
 for n in z.namelist():
  if n.startswith('3D/Objects/') and n.endswith('.model'):
   t=z.read(n).decode(errors='ignore'); vs=re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/>',t); ts=re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"\s*/>',t)
   if vs: rows.append({'path':n,'vertices':len(vs),'triangles':len(ts),'hash':hashlib.sha256((str(vs)+str(ts)).encode()).hexdigest()})
 out={'file':str(p),'archive_crc':'PASS' if bad is None else bad,'model_objects':model.count('<object '),'build_items':model.count('<item '),'plate_instances':cfg.count('<model_instance>'),'mesh_resource_count':len(rows),'stale_ring_model_removed':'Pan_Replaceable_ThrustRing' not in cfg,'R23_fused_yoke_mesh':next((x for x in rows if x['triangles']>=80000),None),'mesh_inventories':rows,'slicer_preview_contains_gcode':any(n.lower().endswith('.gcode') for n in z.namelist()),'metadata_files':[n for n in z.namelist() if n.startswith('Metadata/') and ('slice' in n.lower() or 'process' in n.lower() or 'filament' in n.lower())]}
 if out['build_items']!=11 or out['plate_instances']!=11 or out['model_objects']!=11: raise RuntimeError('Incorrect object count')
 if out['archive_crc']!='PASS':raise RuntimeError('CRC failure')
 (R/'DOCUMENTATION'/'R23_SLICED_3MF_VALIDATION.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
