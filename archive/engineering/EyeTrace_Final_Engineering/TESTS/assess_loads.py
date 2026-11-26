from pathlib import Path
import json,math,csv
import FreeCAD as A,Part,MeshPart
from FreeCAD import Vector as V
r=Path(__file__).resolve().parents[1];d=A.openDocument(str(r/'CAD/EyeTrace_Final_Assembly.FCStd'));obs=[o for o in d.Objects if hasattr(o,'KinematicGroup')];parts=[o for o in obs if o.Printable]
# Density 1.27g/cm3 from Prusament TDS is an illustrative material, not user's unidentified PETG.
rows=[]
for o in obs:
 if o.Printable:mass=o.Shape.Volume*.00127;kind='100% solid PETG bound'
 elif 'KEEP_OUT' in o.Name or o.Name in ['PCB_Cut003','Camera_Lens_PROVISIONAL']:continue
 elif 'Servo_SG90' in o.Name:mass=9;kind='manufacturer nominal SG90 mass'
 elif 'OriginalStar' in o.Name:mass=o.Shape.Volume*.00115;kind='assumed nylon density 1.15g/cm3'
 else:mass=o.Shape.Volume*.00785;kind='assumed steel density 7.85g/cm3'
 c=sum((s.CenterOfMass*s.Volume for s in o.Shape.Solids),V())/o.Shape.Volume;rows.append({'name':o.Name,'frame':o.KinematicGroup,'mass_g':mass,'center_mm':[c.x,c.y,c.z],'basis':kind})
# Camera combined mass sensitivity; actual center independently assumed at geometric lens/PCB region.
models=[]
for cammass in [10,25,50]:
 camera={'name':'Actual camera+lens ASSUMPTION','frame':'tilt','mass_g':cammass,'center_mm':[0,-33,76]}
 tilt=[v for v in rows if v['frame']=='tilt']+[camera];pan=[v for v in rows if v['frame']!='fixed']+[camera]
 mass=sum(v['mass_g'] for v in tilt);com=[sum(v['mass_g']*v['center_mm'][i] for v in tilt)/mass for i in range(3)]
 # Max gravity about X over intended sampled guard travel; pan yaw does not affect gravity torque.
 ts=[]
 for angle in [i*.5 for i in range(-60,61)]:
  a=math.radians(angle);torque=sum(v['mass_g']/1000*9.80665*(v['center_mm'][1]*math.cos(a)-(v['center_mm'][2]-78)*math.sin(a))/1000 for v in tilt);ts.append((abs(torque),angle))
 tg,at=max(ts);alpha=1.0 # deliberately slow rad/s2 assumption, not command calibration
 # Upper point-mass+box diagonal inertia bound: all material point radii <= bboxmax; camera radius<=50mm.
 it=0.;ip=0.
 for v in tilt:
  if v['name'] in [o.Name for o in obs]:
   bb=d.getObject(v['name']).Shape.BoundBox;rr=max(abs(bb.YMin),abs(bb.YMax))**2+max(abs(bb.ZMin-78),abs(bb.ZMax-78))**2
  else:rr=50**2
  it+=v['mass_g']/1000*rr*1e-6
 for v in pan:
  if v['name'] in [o.Name for o in obs]:
   bb=d.getObject(v['name']).Shape.BoundBox;rr=max(abs(bb.XMin),abs(bb.XMax))**2+max(abs(bb.YMin),abs(bb.YMax))**2+(max(abs(bb.ZMin-78),abs(bb.ZMax-78))**2 if v['frame']=='tilt' else 0)
  else:rr=50**2
  ip+=v['mass_g']/1000*rr*1e-6
 totalpan=sum(v['mass_g'] for v in pan);pancom=[sum(v['mass_g']*v['center_mm'][i] for v in pan)/totalpan for i in range(3)];ecc=math.hypot(pancom[0],pancom[1]);W=totalpan/1000*9.80665;mu=.30;reff=.030
 tf=mu*W*reff;cable=.005;tiltdemand=2*tg+it*alpha+cable;pandemand=tf+ip*alpha+cable
 stall=1.8*.0980665;budget=.25*stall
 models.append({'camera_mass_assumption_g':cammass,'camera_com_assumption_mm':[0,-33,76],'tilt_total_mass_solid_bound_g':mass,'tilt_com_mm':com,'tilt_max_static_gravity_Nm':tg,'tilt_worst_angle_deg':at,'tilt_conservative_inertia_kgm2':it,'pan_conservative_inertia_kgm2':ip,'pan_moving_mass_solid_bound_g':totalpan,'pan_thrust_load_N':W,'pan_neutral_com_mm':pancom,'pan_gravity_eccentricity_mm':ecc,'pan_overturning_moment_Nm':W*ecc/1000,'thrust_annulus_mean_pressure_MPa':W/(math.pi*(32**2-27.5**2)),'tilt_right_support_static_load_N':mass/1000*9.80665*(com[0]+40)/77,'tilt_right_journal_projected_pressure_MPa':(mass/1000*9.80665*(com[0]+40)/77)/(5*2.5),'pan_friction_assumption_Nm':tf,'tilt_demand_2xgravity_plus_accel_cable_Nm':tiltdemand,'pan_demand_friction_accel_cable_Nm':pandemand,'assumed_working_budget_Nm':budget,'tilt_within_assumed_budget':tiltdemand<budget,'pan_within_assumed_budget':pandemand<budget,'scope':'SCREENING ONLY. Load budget is analyst 25% of sourced stall torque; not a manufacturer continuous rating. Actual cable/friction/clone torque unknown.'})
# Bracket simple weak-axis plate comparison, conservative arbitrary20mm cantilever: not FEA.
bending={'assumed_force_N':2,'assumed_lever_mm':20,'assumed_effective_width_mm':20,'assumed_wall_thickness_mm':2.5,'stress_MPa':6*2*20/(20*2.5**2),'assumed_effective_modulus_MPa':1000,'tip_deflection_mm':2*20**3/(3*1000*(20*2.5**3/12)),'scope':'Representative plate strip, not measured peak bracket stress. FDM anisotropy, notches, layer bond, preload and creep excluded.'}
report={'source_stall_torque_kgfcm_at4p8V':1.8,'source':'https://towerpro.com.tw/product/sg90-analog/','PETG_density_source':'https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf','assumptions':{'PETG_density_g_cm3':1.27,'solid_fill_bound':True,'angular_acceleration_rad_s2':1,'pan_friction_coefficient':.3,'pan_friction_radius_m':.03,'cable_torque_Nm':.005,'working_budget_stall_fraction':.25,'tilt_gravity_dynamic_factor':2},'mass_components':rows,'camera_sensitivity':models,'simple_bending_sensitivity':bending,'printed_solid_volume_cm3':sum(o.Shape.Volume for o in parts)/1000,'printed_solid_mass_bound_g':sum(o.Shape.Volume for o in parts)*.00127,'certified_strength':False}
(r/'TESTS/results/strength_load_assessment.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'load_sensitivity':models,'strip_bending':bending,'solid_print_mass_g':report['printed_solid_mass_bound_g']},indent=2))
