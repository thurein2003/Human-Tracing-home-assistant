import os,json,math,datetime
import FreeCAD as A,Part
from FreeCAD import Vector as V
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));W=os.path.join(H,'TESTS','results','attachment');W=W if not os.path.exists(W) else W+'_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S');os.makedirs(os.path.join(W,'checks'),exist_ok=False);d=A.openDocument(os.path.join(H,'CAD','EyeTrace_Final_Assembly.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')]
def vol(a,b):
 aa,bb=a.BoundBox,b.BoundBox
 if any(min(getattr(aa,t+'Max'),getattr(bb,t+'Max'))-max(getattr(aa,t+'Min'),getattr(bb,t+'Min'))<=1e-7 for t in ['X','Y','Z']):return 0
 return a.common(b).Volume
# Camera module insertion/removal is checked as an assembly, with its four frame screws removed.
plate=[o for o in obs if o.Printable and o.PrintFileName=='CameraPlate_21x16'][0]
moving=[o for o in obs if o==plate or o.Name=='PCB_Cut003' or o.Name.startswith(('Camera_M2','PCB_Spacer','Camera_Rear','Camera_Lens','Camera_Wire'))]
targets=[o for o in obs if o not in moving and not o.Name.startswith('RailMount_')]
fail=[];unknown=[]
for shift in [-25,-15,-10,-5,-1,0]:
 for a in moving:
  s=a.Shape.copy();s.translate(V(0,shift,0))
  for b in targets:
   v=vol(s,b.Shape)
   if v>.001:
    event={'shift_y':shift,'pair':[a.Name,b.Name],'volume_mm3':v}
    (unknown if a.Name=='Camera_RearComponents_KEEP_OUT' else fail).append(event)
assert not fail,fail[:3]
pairs=[('Pan ear seat','Base_EarMount_ThrustSupport','PanServo_SG90_Reference'),('Tilt ear seat','PanYoke_EarBracket_KeyedDrive','TiltServo_SG90_Reference'),('Pan captive drive nut','PanDrive_M3x10_0','Pan_KeyedHorn_Cover'),('Tilt captive drive nut','TiltDrive_M3x10_0','Tilt_KeyedHorn_CaptiveCover'),('Idler nut-to-stationary-wall GAP','TiltIdler_M3x12','Tilt_Removable_IdlerPillar'),('Idler nut-to-sleeve CONTACT','TiltIdler_M3x12','Tilt_Journal_FlangedSleeve'),('Camera plate/frame CONTACT',plate.Name,'TiltCradle_KeyedHorn_CameraFrame'),('Camera frame fastener/plate CONTACT','RailMount_Lower_M3x10_0',plate.Name),('Camera frame fastener/cradle CONTACT','RailMount_Lower_M3x10_0','TiltCradle_KeyedHorn_CameraFrame'),('PCB spacer/plate CONTACT','PCB_Spacer_Lower_Left',plate.Name),('PCB spacer/PCB CONTACT','PCB_Spacer_Lower_Left','PCB_Cut003')]
contacts=[]
for label,a,b in pairs:contacts.append({'interface':label,'distance_mm':d.getObject(a).Shape.distToShape(d.getObject(b).Shape)[0]})
assert .29<contacts[4]['distance_mm']<.31
for i,c in enumerate(contacts):
 if i!=4:assert c['distance_mm']<1e-5,c
internal=[]
for o in obs:
 ss=o.Shape.Solids;assert o.Shape.isValid()
 for i,a in enumerate(ss):
  for j,b in enumerate(ss[i+1:],i+1):
   v=vol(a,b);internal.append({'component':o.Name,'solids':[i,j],'volume':v});assert v<.001
p=d.getObject('RepairParameters');ribbon=d.getObject('Camera_WireExit_KEEP_OUT')
report={'camera_module_installation':{'sample_shifts_mm':[-25,-15,-10,-5,-1,0],'unintended_penetrations':fail,'unverified_envelope_conflicts':unknown,'procedure':'Remove four M3 camera-frame screws, then slide complete PCB/spacer/plate module forward. Real cables disconnected; keep-out uncertainties are not fit approvals.'},'actual_contact_distances':contacts,'compound_internal_pairs':internal,'ribbon':{'reserved_width_mm':p.RibbonReserveWidth.Value,'reserved_thickness_mm':p.RibbonReserveThickness.Value,'reserved_exit_length_mm':p.RibbonReserveLength.Value,'actual_width_exit_bend_connector':'UNKNOWN','scope':'Flat outlet reservation checked in all motion poses; full flexible ribbon route not established'},'lens':{'nominal_envelope_diameter_mm':p.CameraLensEnvelopeDiameter.Value,'plate_clearance_diameter_mm':p.CameraLensClearanceDiameter.Value,'nominal_radial_margin_mm':(p.CameraLensClearanceDiameter.Value-p.CameraLensEnvelopeDiameter.Value)/2,'actual_barrel_IR_FOV':'UNVERIFIED'},'release_status':'HOLD for hardware fit and unmeasured rear/cable/load evidence'}
json.dump(report,open(os.path.join(W,'checks','mechanical_attachment_and_cables.json'),'x'),indent=2)
print('Camera module path and actual clamping contacts PASS; internal solid pairs',len(internal),'nominal lens margin',report['lens']['nominal_radial_margin_mm'],'mm; physical rear/ribbon data unresolved')
