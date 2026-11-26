import os,json,math,csv,hashlib
import FreeCAD as A, Part, Mesh, MeshPart
from FreeCAD import Vector as V
B=os.path.dirname(os.path.abspath(__file__));R=os.path.join(B,'sg90_reference_revision_01');S=os.path.join(B,'production_candidate_01')
for n in ['checks','coupons','renders']:os.makedirs(os.path.join(R,n),exist_ok=True)
d=A.openDocument(os.path.join(S,'EyeTrace_Assembly.FCStd'));parts=['Base','PanServoRetainer','TiltServoRetainer','PanYoke','TiltCameraCradle','PanHornClamp','TiltHornClamp']
old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()}
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,V(x,y,z))
def cy(r,h,x=0,y=0,z=0,axis=(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),V(*axis))
# Canonical frame: shaft at XY=0; body long axis Y; Z=base to output.
L,W,H=22.7,12.2,22.7;near=5.9;far=L-near; earZ=15.9;earT=2.5;span=32.3;pitch=27.2
mid=(near-far)/2;emin=mid-span/2;emax=mid+span/2
main=box(-W/2,-far,0,W,L,H)
ears=box(-W/2,emin,earZ,W,span,earT)
for yy,sign in [(mid-pitch/2,-1),(mid+pitch/2,1)]:
 ears=ears.cut(cy(1,earT+2,0,yy,earZ-1))
 # Community model's open ear slot, 1.3 mm wide. No M3 fit claim.
 if sign<0:ears=ears.cut(box(-.65,emin-1,earZ-1,1.3,yy-emin+1,earT+2))
 else:ears=ears.cut(box(-.65,yy,earZ-1,1.3,emax-yy+1,earT+2))
case=main.fuse(ears).fuse(cy(W/2,4.3,0,0,H)).fuse(cy(2.5,4.3,0,-6.3,H))
case=case.cut(box(-1.8,near-.8,4.5,3.6,2,1.2)).removeSplitter()
# Smooth NON-MATING output envelope. No spline tooth count or profile is invented.
shaft=cy(2.5,3.3,0,0,27).cut(cy(.85,7,0,0,24))
case=case.cut(cy(.85,7,0,0,24));motor=case.fuse(shaft).removeSplitter()
# Rotations preserve both assembly axes; translation is the original case base.
panP=A.Placement(V(0,0,6),A.Rotation(V(0,0,1),90))
# local X->world Y, local Y->world Z, local Z->world X
rot=A.Rotation(V(0,1,0),V(0,0,1),V(1,0,0),'ZXY');tiltP=A.Placement(V(-70,0,78),rot)
def at(s,p):q=s.copy();q.Placement=p.multiply(q.Placement);return q
for name,p in [('PanServo_ASSUMED',panP),('TiltServo_ASSUMED',tiltP)]:
 o=d.getObject(name);o.Shape=at(motor,p);o.Label=name.replace('_ASSUMED',' - SG90 drawing based, CLONE UNVERIFIED');o.FitStatus='Mixed-source mechanical reference; spline omitted; NOT physical-fit validated'
# Keep original star shape, explicitly provisional; create stepped smooth clearance only.
for hn,p,h0 in [('PanStarHorn_ASSUMED',A.Placement(),35),('TiltStarHorn_ASSUMED',A.Placement(V(-41,0,78),A.Rotation(V(0,1,0),90)),0)]:
 h=old['PanStarHorn_ASSUMED'].copy();h.translate(V(0,0,-35))
 h=h.cut(cy(2.6,1.4,0,0,0)).cut(cy(.95,3,0,0,-.1)).removeSplitter()
 if hn.startswith('Pan'):h.translate(V(0,0,35))
 else:h=at(h,p)
 o=d.getObject(hn);o.Shape=h;o.Label=hn+' - PROVISIONAL smooth socket, NOT spline';o.FitStatus='Horn exterior inherited assumption; stepped bore provisional for clearance only'
# Original retaining screws: smooth illustrative envelopes, not a thread specification.
for name,pos,ax in [('PanOriginalScrew_PROVISIONAL',(0,0,37),(0,0,1)),('TiltOriginalScrew_PROVISIONAL',(-39,0,78),(1,0,0))]:
 sh=cy(.8,5,0,0,-5).fuse(cy(1.75,1));sh=at(sh,A.Placement(V(*pos),A.Rotation(V(0,0,1),V(*ax))))
 o=d.addObject('PartDesign::Feature',name);o.Shape=sh;o.addProperty('App::PropertyString','FitStatus');o.FitStatus='Illustrative envelope only: diameter1.6, head3.5x1, length5 all unmeasured; no thread modeled'
# Establish BEFORE collisions against all printed parts.
def contacts():
 out=[]
 for hn in ['PanServo_ASSUMED','TiltServo_ASSUMED']:
  for pn in parts:
   v=d.getObject(hn).Shape.common(d.getObject(pn).Shape).Volume
   if v>.001:out.append({'hardware':hn,'printed':pn,'volume_mm3':v})
 return out
before=contacts()
# Accommodate documented/explicit-reference tab and boss envelopes, not force the hardware to fit.
tabclear=box(-W/2-.3,emin-.3,earZ-.3,W+.6,span+.6,earT+.6)
base=d.getObject('Base');base.Shape=base.Shape.cut(at(tabclear,panP)).removeSplitter()
pc=d.getObject('PanServoRetainer');pc.Shape=pc.Shape.cut(cy(6.4,6,0,0,27))
# Main case height changed from23 to22.7: add0.3 contact lands away from boss.
for yy in [-4,1]:pc.Shape=pc.Shape.fuse(box(8,yy,28.7,6,3,.3))
pc.Shape=pc.Shape.removeSplitter()
y=d.getObject('PanYoke');y.Shape=y.Shape.cut(at(tabclear,tiltP))
# Seating datum moves case bottom to worldZ61.2. Add contact land0.2 high.
y.Shape=y.Shape.fuse(box(-68,-4,61,9,8,.2)).removeSplitter()
tc=d.getObject('TiltServoRetainer');tc.Shape=tc.Shape.cut(at(tabclear,tiltP)).fuse(box(-68,-4,83.9,9,8,.1)).removeSplitter()
after=contacts()
json.dump({'before':before,'after':after,'scope':'Neutral hardware versus printed parts; reference geometry dimensions remain clone-unverified'},open(os.path.join(R,'checks','mounting_interferences.json'),'x'),indent=2)
# Exact pairwise checks over unique relative poses, includes both horns and original screw envelopes.
fixed=['Base','PanServoRetainer','PanServo_ASSUMED']+[o.Name for o in d.Objects if o.Name.startswith('PanRetainer_M3')]
pang=['PanYoke','TiltServoRetainer','TiltServo_ASSUMED','PanHornClamp','PanStarHorn_ASSUMED','PanOriginalScrew_PROVISIONAL']+[o.Name for o in d.Objects if o.Name.startswith('PanHorn_M3') or o.Name.startswith('TiltRetainer_M3')]
tilg=['TiltCameraCradle','Camera_ASSUMED_38x38x30','TiltHornClamp','TiltStarHorn_ASSUMED','TiltOriginalScrew_PROVISIONAL','Idler_M3']+[o.Name for o in d.Objects if o.Name.startswith('TiltHorn_M3')]
groups={n:g for g,ns in [('fixed',fixed),('pan',pang),('tilt',tilg)] for n in ns};ns=list(groups);cache={};fail=[];ct=0
for pa in range(-60,61,10):
 for ta in range(-30,31,5):
  shapes={}
  for n,g in groups.items():
   q=d.getObject(n).Shape.copy()
   if g=='tilt':q.rotate(V(0,0,78),V(1,0,0),ta)
   if g!='fixed':q.rotate(V(),V(0,0,1),pa)
   shapes[n]=q
  for i,n in enumerate(ns):
   for k in ns[i+1:]:
    if set([n,k])==set(['TiltCameraCradle','Camera_ASSUMED_38x38x30']):continue
    ga,gb=groups[n],groups[k];rel=(0,0) if ga==gb else ((0,ta) if 'fixed' not in [ga,gb] else (pa,ta if 'tilt' in [ga,gb] else 0));key=(n,k,rel);ct+=1
    if key not in cache:
     a,b=shapes[n],shapes[k];aa,bb=a.BoundBox,b.BoundBox
     ov=all(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))>1e-7 for t in ['X','Y','Z'])
     cache[key]=a.common(b).Volume if ov else 0
    if cache[key]>.001:fail.append({'pan':pa,'tilt':ta,'pair':[n,k],'volume':cache[key]})
json.dump({'poses':169,'pair_tests':ct,'unique_tests':len(cache),'collision_instances':len(fail),'collisions':fail,'excluded_contact':['camera to cradle shelf'],'limits':'Discrete poses, no physical tolerances, threads, cable, tool or load proof; star and screw envelopes provisional'},open(os.path.join(R,'checks','motion.json'),'x'),indent=2)
# No full printing exports. In-memory mesh tests for all changed print parts.
meshcheck={}
for n in parts:
 s=d.getObject(n).Shape;m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.06,AngularDeflection=.15,Relative=False)
 meshcheck[n]={'valid':s.isValid(),'solids':len(s.Solids),'closed':m.isSolid(),'components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'bad_normals':m.hasNonUniformOrientedFacets()}
json.dump(meshcheck,open(os.path.join(R,'checks','printed_solid_mesh.json'),'x'),indent=2)
# Small mounting coupon: seating plate at flange-bottom with clear body window and ear holes.
cd=A.newDocument('SG90_Interface_Coupons');mount=box(-8,emin-1,0,16,span+2,2).cut(box(-6.4,-far-.3,-1,12.8,L+.6,4))
for yy in [mid-pitch/2,mid+pitch/2]:mount=mount.cut(cy(1.15,4,0,yy,-1))
# Diagnostic horn sandwich; no spline reproduction. Two pieces; original center screw required separately.
ring=cy(17,1.5).cut(cy(4,3,0,0,-.5));face=cy(17,2).cut(cy(4,3,0,0,-.5))
for i in range(4):
 a=i*math.pi/2;x0=14*math.cos(a);y0=14*math.sin(a)
 ring=ring.cut(cy(1.65,4,x0,y0,-1));face=face.cut(cy(1.65,4,x0,y0,-1))
ca={}
for n,s in [('SG90_TabMount_Test',mount),('StarHorn_Clamp_Test',ring),('StarHorn_MatingFace_Test',face)]:
 b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));o=cd.addObject('PartDesign::Feature',n);o.Shape=s.removeSplitter();m=MeshPart.meshFromShape(Shape=o.Shape,LinearDeflection=.06,AngularDeflection=.15,Relative=False)
 path=os.path.join(R,'coupons',n+'.stl');m.write(path);re=Mesh.Mesh(path)
 ca[n]={'valid':s.isValid(),'solids':len(s.Solids),'closed':re.isSolid(),'components':re.countComponents(),'self_intersections':re.hasSelfIntersections(),'nonmanifold':re.hasNonManifolds()};Part.export([o],os.path.join(R,'coupons',n+'.step'))
cd.recompute();cd.saveAs(os.path.join(R,'coupons','SG90_Test_Coupons.FCStd'));json.dump(ca,open(os.path.join(R,'checks','coupons.json'),'x'),indent=2)
d.addObject('App::DocumentObjectGroup','SG90_Reference_Status').Label='HOLD - manufacturer/CAD based; spline and clone fit UNVERIFIED'
d.License='CreativeCommons Attribution-ShareAlike';d.LicenseURL='https://creativecommons.org/licenses/by-sa/4.0/';d.Comment='SG90 mechanical references adapted from Juan Fenoy, FreeCAD-library. Drawing-based changes and provisional horn/screw envelopes by Eye Trace revision script. No endorsement or clone-fit guarantee.'
d.recompute();d.saveAs(os.path.join(R,'EyeTrace_SG90_Reference_01.FCStd'))
# Confidence ledger: manufacturer dimensions preferred; unresolved dimensions explicitly provisional.
ledger=[('Case length','23','22.7','TowerPro table B + label image','High for published nominal; clone unverified'),('Case width','12','12.2','TowerPro D + headline','High for published nominal; clone unverified'),('Case main height','23','22.7','Juan Fenoy native Box.Height','Medium community reference; clone unverified'),('Shoulder height above base','unseparated','27','TowerPro C label image','Medium datum reading; clone unverified'),('Output top above base','31 pan /30 tilt','30.3 both','TowerPro A label image','High nominal drawing; headline29 conflicts'),('Ear total span','absent','32.3','TowerPro E label image','High nominal drawing; clone unverified'),('Ear bottom / thickness','absent','15.9 /2.5','Juan Fenoy Box001 placement/height','Medium community reference; F17 datum unresolved'),('Hole pitch / diameter / open slot','absent','27.2 /2.0 /1.3','Native hole centers/radii and slot Box geometry','Medium community reference; no M3 fit claim'),('Output center from case end','6','5.9','Native cylinder center and case end','Medium; clone unverified'),('Boss diameter / height','unseparated','12.2 /4.3','D width + C27 minus community case22.7','Medium mixed-source envelope, unverified'),('Secondary gear boss diameter / offset','absent','5 / -6.3 from output','Native cylinder geometry','Medium community reference'),('Cable notch width / height / height from base','absent','3.6 /1.2 /4.5','Native sketch bounds','Medium community reference; wire keep-out absent'),('Output envelope diameter / length','6x8 pan;6x7 tilt','5x3.3 both','Conservative rounded community shaft bounds; A-C height','Low as actual spline fit; smooth keep-out ONLY'),('Axial bore diameter','absent','1.7','Community shaft inner cylinder diameter','Low; NOT thread spec'),('Spline teeth/profile','absent','NOT MODELED','No authoritative spline drawing found','UNKNOWN; no fabricated teeth'),('Star exterior arms / width / length / thickness','five /3.6 /12 /2','unchanged, PROVISIONAL','Inherited EyeTrace placeholder, NOT measured','LOW; original star profile needed'),('Star socket stepped bore','absent','5.2x1.4 deep +1.9 through','PROVISIONAL clearance layout only','LOW; not a spline or physical mating claim'),('Retaining screw shank/head/length','absent','1.6 /3.5x1 /5','PROVISIONAL visualization only','LOW; thread/head/length must be measured'),('Motor mounting datum','pan baseZ6;tilt baseX-70','unchanged axes; native placements in report','Inherited EyeTrace axes retained','Design choice; alignment checked'),('Printed bore correction','8 pan cap center','12.8 pan cap center; ear clearance+.3','Referenced boss/tab envelope +design allowance','Geometric clearance fix, physical fit UNVERIFIED')]
with open(os.path.join(R,'dimension_comparison.csv'),'x',newline='') as f:
 w=csv.writer(f);w.writerow(['Critical dimension','Old mm','Revised mm','Source','Confidence / status']);w.writerows(ledger)
print('BEFORE',before,'AFTER',after);print('MOTION',len(fail),'unique pairs',sorted(set(tuple(x['pair']) for x in fail)));print('MESH',meshcheck);print('COUPONS',ca)
