import struct,zipfile,json,xml.etree.ElementTree as ET
from pathlib import Path
r=Path(r'EyeTrace_Final_Engineering\ABS_Print_Ready')
src=Path(r'EyeTrace_Final_Engineering')
support=src/'STL'/'Supported_Print'
bed=bytearray((support/'STL'/'EyeTrace_Reoriented_13Parts_v02_UNSUPPORTED.stl').read_bytes())
n=struct.unpack_from('<I',bed,80)[0]; assert len(bed)==84+50*n
shifted={'yoke':0,'camera':0}
for i in range(n):
 o=84+50*i; ps=[struct.unpack_from('<3f',bed,o+12+j*12) for j in range(3)]
 cx=sum(p[0] for p in ps)/3; cy=sum(p[1] for p in ps)/3
 if 107.99<=cx<=225.11 and 11.99<=cy<=82.61: dx=4.; key='yoke'
 elif 102.99<=cx<=159.01 and 176.59<=cy<=208.61: dx=2.; key='camera'
 else: continue
 for j,p in enumerate(ps): struct.pack_into('<3f',bed,o+12+j*12,p[0]+dx,p[1],p[2])
 shifted[key]+=1
assert min(shifted.values())>1000,shifted
(r/'STL'/'EyeTrace_K2_ABS_SingleBed_UNSUPPORTED_REFERENCE.stl').write_bytes(bed)
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
old=src/'FIT_TESTS'/'Physical_Verification_01'/'SLICER'/'Named_Geometry_Only.3mf'
with zipfile.ZipFile(old) as zi:
 model=ET.fromstring(zi.read('3D/3dmodel.model')); objs=model.findall('.//c:resources/c:object',ns); assert len(objs)==7
 cfg=json.loads((r/'SLICER'/'EyeTrace_K2_ABS_Resolved_Settings.json').read_text())
 for k,v in {'wall_loops':'3','sparse_infill_density':'100%','sparse_infill_pattern':'rectilinear','enable_support':'0','brim_width':'5','brim_object_gap':'0.1','wall_generator':'arachne','initial_layer_speed':'20','outer_wall_speed':'30','inner_wall_speed':'45','default_acceleration':'2000','xy_hole_compensation':'0','xy_contour_compensation':'0','elefant_foot_compensation':'0'}.items():
  cfg[k]=[str(v)] if isinstance(cfg.get(k),list) else str(v)
 mc=ET.Element('config'); plate=ET.SubElement(mc,'plate')
 for k,v in [('plater_id','1'),('plater_name','EyeTrace ABS Fit Test | seven coupons'),('locked','false'),('bed_type','Textured PEI Plate'),('print_sequence','by layer')]: ET.SubElement(plate,'metadata',{'key':k,'value':v})
 for i,o in enumerate(objs,1):
  oid=o.get('id'); name=o.get('name'); co=ET.SubElement(mc,'object',{'id':oid}); ET.SubElement(co,'metadata',{'key':'name','value':name})
  for k,v in [('enable_support','0'),('extruder','1'),('brim_width','5'),('brim_object_gap','0.1'),('sparse_infill_density','100%')]: ET.SubElement(co,'metadata',{'key':k,'value':v})
  part=ET.SubElement(co,'part',{'id':oid,'subtype':'normal_part'}); ET.SubElement(part,'metadata',{'key':'name','value':name})
  inst=ET.SubElement(plate,'model_instance')
  for k,v in [('object_id',oid),('instance_id','0'),('identify_id',str(i))]: ET.SubElement(inst,'metadata',{'key':k,'value':v})
 cre=b'<config><metadata key="Company" value="Creality"/><metadata key="Application" value="Creality_Print"/><metadata key="AppVersion" value="7.3.1.6378"/></config>'
 target=r/'FIT_TESTS'/'Creality_Print'/'EyeTrace_ABS_FitTest_Project.3mf'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,6) as zo:
  for name in zi.namelist(): zo.writestr(name,zi.read(name))
  zo.writestr('Metadata/model_settings.config',ET.tostring(mc,encoding='utf-8',xml_declaration=True))
  zo.writestr('Metadata/project_settings.config',json.dumps(cfg,indent=2,sort_keys=True).encode())
  zo.writestr('Metadata/creality.config',cre)
report={'STL_facets':n,'shifted_facets':shifted,'projects':['Creality_Print/EyeTrace_K2_ABS_Supported_Project.3mf','FIT_TESTS/Creality_Print/EyeTrace_ABS_FitTest_Project.3mf'],'source_geometry_scaled':False,'fit_coupon_objects':len(objs)}
(r/'CHECKS'/'prepared_project.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
