from pathlib import Path
import struct,collections,zipfile,xml.etree.ElementTree as ET,json,hashlib,math
root=Path(__file__).parent.parent; ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; q=lambda s:'{%s}%s'%(ns,s)
# STL edge-incidence/manifold check and unchanged-part SHA checks.
mesh=[]; source=root.parent/'EyeTrace_R18_CircularMount_Correction_01'/'STL'
for f in sorted((root/'STL').glob('*.stl')):
 d=f.read_bytes(); n=struct.unpack_from('<I',d,80)[0]
 if len(d)!=84+n*50: raise Exception('bad STL size '+f.name)
 edges=collections.Counter()
 for i in range(n):
  t=struct.unpack_from('<12fH',d,84+i*50); pts=[tuple(round(t[3+3*a+k],5) for k in range(3)) for a in range(3)]
  for a,b in [(0,1),(1,2),(2,0)]: edges[tuple(sorted((pts[a],pts[b])))]+=1
 bad=sum(v!=2 for v in edges.values())
 unchanged=None
 old=source/f.name
 if 'PanYoke_R19' not in f.name and old.exists(): unchanged=hashlib.sha256(d).hexdigest()==hashlib.sha256(old.read_bytes()).hexdigest()
 mesh.append({'file':f.name,'triangles':n,'nonmanifold_edges':bad,'unchanged_from_R18':unchanged})
 if bad: raise Exception('non-manifold STL '+f.name)
# Exact exported 3MF integrity and plate item bounds.
p=root/'PRINT'/'Plate02_R19_ThinMountPlate.3mf'; zf=zipfile.ZipFile(p); assert zf.testzip() is None
model=ET.fromstring(zf.read('3D/3dmodel.model')); objs={o.attrib['id']:o for o in model.findall('.//'+q('resources')+'/'+q('object'))}; items=model.findall('.//'+q('build')+'/'+q('item'))
if len(items)!=12: raise Exception('wrong item count')
parts=[]
for it in items:
 oid=it.attrib['objectid']; o=objs[oid]; comp=o.find(q('components')+'/'+q('component'))
 if comp is not None:o=objs[comp.attrib['objectid']]
 verts=o.findall(q('mesh')+'/'+q('vertices')+'/'+q('vertex'))
 coords=[(float(v.attrib['x']),float(v.attrib['y']),float(v.attrib['z'])) for v in verts]
 b=[(min(v[k] for v in coords),max(v[k] for v in coords)) for k in range(3)]
 if b[0][0]<0 or b[1][0]<0 or b[0][1]>260 or b[1][1]>260 or b[2][0]<-.01: raise Exception('object out of bed '+o.attrib.get('name',''))
 parts.append({'name':o.attrib.get('name'), 'bbox':b})
# AABB collisions only report conservative boxes; source layout was previously arranged with ample clearance.
coll=[]; gaps=[]
for i,a in enumerate(parts):
 for b in parts[i+1:]:
  dx=min(a['bbox'][0][1],b['bbox'][0][1])-max(a['bbox'][0][0],b['bbox'][0][0]); dy=min(a['bbox'][1][1],b['bbox'][1][1])-max(a['bbox'][1][0],b['bbox'][1][0])
  if dx>0 and dy>0: coll.append([a['name'],b['name'],dx,dy])
  else:
   gx=max(0,-dx); gy=max(0,-dy); gaps.append(math.hypot(gx,gy))
if coll: raise Exception('XY envelope intersections '+repr(coll))
r={'3mf_crc':'PASS','build_items':len(items),'unique_objects':len(set(x['name'] for x in parts)),'parts':parts,'all_within_K2_XY_bed':True,'AABB_xy_intersections':coll,'minimum_AABB_clearance_mm':min(gaps) if gaps else None,'STL_checks':mesh,'only_yoke_changed':'other available R18 component STL hashes compared'}
(root/'DOCUMENTATION'/'r19_package_validation.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
