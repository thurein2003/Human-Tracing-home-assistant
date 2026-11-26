import os,json,hashlib,math
import FreeCAD as A,Part
from FreeCAD import Vector as V
H=os.path.dirname(os.path.abspath(__file__));B=os.path.join(os.path.dirname(H),'EyeTrace_CAD_20261115_232254');W=os.path.join(H,'work_02');os.makedirs(W,exist_ok=False);os.makedirs(os.path.join(W,'checks'))
# Freeze all earlier project artifacts, not only selected source files.
prior={}
for root,ds,fs in os.walk(B):
 for n in fs:
  p=os.path.join(root,n);prior[os.path.relpath(p,B)]=hashlib.sha256(open(p,'rb').read()).hexdigest()
json.dump(prior,open(os.path.join(W,'checks','prior_artifacts_before.json'),'x'),indent=2)
paths={'camera':os.path.join(B,'camera_mount_21x16_01','validated','EyeTrace_Camera_21x16_Reviewed.FCStd'),'repair':os.path.join(B,'sg90_interface_repair_01','EyeTrace_Repair_Assembly.FCStd'),'reference':os.path.join(B,'sg90_reference_revision_02','EyeTrace_SG90_Reference_01.FCStd')}
d=A.openDocument(paths['camera']);repair=A.openDocument(paths['repair']);ref=A.openDocument(paths['reference']);A.setActiveDocument(d.Name)
old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'KinematicGroup')};mapdata={}
for n,source in [('PanServo_SG90_Reference','PanServo_ASSUMED'),('TiltServo_SG90_Reference','TiltServo_ASSUMED')]:
 a=d.getObject(n).Shape;b=ref.getObject(source).Shape;v=a.cut(b).Volume+b.cut(a).Volume;assert v<.001;mapdata[n]={'source':'sg90_reference_revision_02','symmetric_difference_mm3':v}
for n in ['Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive','Pan_KeyedHorn_Cover','Tilt_KeyedHorn_CaptiveCover','Tilt_Removable_IdlerPillar','Tilt_Journal_FlangedSleeve','Pan_Replaceable_ThrustRing']:
 a=d.getObject(n).Shape;b=repair.getObject(n).Shape;v=a.cut(b).Volume+b.cut(a).Volume;assert v<.001;mapdata[n]={'source':'sg90_interface_repair_01','symmetric_difference_mm3':v}
mapdata['camera']={'source':'camera_mount_21x16_01','hole_pitch_mm':[21,16],'changes_retained':'Fixed four-hole plate and frame slots extended for16mm vertical spacing; PCB dimensions remain separate'}
p=d.getObject('RepairParameters');assert p.CameraPitchX.Value==21 and p.CameraPitchZ.Value==16
for n,v in [('RibbonReserveWidth',20),('RibbonReserveThickness',1),('RibbonReserveLength',18),('RibbonReserveCenterZ',84)]:p.addProperty('App::PropertyLength',n);setattr(p,n,v)
p.addProperty('App::PropertyString','RibbonReservationStatus');p.RibbonReservationStatus='Illustrative reserved space, NOT measured ribbon dimensions, connector position or bend radius'
# Retain the unknown rear box as uncertainty. Never trim it to manufacture a clearance PASS.
rear=d.getObject('Camera_RearComponents_KEEP_OUT');rear.CollisionRole='UNVERIFIED_REAR_COMPONENT_ENVELOPE'
d.removeObject('Camera_WireExit_KEEP_OUT');r=d.addObject('Part::Box','Camera_WireExit_KEEP_OUT');r.setExpression('Length','RepairParameters.RibbonReserveWidth');r.setExpression('Width','RepairParameters.RibbonReserveLength');r.setExpression('Height','RepairParameters.RibbonReserveThickness');r.setExpression('Placement.Base.x','-RepairParameters.RibbonReserveWidth / 2');r.Placement.Base.y=-6;r.setExpression('Placement.Base.z','RepairParameters.RibbonReserveCenterZ - RepairParameters.RibbonReserveThickness / 2');r.addProperty('App::PropertyString','KinematicGroup');r.KinematicGroup='tilt';r.addProperty('App::PropertyBool','Printable');r.Printable=False;r.addProperty('App::PropertyString','CollisionRole');r.CollisionRole='NOMINAL_RIBBON_SPACE_RESERVATION';r.Label='Ribbon clearance reservation20x18x1 - physical route UNVERIFIED';d.getObject('HardwareReferences').addObject(r)
record=d.addObject('App::DocumentObjectGroup','IntegrationRecord')
for n,v in [('SourceAuthority','sg90_interface_audit_01'),('CameraHoleSpacing','USER nominal21x16mm center-to-center, NOT PCB outside size'),('ReleaseStatus','HOLD: software checked candidate; actual clone/horn/camera/cable/PETG fit unverified'),('SourceRevisions','sg90_interface_repair_01;sg90_reference_revision_02;camera_mount_21x16_01')]:record.addProperty('App::PropertyString',n);setattr(record,n,v)
d.getObject('Verification_HOLD').Label='INTEGRATED CANDIDATE - PHYSICAL RELEASE HOLD'
for o in d.Objects:
 if o.Name.startswith('RailMount_'):o.Label=o.Name.replace('RailMount','CameraPlateMount')
 if hasattr(o,'KinematicGroup') and o.Printable:
  o.addProperty('App::PropertyString','PrintFileName');o.PrintFileName='CameraPlate_21x16' if o.Label.startswith('Camera mounting plate') else o.Name
obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];assert len(obs)==49
for o in d.Objects:
 if hasattr(o,'Shape') and A.GuiUp:o.Visibility=o in obs
d.recompute()
for o in obs:assert o.Shape.isValid()
d.recompute();d.Comment='Integrated retained Eye Trace geometry. Juan Fenoy SG90-derived references attributed CC BY-SA4.0. No exact spline or physical-fit certification.';d.saveAs(os.path.join(W,'Integrated_Snapshot.FCStd'))
# Check only intended integration change is the cable reservation, not accidental mechanism edits.
delta={}
for o in obs:
 if o.Name in old:
  v=old[o.Name].cut(o.Shape).Volume+o.Shape.cut(old[o.Name]).Volume
  if v>.001:delta[o.Name]=v
assert set(delta)<=set(['Camera_WireExit_KEEP_OUT'])
json.dump({'selected_sources':paths,'retained_geometry_checks':mapdata,'integration_geometry_changes':delta,'component_count':49,'printed_count':sum(o.Printable for o in obs),'original_star_status':'Provisional exterior; original factory spline kept physically; no teeth invented','ribbon_scope':'Flat exit reservation only; flexible loop, actual connector and minimum bend unknown'},open(os.path.join(W,'checks','integration_provenance.json'),'x'),indent=2)
print('Integrated49 components /13 printed parts; only ribbon reservation changed from corrected camera assembly. Source artifacts hashed:',len(prior))

