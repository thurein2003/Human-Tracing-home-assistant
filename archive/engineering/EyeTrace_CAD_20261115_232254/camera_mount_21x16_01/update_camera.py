import os,json,hashlib,math,csv
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
H=os.path.dirname(os.path.abspath(__file__));S=os.path.join(os.path.dirname(H),'sg90_interface_repair_01')
for n in ['parts','checks','renders','coupons']:os.makedirs(os.path.join(H,n),exist_ok=False)
d=A.openDocument(os.path.join(S,'EyeTrace_Repair_Assembly.FCStd'));original={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'KinematicGroup')}
p=d.getObject('RepairParameters');p.CameraPitchX=21;p.CameraPitchZ=16
for n,v in [('CameraPCBWidth',38),('CameraPCBHeight',38),('CameraPCBThickness',1.6),('CameraPCBMountHoleDiameter',2.2),('CameraPlateHoleDiameter',2.4),('CameraLensEnvelopeDiameter',14),('CameraLensProjection',10),('CameraLensClearanceDiameter',18),('CameraLensOffsetX',0),('CameraLensOffsetZ',0)]:p.addProperty('App::PropertyLength',n);setattr(p,n,v)
p.addProperty('App::PropertyString','HoleSpacingSource');p.HoleSpacingSource='USER supplied nominal: horizontal21mm, vertical16mm CENTER-TO-CENTER; NOT PCB outside size'
p.Verification='Hole spacing user supplied; PCB size, diameters, lens and rear keep-outs remain UNVERIFIED'
blank=d.getObject('CameraPCB_Blank')
for prop,ex in [('Length','RepairParameters.CameraPCBWidth'),('Width','RepairParameters.CameraPCBThickness'),('Height','RepairParameters.CameraPCBHeight'),('Placement.Base.x','-RepairParameters.CameraPCBWidth / 2'),('Placement.Base.z','RepairParameters.CameraCenterZ - RepairParameters.CameraPCBHeight / 2')]:blank.setExpression(prop,ex)
for o in d.Objects:
 if o.Name.startswith('PCB_Hole'):o.setExpression('Radius','RepairParameters.CameraPCBMountHoleDiameter / 2')
# Camera support geometry is changed; other mechanism parts are retained from the saved assembly.
cr=d.getObject('TiltCradle_KeyedHorn_CameraFrame')
def cy(r,h,x,y,z):return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))
for x in [-24,24]:
 for lo,hi in [(60,68),(84,92)]:
  slot=cy(1.7,5,x,-25,lo).fuse(cy(1.7,5,x,-25,hi)).fuse(Part.makeBox(3.4,5,hi-lo,V(x-1.7,-25,lo)))
  cr.Shape=cr.Shape.cut(slot).removeSplitter()
for n in ['Camera_SlidingRail_Lower','Camera_SlidingRail_Upper']:d.removeObject(n)
# Fixed 21x16 camera plate: four PCB clearance holes + four separate M3 frame holes.
plate=d.addObject('Part::Box','CameraPlate_Blank');plate.Length=56;plate.Width=3;plate.Placement.Base=V(-28,-27.4,0)
plate.setExpression('Height','RepairParameters.CameraPitchZ + 16 mm');plate.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ - RepairParameters.CameraPitchZ / 2 - 8 mm')
cur=plate
lens=d.addObject('Part::Cylinder','PlateLensClearance');lens.Height=5;lens.Placement=A.Placement(V(0,-28,0),A.Rotation(V(0,0,1),V(0,1,0)));lens.setExpression('Radius','RepairParameters.CameraLensClearanceDiameter / 2');lens.setExpression('Placement.Base.x','RepairParameters.CameraLensOffsetX');lens.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ + RepairParameters.CameraLensOffsetZ')
cut=d.addObject('Part::Cut','CameraPlate_LensCut');cut.Base=cur;cut.Tool=lens;cur=cut
for sx in [-1,1]:
 for sz in [-1,1]:
  h=d.addObject('Part::Cylinder','PlatePCB_Hole');h.Height=5;h.Placement=A.Placement(V(0,-28,0),A.Rotation(V(0,0,1),V(0,1,0)));h.setExpression('Radius','RepairParameters.CameraPlateHoleDiameter / 2');h.setExpression('Placement.Base.x',('' if sx>0 else '-')+'RepairParameters.CameraPitchX / 2');h.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sz>0 else '-')+' RepairParameters.CameraPitchZ / 2')
  cut=d.addObject('Part::Cut','CameraPlate_Cut');cut.Base=cur;cut.Tool=h;cur=cut
for x in [-24,24]:
 for sz in [-1,1]:
  h=d.addObject('Part::Cylinder','PlateFrame_Hole');h.Radius=1.7;h.Height=5;h.Placement=A.Placement(V(x,-28,0),A.Rotation(V(0,0,1),V(0,1,0)));h.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ '+('+' if sz>0 else '-')+' RepairParameters.CameraPitchZ / 2')
  cut=d.addObject('Part::Cut','CameraPlate_Cut');cut.Base=cur;cut.Tool=h;cur=cut
cur.Label='Camera mounting plate -21x16mm HOLE CENTERS';cur.addProperty('App::PropertyString','KinematicGroup');cur.KinematicGroup='tilt';cur.addProperty('App::PropertyBool','Printable');cur.Printable=True;cur.addProperty('App::PropertyString','FitStatus');cur.FitStatus='User nominal center spacing21x16; diameters/lens/PCB and physical fit UNVERIFIED';d.getObject('PrintedComponents').addObject(cur)
# Keep lens size independent and genuinely editable in the native file.
d.removeObject('Camera_Lens_PROVISIONAL');le=d.addObject('Part::Cylinder','Camera_Lens_PROVISIONAL');le.setExpression('Radius','RepairParameters.CameraLensEnvelopeDiameter / 2');le.setExpression('Height','RepairParameters.CameraLensProjection');le.Placement=A.Placement(V(0,0,0),A.Rotation(V(0,0,1),V(0,1,0)));le.setExpression('Placement.Base.x','RepairParameters.CameraLensOffsetX');le.setExpression('Placement.Base.y','-32 mm - RepairParameters.CameraLensProjection');le.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ + RepairParameters.CameraLensOffsetZ');le.addProperty('App::PropertyString','KinematicGroup');le.KinematicGroup='tilt';le.addProperty('App::PropertyBool','Printable');le.Printable=False;d.getObject('HardwareReferences').addObject(le)
keep=d.getObject('Camera_RearComponents_KEEP_OUT');keep.addProperty('App::PropertyString','CollisionRole');keep.CollisionRole='UNVERIFIED_REAR_COMPONENT_ENVELOPE';keep.Label='UNKNOWN rear-component envelope - NOT measured camera geometry'
d.recompute();obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable]
for o in d.Objects:
 if hasattr(o,'Shape'):o.Visibility=o in obs
cur.ViewObject.ShapeColor=(.9,.5,.15);le.ViewObject.ShapeColor=(.08,.09,.1);keep.ViewObject.Transparency=80
# Critical geometry alignment, read from saved shapes rather than only properties.
def centers(obj,r):return sorted(set((round(f.Surface.Center.x,5),round(f.Surface.Center.z-76,5)) for f in obj.Shape.Faces if type(f.Surface).__name__=='Cylinder' and abs(f.Surface.Radius-r)<1e-6 and abs(f.Surface.Axis.y)>.999))
expected=sorted([(x,z) for x in [-10.5,10.5] for z in [-8,8]])
pcb=d.getObject('PCB_Cut003');assert centers(cur,1.2)==expected and centers(pcb,1.1)==expected
align={'user_nominal_hole_center_spacing_mm':[21,16],'expected_offsets_from_pattern_center_XZ_mm':expected,'plate_measured_hole_centers_XZ_mm':centers(cur,1.2),'pcb_measured_hole_centers_XZ_mm':centers(pcb,1.1),'pcb_outside_dimensions_mm':[blank.Length.Value,blank.Height.Value,blank.Width.Value],'pcb_outside_status':'UNVERIFIED independent assumptions, NOT21x16','pcb_hole_diameter_mm':2.2,'plate_clearance_hole_diameter_mm':2.4,'lens_envelope_diameter_mm':14,'lens_clearance_diameter_mm':18,'lens_projection_mm':10,'non_pitch_hardware_dimensions_status':'UNVERIFIED','frame_slot_vertical_pitch_range_mm':[16,32]}
for row,sg in [('Lower',-1),('Upper',1)]:
 for col,sx in [('Left',-1),('Right',1)]:
  for pref in ['PCB_Spacer_','Camera_M2x12_']:
   bb=d.getObject(pref+row+'_'+col).Shape.BoundBox;assert abs((bb.XMin+bb.XMax)/2-sx*10.5)<1e-6 and abs((bb.ZMin+bb.ZMax)/2-(76+sg*8))<1e-6
json.dump(align,open(os.path.join(H,'checks','camera_alignment.json'),'x'),indent=2)
# Prove unrelated mechanism geometry is retained exactly.
changes={}
for n,s in original.items():
 o=d.getObject(n)
 if not o:changes[n]='replaced by fixed camera plate';continue
 delta=s.cut(o.Shape).Volume+o.Shape.cut(s).Volume
 if delta>.001:changes[n]=delta
json.dump(changes,open(os.path.join(H,'checks','changed_geometry.json'),'x'),indent=2)
# Unknown old component box is retained, not silently shrunk to hide warnings.
def vol(a,b):
 aa,bb=a.BoundBox,b.BoundBox
 if any(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))<=1e-7 for t in ['X','Y','Z']):return 0
 return a.common(b).Volume
cache={};unint=[];uncertain={};count=0
for pa in range(-60,61,10):
 for ta in range(-30,31,5):
  ss={}
  for o in obs:
   s=o.Shape.copy()
   if o.KinematicGroup=='tilt':s.rotate(V(0,0,78),V(1,0,0),ta)
   if o.KinematicGroup!='fixed':s.rotate(V(),V(0,0,1),pa)
   ss[o.Name]=s
  for i,a in enumerate(obs):
   for b in obs[i+1:]:
    count+=1;ga,gb=a.KinematicGroup,b.KinematicGroup;rel=(0,0) if ga==gb else ((0,ta) if 'fixed' not in [ga,gb] else (pa,ta if 'tilt' in [ga,gb] else 0));key=(a.Name,b.Name,rel)
    if key not in cache:cache[key]=vol(ss[a.Name],ss[b.Name])
    v=cache[key]
    if v>.001:
     item={'pair':[a.Name,b.Name],'volume_mm3':v,'pose':[pa,ta]}
     if keep in [a,b]:uncertain[(a.Name,b.Name)]=item
     else:unint.append(item)
report={'poses':169,'component_pair_tests':count,'modeled_components':len(obs),'unintended_nominal_hardware_penetrations':unint,'unverified_rear_envelope_conflicts':list(uncertain.values()),'rear_envelope_classification':'Existing unmeasured placeholder retained as UNCERTAINTY, not asserted solid camera material. These conflicts REQUIRE physical rear-clearance verification, not an automatic PASS.','physical_fit':'UNVERIFIED'}
json.dump(report,open(os.path.join(H,'checks','collision_motion.json'),'x'),indent=2)
d.recompute();d.saveAs(os.path.join(H,'EyeTrace_Camera_21x16.FCStd'));Part.export(obs,os.path.join(H,'EyeTrace_Camera_21x16.step'))
# Export every printable part to keep a complete consistent revision, without altering the original assembly.
meshchecks={}
for o in parts:
 s=o.Shape;assert s.isValid() and len(s.Solids)==1
 pp=s.copy()
 if o.Name.startswith(('TiltCradle','Tilt_KeyedHorn')):pp.rotate(V(),V(0,1,0),90)
 elif o.Name.startswith('Tilt_Journal'):pp.rotate(V(),V(0,1,0),-90)
 elif o.Name.startswith('Pan_KeyedHorn'):pp.rotate(V(),V(1,0,0),180)
 elif o==cur or o.Name.startswith('PCB_Spacer'):pp.rotate(V(),V(1,0,0),90)
 bb=pp.BoundBox;pp.translate(V(-bb.XMin,-bb.YMin,-bb.ZMin));m=MeshPart.meshFromShape(Shape=pp,LinearDeflection=.08,AngularDeflection=.15,Relative=False);path=os.path.join(H,'parts',o.Name+'.stl');m.write(path);r=Mesh.Mesh(path)
 q={'closed':r.isSolid(),'components':r.countComponents(),'nonmanifold':r.hasNonManifolds(),'self_intersections':r.hasSelfIntersections(),'bad_normals':r.hasNonUniformOrientedFacets(),'brep_valid':s.isValid()};assert q['closed'] and q['components']==1 and not q['self_intersections'] and not q['nonmanifold'] and not q['bad_normals'],o.Name
 meshchecks[o.Name]=q;Part.export([o],os.path.join(H,'parts',o.Name+'.step'))
# Small true21x16 fit gauge; outside size is independently30x25, NOT PCB size.
gauge=Part.makeBox(30,25,1.5,V(-15,-12.5,0))
for x in [-10.5,10.5]:
 for z in [-8,8]:gauge=gauge.cut(Part.makeCylinder(1.2,3,V(x,z,-.5)))
gauge=gauge.cut(Part.makeCylinder(4,3,V(0,0,-.5)))
gm=MeshPart.meshFromShape(Shape=gauge,LinearDeflection=.06,AngularDeflection=.15,Relative=False);path=os.path.join(H,'coupons','Camera_HoleCenters_21x16_Gauge.stl');gm.write(path);gr=Mesh.Mesh(path);assert gr.isSolid() and not gr.hasSelfIntersections();meshchecks['camera_gauge']={'closed':gr.isSolid(),'components':gr.countComponents(),'self_intersections':gr.hasSelfIntersections(),'outside_size_mm':[30,25],'hole_center_spacing_mm':[21,16],'hole_diameter_mm':2.4}
json.dump(meshchecks,open(os.path.join(H,'checks','mesh_validation.json'),'x'),indent=2)
print('ALIGNMENT',align);print('MOTION unintended',len(unint),'unknown rear conflicts',len(uncertain),'pairs',count,'PRINT PARTS',len(parts));print('CHANGES',changes)
