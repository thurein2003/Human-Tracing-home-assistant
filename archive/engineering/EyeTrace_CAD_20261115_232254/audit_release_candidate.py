import os,json,FreeCAD as A,Mesh,Part
r=os.path.join(os.path.dirname(os.path.abspath(__file__)),'release_candidate')
res={}
for name in sorted(os.listdir(os.path.join(r,'parts')))+['../single_bed.stl']:
 if not name.endswith('.stl'):continue
 path=os.path.normpath(os.path.join(r,'parts',name));m=Mesh.Mesh(path)
 res[os.path.basename(path)]={'facets':m.CountFacets,'closed':m.isSolid(),'components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'nonuniform_orientation':m.hasNonUniformOrientedFacets(),'volume_mm3':m.Volume,'z_min_mm':m.BoundBox.ZMin}
for name in sorted(os.listdir(os.path.join(r,'parts'))):
 if name.endswith('.step'):
  s=Part.read(os.path.join(r,'parts',name));res[name]={'valid':s.isValid(),'solid_count':len(s.Solids),'volume_mm3':s.Volume}
doc=A.openDocument(os.path.join(r,'EyeTrace.FCStd'))
print_names=['Base','PanServoRetainer','TiltServoRetainer','PanYoke','TiltCameraCradle','PanHornClamp','TiltHornClamp']
clashes=[]
for hn in ['PanServo_ASSUMED','TiltServo_ASSUMED','PanStarHorn_ASSUMED','TiltStarHorn_ASSUMED']:
 for pn in print_names:
  vol=doc.getObject(hn).Shape.common(doc.getObject(pn).Shape).Volume
  if vol>0.001:clashes.append({'hardware':hn,'printed':pn,'volume_mm3':vol})
res['neutral_hardware_envelopes']={'tested_pairs':28,'positive_volume_intersections':clashes,'limitation':'simplified case and horn envelopes only; no spline mating validation'} 
json.dump(res,open(os.path.join(r,'checks','export_audit.json'),'w'),indent=2)
print(json.dumps(res,indent=2))

