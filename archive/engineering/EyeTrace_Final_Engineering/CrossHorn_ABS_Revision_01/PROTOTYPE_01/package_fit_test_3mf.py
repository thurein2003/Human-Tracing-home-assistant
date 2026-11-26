import json, struct, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

root=Path(r"EyeTrace_Final_Engineering")
out=root/"CrossHorn_ABS_Revision_01"/"PROTOTYPE_01"
template=root/"Camera_21x14_Correction_01"/"FIT_TESTS"/"Camera_21x14_ABS_FitTest.3mf"
stl=out/"CrossHorn_ABS_Clearance_Coupons_01.stl"
target=out/"Creality_Print_CrossHorn_ABS_FitTest_01.3mf"
ns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
ET.register_namespace("",ns); tag=lambda s:"{%s}%s"%(ns,s)
data=stl.read_bytes(); n=struct.unpack_from("<I",data,80)[0]; off=84
verts=[]; faces=[]; lut={}
def vid(v):
    v=tuple(round(float(x),6) for x in v)
    if v not in lut: lut[v]=len(verts); verts.append(v)
    return lut[v]
for _ in range(n):
    tri=[struct.unpack_from("<3f",data,off+12+12*j) for j in range(3)]; off+=50
    faces.append(tuple(vid(v) for v in tri))
with zipfile.ZipFile(template) as z:
    model=ET.fromstring(z.read("3D/3dmodel.model"))
    settings=json.loads(z.read("Metadata/project_settings.config"))
    model_settings=ET.fromstring(z.read("Metadata/model_settings.config"))
objects=model.find(tag("resources")).findall(tag("object"))
obj=next(o for o in objects if o.attrib.get("id")=="4")
obj.attrib["name"]="Cross horn ABS pocket clearance coupons 0.10 0.20 0.30 total mm"
for c in list(obj): obj.remove(c)
mesh=ET.SubElement(obj,tag("mesh")); vs=ET.SubElement(mesh,tag("vertices"))
for x,y,z in verts: ET.SubElement(vs,tag("vertex"),{"x":"%.8g"%x,"y":"%.8g"%y,"z":"%.8g"%z})
ts=ET.SubElement(mesh,tag("triangles"))
for a,b,c in faces: ET.SubElement(ts,tag("triangle"),{"v1":str(a),"v2":str(b),"v3":str(c)})
settings["layer_height"]="0.2"; settings["wall_loops"]="4"; settings["nozzle_temperature"]=["255"]
settings["hot_plate_temp"]=["100"]; settings["brim_width"]=["4"]
settings["support_type"]="tree(auto)"; settings["enable_support"]="0"
changes={"3D/3dmodel.model":ET.tostring(model,encoding="utf-8",xml_declaration=True),"Metadata/project_settings.config":json.dumps(settings,indent=2).encode()}
for e in model_settings.iter():
    if e.attrib.get("key")=="plater_name": e.attrib["value"]="Eye Trace cross-horn ABS fit test"
    if e.attrib.get("key")=="name": e.attrib["value"]="Cross-horn clearance coupon bed"
changes["Metadata/model_settings.config"]=ET.tostring(model_settings,encoding="utf-8",xml_declaration=True)
with zipfile.ZipFile(template) as zin,zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as zout:
    for inf in zin.infolist(): zout.writestr(inf,changes.get(inf.filename,zin.read(inf.filename)))
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    check=ET.fromstring(z.read("3D/3dmodel.model"))
    meshobj=next(o for o in check.findall(".//"+tag("object")) if o.attrib.get("id")=="4")
    assert len(meshobj.find(tag("mesh")).find(tag("triangles")))==n
print(json.dumps({"file":str(target),"triangles":n,"vertices":len(verts),"valid_zip":True,"settings":{"ABS_nozzle_C":255,"ABS_bed_C":100,"layer_mm":0.2,"walls":4,"support":False,"brim_mm":4}},indent=2))
