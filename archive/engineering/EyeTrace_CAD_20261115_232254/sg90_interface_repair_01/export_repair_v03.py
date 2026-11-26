import os,json,math,shutil,hashlib,sys
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
BASE=os.path.dirname(os.path.abspath(__file__));W=os.path.join(BASE,sys.argv[1] if len(sys.argv)>1 else 'work_07');H=os.path.join(BASE,sys.argv[2]) if len(sys.argv)>2 else BASE
if H!=BASE:os.makedirs(H,exist_ok=False)
summary=json.load(open(os.path.join(W,'checks','independent_validation_summary.json')))
assert not summary['critical_software_failures'] and summary['motion_penetrations']==0
for n in ['parts','coupons','checks','renders','measurements']:os.makedirs(os.path.join(H,n),exist_ok=False)
d=A.openDocument(os.path.join(W,'EyeTrace_Repair.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable]
for n in ['EyeTrace_Repair.FCStd','component_manifest.json','repair_parameters.json']:shutil.copy2(os.path.join(W,n),os.path.join(H,n))
for n in os.listdir(os.path.join(W,'checks')):
 if n=='neutral_pairs.json':
  data=json.load(open(os.path.join(W,'checks',n)))
  for row in data['designed_contacts']:
   if row['kind']=='journal with radial clearance':
    row['pair']=['Tilt_Removable_IdlerPillar','Tilt_Journal_FlangedSleeve'];row['distance_mm']=d.getObject(row['pair'][0]).Shape.distToShape(d.getObject(row['pair'][1]).Shape)[0]
  json.dump(data,open(os.path.join(H,'checks',n),'x'),indent=2)
 else:shutil.copy2(os.path.join(W,'checks',n),os.path.join(H,'checks',n))
Part.export(obs,os.path.join(H,'EyeTrace_Assembly.step'));step=Part.read(os.path.join(H,'EyeTrace_Assembly.step'));assert step.isValid()
report={'assembly_step':{'valid':step.isValid(),'solids':len(step.Solids),'volume_difference_mm3':abs(step.Volume-sum(o.Shape.Volume for o in obs))},'parts':{}}
assert report['assembly_step']['volume_difference_mm3']<.01
flatparts=[];flatmap={}
def flat(s,name):
 p=s.copy()
 if name.startswith('TiltCradle') or name.startswith('Tilt_KeyedHorn'):p.rotate(V(),V(0,1,0),90)
 elif name.startswith('Tilt_Journal'):p.rotate(V(),V(0,1,0),-90)
 elif name.startswith('Pan_KeyedHorn'):p.rotate(V(),V(1,0,0),180)
 elif name.startswith(('Camera_SlidingRail','PCB_Spacer')):p.rotate(V(),V(1,0,0),90)
 b=p.BoundBox;p.translate(V(-b.XMin,-b.YMin,-b.ZMin));return p
def mesh_export(s,path):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.08,AngularDeflection=.15,Relative=False);m.write(path);r=Mesh.Mesh(path)
 q={'closed':r.isSolid(),'components':r.countComponents(),'nonmanifold':r.hasNonManifolds(),'self_intersections':r.hasSelfIntersections(),'bad_normals':r.hasNonUniformOrientedFacets(),'facets':r.CountFacets,'volume_relative_error':abs(r.Volume-s.Volume)/s.Volume,'min_z':r.BoundBox.ZMin}
 assert q['closed'] and not q['nonmanifold'] and not q['self_intersections'] and not q['bad_normals'] and q['volume_relative_error']<.002,path
 return q,r
for o in parts:
 Part.export([o],os.path.join(H,'parts',o.Name+'.step'));s=Part.read(os.path.join(H,'parts',o.Name+'.step'));diff=o.Shape.cut(s).Volume+s.cut(o.Shape).Volume;assert s.isValid() and len(s.Solids)==1 and diff<.001
 p=flat(o.Shape,o.Name);q,m=mesh_export(p,os.path.join(H,'parts',o.Name+'.stl'));q['step_difference_mm3']=diff
 q['max_STL_vertex_to_BRep_mm']=max(Part.Vertex(v).distToShape(p)[0] for v in m.Topology[0]);assert q['max_STL_vertex_to_BRep_mm']<.01
 report['parts'][o.Name]=q;flatparts.append((o.Name,p));flatmap[o.Name]=p
# All printable components, with8mm gap and10mm margins; no supports/brims baked in.
bed=A.newDocument('EyeTrace_Prototype_PrintLayout');positions=[];packed=[];x=10;y=10;row=0
for name,p in sorted(flatparts,key=lambda a:-a[1].BoundBox.YLength):
 if x+p.BoundBox.XLength>250:x=10;y+=row+8;row=0
 q=p.copy();q.translate(V(x,y,0));o=bed.addObject('PartDesign::Feature',name);o.Shape=q;packed.append(q);positions.append({'name':name,'offset_mm':[x,y,0],'size_mm':[p.BoundBox.XLength,p.BoundBox.YLength,p.BoundBox.ZLength]});x+=p.BoundBox.XLength+8;row=max(row,p.BoundBox.YLength)
comp=Part.makeCompound(packed);assert comp.BoundBox.XMax<=250 and comp.BoundBox.YMax<=250
for i,a in enumerate(packed):
 for b in packed[i+1:]:assert a.distToShape(b)[0]>=8-1e-5
bed.recompute();bed.saveAs(os.path.join(H,'PrintLayout.FCStd'));q,m=mesh_export(comp,os.path.join(H,'prototype_print_layout.stl'));assert q['components']==len(parts)
report['bed']=dict(q,dimensions_mm=[comp.BoundBox.XLength,comp.BoundBox.YLength,comp.BoundBox.ZLength],min_gap_mm=8,within_260x260=True,scope='Geometry packing only; slice/support/brim review still required; prototype layout, not production release')
json.dump(positions,open(os.path.join(H,'checks','print_layout_positions.json'),'x'),indent=2)
# Fit coupons independent of full mechanism, from the same configured interface dimensions.
P=json.load(open(os.path.join(H,'repair_parameters.json')))
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,V(x,y,z))
def cy(r,h,x=0,y=0,z=0):return Part.makeCylinder(r,h,V(x,y,z))
def profile(h,z,clear):
 s=cy(P['horn_hub_radius']+clear,h,0,0,z)
 for ang,ln,wd in zip(P['horn_angles'],P['horn_lengths'],P['horn_widths']):
  a=box(0,-wd/2-clear,z,ln+clear,wd+2*clear,h);a.rotate(V(),V(0,0,1),ang);s=s.fuse(a)
 return s.removeSplitter()
mid=(5.9-16.8)/2;ear=box(-8,mid-32.3/2-1,0,16,34.3,2.5).cut(box(-6.4,-17.1,-1,12.8,23.3,5))
for yy in [mid-13.6,mid+13.6]:ear=ear.cut(cy(.95,5,0,yy,-1))
hc=cy(21,4).cut(profile(2.3,1.8,P['horn_pocket_clearance'])).cut(cy(4,6,0,0,-1))
for a in [0,90,180,270]:hc=hc.cut(cy(1.65,6,15*math.cos(math.radians(a)),15*math.sin(math.radians(a)),-1))
w=P['camera_width'];hh=P['camera_height'];inner=max(8,min(P['camera_pitch_x'],P['camera_pitch_z'])-8)
cg=box(-w/2,-hh/2,0,w,hh,1.5).cut(box(-inner/2,-inner/2,-1,inner,inner,4))
for sx in [-1,1]:
 for sz in [-1,1]:cg=cg.cut(cy(1.2,4,sx*P['camera_pitch_x']/2,sz*P['camera_pitch_z']/2,-1))
clear=box(0,0,0,52,12,3)
for xx,diam in zip([5,13,21,29,37,45],[1.9,2.4,3.3,5.0,5.2,5.4]):clear=clear.cut(cy(diam/2,5,xx,6,-1))
coupons=[('SG90_EarMount_Coupon',ear),('StarHorn_PositivePocket_Coupon',hc),('StarHorn_CaptiveCover_Coupon',flatmap['Tilt_KeyedHorn_CaptiveCover']),('Camera_4Hole_Gauge_PROVISIONAL',cg),('PETG_Hole_Journal_Gauge',clear)]
cd=A.newDocument('EyeTrace_FitCoupons');cp=[];cx=10;cyy=10;rh=0;report['coupons']={}
for n,s in coupons:
 s=s.removeSplitter();bb=s.BoundBox;s.translate(V(-bb.XMin,-bb.YMin,-bb.ZMin));assert s.isValid() and len(s.Solids)==1
 o=cd.addObject('PartDesign::Feature',n);o.Shape=s;Part.export([o],os.path.join(H,'coupons',n+'.step'));st=Part.read(os.path.join(H,'coupons',n+'.step'));assert st.isValid() and len(st.Solids)==1
 q,m=mesh_export(s,os.path.join(H,'coupons',n+'.stl'));report['coupons'][n]=q
 if cx+s.BoundBox.XLength>220:cx=10;cyy+=rh+8;rh=0
 p=s.copy();p.translate(V(cx,cyy,0));o.Shape=p;cp.append(p);cx+=s.BoundBox.XLength+8;rh=max(rh,s.BoundBox.YLength)
cd.recompute();cd.saveAs(os.path.join(H,'coupons','FitCoupons_Layout.FCStd'));q,m=mesh_export(Part.makeCompound(cp),os.path.join(H,'coupons','coupon_layout.stl'));assert q['components']==5;report['coupon_layout']=q
json.dump(report,open(os.path.join(H,'checks','export_and_layout_audit.json'),'x'),indent=2)
print(json.dumps({'part_count':len(parts),'assembly_step':report['assembly_step'],'layout':report['bed'],'coupon_count':len(coupons)},indent=2))


