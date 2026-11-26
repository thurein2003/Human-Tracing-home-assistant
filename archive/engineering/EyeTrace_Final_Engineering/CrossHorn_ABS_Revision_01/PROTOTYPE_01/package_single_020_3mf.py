import json,struct,zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
root=Path(r"EyeTrace_Final_Engineering")
out=root/"CrossHorn_ABS_Revision_01"/"PROTOTYPE_01"
template=root/"Camera_21x14_Correction_01"/"FIT_TESTS"/"Camera_21x14_ABS_FitTest.3mf"
stl=out/"CrossHorn_Single_FitTest_020.stl"; target=out/"CrossHorn_Single_FitTest_020.3mf"
ns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"; ET.register_namespace("",ns); tag=lambda s:"{%s}%s"%(ns,s)
b=stl.read_bytes(); count=struct.unpack_from('<I',b,80)[0]; off=84; verts=[]; faces=[]; idx={}
def vid(v):
    v=tuple(round(float(x),6) for x in v)
    if v not in idx: idx[v]=len(verts); verts.append(v)
    return idx[v]
for _ in range(count):
    tri=[struct.unpack_from('<3f',b,off+12+12*j) for j in range(3)]; off+=50; faces.append(tuple(vid(v) for v in tri))
with zipfile.ZipFile(template) as z:
    model=ET.fromstring(z.read('3D/3dmodel.model')); settings=json.loads(z.read('Metadata/project_settings.config')); ms=ET.fromstring(z.read('Metadata/model_settings.config'))
obj=next(o for o in model.find(tag('resources')).findall(tag('object')) if o.attrib.get('id')=='4'); obj.attrib['name']='CrossHorn Single FitTest 020 - 0.20 mm total lateral clearance'
for child in list(obj): obj.remove(child)
mesh=ET.SubElement(obj,tag('mesh')); vs=ET.SubElement(mesh,tag('vertices'))
for x,y,z in verts: ET.SubElement(vs,tag('vertex'),{'x':str(x),'y':str(y),'z':str(z)})
ts=ET.SubElement(mesh,tag('triangles'))
for a,c,d in faces: ET.SubElement(ts,tag('triangle'),{'v1':str(a),'v2':str(c),'v3':str(d)})
settings.update({'layer_height':'0.2','wall_loops':'4','nozzle_temperature':['255'],'nozzle_temperature_initial_layer':['255'],'hot_plate_temp':['100'],'hot_plate_temp_initial_layer':['100'],'enable_support':'0','support_type':'tree(auto)','brim_width':['4']})
changes={'3D/3dmodel.model':ET.tostring(model,encoding='utf-8',xml_declaration=True),'Metadata/project_settings.config':json.dumps(settings,indent=2).encode()}
for e in ms.iter():
    if e.attrib.get('key')=='plater_name': e.attrib['value']='Eye Trace single cross-horn ABS fit test 020'
    if e.attrib.get('key')=='name': e.attrib['value']='Single 0.20 mm clearance coupon'
changes['Metadata/model_settings.config']=ET.tostring(ms,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(template) as zin,zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist(): zout.writestr(info,changes.get(info.filename,zin.read(info.filename)))
with zipfile.ZipFile(target) as z: assert z.testzip() is None
print(json.dumps({'file':str(target),'triangles':count,'vertices':len(verts),'zip_valid':True,'bed_bbox_mm':[43,27,4.35],'supports':False},indent=2))
