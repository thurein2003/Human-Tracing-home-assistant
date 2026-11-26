from pathlib import Path
import json,sys,math
import FreeCAD as A,Part
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];p=json.loads((r/'CAD/parameters.json').read_text());d=A.openDocument(str(r/'CAD/SOURCE_SNAPSHOT/Integrated_Source.FCStd'));pr=d.getObject('RepairParameters')
assert p['camera_hole_spacing_mm']==[21,16],'User hole pattern is locked at nominal21x16'
for prop,key in [('CameraPCBWidth','camera_pcb_width_mm'),('CameraPCBHeight','camera_pcb_height_mm'),('CameraPCBThickness','camera_pcb_thickness_mm'),('CameraPCBMountHoleDiameter','camera_hole_diameter_mm'),('CameraLensEnvelopeDiameter','lens_envelope_diameter_mm'),('CameraLensProjection','lens_projection_mm'),('CameraLensClearanceDiameter','lens_clearance_diameter_mm'),('CameraLensOffsetX','lens_offset_x_mm'),('CameraLensOffsetZ','lens_offset_z_mm')]:setattr(pr,prop,p[key])
for prop,val in zip(['RibbonReserveWidth','RibbonReserveThickness','RibbonReserveLength'],p['ribbon_reservation_width_thickness_length_mm']):setattr(pr,prop,val)
# Replace only a fixed reference box by an expression-driven box; same default BRep.
old=d.getObject('Camera_RearComponents_KEEP_OUT');oldshape=old.Shape.copy();d.removeObject(old.Name)
for prop,val in zip(['RearEnvelopeWidth','RearEnvelopeDepth','RearEnvelopeHeight'],p['rear_component_envelope_mm']):
 pr.addProperty('App::PropertyLength',prop);setattr(pr,prop,val)
for prop,val in zip(['RearEnvelopeCenterX','RearEnvelopeCenterZ'],p['rear_envelope_center_x_z_mm']):
 pr.addProperty('App::PropertyDistance',prop);setattr(pr,prop,val)
rear=d.addObject('Part::Box','Camera_RearComponents_KEEP_OUT')
for prop,expr in [('Length','RearEnvelopeWidth'),('Width','RearEnvelopeDepth'),('Height','RearEnvelopeHeight')]:rear.setExpression(prop,'RepairParameters.'+expr)
rear.setExpression('Placement.Base.x','RepairParameters.RearEnvelopeCenterX - RepairParameters.RearEnvelopeWidth / 2');rear.setExpression('Placement.Base.z','RepairParameters.RearEnvelopeCenterZ - RepairParameters.RearEnvelopeHeight / 2');rear.Placement.Base.y=-30.4
for prop,typ,val in [('KinematicGroup','App::PropertyString','tilt'),('Printable','App::PropertyBool',False),('CollisionRole','App::PropertyString','UNVERIFIED_REAR_COMPONENT_ENVELOPE')]:rear.addProperty(typ,prop);setattr(rear,prop,val)
rear.Label='UNKNOWN rear camera envelope - parameterized, physical evidence required';d.getObject('HardwareReferences').addObject(rear)
# Live camera standoff and screw-stack parameters, independently editable from hole pitch.
for prop,key in [('CameraStandoffHeight','camera_standoff_height_mm'),('CameraStandoffOuterDiameter','camera_standoff_outer_diameter_mm'),('CameraMountScrewLength','camera_mount_screw_length_mm')]:
 pr.addProperty('App::PropertyLength',prop);setattr(pr,prop,p[key])
pr.CameraPlateHoleDiameter=p['camera_plate_hole_diameter_mm']
blank=d.getObject('CameraPCB_Blank');blank.setExpression('Placement.Base.y','-27.4 mm - RepairParameters.CameraStandoffHeight - RepairParameters.CameraPCBThickness')
for o in d.Objects:
 if o.Name.startswith('PCB_Hole'):
  o.setExpression('Height','RepairParameters.CameraPCBThickness + 2 mm');o.setExpression('Placement.Base.y','-28.4 mm - RepairParameters.CameraStandoffHeight - RepairParameters.CameraPCBThickness')
d.getObject('Camera_Lens_PROVISIONAL').setExpression('Placement.Base.y','-27.4 mm - RepairParameters.CameraStandoffHeight - RepairParameters.CameraPCBThickness - RepairParameters.CameraLensProjection')
rear.setExpression('Placement.Base.y','-27.4 mm - RepairParameters.CameraStandoffHeight')
def hexnut(af,h,z):
 rr=af/math.sqrt(3);pts=[V(rr*math.cos(math.radians(30+60*i)),rr*math.sin(math.radians(30+60*i)),z) for i in range(6)];return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(0,0,h))
st=p['camera_standoff_height_mm'];t=p['camera_pcb_thickness_mm'];yy=-27.4-st-t;grip=st+t+3
assert st>0 and p['camera_mount_screw_length_mm']>=grip+1.6+1,'Camera screw must clear stack/nut with at least1mm nominal projection'
for o in d.Objects:
 if o.Name.startswith('PCB_Spacer_'):
  sp=Part.makeCylinder(p['camera_standoff_outer_diameter_mm']/2,st,V(0,-27.4-st,0),V(0,1,0)).cut(Part.makeCylinder(p['camera_plate_hole_diameter_mm']/2,st+2,V(0,-28.4-st,0),V(0,1,0)));o.Shape=sp
 if o.Name.startswith('Camera_M2x12_'):
  shaft=Part.makeCylinder(1,p['camera_mount_screw_length_mm']).fuse(Part.makeCylinder(2,2,V(0,0,-2)));nut=hexnut(4,1.6,grip).cut(Part.makeCylinder(1,2.6,V(0,0,grip-.2)));comp=Part.makeCompound([shaft,nut]);comp.Placement=A.Placement(V(0,yy,0),A.Rotation(V(0,0,1),V(0,1,0)));o.Shape=comp;o.Label='Camera M2x%g provisional screw/nut'%p['camera_mount_screw_length_mm']

# Retain source mechanical design. Rebuild horn and positive pockets from provisional or measured profile.
def profile(angles,lengths,widths,hub,h,z=0,clear=0):
 s=Part.makeCylinder(hub+clear,h,V(0,0,z))
 for ang,ln,wd in zip(angles,lengths,widths):
  arm=Part.makeBox(ln+clear,wd+2*clear,h,V(0,-wd/2-clear,z));arm.rotate(V(),V(0,0,1),ang);s=s.fuse(arm)
 return s.removeSplitter()
args=[p['horn_arm_angles_deg'],p['horn_arm_lengths_mm'],p['horn_arm_widths_mm'],p['horn_hub_radius_mm']];assert len(args[0])==len(args[1])==len(args[2])
def moved(s,pl):s=s.copy();s.Placement=pl.multiply(s.Placement);return s
oldargs=[[0,72,144,216,288],[12]*5,[3.6]*5,4]
for name,carrier,pl in [('Pan_OriginalStar_PROVISIONAL','PanYoke_EarBracket_KeyedDrive',A.Placement(V(0,0,35),A.Rotation())),('Tilt_OriginalStar_PROVISIONAL','TiltCradle_KeyedHorn_CameraFrame',A.Placement(V(-41,0,78),A.Rotation(V(0,1,0),90)))]:
 h=profile(*args,p['horn_web_thickness_mm']).cut(Part.makeCylinder(p['horn_socket_envelope_diameter_mm']/2,p['horn_socket_envelope_depth_mm'])).cut(Part.makeCylinder(p['horn_clearance_bore_mm']/2,10,V(0,0,-1))).removeSplitter();d.getObject(name).Shape=moved(h,pl)
 oldpocket=moved(profile(*oldargs,2.3 if name.startswith('Pan') else 2.2,clear=.25),pl)
 newpocket=moved(profile(*args,p['horn_pocket_depth_mm']+.1 if name.startswith('Pan') else p['horn_pocket_depth_mm'],clear=p['horn_pocket_clearance_mm']),pl)
 c=d.getObject(carrier);c.Shape=c.Shape.fuse(oldpocket).cut(newpocket)
 if name.startswith('Pan'):c.Shape=c.Shape.cut(Part.makeCylinder(4,12,V(0,0,32)))
 else:c.Shape=c.Shape.cut(Part.makeCylinder(3.5,10,V(-42,0,78),V(1,0,0)))
 c.Shape=c.Shape.removeSplitter()
 # Parametric data lives in native document and portable JSON; rebuild required for profile edits.
 if not hasattr(c,'HornProfileParameters'):c.addProperty('App::PropertyString','HornProfileParameters')
 c.HornProfileParameters=json.dumps({k:v for k,v in p.items() if k.startswith('horn_')})
 d.getObject(name).FitStatus='PROVISIONAL original star outline and smooth socket; not a spline specification'
d.getObject('Verification_HOLD').Label='FINAL ENGINEERING - FIT TEST READY; FULL PRINT HOLD'
d.getObject('IntegrationRecord').ReleaseStatus='CAD verified nominal geometry; physical fit and rear/cable uncertainty HOLD'
d.recompute();obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')]
for o in obs:assert o.Shape.isValid() and len(o.Shape.Solids)>0,o.Name
src=A.openDocument(str(r/'CAD/SOURCE_SNAPSHOT/Integrated_Source.FCStd'));deltas={}
for o in obs:
 q=src.getObject(o.Name);dv=o.Shape.cut(q.Shape).Volume+q.Shape.cut(o.Shape).Volume
 if dv>.001:deltas[o.Name]=dv
# Default parameters must preserve inherited mechanically reviewed assembly.
if p==json.loads((r/'CAD/SOURCE_SNAPSHOT/default_parameters.json').read_text()):assert not deltas,('unexpected default geometry change',deltas)
d.recompute();d.saveAs(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'))
(r/'TESTS/results/final_generation.json').write_text(json.dumps({'native_valid':True,'component_count':len(obs),'printed_count':sum(o.Printable for o in obs),'default_source_shape_differences_mm3':deltas,'parameterization':'Rear box now live; horn and pocket shapes rebuild from JSON; no change to nominal BReps','version':A.Version()[:3]},indent=2))
print('Final editable49 component assembly generated; default geometric deltas',deltas)
