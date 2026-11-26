import FreeCAD as A, json, math, hashlib
from pathlib import Path

ROOT=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
SRC=Path(r"EyeTrace_Final_Engineering\Camera_21x14_Correction_01\CAD\EyeTrace_Final_Assembly_Native_21x14.FCStd")
d=A.openDocument(str(SRC)); assembly=d.getObject("EyeTraceNativeAssembly"); joints=d.getObject("Joints")
def ang(o): return abs(float(o.Placement.Rotation.Angle)*180/math.pi)
def axis(o):
    a=o.Placement.Rotation.Axis
    return (float(a.x),float(a.y),float(a.z))
def relative_angle_deg(parent, child):
    r=parent.Placement.Rotation.inverted().multiply(child.Placement.Rotation)
    return float(r.Angle)*180/math.pi
links={n:d.getObject(n) for n in ["BaseBodyLink","PanServoBodyLink","PanRotorBodyLink","PanHornBodyLink","TiltServoBodyLink","TiltCradleBodyLink","TiltHornBodyLink"]}
solver=assembly.solve()
joint_summary=[{"name":j.Name,"type":getattr(j,"JointType","Ground"),"label":j.Label,
                "reference1":getattr(getattr(j,"Reference1",(None,None))[0],"Name",None),
                "reference2":getattr(getattr(j,"Reference2",(None,None))[0],"Name",None)} for j in joints.Group]
revolutes=[j for j in joints.Group if getattr(j,"JointType","")=="Revolute"]
fixed=[j for j in joints.Group if getattr(j,"JointType","")=="Fixed"]
simulations=d.getObject("Simulations").Group
sim_results=[]
for sim in simulations:
    assembly.generateSimulation(sim)
    frames=assembly.numberOfFrames()
    sample_indices=sorted(set([0,13,min(25,frames-1),38,frames-1]))
    samples=[]
    for idx in sample_indices:
        assembly.updateForFrame(idx)
        samples.append({"frame":idx,"rotations_deg":{k:round(ang(links[k]),4) for k in links},
                        "relative_tilt_deg":round(relative_angle_deg(links["PanRotorBodyLink"],links["TiltCradleBodyLink"]),4),
                        "axes":{k:[round(v,4) for v in axis(links[k])] for k in links if k in ["PanRotorBodyLink","TiltCradleBodyLink"]}})
    pan_sample=next(x for x in samples if x["frame"]==13)
    sim_results.append({"name":sim.Name,"label":sim.Label,"motion_count":len(sim.Group),"frame_count":frames,
                        "time_step_s":float(sim.cTimeStepOutput.Value),"formulas":[m.Formula for m in sim.Group],"samples":samples})
    if sim.Name=="Simulation":
        r=pan_sample["rotations_deg"]
        assert r["PanServoBodyLink"]<1e-5
        assert abs(r["PanRotorBodyLink"]-60)<1.0
        assert abs(r["PanHornBodyLink"]-r["PanRotorBodyLink"])<1e-5
        assert abs(r["TiltServoBodyLink"]-r["PanRotorBodyLink"])<1e-5
        assert abs(r["TiltCradleBodyLink"]-r["PanRotorBodyLink"])<1e-5
        sim_results[-1]["motion_check"]="PASS: rotor, pan horn, tilt stator and cradle follow pan; pan stator remains fixed"
    elif sim.Name=="Simulation001":
        r=pan_sample["rotations_deg"]
        assert r["PanRotorBodyLink"]<1e-5 and r["TiltServoBodyLink"]<1e-5
        assert abs(r["TiltCradleBodyLink"]-25)<1.0
        assert abs(r["TiltHornBodyLink"]-r["TiltCradleBodyLink"])<1e-5
        sim_results[-1]["motion_check"]="PASS: tilt cradle and horn move; pan carrier and tilt stator remain fixed"
    else:
        r=pan_sample["rotations_deg"]
        assert abs(r["PanRotorBodyLink"]-45)<1.0
        rel=pan_sample["relative_tilt_deg"]
        assert abs(abs(rel)-20)<1.0,("combined relative tilt",rel)
        sim_results[-1]["motion_check"]="PASS: combined pan and relative tilt motions generated"

params=d.getObject("RepairParameters")
camera={"horizontal_pitch_mm":float(params.CameraPitchX.Value),"vertical_pitch_mm":float(params.CameraPitchZ.Value)}
pcb_holes=[o for o in d.Objects if o.Name.startswith("PCB_Hole") and hasattr(o,"Shape")]
xs=sorted(set(round((o.Shape.BoundBox.XMin+o.Shape.BoundBox.XMax)/2,4) for o in pcb_holes))
zs=sorted(set(round((o.Shape.BoundBox.ZMin+o.Shape.BoundBox.ZMax)/2,4) for o in pcb_holes))
camera["hole_center_x_mm"]=xs; camera["hole_center_z_mm"]=zs
camera["pitch_from_centers_mm"]=[round(xs[-1]-xs[0],4),round(zs[-1]-zs[0],4)] if len(xs)==2 and len(zs)==2 else None

drives=[]
for horn_name,carrier_name,cover_name in [
    ("Pan_OriginalStar_PROVISIONAL","PanYoke_EarBracket_KeyedDrive","Pan_KeyedHorn_Cover"),
    ("Tilt_OriginalStar_PROVISIONAL","TiltCradle_KeyedHorn_CameraFrame","Tilt_KeyedHorn_CaptiveCover")]:
    horn=d.getObject(horn_name); carrier=d.getObject(carrier_name); cover=d.getObject(cover_name)
    dist_carrier=float(horn.Shape.distToShape(carrier.Shape)[0]); dist_cover=float(horn.Shape.distToShape(cover.Shape)[0])
    drives.append({"horn_proxy":horn_name,"carrier":carrier_name,"cover":cover_name,
                   "horn_bbox_mm":[float(getattr(horn.Shape.BoundBox,k)) for k in ["XMin","YMin","ZMin","XMax","YMax","ZMax"]],
                   "horn_to_carrier_gap_mm":dist_carrier,"horn_to_cover_gap_mm":dist_cover,
                   "profile_parameters":json.loads(getattr(carrier,"HornProfileParameters","{}")),
                   "status":"OLD FIVE-ARM PROVISIONAL PROFILE; replace after real cross-horn measurements"})

solid_objs=[o for o in d.Objects if hasattr(o,"Shape") and not o.Shape.isNull() and len(o.Shape.Solids)>0]
invalid=[o.Name for o in solid_objs if not o.Shape.isValid()]
connected={n:bool(assembly.isPartConnected(links[n])) for n in links}
result={"source_file":str(SRC),"source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "freecad_version":A.Version()[:3],"solver_return":solver,
        "native_joint_counts":{"ground":sum(hasattr(j,"ObjectToGround") for j in joints.Group),"fixed":len(fixed),"revolute":len(revolutes),"intended_dof":len(revolutes)},
        "joints":joint_summary,"all_rigid_bodies_connected":all(connected.values()),"connected_bodies":connected,
        "solid_object_count":len(solid_objs),"invalid_solids":invalid,
        "camera_pattern":camera,"drive_interfaces":drives,
        "native_simulations":sim_results,
        "scope_note":"This revalidates the unmodified 21x14 native assembly and its stored star-proxy simulations. It does not validate a cross-horn interface, physical fit, or motion collisions for a corrected cross-horn design."}
out=ROOT/"CHECKS"/"native_21x14_motion_revalidation.json"
out.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ["solver_return","native_joint_counts","all_rigid_bodies_connected","solid_object_count","invalid_solids","camera_pattern","native_simulations","drive_interfaces"]},indent=2))
if solver!=0 or invalid or not all(connected.values()) or camera["pitch_from_centers_mm"]!=[21.0,14.0] or len(revolutes)!=2 or len(sim_results)!=3:
    raise SystemExit("native assembly validation did not satisfy expected structure")
