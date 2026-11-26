import zipfile, xml.etree.ElementTree as ET, struct, pathlib, json, collections
root=pathlib.Path(__file__).parent.parent
p=root/'PRINT'/'Plate02_R18_CircularMount_Correction_01.3mf'
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
z=zipfile.ZipFile(p); assert z.testzip() is None
xml=ET.fromstring(z.read('3D/3dmodel.model'))
objs={o.attrib['id']:o for o in xml.findall('.//m:resources/m:object',ns)}
items=xml.findall('.//m:build/m:item',ns); assert len(items)==12
names=[objs[i.attrib['objectid']].attrib.get('name','') for i in items]
assert len(set(names))==12
stl_results=[]
for f in sorted((root/'STL').glob('*.stl')):
    data=f.read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    if len(data)!=84+n*50: stl_results.append((f.name,n,'size-mismatch')); continue
    edges=collections.Counter()
    for j in range(n):
        vals=struct.unpack_from('<12fH',data,84+j*50); pts=[tuple(round(vals[3+a*3+k],5) for k in range(3)) for a in range(3)]
        for a,b in ((0,1),(1,2),(2,0)): edges[tuple(sorted((pts[a],pts[b])))]+=1
    bad=sum(v!=2 for v in edges.values())
    stl_results.append((f.name,n,bad))
print(json.dumps({'3mf_crc':'PASS','build_instances':len(items),'unique_names':len(set(names)),'names':names,'stl_mesh_topology':stl_results},indent=2))
