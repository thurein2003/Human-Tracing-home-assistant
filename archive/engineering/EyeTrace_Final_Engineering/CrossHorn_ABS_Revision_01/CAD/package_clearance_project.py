import zipfile, xml.etree.ElementTree as ET, struct, os
import json
from pathlib import Path

ROOT=Path(r"EyeTrace_Final_Engineering")
REV=ROOT/"CrossHorn_ABS_Revision_01"
TEMPLATE=ROOT/"Camera_21x14_Correction_01"/"FIT_TESTS"/"Camera_21x14_ABS_FitTest.3mf"
STL=REV/"FIT_TESTS"/"ABS_Circular_Clearance_Calibration_Bed.stl"
OUT=REV/"Creality_Print"/"EyeTrace_ABS_Circular_Clearance_Calibration.3mf"
NS="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
ET.register_namespace("",NS)
tag=lambda s:"{%s}%s"%(NS,s)
data=STL.read_bytes(); n=struct.unpack_from("<I",data,80)[0]; off=84
verts=[]; faces=[]; lookup={}
def vid(v):
    v=tuple(round(float(x),6) for x in v)
    if v not in lookup: lookup[v]=len(verts); verts.append(v)
    return lookup[v]
for _ in range(n):
    tri=[struct.unpack_from("<3f",data,off+12+12*j) for j in range(3)]; off+=50
    faces.append(tuple(vid(v) for v in tri))
with zipfile.ZipFile(TEMPLATE) as z:
    model=ET.fromstring(z.read("3D/3dmodel.model"))
    ms=ET.fromstring(z.read("Metadata/model_settings.config"))
    ps=json.loads(z.read("Metadata/project_settings.config").decode("utf-8"))
res=model.find(tag("resources")); objs=res.findall(tag("object"))
obj=next(o for o in objs if o.attrib.get("id")=="4")
obj.attrib["name"]="ABS pan and tilt clearance calibration coupons"
for c in list(obj): obj.remove(c)
mesh=ET.SubElement(obj,tag("mesh")); vs=ET.SubElement(mesh,tag("vertices"))
for x,y,z in verts: ET.SubElement(vs,tag("vertex"),{"x":"%.8g"%x,"y":"%.8g"%y,"z":"%.8g"%z})
ts=ET.SubElement(mesh,tag("triangles"))
for a,b,c in faces: ET.SubElement(ts,tag("triangle"),{"v1":str(a),"v2":str(b),"v3":str(c)})
changes={"3D/3dmodel.model":ET.tostring(model,encoding="utf-8",xml_declaration=True)}
for e in ms.iter():
    if e.attrib.get("key")=="plater_name": e.attrib["value"]="EyeTrace ABS circular clearance calibration"
    if e.attrib.get("key")=="name" and "camera" in e.attrib.get("value","").lower(): e.attrib["value"]="ABS circular clearance calibration bed"
changes["Metadata/model_settings.config"]=ET.tostring(ms,encoding="utf-8",xml_declaration=True)
ps["wall_loops"]="4"
changes["Metadata/project_settings.config"]=json.dumps(ps,indent=2).encode("utf-8")
with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as zout:
    for inf in zin.infolist(): zout.writestr(inf,changes.get(inf.filename,zin.read(inf.filename)))
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    check=ET.fromstring(z.read("3D/3dmodel.model"))
    meshobj=next(o for o in check.findall(".//"+tag("object")) if o.attrib.get("id")=="4")
    assert len(meshobj.find(tag("mesh")).find(tag("triangles")))==n
print("created",OUT,"vertices",len(verts),"triangles",len(faces),"bytes",OUT.stat().st_size)
