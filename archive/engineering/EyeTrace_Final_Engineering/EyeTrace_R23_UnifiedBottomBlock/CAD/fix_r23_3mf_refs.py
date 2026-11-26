import zipfile,json,re
from pathlib import Path
R=Path(r'EyeTrace_Final_Engineering\EyeTrace_R23_UnifiedBottomBlock')
SRC=R/'PRINT'/'Plate02_R23_UnifiedBottomBlock_UNSLICED.3mf'; OUT=R/'PRINT'/'Plate02_R23_UnifiedBottomBlock_IMPORTFIX_UNSLICED.3mf'
with zipfile.ZipFile(SRC) as zi:
 rel=zi.read('3D/_rels/3dmodel.model.rels').decode()
 rel=re.sub(r'\s*<Relationship Target="/3D/Objects/object_1.model"[^>]*/>','',rel)
 plate=json.loads(zi.read('Metadata/plate_1.json'))
 plate['bbox_objects']=[o for o in plate['bbox_objects'] if o.get('name')!='Pan_Replaceable_ThrustRing']
 for o in plate['bbox_objects']:
  if o.get('name')=='PanYoke_EarBracket_KeyedDrive':o['name']='PanYoke_UnifiedBottomBlock_R23'
 plate['bbox_all']=[min(o['bbox'][0] for o in plate['bbox_objects']),min(o['bbox'][1] for o in plate['bbox_objects']),max(o['bbox'][2] for o in plate['bbox_objects']),max(o['bbox'][3] for o in plate['bbox_objects'])]
 with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zo:
  for n in zi.namelist():
   if n=='3D/_rels/3dmodel.model.rels':data=rel.encode()
   elif n=='Metadata/plate_1.json':data=json.dumps(plate,separators=(',',':')).encode()
   else:data=zi.read(n)
   zo.writestr(n,data)
with zipfile.ZipFile(OUT) as z:
 if z.testzip():raise RuntimeError('CRC invalid')
 rel=z.read('3D/_rels/3dmodel.model.rels').decode();model=z.read('3D/3dmodel.model').decode(); cfg=z.read('Metadata/model_settings.config').decode()
 if 'object_1.model' in rel or 'Pan_Replaceable_ThrustRing' in z.read('Metadata/plate_1.json').decode():raise RuntimeError('Stale ring metadata/reference')
 if model.count('<item ' )!=11 or cfg.count('<model_instance>')!=11:raise RuntimeError('Wrong counts')
 print(json.dumps({'file':str(OUT),'crc':'PASS','instances':cfg.count('<model_instance>'),'build_items':model.count('<item '),'object_resource_relationships':rel.count('<Relationship Target="/3D/Objects/'),'stale_ring_references':'none'},indent=2))
