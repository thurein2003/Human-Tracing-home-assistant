import os,json,FreeCAD as A,Mesh,Part
r=os.path.join(os.path.dirname(os.path.abspath(__file__)),'final_prototype')
res={}
for name in sorted(os.listdir(os.path.join(r,'parts')))+['../single_bed.stl']:
 if not name.endswith('.stl'):continue
 path=os.path.normpath(os.path.join(r,'parts',name));m=Mesh.Mesh(path)
 res[os.path.basename(path)]={'facets':m.CountFacets,'closed':m.isSolid(),'components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'nonuniform_orientation':m.hasNonUniformOrientedFacets(),'volume_mm3':m.Volume,'z_min_mm':m.BoundBox.ZMin}
for name in sorted(os.listdir(os.path.join(r,'parts'))):
 if name.endswith('.step'):
  s=Part.read(os.path.join(r,'parts',name));res[name]={'valid':s.isValid(),'solid_count':len(s.Solids),'volume_mm3':s.Volume}
json.dump(res,open(os.path.join(r,'checks','export_audit.json'),'w'),indent=2)
print(json.dumps(res,indent=2))
