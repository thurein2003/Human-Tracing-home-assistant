from pathlib import Path
import json,csv,math
import FreeCAD as A,Part,MeshPart,Mesh
from FreeCAD import Vector as V
r=Path(__file__).resolve().parent;old=r.parent;doc=A.openDocument(str(old/'FitTests.FCStd'));objects={o.Name:o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};assert len(objects)==7
specs=[('SG90_EarMount_Coupon','01_SG90_Body_Ears',(20,96)),('StarHorn_PositivePocket_Coupon','02_StarHorn_Positive_Pocket',(29,29)),('StarHorn_CaptiveCover_Coupon','03_StarHorn_Captive_Cover',(121,29)),('Camera_21x16_HoleCenter_Gauge','04_Camera_21x16',(120,96)),('PanJournal_Male_SizeTest','05_Pan_Male_OD64',(110,18)),('PanJournal_Female_ClearanceTest','06_Pan_Female_Tilt_Bore',(14.7,14.7)),('Tilt_Journal_FlangedSleeve','07_Tilt_Sleeve',(90,96))]
new=A.newDocument('EyeTrace_Physical_Verification');items=[];audit=[]
for source,name,(px,py) in specs:
 o=objects[source];s=o.Shape.copy();b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));orig=s.copy()
 if name.startswith('06'):
  # A bore gauge tab only. The original full-diameter pan ring is preserved exactly.
  s=s.fuse(Part.makeBox(12,12,2.5,V(69,29.3,0))).cut(Part.makeCylinder(2.6,4,V(75,35.3,-.5))).removeSplitter()
  assert orig.cut(s).Volume<1e-6
  assert s.cut(orig).common(Part.makeCylinder(32.3,4,V(35.3,35.3,-.5))).Volume<1e-6
  cylinders=[f for f in s.Faces if type(f.Surface).__name__=='Cylinder' and abs(f.Surface.Radius-2.6)<1e-6];assert cylinders
  for f in cylinders:assert abs(f.BoundBox.ZLength-2.5)<1e-6
 else:assert orig.cut(s).Volume+s.cut(orig).Volume<1e-6
 assert s.isValid() and len(s.Solids)==1
 # Save native in the actual printer orientation, individual STL independently reopened.
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.05,AngularDeflection=.1,Relative=False);m.write(str(r/'STL'/(name+'.stl')));m=Mesh.Mesh(str(r/'STL'/(name+'.stl')))
 assert m.isSolid() and m.countComponents()==1 and not m.hasNonManifolds() and not m.hasSelfIntersections() and not m.hasNonUniformOrientedFacets()
 placed=s.copy();placed.translate(V(px,py,0));q=new.addObject('PartDesign::Feature',name);q.Shape=placed;q.Label=name.replace('_',' ');q.addProperty('App::PropertyString','SourceCoupon');q.SourceCoupon=source
 items.append((name,placed));audit.append({'number':len(audit)+1,'name':name,'source':source,'dims_mm':[s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength],'volume_mm3':s.Volume,'watertight':True,'printed_face':'Z0 flat face on bed; holes/pockets open upwards','source_material_removed_mm3':orig.cut(s).Volume,'added_tab_mm3':s.cut(orig).Volume if name.startswith('06') else 0,'position_mm':[px,py,0]})
new.recompute();new.saveAs(str(r/'CAD/Physical_Verification_Optimized.FCStd'))
gaps=[]
for i,(na,a) in enumerate(items):
 for nb,b in items[i+1:]:
  gap=a.distToShape(b)[0];gaps.append({'pair':[na,nb],'gap_mm':gap});assert gap>=8-1e-5,(na,nb,gap)
comp=Part.makeCompound([s for _,s in items]);m=MeshPart.meshFromShape(Shape=comp,LinearDeflection=.05,AngularDeflection=.1,Relative=False);m.write(str(r/'PRINT_FIRST_FitTests_Optimized.stl'));m=Mesh.Mesh(str(r/'PRINT_FIRST_FitTests_Optimized.stl'));b=m.BoundBox
assert m.isSolid() and m.countComponents()==7 and not m.hasNonManifolds() and not m.hasSelfIntersections() and not m.hasNonUniformOrientedFacets()
assert b.XMin>=10 and b.YMin>=10 and b.XMax<=250 and b.YMax<=250 and abs(b.ZMin)<1e-6 and b.ZMax<260
# Every model triangle must have material directly below it until the bed. All pieces have open-top pockets.
overhangs={}
for name,s in items:
 vs,ts=s.tessellate(.1);down=0
 for a,c,e in ts:
  p,q,t=vs[a],vs[c],vs[e];n=(q-p).cross(t-p)
  if n.Length>1e-9 and n.z/n.Length<-.7071 and min(p.z,q.z,t.z)>.01:down+=n.Length/2
 overhangs[name]=down
 assert down<1e-5,(name,down)
report={'assembly_modified':False,'release_status_modified':False,'coupon_count':7,'reason_keep_all':'No purpose redundant. Two horn pieces test positive drive and retention; two pan rings test actual full-diameter sliding fit; body, camera and actual tilt sleeve each distinct.','improvement':'Female pan ring gets standalone5.2mm through-bore in2.5mm-thick tab; original ring material/ID untouched. Horn coupons nest in separate ring openings.','parts':audit,'pair_separations':gaps,'minimum_surface_gap_mm':min(v['gap_mm'] for v in gaps),'support_required_by_geometry':False,'downward_overhang_area_mm2':overhangs,'bed_occupied_bounds_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'bed_dimensions_mm':[b.XLength,b.YLength,b.ZLength],'print_bed_nominal_mm':[260,260,260],'three_mm_brims_minimum_remaining_clearance_mm':min(v['gap_mm'] for v in gaps)-6,'old_bed_area_mm2':192.6*120.6,'new_bounding_area_mm2':b.XLength*b.YLength,'solid_material_volume_cm3':sum(s.Volume for _,s in items)/1000,'toolpaths_verified':False,'physical_tests':'NOT PERFORMED'}
(r/'CHECKS/geometry_mesh_layout.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ['coupon_count','bed_dimensions_mm','minimum_surface_gap_mm','support_required_by_geometry','solid_material_volume_cm3','physical_tests']},indent=2))
