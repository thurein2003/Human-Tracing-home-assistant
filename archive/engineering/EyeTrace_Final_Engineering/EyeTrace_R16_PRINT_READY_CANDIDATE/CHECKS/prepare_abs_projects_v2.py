import zipfile,json,os
base=r'EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R16_COMPACT_SERVO\PRINT'
out=r'EyeTrace_Final_Engineering\EyeTrace_R16_PRINT_READY_CANDIDATE\PRINT'
for plate in (1,2):
 src=os.path.join(base,f'EyeTrace_R16_Plate_0{plate}_ABS_HOLD.3mf')
 dst=os.path.join(out,f'Plate_0{plate}_ABS_HOLD.3mf')
 with zipfile.ZipFile(src,'r') as zin: entries={n:zin.read(n) for n in zin.namelist()}
 d=json.loads(entries['Metadata/project_settings.config'])
 d['print_settings_id']=f'EyeTrace ABS 3W20 Tree Support — Plate {plate:02d}'
 d['first_layer_temperature']='255'; d['nozzle_temperature']=['255']; d['nozzle_temperature_initial_layer']=['255']
 d['first_layer_bed_temperature']='100'; d['hot_plate_temp']=['100']; d['hot_plate_temp_initial_layer']=['100']
 d['textured_plate_temp']=['100']; d['textured_plate_temp_initial_layer']=['100']
 d['curr_bed_type']='Textured PEI Plate'; d['support_type']='tree(auto)'; d['support_on_build_plate_only']='1'
 entries['Metadata/project_settings.config']=json.dumps(d,indent=2).encode('utf-8')
 entries['Metadata/model_settings.config']=entries['Metadata/model_settings.config'].replace(b'EyeTrace K2 ABS | 13 Parts | hardware fit pending',f'EyeTrace R16 ABS Plate {plate:02d}'.encode())
 with zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED) as zout:
  for n,data in entries.items(): zout.writestr(n,data)
 with zipfile.ZipFile(dst) as check:
  assert check.testzip() is None
  assert check.read('3D/3dmodel.model')==zipfile.ZipFile(src).read('3D/3dmodel.model')
 print(dst,os.path.getsize(dst),'model entry preserved')
