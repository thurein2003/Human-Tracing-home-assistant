"""Package the generated cross-horn coupon bed in the existing ABS K2 profile.
Run only after build_cross_horn_revision.py has emitted the coupon STL.
"""
import json, struct, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
SRC=ROOT/"FIT_TESTS"/"CrossHorn_Pocket_Clearance_Coupon_Bed.stl"
TEMPLATE=ROOT/"Creality_Print"/"EyeTrace_ABS_Circular_Clearance_Calibration.3mf"
OUT=ROOT/"Creality_Print"/"CrossHorn_Pocket_Clearance_ABS.3mf"
NS="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"; ET.register_namespace("",NS)
tag=lambda s:"{%s}%s"%(NS,s)
if not SRC.exists(): raise SystemExit("Missing generated coupon STL; fill measurements and run build_cross_horn_revision.py first")
b=SRC.read_bytes(); n=struct.unpack_from("<I",b,80)[0]
if len(b)!=84+50*n: raise SystemExit("Expected binary STL")
verts=[]; faces=[]; index={}; off=84
def vindex(v):
    v=tuple(round(float(x),6) for x in v)
    if v not in index: index[v]=len(verts);verts.append(v)
    return index[v]
for _ in range(n):
    tri=[struct.unpack_from("<3f",b,off+12+12*j) for j in range(3)]; off+=50
    faces.append(tuple(vindex(v) for v in tri))
with zipfile.ZipFile(TEMPLATE) as z:
    model=ET.fromstring(z.read("3D/3dmodel.model")); meta=ET.fromstring(z.read("Metadata/model_settings.config"))
    cfg=json.loads(z.read("Metadata/project_settings.config"))
obj=next(o for o in model.findall(".//"+tag("object")) if o.attrib.get("id")=="4")
obj.attrib["name"]="Cross-horn pocket clearance coupon bed"
for c in list(obj): obj.remove(c)
mesh=ET.SubElement(obj,tag("mesh")); vs=ET.SubElement(mesh,tag("vertices"))
for x,y,z in verts: ET.SubElement(vs,tag("vertex"),{"x":"%.8g"%x,"y":"%.8g"%y,"z":"%.8g"%z})
ts=ET.SubElement(mesh,tag("triangles"))
for a,b,c in faces: ET.SubElement(ts,tag("triangle"),{"v1":str(a),"v2":str(b),"v3":str(c)})
for e in meta.iter():
    if e.attrib.get("key")=="plater_name": e.attrib["value"]="Eye Trace cross-horn ABS fit coupon"
    if e.attrib.get("key")=="name" and e.attrib.get("value"): e.attrib["value"]="Cross-horn pocket clearance coupon"
changes={"3D/3dmodel.model":ET.tostring(model,encoding="utf-8",xml_declaration=True),
         "Metadata/model_settings.config":ET.tostring(meta,encoding="utf-8",xml_declaration=True),
         "Metadata/project_settings.config":json.dumps(cfg,indent=2).encode("utf-8")}
with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as zout:
    for inf in zin.infolist(): zout.writestr(inf,changes.get(inf.filename,zin.read(inf.filename)))
with zipfile.ZipFile(OUT) as z:
    if z.testzip() is not None: raise SystemExit("3MF archive verification failed")
    check=ET.fromstring(z.read("3D/3dmodel.model"))
    actual=len(next(o for o in check.findall(".//"+tag("object")) if o.attrib.get("id")=="4").find(tag("mesh")).find(tag("triangles")))
    if actual!=n: raise SystemExit("3MF triangle count mismatch")
print("Created",OUT,"triangles",n,"ABS layer",cfg.get("layer_height"),"supports",cfg.get("enable_support"))
