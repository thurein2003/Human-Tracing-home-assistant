import FreeCAD as A, FreeCADGui as G, Part, MeshPart, Mesh, json, os, zipfile, xml.etree.ElementTree as ET, traceback, shutil
from FreeCAD import Vector as V
ROOT=r'EyeTrace_Final_Engineering'; OUT=os.path.join(ROOT,'Camera_21x14_Correction_01')
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',NS)
def tag(x): return '{%s}%s'%(NS,x)
def mesh_data(shape):
    m=MeshPart.meshFromShape(Shape=shape,LinearDeflection=0.08,AngularDeflection=0.12,Relative=False)
    pts,faces=m.Topology
    return [(float(v.x),float(v.y),float(v.z)) for v in pts], [tuple(int(i) for i in face) for face in faces]
def set_mesh(obj,verts,faces):
    for c in list(obj): obj.remove(c)
    mesh=ET.SubElement(obj,tag('mesh')); vs=ET.SubElement(mesh,tag('vertices'))
    for x,y,z in verts: ET.SubElement(vs,tag('vertex'),{'x':'%.9g'%x,'y':'%.9g'%y,'z':'%.9g'%z})
    fs=ET.SubElement(mesh,tag('triangles'))
    for a,b,c in faces: ET.SubElement(fs,tag('triangle'),{'v1':str(a),'v2':str(b),'v3':str(c)})
def patch_archive(src,dst,changes):
    with zipfile.ZipFile(src,'r') as zin, zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=changes.get(item.filename,zin.read(item.filename))
            zout.writestr(item,data)
def main():
    # Correct camera plate mesh in the existing full-bed Creality project, retaining the other 12 meshes/settings.
    doc=A.openDocument(os.path.join(OUT,'CAD','K2_PrintLayout_21x14.FCStd'))
    bo=doc.getObject('CameraPlate_21x16'); shape=bo.Shape.copy(); shape.translate(V(45,16,0)); verts,faces=mesh_data(shape)
    src=os.path.join(ROOT,'ABS_Print_Ready','Creality_Print','EyeTrace_K2_ABS_Supported_Project_v2.3mf')
    dst=os.path.join(OUT,'Creality_Print','EyeTrace_K2_ABS_Full_21x14.3mf')
    with zipfile.ZipFile(src) as z: model=ET.fromstring(z.read('3D/3dmodel.model')); ms=ET.fromstring(z.read('Metadata/model_settings.config')); ps=z.read('Metadata/project_settings.config').decode('utf8','ignore')
    objs=model.findall('.//'+tag('resources')+'/'+tag('object'))
    plate=[o for o in objs if o.attrib.get('id')=='13'][0]; plate.attrib['name']='CameraPlate_21x14'; set_mesh(plate,verts,faces)
    for o in objs:
        if o.attrib.get('id')=='113': o.attrib['name']='CameraPlate_21x14'
    for n in ms.iter():
        for k,v in list(n.attrib.items()):
            if '21x16' in v: n.attrib[k]=v.replace('21x16','21x14')
    ps=ps.replace('21x16','21x14')
    changes={'3D/3dmodel.model':ET.tostring(model,encoding='utf-8',xml_declaration=True),'Metadata/model_settings.config':ET.tostring(ms,encoding='utf-8',xml_declaration=True),'Metadata/project_settings.config':ps.encode('utf8')}
    patch_archive(src,dst,changes)
    # Make a one-part corrected camera coupon project by retaining only coupon 4 from the seven-test project.
    csrc=os.path.join(ROOT,'ABS_Print_Ready','FIT_TESTS','Creality_Print','EyeTrace_ABS_FitTest_Project_v5.3mf')
    cdst=os.path.join(OUT,'FIT_TESTS','Camera_21x14_ABS_FitTest.3mf')
    coupon=Mesh.Mesh(os.path.join(OUT,'FIT_TESTS','Camera_Hole_Pattern_21x14_ABS.stl'))
    coupon.translate(135,108.5,0); cverts, cfaces=coupon.Topology
    cverts=[(float(v.x),float(v.y),float(v.z)) for v in cverts]; cfaces=[tuple(int(i) for i in f) for f in cfaces]
    with zipfile.ZipFile(csrc) as z: cm=ET.fromstring(z.read('3D/3dmodel.model')); cms=ET.fromstring(z.read('Metadata/model_settings.config')); cps=z.read('Metadata/project_settings.config').decode('utf8','ignore')
    cres=cm.find(tag('resources'))
    for o in list(cres):
        if o.attrib.get('id')!='4': cres.remove(o)
    cplate=cres.find(tag('object')); cplate.attrib['name']='Camera hole-pattern coupon 21x14'; set_mesh(cplate,cverts,cfaces)
    build=cm.find(tag('build'))
    for it in list(build):
        if it.attrib.get('objectid')!='4': build.remove(it)
    for e in list(cms):
        if e.tag=='plate':
            for inst in list(e):
                if inst.tag=='model_instance':
                    vals={x.attrib.get('key'):x.attrib.get('value') for x in list(inst)}
                    if vals.get('object_id')!='4': e.remove(inst)
                if e.tag=='plate' and e.tag=='plate':
                    for md in list(e):
                        if md.attrib.get('key')=='plater_name': md.attrib['value']='EyeTrace ABS camera pattern coupon 21x14'
        elif e.tag=='object' and e.attrib.get('id')!='4': cms.remove(e)
        elif e.tag=='object' and e.attrib.get('id')=='4':
            for md in e.iter():
                if md.attrib.get('key')=='name': md.attrib['value']='Camera hole-pattern coupon 21x14'
                if md.attrib.get('value') and '21x16' in md.attrib['value']: md.attrib['value']=md.attrib['value'].replace('21x16','21x14')
    cps=cps.replace('21x16','21x14')
    cchanges={'3D/3dmodel.model':ET.tostring(cm,encoding='utf-8',xml_declaration=True),'Metadata/model_settings.config':ET.tostring(cms,encoding='utf-8',xml_declaration=True),'Metadata/project_settings.config':cps.encode('utf8')}
    patch_archive(csrc,cdst,cchanges)
    # Structural checks on the two ZIP-contained 3MF projects.
    qa={}
    for p,nobj in [(dst,13),(cdst,1)]:
        with zipfile.ZipFile(p) as z:
            model=ET.fromstring(z.read('3D/3dmodel.model'))
            resource=model.find(tag('resources')); meshes=[o for o in resource.findall(tag('object')) if o.find(tag('mesh')) is not None]
            items=model.findall('.//'+tag('build')+'/'+tag('item'))
            qa[os.path.basename(p)]={'zip_test':z.testzip(),'mesh_objects':len(meshes),'build_items':len(items),'bytes':os.path.getsize(p)}
            assert z.testzip() is None and len(meshes)==nobj and len(items)==nobj,(p,len(meshes),len(items))
    with open(os.path.join(OUT,'CHECKS','3mf_project_validation.json'),'w') as f: json.dump(qa,f,indent=2)
    print(json.dumps(qa,indent=2))
    A.closeDocument(doc.Name)
try: main()
except Exception:
    with open(os.path.join(OUT,'CHECKS','project_packaging_error.txt'),'w') as f:f.write(traceback.format_exc())
    raise
finally:
    for n in list(A.listDocuments()): A.closeDocument(n)


