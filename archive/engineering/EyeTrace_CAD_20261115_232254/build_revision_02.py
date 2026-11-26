import os,sys,json,math,traceback
import FreeCAD as A, Part, Mesh, MeshPart
from FreeCAD import Vector as V
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'revision_02')
os.makedirs(ROOT,exist_ok=False)
for sub in ['parts','renders','checks']: os.makedirs(os.path.join(ROOT,sub),exist_ok=True)
doc=A.newDocument('EyeTrace_Prototype')
P={'servo_body':[23,12,23],'servo_clearance':0.6,'camera_envelope':[38,38,30],'pan_limit_deg':60,'tilt_limit_deg':30,'units':'mm','status':'PROTOTYPE: physical fit unverified'}
json.dump(P,open(os.path.join(ROOT,'parameters.json'),'w'),indent=2)
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(r,h,x,y,z,d=(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),V(*d))
def clean(s):return s.removeSplitter()
def holes(s,points,r,h,d=(0,0,1)):
 for p in points:s=s.cut(cyl(r,h,*p,d))
 return clean(s)
parts=[]; fixtures=[]
def add(name,s,color,group='print'):
 o=doc.addObject('PartDesign::Feature',name);o.Shape=clean(s)
 o.addProperty('App::PropertyString','FitStatus');o.FitStatus='Unverified hardware fit'
 if A.GuiUp:o.ViewObject.ShapeColor=color
 (parts if group=='print' else fixtures).append(o)
 return o
# Base: open cable exit on rear; oversized cradle accepts an assumed SG90 case.
base=box(-40,-35,0,80,70,4)
base=holes(base,[(x,y,-1) for x in [-32,32] for y in [-27,27]],1.7,6)
socket=box(-10,-9,4,31,18,25).cut(box(-6.6,-6.6,3,24.2,13.2,28))
socket=socket.cut(box(0,-10,4,11,5,8))
# Flange mounting lands at either end of assumed 32 mm ear pitch.
socket=holes(socket,[(-10.5,0,22),(21.5,0,22)],1.1,10)
base=add('Base',base.fuse(socket),(0.22,0.28,0.34))
# Pan output bearing is the actual servo; no false M3 screw through its spline.
platform=cyl(25,4,0,0,37).fuse(box(-47,-21,37,88.5,42,4))
platform=platform.cut(cyl(4,6,0,0,36))
# Horn screw pattern deliberately not assumed: universal radial slots require physical match.
for ang in [0,90,180,270]:
 cut=box(5,-1.3,36,10,2.6,6);cut.rotate(V(0,0,0),V(0,0,1),ang);platform=platform.cut(cut)
left=box(-47,-21,40,4,42,57).cut(box(-48,-6.6,60.4,6,13.2,24.2))
# Small flange holes are pilot holes, not claimed to accept M3.
left=holes(left,[(-48,0,z) for z in [56.5,88.5]],1.1,6,(1,0,0))
right=box(36.5,-21,40,2.5,42,57)
right=holes(right,[(35.5,0,78)],1.65,5,(1,0,0))
for x,y in [(18,0),(-18,0),(0,18),(0,-18)]:
 platform=platform.cut(cyl(1.65,6,x,y,36)).cut(cyl(3.5,3,x,y,39))
yoke=add('PanYoke',platform.fuse(left).fuse(right),(0.16,0.48,0.68))
# Camera shelf and two side cheeks, coaxial with X tilt axis at z=78.
cr=box(-33,-20,54,66,40,3)
cr=cr.fuse(box(-37,-20,54,4,40,40)).fuse(box(33,-20,54,3,40,40))
cr=cr.fuse(cyl(17,2,-40,0,78,(1,0,0)))
cr=holes(cr,[(-41,0,78)],3.5,9,(1,0,0))
cr=holes(cr,[(32,0,78)],1.65,6,(1,0,0))
# Camera retention uses removable straps; slots through shelf.
for x in [-25,23]:cr=cr.cut(box(x,-16,53,2.5,32,5))
for y in [-14,10]:cr=cr.cut(box(-10,y,53,20,3,5))
# Radial horn fastener access slots at nominal 6..13 mm radius.
for ang in [0,90,180,270]:
 cut=box(-41,5,76.7,5,8,2.6);cut.rotate(V(0,0,78),V(1,0,0),ang);cr=cr.cut(cut)
for y,z in [(14,78),(-14,78),(0,92),(0,64)]:
 cr=cr.cut(cyl(1.65,4,-41,y,z,(1,0,0))).cut(cyl(3.5,7,-38,y,z,(1,0,0)))
cradle=add('TiltCameraCradle',cr,(0.87,0.48,0.16))
panring=cyl(22,1.5,0,0,33.5).cut(cyl(4,3,0,0,33))
panring=holes(panring,[(18,0,33),(-18,0,33),(0,18,33),(0,-18,33)],1.65,3)
add('PanHornClamp',panring,(0.7,0.7,0.72))
tiltring=cyl(17,1.5,-43.5,0,78,(1,0,0)).cut(cyl(4,3,-44,0,78,(1,0,0)))
tiltring=holes(tiltring,[(-44,y,z) for y,z in [(14,78),(-14,78),(0,92),(0,64)]],1.65,3,(1,0,0))
add('TiltHornClamp',tiltring,(0.7,0.7,0.72))
# Physical envelopes kept separate from printable geometry.
servo=add('PanServo_ASSUMED',box(-6,-6,6,23,12,23).fuse(cyl(3,8,0,0,29)),(0.15,0.24,0.72),'hardware')
tilt=add('TiltServo_ASSUMED',box(-70,-6,61,23,12,23).fuse(cyl(3,7,-47,0,78,(1,0,0))),(0.15,0.24,0.72),'hardware')
cam=add('Camera_ASSUMED_38x38x30',box(-19,-19,57,38,38,30).fuse(cyl(7,10,0,-19,74,(0,-1,0))),(0.16,0.18,0.18),'hardware')
# Star-shaped horn envelopes: visual assumptions only.
def horn_z():
 s=cyl(4,2,0,0,35)
 for a in range(0,360,72):
  arm=box(0,-1.8,35,12,3.6,2);arm.rotate(V(),V(0,0,1),a);s=s.fuse(arm)
 return clean(s)
h1=add('PanStarHorn_ASSUMED',horn_z(),(0.92,0.92,0.92),'hardware')
hs=horn_z();hs.translate(V(0,0,-35));hs.rotate(V(),V(0,1,0),90);hs.translate(V(-42,0,78))
h2=add('TiltStarHorn_ASSUMED',hs,(0.92,0.92,0.92),'hardware')
doc.recompute()
report={'freecad_version':A.Version(),'parameters':P,'solids':{},'meshes':{},'motion':{},'hardware_fit':'NOT VALIDATED','release_status':'NOT PRINT-RELEASED: measurement and attachment blockers'}
# Standalone exports are moved to the bed with largest flat base or cheek down.
bed=[];cursor=5; row_y=5; row_height=0; ymax=0
for o in parts:
 s=o.Shape
 report['solids'][o.Name]={'valid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume}
 Part.export([o],os.path.join(ROOT,'parts',o.Name+'.step'))
 p=s.copy()
 if o==cradle:p.rotate(V(),V(0,1,0),90)
 b=p.BoundBox;p.translate(V(-b.XMin,-b.YMin,-b.ZMin))
 m=MeshPart.meshFromShape(Shape=p,LinearDeflection=0.08,AngularDeflection=0.15,Relative=False)
 path=os.path.join(ROOT,'parts',o.Name+'.stl');m.write(path)
 re=Mesh.Mesh(path)
 report['meshes'][o.Name]={'facets':re.CountFacets,'closed':re.isSolid(),'components':re.countComponents(),'bounds_mm':[p.BoundBox.XLength,p.BoundBox.YLength,p.BoundBox.ZLength]}
 if cursor+p.BoundBox.XLength>250:
  cursor=5;row_y+=row_height+8;row_height=0
 row_height=max(row_height,p.BoundBox.YLength)
 p.translate(V(cursor,row_y,0));cursor+=p.BoundBox.XLength+8;ymax=max(ymax,p.BoundBox.YMax);bed.append(p)
compound=Part.makeCompound(bed)
MeshPart.meshFromShape(Shape=compound,LinearDeflection=0.08,AngularDeflection=0.15,Relative=False).write(os.path.join(ROOT,'single_bed.stl'))
report['bed']={'bounds_mm':[compound.BoundBox.XLength,compound.BoundBox.YLength,compound.BoundBox.ZLength],'minimum_gap_mm':8,'fits_assumed_260_square':compound.BoundBox.XMax<=260 and ymax<=260,'printer_bed_dimension':'assumed 260 mm; verify exact K2 variant','orientation':'base and yoke upright; camera cradle on side; supports required for yoke and cradle'}
# Exact BRep intersection on sampled poses, with rigid bodies transformed about their actual axes.
collisions=[]; minimum=1e9; samples=0
for pa in range(-60,61,10):
 for ta in range(-30,31,5):
  samples+=1
  moving=[]
  for name,s,tilts in [('yoke',yoke.Shape,False),('cradle',cradle.Shape,True),('camera',cam.Shape,True),('tilt_servo',tilt.Shape,False)]:
   q=s.copy()
   if tilts:q.rotate(V(0,0,78),V(1,0,0),ta)
   q.rotate(V(),V(0,0,1),pa);moving.append((name,q))
  pairs=[('base',base.Shape,n,s) for n,s in moving]
  pairs += [(moving[0][0],moving[0][1],n,s) for n,s in moving[1:] if n!='tilt_servo']
  for n,a,k,b in pairs:
   vol=a.common(b).Volume
   if vol>0.001:collisions.append({'pan':pa,'tilt':ta,'pair':[n,k],'volume_mm3':vol})
   else:minimum=min(minimum,a.distToShape(b)[0])
report['motion']={'sampled_poses':samples,'pan_range':[-60,60],'tilt_range':[-30,30],'pan_step':10,'tilt_step':5,'collision_count':len(collisions),'collisions':collisions,'minimum_separation_mm':minimum,'limitation':'sampled rigid envelopes only; excludes wires, fasteners, horn deformation, servo torque and continuous sweep; no installed motion stops'}
Part.export(parts+fixtures,os.path.join(ROOT,'assembly.step'))
doc.recompute();doc.saveAs(os.path.join(ROOT,'EyeTrace.FCStd'))
json.dump(report,open(os.path.join(ROOT,'checks','validation.json'),'w'),indent=2)
print(json.dumps(report,indent=2))

