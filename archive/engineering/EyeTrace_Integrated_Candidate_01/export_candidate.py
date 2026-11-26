import os,json,math,csv,shutil
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
H=os.path.dirname(os.path.abspath(__file__));B=os.path.join(os.path.dirname(H),'EyeTrace_CAD_20261115_232254');W=os.path.join(H,'work_02')
s=json.load(open(os.path.join(W,'checks','independent_validation_summary.json')));assert not s['critical_software_failures'] and s['motion_penetrations']==0
for n in ['parts','coupons','checks','renders','measurements']:os.makedirs(os.path.join(H,n),exist_ok=False)
for n in os.listdir(os.path.join(W,'checks')):shutil.copy2(os.path.join(W,'checks',n),os.path.join(H,'checks',n))
d=A.openDocument(os.path.join(W,'Integrated_Snapshot.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable];assert len(parts)==13
Part.export(obs,os.path.join(H,'EyeTrace_Integrated_Assembly.step'));st=Part.read(os.path.join(H,'EyeTrace_Integrated_Assembly.step'));assert st.isValid()
report={'assembly_step':{'valid':st.isValid(),'solids':len(st.Solids),'volume_error_mm3':abs(st.Volume-sum(o.Shape.Volume for o in obs)),'scope':'Includes explicitly labeled uncertainty and cable reference envelopes; not a fused manufacturing solid'},'parts':{}}
assert report['assembly_step']['volume_error_mm3']<.01
flatparts={}
def flat(s,name):
 p=s.copy()
 if name.startswith(('TiltCradle','Tilt_KeyedHorn')):p.rotate(V(),V(0,1,0),90)
 elif name.startswith('Tilt_Journal'):p.rotate(V(),V(0,1,0),-90)
 elif name.startswith('Pan_KeyedHorn'):p.rotate(V(),V(1,0,0),180)
 elif name.startswith(('CameraPlate','PCB_Spacer')):p.rotate(V(),V(1,0,0),90)
 b=p.BoundBox;p.translate(V(-b.XMin,-b.YMin,-b.ZMin));return p
def mesh(s,path):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.08,AngularDeflection=.15,Relative=False);m.write(path);r=Mesh.Mesh(path)
 q={'watertight':r.isSolid(),'components':r.countComponents(),'nonmanifold':r.hasNonManifolds(),'self_intersections':r.hasSelfIntersections(),'bad_normals':r.hasNonUniformOrientedFacets(),'facets':r.CountFacets,'relative_volume_error':abs(r.Volume-s.Volume)/s.Volume,'z_min_mm':r.BoundBox.ZMin}
 assert q['watertight'] and not q['nonmanifold'] and not q['self_intersections'] and not q['bad_normals'] and q['relative_volume_error']<.002,path
 return q,r
inventory=[]
for o in parts:
 n=o.PrintFileName;Part.export([o],os.path.join(H,'parts',n+'.step'));t=Part.read(os.path.join(H,'parts',n+'.step'));delta=o.Shape.cut(t).Volume+t.cut(o.Shape).Volume;assert t.isValid() and len(t.Solids)==1 and delta<.001
 p=flat(o.Shape,n);q,m=mesh(p,os.path.join(H,'parts',n+'.stl'));assert q['components']==1
 q['STEP_symmetric_difference_mm3']=delta;q['max_STL_vertex_to_native_surface_mm']=max(Part.Vertex(v).distToShape(p)[0] for v in m.Topology[0]);assert q['max_STL_vertex_to_native_surface_mm']<.01
 report['parts'][n]=q;flatparts[n]=p;inventory.append([n,1,n+'.stl',o.Name,o.KinematicGroup,p.BoundBox.XLength,p.BoundBox.YLength,p.BoundBox.ZLength])
with open(os.path.join(H,'printed_part_inventory.csv'),'x',newline='') as f:wr=csv.writer(f);wr.writerow(['Part','Quantity','STL file','Native object','Moving frame','Print X mm','Print Y mm','Print Z mm']);wr.writerows(inventory)
def layout(items,docname,native_path,stl_path):
 doc=A.newDocument(docname);x=10;y=10;rh=0;out=[];rows=[]
 for n,s in sorted(items,key=lambda q:-q[1].BoundBox.YLength):
  if x+s.BoundBox.XLength>250:x=10;y+=rh+8;rh=0
  q=s.copy();q.translate(V(x,y,0));o=doc.addObject('PartDesign::Feature',n);o.Shape=q;out.append(q);rows.append({'name':n,'offset':[x,y,0]});x+=s.BoundBox.XLength+8;rh=max(rh,s.BoundBox.YLength)
 comp=Part.makeCompound(out);assert comp.BoundBox.XMax<=250 and comp.BoundBox.YMax<=250
 for i,a in enumerate(out):
  for b in out[i+1:]:assert a.distToShape(b)[0]>=8-1e-5
 doc.recompute();doc.saveAs(native_path);q,m=mesh(comp,stl_path);assert q['components']==len(items);q.update({'dimensions_mm':[comp.BoundBox.XLength,comp.BoundBox.YLength,comp.BoundBox.ZLength],'positions':rows,'bed_nominal_mm':[260,260,260],'minimum_gap_mm':8,'slicer_supports_brims_purge_verified':False});return q
report['complete_bed']=layout(list(flatparts.items()),'K2_CompleteBed',os.path.join(H,'K2_PrintLayout.FCStd'),os.path.join(H,'EyeTrace_K2_SingleBed.stl'))
# Minimal interface fixtures: retain existing small tests, use CORRECT21x16 gauge.
rep=os.path.join(B,'sg90_interface_repair_01','coupons');coupons=[]
for n in ['SG90_EarMount_Coupon','StarHorn_PositivePocket_Coupon','StarHorn_CaptiveCover_Coupon','PETG_Hole_Journal_Gauge']:coupons.append((n,Part.read(os.path.join(rep,n+'.step'))))
gauge=Part.makeBox(30,25,1.5,V(-15,-12.5,0))
for x in [-10.5,10.5]:
 for y in [-8,8]:gauge=gauge.cut(Part.makeCylinder(1.2,3,V(x,y,-.5)))
gauge=gauge.cut(Part.makeCylinder(4,3,V(0,0,-.5)));coupons.append(('Camera_21x16_HoleCenter_Gauge',gauge));coupons.append(('Camera_Standoff_Test',flatparts['PCB_Spacer_Lower_Left'].copy()))
coupons.append(('PanJournal_Male_SizeTest',Part.makeCylinder(32,2).cut(Part.makeCylinder(30,3,V(0,0,-.5)))))
coupons.append(('PanJournal_Female_ClearanceTest',Part.makeCylinder(35.3,2).cut(Part.makeCylinder(32.3,3,V(0,0,-.5)))))
report['coupons']={};cf=[];cd=A.newDocument('CouponExports')
for n,s in coupons:
 s=s.removeSplitter();b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));assert s.isValid() and len(s.Solids)==1
 o=cd.addObject('PartDesign::Feature',n);o.Shape=s;Part.export([o],os.path.join(H,'coupons',n+'.step'));t=Part.read(os.path.join(H,'coupons',n+'.step'));assert t.isValid() and len(t.Solids)==1
 q,m=mesh(s,os.path.join(H,'coupons',n+'.stl'));assert q['components']==1;report['coupons'][n]=q;cf.append((n,s))
report['coupon_bed']=layout(cf,'FitTestBed',os.path.join(H,'coupons','FitTests.FCStd'),os.path.join(H,'coupons','FitTests_SingleBed.stl'))
json.dump(report,open(os.path.join(H,'checks','STL_STEP_layout_validation.json'),'x'),indent=2)
json.dump({'components':[{'name':o.Name,'label':o.Label,'printable':bool(o.Printable),'frame':o.KinematicGroup} for o in obs]},open(os.path.join(H,'component_inventory.json'),'x'),indent=2)
print(json.dumps({'printed_parts':len(parts),'full_step':report['assembly_step'],'K2_dimensions_mm':report['complete_bed']['dimensions_mm'],'bed_mesh_components':report['complete_bed']['components'],'fit_test_pieces':len(coupons),'release_status':'HOLD - critical physical dimensions remain unverified'},indent=2))
