import json,struct,zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
root=Path(r"EyeTrace_Final_Engineering")
out=root/"CrossHorn_ABS_Revision_01"/"PROTOTYPE_02"/"CORRECTION_01"
template=root/"Camera_21x14_Correction_01"/"FIT_TESTS"/"Camera_21x14_ABS_FitTest.3mf"
stl=out/"CrossHorn_Single_FitTest_02.stl"; target=out/"CrossHorn_Single_FitTest_02.3mf"
ns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"; ET.register_namespace('',ns); tag=lambda x:'{%s}%s'%(ns,x)
b=stl.read_bytes(); n=struct.unpack_from('<I',b,80)[0]; off=84; vs=[]; fs=[]; lut={}
def vi(v):
 v=tuple(round(float(x),6) for x in v)
 if v not in lut: lut[v]=len(vs); vs.append(v)
 return lut[v]
for _ in range(n):
 t=[struct.unpack_from('<3f',b,off+12+12*j) for j in range(3)]; off+=50; fs.append(tuple(vi(x) for x in t))
with zipfile.ZipFile(template) as z:
 model=ET.fromstring(z.read('3D/3dmodel.model')); settings=json.loads(z.read('Metadata/project_settings.config')); ms=ET.fromstring(z.read('Metadata/model_settings.config'))
obj=next(o for o in model.find(tag('resources')).findall(tag('object')) if o.attrib.get('id')=='4'); obj.attrib['name']='Single cross horn correction coupon with 7.4 mm hub seat'
for x in list(obj): obj.remove(x)
m=ET.SubElement(obj,tag('mesh')); vr=ET.SubElement(m,tag('vertices'))
for x,y,z in vs: ET.SubElement(vr,tag('vertex'),{'x':str(x),'y':str(y),'z':str(z)})
fr=ET.SubElement(m,tag('triangles'))
for a,b,c in fs: ET.SubElement(fr,tag('triangle'),{'v1':str(a),'v2':str(b),'v3':str(c)})
settings.update({'layer_height':'0.2','wall_loops':'4','nozzle_temperature':['255'],'nozzle_temperature_initial_layer':['255'],'hot_plate_temp':['100'],'hot_plate_temp_initial_layer':['100'],'enable_support':'0','brim_width':['4']})
changes={'3D/3dmodel.model':ET.tostring(model,encoding='utf-8',xml_declaration=True),'Metadata/project_settings.config':json.dumps(settings,indent=2).encode()}
for e in ms.iter():
 if e.attrib.get('key')=='plater_name': e.attrib['value']='Eye Trace cross-horn correction coupon 01'
changes['Metadata/model_settings.config']=ET.tostring(ms,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(template) as zi,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as zo:
 for info in zi.infolist(): zo.writestr(info,changes.get(info.filename,zi.read(info.filename)))
with zipfile.ZipFile(target) as z: assert z.testzip() is None
print(json.dumps({'file':str(target),'triangles':n,'unique_vertices':len(vs),'zip_valid':True,'ABS':'255C nozzle / 100C bed / 0.20 mm / 4 walls / 4 mm brim / support off'},indent=2))
