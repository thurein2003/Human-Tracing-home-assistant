import pathlib,zipfile,xml.etree.ElementTree as ET,struct,shutil,json,collections
root=pathlib.Path(__file__).parent.parent
src=root/'BACKUP'/'Plate02_R18_CircularMount_Correction_01.3mf'
out=root/'PRINT'/'Plate02_R19_ThinMountPlate.3mf'
srcstls=root.parent/'EyeTrace_R18_CircularMount_Correction_01'/'STL'
# Copy all unchanged print components from R18, substituting only the redesigned pan yoke.
for f in srcstls.glob('*.stl'):
    if 'PanYoke_CircularMount_R18C1' in f.name: continue
    shutil.copy2(f,root/'STL'/f.name)
# Read the binary STL to reuse its exact triangulated print-space geometry.
stl=(root/'STL'/'PanYoke_R19_ThinMountPlate.stl').read_bytes(); n=struct.unpack_from('<I',stl,80)[0]
if len(stl)!=84+n*50: raise SystemExit('STL binary size mismatch')
verts=[]; tris=[]
for j in range(n):
    a=struct.unpack_from('<12fH',stl,84+j*50)
    ids=[]
    for k in range(3):
        ids.append(len(verts)); verts.append((a[3+k*3],a[4+k*3],a[5+k*3]))
    tris.append(tuple(ids))
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',ns); q=lambda t:'{%s}%s'%(ns,t)
with zipfile.ZipFile(src,'r') as zin:
    payload={name:zin.read(name) for name in zin.namelist()}
model=ET.fromstring(payload['3D/3dmodel.model'])
objs={o.attrib['id']:o for o in model.findall('.//'+q('resources')+'/'+q('object'))}
obj=objs['3']; mesh=obj.find(q('mesh'))
for child in list(mesh): mesh.remove(child)
vnode=ET.SubElement(mesh,q('vertices'))
for x,y,z in verts: ET.SubElement(vnode,q('vertex'),{'x':format(x,'.8g'),'y':format(y,'.8g'),'z':format(z,'.8g')})
tnode=ET.SubElement(mesh,q('triangles'))
for v1,v2,v3 in tris: ET.SubElement(tnode,q('triangle'),{'v1':str(v1),'v2':str(v2),'v3':str(v3)})
for m in model.findall('.//'+q('metadata')):
    if m.attrib.get('name')=='Title': m.text='EyeTrace R19 Thin Mount Plate - HOLD'
    if m.attrib.get('name')=='Description': m.text='Plate 02 candidate with 2.5 mm thin pan mounting web, exact R15 horn floor backing, local mounting pads and outer support land. Unsliced; fit/assembly and slicer validation pending.'
payload['3D/3dmodel.model']=ET.tostring(model,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as zout:
    for name,data in payload.items(): zout.writestr(name,data)
# Integrity, component-instance and bed bounds validation from exact exported 3MF.
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    mo=ET.fromstring(z.read('3D/3dmodel.model'))
    oo={o.attrib['id']:o for o in mo.findall('.//'+q('resources')+'/'+q('object'))}
    items=mo.findall('.//'+q('build')+'/'+q('item'))
    names=[oo[i.attrib['objectid']].attrib.get('name','') for i in items]
    assert len(items)==12 and len(set(names))==12,(len(items),names)
    m=oo['3'].find(q('mesh')); vv=m.findall(q('vertices')+'/'+q('vertex'))
    bb=[[min(float(v.attrib[c]) for v in vv),max(float(v.attrib[c]) for v in vv)] for c in 'xyz']
    assert bb[2][0]>=-0.001 and bb[2][1]<=260.001
report={'3mf_crc':'PASS','build_instances':len(items),'unique_parts':len(set(names)),'parts':names,'replacement_yoke_bounds_xyz_mm':bb,'yoke_triangles':len(tris),'layout_coordinates_preserved':'mesh is in same bed-coordinate frame as source R18 object id 3; unchanged 11 object meshes/build instances retained','3mf_path':str(out)}
(root/'DOCUMENTATION'/'r19_package_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

