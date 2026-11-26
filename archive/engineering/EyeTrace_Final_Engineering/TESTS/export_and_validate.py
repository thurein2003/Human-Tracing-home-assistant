from pathlib import Path
import os,json,csv,math
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable];folder=r/'STL/individual';folder.mkdir(exist_ok=True);steps=r/'CAD/individual_STEP';steps.mkdir(exist_ok=True)
def flat(s,name):
 p=s.copy()
 if name.startswith(('TiltCradle','Tilt_KeyedHorn')):p.rotate(V(),V(0,1,0),90)
 elif name.startswith('Tilt_Journal'):p.rotate(V(),V(0,1,0),-90)
 elif name.startswith('Pan_KeyedHorn'):p.rotate(V(),V(1,0,0),180)
 elif name.startswith(('CameraPlate','PCB_Spacer')):p.rotate(V(),V(1,0,0),90)
 b=p.BoundBox;p.translate(V(-b.XMin,-b.YMin,-b.ZMin));return p
def mesh(s,path):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.08,AngularDeflection=.15,Relative=False);m.write(str(path));m=Mesh.Mesh(str(path));q={'watertight':m.isSolid(),'components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'bad_normals':m.hasNonUniformOrientedFacets(),'facets':m.CountFacets,'relative_volume_error':abs(m.Volume-s.Volume)/s.Volume,'z_min_mm':m.BoundBox.ZMin}
 assert q['watertight'] and not any(q[k] for k in ['nonmanifold','self_intersections','bad_normals']) and q['relative_volume_error']<.002
 return q,m
def layout(items,name,native,stl):
 doc=A.newDocument(name);x=y=10;rh=0;out=[];positions=[]
 for n,s in sorted(items,key=lambda q:-q[1].BoundBox.YLength):
  if x+s.BoundBox.XLength>250:x=10;y+=rh+8;rh=0
  q=s.copy();q.translate(V(x,y,0));o=doc.addObject('PartDesign::Feature',n);o.Shape=q;out.append(q);positions.append({'part':n,'offset_mm':[x,y,0]});x+=s.BoundBox.XLength+8;rh=max(rh,s.BoundBox.YLength)
 c=Part.makeCompound(out);assert c.BoundBox.XMax<=250 and c.BoundBox.YMax<=250
 for i,a in enumerate(out):
  for b in out[i+1:]:assert a.distToShape(b)[0]>=8-1e-5
 doc.recompute();doc.saveAs(str(native));q,m=mesh(c,stl);assert q['components']==len(items);q.update({'dimensions_mm':[c.BoundBox.XLength,c.BoundBox.YLength,c.BoundBox.ZLength],'parts':positions,'bed_mm':[260,260,260],'minimum_gap_mm':8,'support_brim_toolpath_verified':False});return q
Part.export(obs,str(r/'CAD/EyeTrace_Final_Assembly.step'));step=Part.read(str(r/'CAD/EyeTrace_Final_Assembly.step'));assert step.isValid();error=abs(step.Volume-sum(o.Shape.Volume for o in obs));assert error<.01
report={'assembly_step':{'valid':True,'solids':len(step.Solids),'volume_error_mm3':error,'includes_labeled_reference_envelopes':True},'parts':{}};flatparts={};inventory=[]
for o in parts:
 n=o.PrintFileName;Part.export([o],str(steps/(n+'.step')));t=Part.read(str(steps/(n+'.step')));delta=o.Shape.cut(t).Volume+t.cut(o.Shape).Volume;assert t.isValid() and len(t.Solids)==1 and delta<.001
 s=flat(o.Shape,n);q,m=mesh(s,folder/(n+'.stl'));assert q['components']==1
 q['STEP_symmetric_difference_mm3']=delta;q['max_vertex_native_surface_mm']=max(Part.Vertex(v).distToShape(s)[0] for v in m.Topology[0]);assert q['max_vertex_native_surface_mm']<.01
 report['parts'][n]=q;flatparts[n]=s;inventory.append([n,1,o.Name,o.KinematicGroup,s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength,s.Volume/1000])
with (r/'DOCUMENTATION/printed_part_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Part','Quantity','Native object','Frame','Print X mm','Print Y mm','Print Z mm','Solid volume cm3']);w.writerows(inventory)
report['complete_bed']=layout(list(flatparts.items()),'K2_FinalBed',r/'CAD/K2_PrintLayout.FCStd',r/'STL/EyeTrace_Final_K2_SingleBed.stl')
# Seven pieces serve four interface classes. Sleeve is the actual usable printed part; no redundant stand-off or hole-gauge bed.
names=['SG90_EarMount_Coupon','StarHorn_PositivePocket_Coupon','StarHorn_CaptiveCover_Coupon','PanJournal_Male_SizeTest','PanJournal_Female_ClearanceTest','Camera_21x16_HoleCenter_Gauge'];cs=[];report['fit_tests']={}
for n in names:
 s=Part.read(str(r/'CAD/SOURCE_SNAPSHOT'/(n+'.step')))
 if n=='StarHorn_CaptiveCover_Coupon':s=flatparts['Tilt_KeyedHorn_CaptiveCover'].copy()
 if n=='StarHorn_PositivePocket_Coupon':
  p=json.loads((r/'CAD/parameters.json').read_text());c=p['horn_pocket_clearance_mm'];depth=p['horn_pocket_depth_mm'];profile=Part.makeCylinder(p['horn_hub_radius_mm']+c,depth+.1,V(0,0,1.8))
  for angle,length,width in zip(p['horn_arm_angles_deg'],p['horn_arm_lengths_mm'],p['horn_arm_widths_mm']):
   arm=Part.makeBox(length+c,width+2*c,depth+.1,V(0,-width/2-c,1.8));arm.rotate(V(),V(0,0,1),angle);profile=profile.fuse(arm)
  s=Part.makeCylinder(21,depth+1.8).cut(profile).cut(Part.makeCylinder(4,10,V(0,0,-1)))
  for angle in [0,90,180,270]:s=s.cut(Part.makeCylinder(1.65,10,V(15*math.cos(math.radians(angle)),15*math.sin(math.radians(angle)),-1)))
  s=s.removeSplitter()
 b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));cs.append((n,s))
cs.append(('Tilt_Journal_FlangedSleeve',flatparts['Tilt_Journal_FlangedSleeve']))
for n,s in cs:
 q,m=mesh(s,r/'FIT_TESTS'/(n+'.stl'));assert q['components']==1;report['fit_tests'][n]=q
report['fit_test_bed']=layout(cs,'InterfaceTests',r/'FIT_TESTS/FitTests.FCStd',r/'FIT_TESTS/FitTests_K2_Bed.stl')
(r/'TESTS/results/export_mesh_layout.json').write_text(json.dumps(report,indent=2))
print('Export PASS:13 parts, STEP solids',len(step.Solids),'bed',report['complete_bed']['dimensions_mm'],'fit-test pieces',len(cs))
# Overhang screen uses exported orientation. It is an area diagnostic, not a substitute for slicing.
manufacturing={}
for n,s in flatparts.items():
 vertices,triangles=s.tessellate(.20);total=down=0.;slopes=[]
 for ia,ib,ic in triangles:
  a,b,c=vertices[ia],vertices[ib],vertices[ic];normal=(b-a).cross(c-a);area=normal.Length/2
  if area<1e-9:continue
  nz=normal.z/normal.Length;total+=area
  if nz<-.70710678 and (a.z+b.z+c.z)/3>.21:down+=area
 manufacturing[n]={'surface_area_mm2':total,'downward_area_over45deg_excluding_first_layer_mm2':down,'support_review_required':down>1,'screen':'Triangle normal area screening; bridge length, support access and toolpaths must be reviewed in slicer','bbox_print_mm':[s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength]}
(r/'TESTS/results/FDM_overhang_screen.json').write_text(json.dumps(manufacturing,indent=2))
