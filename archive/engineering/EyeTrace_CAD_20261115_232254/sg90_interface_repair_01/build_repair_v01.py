import os,sys,json,math,hashlib,csv
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
HOME=os.path.dirname(os.path.abspath(__file__)); B=os.path.dirname(HOME)
RUN=sys.argv[1] if len(sys.argv)>1 else 'work_01'; R=os.path.join(HOME,RUN);os.makedirs(R,exist_ok=False)
for n in ['checks','parts','coupons','renders']:os.makedirs(os.path.join(R,n))
P={'camera_pitch_x':28.,'camera_pitch_z':28.,'camera_width':38.,'camera_height':38.,'camera_pcb_thickness':1.6,'camera_hole_diameter':2.2,'camera_standoff':3.,'camera_center_z':76.,'horn_angles':[0,72,144,216,288],'horn_lengths':[12]*5,'horn_widths':[3.6]*5,'horn_hub_radius':4.,'horn_thickness':2.,'horn_pocket_clearance':.25,'pan_range':[-60,60],'tilt_range':[-30,30]}
if len(sys.argv)>2:P.update(json.load(open(sys.argv[2])))
json.dump(P,open(os.path.join(R,'repair_parameters.json'),'x'),indent=2)
source=A.openDocument(os.path.join(B,'sg90_reference_revision_02','EyeTrace_SG90_Reference_01.FCStd'));old={o.Name:o.Shape.copy() for o in source.Objects if hasattr(o,'Shape') and not o.Shape.isNull()}
d=A.newDocument('EyeTrace_Interface_Repair');parts=[];hardware=[];groups={};joints=[];tools=[]
pr=d.addObject('App::DocumentObjectGroup','RepairParameters')
for k,v in [('CameraPitchX',P['camera_pitch_x']),('CameraPitchZ',P['camera_pitch_z']),('CameraCenterZ',P['camera_center_z'])]:pr.addProperty('App::PropertyLength',k);setattr(pr,k,v)
pr.addProperty('App::PropertyString','Verification');pr.Verification='Camera and original horn dimensions PROVISIONAL; source audit sg90_interface_audit_01 authoritative'
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,V(x,y,z))
def cy(r,h,x=0,y=0,z=0,axis=(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),V(*axis))
def moved(s,p):q=s.copy();q.Placement=p.multiply(q.Placement);return q
def hexsolid(af,h,z=0):
 rr=af/math.sqrt(3);pts=[V(rr*math.cos(math.radians(30+60*i)),rr*math.sin(math.radians(30+60*i)),z) for i in range(6)];return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(0,0,h))
def add(n,s,g,printable=True,color=None):
 o=d.addObject('PartDesign::Feature',n);o.Shape=s.removeSplitter();o.addProperty('App::PropertyString','FitStatus');o.FitStatus='CAD reference validation only; physical fit unverified'
 (parts if printable else hardware).append(o);groups[n]=g
 if A.GuiUp:o.ViewObject.ShapeColor=color or ((.15,.5,.7) if printable else (.65,.65,.68))
 return o
# Threadless shank/head/nut/washer; dimensions include nominal projected thread, not thread engagement proof.
def bolt(n,p,axis,g,diam=3,length=10,grip=5.5,headD=5.6,headH=3,nutAF=5.5,nutH=2.4,washer=False):
 s=cy(diam/2,length).fuse(cy(headD/2,headH,0,0,-headH));sol=[s,hexsolid(nutAF,nutH,grip).cut(cy(diam/2,nutH+1,0,0,grip-.2))]
 if washer:sol.append(cy(2,.5).cut(cy(.9,1,0,0,-.1)))
 rot=A.Rotation(V(0,0,1),V(*axis));o=add(n,moved(Part.makeCompound(sol),A.Placement(V(*p),rot)),g,False)
 joints.append({'name':n,'diameter':diam,'under_head_length':length,'grip':grip,'nut_height':nutH,'projection':length-grip-nutH,'axis':axis,'under_head':p,'locking':'nyloc required' if n=='TiltIdler_M3x12' else 'captive hex nut / verify locking'})
 return o
# Base reuses inherited footprint, mounting coordinates and pan datum.
base=box(-40,-35,0,80,70,4)
for x in [-32,32]:
 for y in [-27,27]:base=base.cut(cy(1.7,6,x,y,-1))
plate=box(-13,-9,19.4,37,18,2.5)
for x in [-8.15,19.05]:
 plate=plate.fuse(cy(2.8,1.6,x,0,17.8)).cut(moved(hexsolid(3.45,1.8),A.Placement(V(x,0,17.7),A.Rotation())))
 plate=plate.cut(cy(.95,6,x,0,17))
plate=plate.cut(box(-6.2,-6.4,17,23.3,12.8,6))
base=base.fuse(plate)
for x in [-13,20]:
 for y in [-9,6]:base=base.fuse(box(x,y,4,4,3,15.4))
# Printed thrust support and radial backup journal: shaft no longer sole pan support.
ring=cy(32,32,0,0,4).cut(cy(27.5,34,0,0,3))
ring=ring.cut(box(-34,-3,4,9,6,10));base=base.fuse(ring)
for a in [0,120,240]:base=base.fuse(cy(.75,.5,30*math.cos(math.radians(a)),30*math.sin(math.radians(a)),36))
baseO=add('Base_EarMount_ThrustSupport',base,'fixed')
wear=cy(32,1,0,0,36).cut(cy(27.5,2,0,0,35.5))
for a in [0,120,240]:wear=wear.cut(cy(.9,2,30*math.cos(math.radians(a)),30*math.sin(math.radians(a)),35.5))
add('Pan_Replaceable_ThrustRing',wear,'fixed')
for n,g in [('PanServo_ASSUMED','fixed'),('TiltServo_ASSUMED','pan')]:add(n.replace('_ASSUMED','_SG90_Reference'),old[n],g,False,(.15,.25,.75))
# Positive keyed horn profile (no spline). Original star exterior remains provisional.
def profile(h,z=0,clear=0):
 s=cy(P['horn_hub_radius']+clear,h,0,0,z)
 for ang,ln,wd in zip(P['horn_angles'],P['horn_lengths'],P['horn_widths']):
  arm=box(0,-wd/2-clear,z,ln+clear,wd+2*clear,h);arm.rotate(V(),V(0,0,1),ang);s=s.fuse(arm)
 return s.removeSplitter()
horn=profile(P['horn_thickness']).cut(cy(2.6,1.4)).cut(cy(.95,3,0,0,-.1)).removeSplitter()
panHornP=A.Placement(V(0,0,35),A.Rotation());tiltHornP=A.Placement(V(-41,0,78),A.Rotation(V(0,1,0),90))
add('Pan_OriginalStar_PROVISIONAL',moved(horn,panHornP),'pan',False)
add('Tilt_OriginalStar_PROVISIONAL',moved(horn,tiltHornP),'tilt',False)
for n,g in [('PanOriginalScrew_PROVISIONAL','pan'),('TiltOriginalScrew_PROVISIONAL','tilt')]:add(n,old[n],g,False)
# Carrier platform retains original pan mount and output center.
platform=old['PanYoke'].common(box(-80,-40,37,130,80,4)).fuse(cy(35.3,4,0,0,37))
platform=platform.fuse(cy(35.3,4,0,0,33).cut(cy(32.3,6,0,0,32)))
platform=platform.fuse(cy(16,2.2,0,0,35)).cut(profile(2.3,35,P['horn_pocket_clearance']))
platform=platform.cut(cy(4,12,0,0,32))
for x,y in [(18,0),(-18,0),(0,18),(0,-18)]:platform=platform.cut(cy(1.65,12,x,y,32)).cut(cy(3.5,4,x,y,39))
# New left wall allows complete ear passage during staged motor installation.
left=box(-51,-24,41,8,48,62).cut(box(-52,-6.5,55.8,10,13,33.5))
left=left.cut(cy(20.1,6,-47.3,0,78,(1,0,0)).cut(cy(9.9,7,-48,0,78,(1,0,0))))
# Ear ledge: canonical holes transformed to worldZ58.95/86.15; captive small nuts.
tplate=box(-56.6,-9,54,2.5,18,37)
for z in [58.95,86.15]:
 tplate=tplate.fuse(cy(2.8,1.6,-58.2,0,z,(1,0,0)))
 tplate=tplate.cut(moved(hexsolid(3.45,1.8),A.Placement(V(-58.3,0,z),A.Rotation(V(0,0,1),V(1,0,0)))))
 tplate=tplate.cut(cy(.95,6,-59,0,z,(1,0,0)))
tplate=tplate.cut(box(-59,-6.4,60.9,6,12.8,23.3));left=left.fuse(tplate)
for yy in [-9,6.5]:
 for zz in [54,88]:left=left.fuse(box(-56.6,yy,zz,13.6,2.5,3))
right=box(36.5,-21,41,2.5,42,57).cut(cy(2.6,5,35.5,0,78,(1,0,0)))
yoke=add('PanYoke_EarBracket_KeyedDrive',platform.fuse(left).fuse(right),'pan')
# Axial covers, with captive nuts, carry no friction-only torque demand.
pc=cy(24,1.5,0,0,33.5).cut(cy(4,8,0,0,29))
for x,y in [(18,0),(-18,0),(0,18),(0,-18)]:
 pc=pc.fuse(cy(4.7,2.7,x,y,30.8)).cut(moved(hexsolid(5.8,2.9),A.Placement(V(x,y,30.7),A.Rotation()))).cut(cy(1.65,7,x,y,29))
panCover=add('Pan_KeyedHorn_Cover',pc,'pan')
for i,(x,y) in enumerate([(18,0),(-18,0),(0,18),(0,-18)]):bolt('PanDrive_M3x10_'+str(i),(x,y,39),(0,0,-1),'pan')
# Keep original cradle/shelf datum; fill old friction slots with positive profiled carrier.
cr=old['TiltCameraCradle'].fuse(cy(21,4,-41,0,78,(1,0,0)))
cr=cr.cut(moved(profile(2.2,0,P['horn_pocket_clearance']),tiltHornP)).cut(cy(3.5,10,-42,0,78,(1,0,0)))
for y,z in [(15,78),(-15,78),(0,93),(0,63)]:cr=cr.cut(cy(1.65,10,-42,y,z,(1,0,0))).cut(cy(3.1,6,-37,y,z,(1,0,0)))
cr=cr.cut(cy(3,6,0,0,53)) # original pan screw service path after camera PCB removal
# New camera attachment frame atY=-24.4, outside tilt driver access corridors.
frame=box(-28,-24.4,54,7,3,44).fuse(box(21,-24.4,54,7,3,44)).fuse(box(-28,-24.4,54,56,3,4)).fuse(box(-28,-24.4,94,56,3,4))
def zslot(x,zlo,zhi,r,y0,h):return cy(r,h,x,y0,zlo,(0,1,0)).fuse(cy(r,h,x,y0,zhi,(0,1,0))).fuse(box(x-r,y0,zlo,2*r,h,zhi-zlo))
for x in [-24,24]:
 for lo,hi in [(60,66),(86,92)]:frame=frame.cut(zslot(x,lo,hi,1.7,-25,5))
cr=cr.fuse(box(-28,-24.4,54,56,4.4,3)).fuse(frame)
cradle=add('TiltCradle_KeyedHorn_CameraFrame',cr,'tilt')
tc=cy(21,1.5,-42.5,0,78,(1,0,0)).cut(cy(4,8,-47,0,78,(1,0,0)))
for y,z in [(15,78),(-15,78),(0,93),(0,63)]:
 tc=tc.fuse(cy(4.7,2.7,-45.2,y,z,(1,0,0))).cut(moved(hexsolid(5.8,2.9),A.Placement(V(-45.3,y,z),A.Rotation(V(0,0,1),V(1,0,0))))).cut(cy(1.65,9,-48,y,z,(1,0,0)))
add('Tilt_KeyedHorn_CaptiveCover',tc,'tilt')
for i,(y,z) in enumerate([(15,78),(-15,78),(0,93),(0,63)]):bolt('TiltDrive_M3x10_'+str(i),(-37,y,z),(-1,0,0),'tilt')
# Rotating journal sleeve: bolt threads no longer run against the stationary wall.
bush=cy(2.5,2.5,36.5,0,78,(1,0,0)).fuse(cy(3.5,.5,36,0,78,(1,0,0))).cut(cy(1.6,5,35,0,78,(1,0,0)))
add('Tilt_Journal_FlangedSleeve',bush,'tilt');bolt('TiltIdler_M3x12',(33,0,78),(1,0,0),'tilt',length=12,grip=6,nutH=4)
# Ear fasteners: M1.6, not M3. Washers on the ORIGINAL ear faces; small nuts captive in ledges.
for i,x in enumerate([-8.15,19.05]):bolt('PanEar_M1p6x8_'+str(i),(x,0,24.9),(0,0,-1),'fixed',diam=1.6,length=8,grip=5.5,headD=3,headH=1.6,nutAF=3.2,nutH=1.3,washer=True)
for i,z in enumerate([58.95,86.15]):bolt('TiltEar_M1p6x8_'+str(i),(-51.1,0,z),(-1,0,0),'pan',diam=1.6,length=8,grip=5.5,headD=3,headH=1.6,nutAF=3.2,nutH=1.3,washer=True)
# Live native camera pitch: rail placement, PCB holes and all four fasteners/spacers follow expressions.
for row,sg in [('Lower',-1),('Upper',1)]:
 rail=box(-28,-27.4,-3,56,3,6)
 for sign in [-1,1]:
  lo,hi=(10,16) if sign>0 else (-16,-10)
  cut=cy(1.2,5,lo,-28,0,(0,1,0)).fuse(cy(1.2,5,hi,-28,0,(0,1,0))).fuse(box(lo,-28,-1.2,hi-lo,5,2.4));rail=rail.cut(cut)
 for x in [-24,24]:rail=rail.cut(cy(1.7,5,x,-28,0,(0,1,0)))
 o=add('Camera_SlidingRail_'+row,rail,'tilt');o.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sg>0 else '-')+' RepairParameters.CameraPitchZ / 2')
 z=P['camera_center_z']+sg*P['camera_pitch_z']/2
 for i,x in enumerate([-24,24]):bolt('RailMount_'+row+'_M3x10_'+str(i),(x,-27.4,z),(0,1,0),'tilt',grip=6)
 for col,sx in [('Left',-1),('Right',1)]:
  x=sx*P['camera_pitch_x']/2
  spacer=cy(2.5,3,0,-30.4,0,(0,1,0)).cut(cy(1.2,5,0,-31,0,(0,1,0)))
  sp=add('PCB_Spacer_'+row+'_'+col,spacer,'tilt');sp.setExpression('Placement.Base.x',('' if sx>0 else '-')+'RepairParameters.CameraPitchX / 2');sp.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sg>0 else '-')+' RepairParameters.CameraPitchZ / 2')
  bo=bolt('Camera_M2x12_'+row+'_'+col,(0,-32,0),(0,1,0),'tilt',diam=2,length=12,grip=7.6,headD=4,headH=2,nutAF=4,nutH=1.6)
  bo.setExpression('Placement.Base.x',('' if sx>0 else '-')+'RepairParameters.CameraPitchX / 2');bo.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sg>0 else '-')+' RepairParameters.CameraPitchZ / 2')
  joints[-1]['under_head']=[x,-32,z]
# Native four-hole PCB; no claim default28mm pitch belongs to actual camera.
pcb=d.addObject('Part::Box','CameraPCB_Blank');pcb.Length=P['camera_width'];pcb.Width=P['camera_pcb_thickness'];pcb.Height=P['camera_height'];pcb.Placement.Base=V(-P['camera_width']/2,-32,P['camera_center_z']-P['camera_height']/2)
cur=pcb
for sx in [-1,1]:
 for sz in [-1,1]:
  h=d.addObject('Part::Cylinder','PCB_Hole');h.Radius=P['camera_hole_diameter']/2;h.Height=3;h.Placement=A.Placement(V(0,-32.5,0),A.Rotation(V(0,0,1),V(0,1,0)));h.setExpression('Placement.Base.x',('' if sx>0 else '-')+'RepairParameters.CameraPitchX / 2');h.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sz>0 else '-')+' RepairParameters.CameraPitchZ / 2')
  cut=d.addObject('Part::Cut','PCB_Cut');cut.Base=cur;cut.Tool=h;cur=cut
cur.Label='Camera four-hole PCB - PROVISIONAL';hardware.append(cur);groups[cur.Name]='tilt'
add('Camera_RearComponents_KEEP_OUT',box(-10,-30.4,66,20,24.4,20),'tilt',False,(.15,.16,.17))
add('Camera_Lens_PROVISIONAL',cy(7,10,0,-42,76,(0,1,0)),'tilt',False,(.15,.16,.17))
# Wire exit keep-outs only; unknown flexible interconnects remain a physical verification item.
add('PanServo_WireExit_KEEP_OUT',box(-36,-1.7,10.55,30.15,3.4,1.1),'fixed',False,(.9,.5,.1))
add('TiltServo_WireExit_KEEP_OUT',box(-65.45,-1.7,83.85,1.1,3.4,18.15),'pan',False,(.9,.5,.1))
add('Camera_WireExit_KEEP_OUT',cy(1.5,18,0,-6,84,(0,1,0)),'tilt',False,(.9,.5,.1))
d.recompute()
# Hide all Boolean operands, leaving only actual component objects visible.
for o in d.Objects:
 if A.GuiUp and hasattr(o,'Shape'):o.Visibility=o in parts+hardware
for o in parts+hardware:
 if A.GuiUp and o in hardware and o==cur:o.ViewObject.ShapeColor=(.12,.4,.16)
json.dump(joints,open(os.path.join(R,'checks','fastener_stacks.json'),'x'),indent=2)
# All component solids are checked; compound hardware includes separate nut and washer solids.
solid={o.Name:{'valid':o.Shape.isValid(),'solids':len(o.Shape.Solids),'volume':o.Shape.Volume} for o in parts+hardware}
json.dump(solid,open(os.path.join(R,'checks','solids.json'),'x'),indent=2)
# Explicit pair classification. Designed contacts are not exempt from positive-volume testing.
expected={frozenset(['Base_EarMount_ThrustSupport','Pan_Replaceable_ThrustRing']):'static keyed bearing ring',frozenset(['Pan_Replaceable_ThrustRing','PanYoke_EarBracket_KeyedDrive']):'sliding thrust face',frozenset(['Tilt_Journal_FlangedSleeve','TiltCradle_KeyedHorn_CameraFrame']):'sleeve flange against rotor',frozenset(['Tilt_Journal_FlangedSleeve','PanYoke_EarBracket_KeyedDrive']):'journal with radial clearance'}
obs=parts+hardware;neutral=[];touch=[]
for i,a in enumerate(obs):
 for b in obs[i+1:]:
  aa,bb=a.Shape.BoundBox,b.Shape.BoundBox
  overlap=all(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))>1e-7 for t in ['X','Y','Z'])
  if overlap:
   vol=a.Shape.common(b.Shape).Volume
   if vol>.001:neutral.append({'pair':[a.Name,b.Name],'volume_mm3':vol,'class':'UNINTENDED penetration (no overlap whitelist)'})
  if frozenset([a.Name,b.Name]) in expected:touch.append({'pair':[a.Name,b.Name],'kind':expected[frozenset([a.Name,b.Name])],'distance_mm':a.Shape.distToShape(b.Shape)[0]})
json.dump({'unintended':neutral,'designed_contacts':touch},open(os.path.join(R,'checks','neutral_pairs.json'),'x'),indent=2)
d.addObject('App::DocumentObjectGroup','Verification_HOLD').Label='HOLD: hardware reference dimensions and camera pitch unmeasured; no production approval'
d.License='CreativeCommons Attribution-ShareAlike';d.LicenseURL='https://creativecommons.org/licenses/by-sa/4.0/';d.Comment='SG90 references adapted from Juan Fenoy / FreeCAD-library. Audit authority sg90_interface_audit_01. No spline definition or physical-fit certification.'
d.recompute();d.saveAs(os.path.join(R,'EyeTrace_Repair.FCStd'))
json.dump({'printed':[o.Name for o in parts],'hardware':[o.Name for o in hardware],'groups':groups,'camera_pcb_name':cur.Name},open(os.path.join(R,'component_manifest.json'),'x'),indent=2)
print('PRINT PARTS',len(parts),'COMPONENTS',len(obs),'SOLID FAILS',[n for n,v in solid.items() if not v['valid'] or v['solids']==0]);print('NEUTRAL',json.dumps(neutral));print('CONTACTS',touch)
