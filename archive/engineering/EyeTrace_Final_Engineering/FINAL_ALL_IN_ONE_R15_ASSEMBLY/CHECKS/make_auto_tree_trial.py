import zipfile, xml.etree.ElementTree as ET, pathlib
src=pathlib.Path(r'EyeTrace_Final_Engineering\FINAL_ALL_IN_ONE_R15_LAYOUT_FIXED\EyeTrace_K2_ABS_All_In_One_R15_Fixed.3mf')
out=pathlib.Path(r'EyeTrace_Final_Engineering\FINAL_ALL_IN_ONE_R15_ASSEMBLY\EyeTrace_R15_ABS_AutoTree_SupportTrial.3mf')
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
changed=[]
with zipfile.ZipFile(src) as zin:
 files={n:zin.read(n) for n in zin.namelist()}
 root=ET.fromstring(files['Metadata/model_settings.config'])
 for obj in root.findall('object'):
  meta={m.get('key'):m for m in obj.findall('metadata')}
  name=meta.get('name').get('value') if meta.get('name') is not None else ''
  if name in {'Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive','TiltCradle_KeyedHorn_CameraFrame'}:
   if 'enable_support' in meta:meta['enable_support'].set('value','1')
   if 'support_type' in meta:meta['support_type'].set('value','tree(auto)')
   else:ET.SubElement(obj,'metadata',{'key':'support_type','value':'tree(auto)'})
   if 'support_style' in meta:meta['support_style'].set('value','tree_slim')
   if 'support_on_build_plate_only' in meta:meta['support_on_build_plate_only'].set('value','1')
   else:ET.SubElement(obj,'metadata',{'key':'support_on_build_plate_only','value':'1'})
   changed.append(name)
 files['Metadata/model_settings.config']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
 settings=__import__('json').loads(files['Metadata/project_settings.config'])
 settings['support_type']='tree(auto)';settings['support_on_build_plate_only']='1';settings['filament_type']=['ABS'];settings['layer_height']='0.2';settings['wall_loops']='4';settings['sparse_infill_density']='35%'
 files['Metadata/project_settings.config']=__import__('json').dumps(settings,indent=2).encode()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as zout:
 for n,b in files.items():zout.writestr(n,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 model=ET.fromstring(z.read('3D/3dmodel.model')); assert len(model.findall('.//{%s}build/{%s}item'%(ns,ns)))==13
print({'file':str(out),'support_trial_parts':changed,'archive_ok':True,'mesh_geometry_untouched':True})
