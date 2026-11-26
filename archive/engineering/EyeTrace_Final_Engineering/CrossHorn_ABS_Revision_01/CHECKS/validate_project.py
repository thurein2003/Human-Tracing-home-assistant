import json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
root=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
p=root/"Creality_Print"/"EyeTrace_ABS_Circular_Clearance_Calibration.3mf"
ns={"c":"http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    model=ET.fromstring(z.read("3D/3dmodel.model"))
    objects=model.findall(".//c:resources/c:object",ns)
    build=model.findall(".//c:build/c:item",ns)
    meshes=[o.find("c:mesh",ns) for o in objects if o.find("c:mesh",ns) is not None]
    assert len(meshes)==1 and len(build)==1
    mesh=meshes[0]; vertices=mesh.findall("c:vertices/c:vertex",ns); tris=mesh.findall("c:triangles/c:triangle",ns)
    coords=[(float(v.attrib["x"]),float(v.attrib["y"]),float(v.attrib["z"])) for v in vertices]
    bounds=[min(v[i] for v in coords) for i in range(3)]+[max(v[i] for v in coords) for i in range(3)]
    cfg=json.loads(z.read("Metadata/project_settings.config"))
    settings=ET.fromstring(z.read("Metadata/model_settings.config"))
    md={e.attrib.get("key"):e.attrib.get("value") for e in settings.iter() if e.attrib.get("key")}
    result={"zip_integrity":"PASS","mesh_objects":len(meshes),"build_items":len(build),"vertices":len(vertices),"triangles":len(tris),
            "bounds_mm":[round(v,3) for v in bounds],"fits_260mm_bed":bounds[0]>=0 and bounds[1]>=0 and bounds[3]<=260 and bounds[4]<=260,
            "layer_height_mm":cfg.get("layer_height"),"nozzle_C":cfg.get("nozzle_temperature_initial_layer"),"bed_C":cfg.get("hot_plate_temp_initial_layer"),
            "wall_loops":cfg.get("wall_loops"),"infill":cfg.get("sparse_infill_density"),"supports":cfg.get("enable_support"),
            "brim_type":cfg.get("brim_type"),"brim_mm":md.get("brim_width"),"toolpath_sliced":False}
    assert result["fits_260mm_bed"] and result["layer_height_mm"]=="0.2" and result["wall_loops"]=="4" and result["supports"]=="0"
(root/"CHECKS"/"creality_project_validation.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
