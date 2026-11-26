import FreeCAD as A,Part,MeshPart,Mesh,zipfile,json,xml.etree.ElementTree as E
from FreeCAD import Vector as V
from pathlib import Path
r=Path(r'EyeTrace_Final_Engineering\ABS_Print_Ready')
src=Path(r'EyeTrace_Final_Engineering\FIT_TESTS\Physical_Verification_01')
d=A.openDocument(str(src/'CAD'/'Physical_Verification_Optimized.FCStd'))
obs=[o for o in d.Objects if hasattr(o,'SourceCoupon')]
targets={'01 SG90 Body Ears':(168,96),'02 StarHorn Positive Pocket':(12,96),'03 StarHorn Captive Cover':(66,96),'04 Camera 21x16':(120,96),'05 Pan Male OD64':(105,12),'06 Pan Female Tilt Bore':(12,12),'07 Tilt Sleeve':(204,96)}
shapes=[]; trans={}
for o in obs:
 s=o.Shape.copy(); dx=targets[o.Label][0]-s.BoundBox.XMin; dy=targets[o.Label][1]-s.BoundBox.YMin
 s.translate(V(dx,dy,0)); shapes.append(s); trans[o.Label]=[dx,dy,0]
m=MeshPart.meshFromShape(Shape=Part.makeCompound(shapes),LinearDeflection=.05,AngularDeflection=.1,Relative=False)
assert m.isSolid() and not m.hasNonManifolds() and not m.hasSelfIntersections()
m.write(str(r/'FIT_TESTS'/'STL'/'EyeTrace_ABS_FitTests_SevenCoupons_v5.stl'))
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
p=r/'FIT_TESTS'/'Creality_Print'/'EyeTrace_ABS_FitTest_Project_v3.3mf'
with zipfile.ZipFile(p) as z: files={n:z.read(n) for n in z.namelist()}
model=E.fromstring(files['3D/3dmodel.model'])
items={o.get('name'):o for o in model.findall('.//c:resources/c:object',ns) if o.find('c:mesh',ns)is not None}
assert len(items)==7
for name,obj in items.items():
 verts=obj.findall('c:mesh/c:vertices/c:vertex',ns); minx=min(float(v.get('x')) for v in verts); miny=min(float(v.get('y')) for v in verts)
 dx=targets[name][0]-minx; dy=targets[name][1]-miny
 for v in verts: v.set('x',format(float(v.get('x'))+dx,'.10g')); v.set('y',format(float(v.get('y'))+dy,'.10g'))
E.register_namespace('',ns['c']); files['3D/3dmodel.model']=E.tostring(model,encoding='utf-8',xml_declaration=True)
q=r/'FIT_TESTS'/'Creality_Print'/'EyeTrace_ABS_FitTest_Project_v5.3mf'; tmp=q.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,6) as z:
 for n,b in files.items(): z.writestr(n,b)
tmp.rename(q)
print(json.dumps({'solids':len(obs),'facets':len(m.Facets),'bounds':[m.BoundBox.XMin,m.BoundBox.YMin,m.BoundBox.XMax,m.BoundBox.YMax],'translations':trans},indent=2))
