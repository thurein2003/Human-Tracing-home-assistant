import zipfile,json,xml.etree.ElementTree as ET,os
base=r'EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R16_COMPACT_SERVO\PRINT'
out=r'EyeTrace_Final_Engineering\EyeTrace_R16_PRINT_READY_CANDIDATE\PRINT'
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
for plate in (1,2):
 src=os.path.join(base,f'EyeTrace_R16_Plate_0{plate}_ABS_HOLD.3mf')
 dst=os.path.join(out,f'Plate_0{plate}_ABS_HOLD.3mf')
 with zipfile.ZipFile(src,'r') as zin:
  entries={n:zin.read(n) for n in zin.namelist()}
 settings=json.loads(entries['Metadata/project_settings.config'])
 settings['print_settings_id']=f'EyeTrace ABS 3W20 Tree Support — Plate {plate:02d}'
 settings['first_layer_temperature']='255'
 settings['nozzle_temperature']=['255']
 settings['nozzle_temperature_initial_layer']=['255']
 settings['first_layer_bed_temperature']='100'
 settings['hot_plate_temp']=['100']; settings['hot_plate_temp_initial_layer']=['100']
 settings['textured_plate_temp']=['100']; settings['textured_plate_temp_initial_layer']=['100']
 settings['curr_bed_type']='Textured PEI Plate'
 settings['support_type']='tree(auto)'; settings['support_on_build_plate_only']='1'
 entries['Metadata/project_settings.config']=json.dumps(settings,indent=2).encode('utf-8')
 model=ET.fromstring(entries['3D/3dmodel.model'])
 for md in model.findall('.//m:metadata',ns):
  if md.get('name')=='Title': md.text=f'EyeTrace R16 ABS Plate {plate:02d}'
 entries['3D/3dmodel.model']=ET.tostring(model,encoding='utf-8',xml_declaration=True)
 config=ET.fromstring(entries['Metadata/model_settings.config'])
 for md in config.findall('.//metadata'):
  if md.get('key')=='plater_name': md.set('value',f'EyeTrace R16 ABS Plate {plate:02d}')
 entries['Metadata/model_settings.config']=ET.tostring(config,encoding='utf-8',xml_declaration=True)
 with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED) as zout:
  for name,data in entries.items(): zout.writestr(name,data)
 print(dst,os.path.getsize(dst))
