"""Measurement-gated cross-horn CAD builder for Eye Trace.

No horn geometry is guessed. With missing JSON values, this script reports the
missing measurements and exits before opening or writing any CAD document.
After filling measured values, it creates a separate candidate assembly and a
small multi-clearance ABS coupon; source revisions are never overwritten.
"""
import json, math, os, sys
from pathlib import Path
import FreeCAD as App
import Part, MeshPart
from FreeCAD import Vector as V

ROOT=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
SOURCE=Path(r"EyeTrace_Final_Engineering\Camera_21x14_Correction_01\CAD\EyeTrace_Final_Assembly_Native_21x14.FCStd")
PARAM=ROOT/"CAD"/"cross_horn_measurements_template.json"
OUT_CAD=ROOT/"CAD"/"EyeTrace_CrossHorn_21x14_Provisional.FCStd"
COUPON_DOC=ROOT/"FIT_TESTS"/"CrossHorn_Pocket_Clearance_Coupon.FCStd"
COUPON_STL=ROOT/"FIT_TESTS"/"CrossHorn_Pocket_Clearance_Coupon_Bed.stl"
OUT_STEP=ROOT/"CAD"/"EyeTrace_CrossHorn_21x14_Provisional.step"
PAN_STL=ROOT/"STL"/"PanYoke_CrossHorn_Provisional.stl"
TILT_STL=ROOT/"STL"/"TiltCradle_CrossHorn_Provisional.stl"

REQUIRED=["long_tip_to_tip","short_tip_to_tip","long_arm_width_root","long_arm_width_tip",
          "short_arm_width_root","short_arm_width_tip","long_arm_tip_radius","short_arm_tip_radius",
          "plate_thickness","arm_cross_center_offset_x","arm_cross_center_offset_y","raised_hub_od","raised_hub_height_above_plate",
          "center_retaining_screw_clearance_diameter","retaining_screw_head_od",
          "retaining_screw_head_height","retaining_driver_access_diameter"]
SIGNED_REQUIRED=["arm_cross_center_offset_x","arm_cross_center_offset_y"]
CLEARANCE_CANDIDATES=[0.10,0.20,0.25,0.30,0.40]  # 0.25 is legacy-source control; select after ABS test
AXIAL_CANDIDATE=0.20  # sourced as the old CAD nominal allowance; remains provisional

def load_parameters():
    p=json.loads(PARAM.read_text(encoding="utf-8"))
    missing=[k for k in REQUIRED if not isinstance(p.get(k),(int,float)) or (p[k]<=0 and k not in SIGNED_REQUIRED)]
    if p.get("opposing_pairs_symmetric_confirmed") is not True:
        missing.insert(0,"opposing_pairs_symmetric_confirmed (confirm true; if false, measure/model each of the four arms separately)")
    if missing:
        print(json.dumps({"status":"BLOCKED_PENDING_MEASUREMENT","missing":missing,"no_geometry_written":True},indent=2))
        raise SystemExit(2)
    od=p.get("underside_boss_od"); depth=p.get("underside_boss_depth")
    if (od is None)!=(depth is None) or (od is not None and (od<=0 or depth<=0)):
        raise SystemExit("Measure both underside boss fields or set both null if no boss exists")
    if p["long_tip_to_tip"]<=2*p["long_arm_tip_radius"] or p["short_tip_to_tip"]<=2*p["short_arm_tip_radius"]:
        raise SystemExit("Arm tip radii must be less than half of their respective tip-to-tip lengths")
    return p

def tapered_arm_pair(length, root_w, tip_w, tip_r, height, clearance=0.0):
    half=length/2.0+clearance
    r=tip_r+clearance
    cap=max(0.0,half-r)
    wr=root_w+2*clearance; wt=tip_w+2*clearance
    result=None
    for sign in (-1.0,1.0):
        pts=[V(0,-wr/2,0),V(sign*cap,-wt/2,0),V(sign*cap,wt/2,0),V(0,wr/2,0),V(0,-wr/2,0)]
        prism=Part.Face(Part.Wire(Part.makePolygon(pts))).extrude(V(0,0,height))
        capshape=Part.makeCylinder(r,height,V(sign*cap,0,0))
        result=prism.fuse(capshape) if result is None else result.fuse(prism).fuse(capshape)
    return result.removeSplitter()

def cross_plate(p,height,clearance=0.0):
    longbar=tapered_arm_pair(p["long_tip_to_tip"],p["long_arm_width_root"],p["long_arm_width_tip"],p["long_arm_tip_radius"],height,clearance)
    shortbar=tapered_arm_pair(p["short_tip_to_tip"],p["short_arm_width_root"],p["short_arm_width_tip"],p["short_arm_tip_radius"],height,clearance)
    shortbar.rotate(V(0,0,0),V(0,0,1),90)
    return longbar.fuse(shortbar).removeSplitter()

def horn_solid(p):
    t=p["plate_thickness"]; boss=p.get("underside_boss_od") or 0.0; boss_h=p.get("underside_boss_depth") or 0.0
    s=cross_plate(p,t)
    dx=p["arm_cross_center_offset_x"]; dy=p["arm_cross_center_offset_y"]
    s.translate(V(dx,dy,0))
    if p["raised_hub_height_above_plate"]>0:
        s=s.fuse(Part.makeCylinder(p["raised_hub_od"]/2,p["raised_hub_height_above_plate"],V(0,0,t)))
    if boss>0 and boss_h>0:
        s=s.fuse(Part.makeCylinder(boss/2,boss_h,V(0,0,-boss_h)))
    hole=p["center_retaining_screw_clearance_diameter"]
    total=t+p["raised_hub_height_above_plate"]+boss_h+2
    s=s.cut(Part.makeCylinder(hole/2,total,V(0,0,-boss_h-1)))
    for h in p.get("small_horn_holes",[]):
        dia=float(h["diameter_mm"]); x=float(h["x_center_mm"]); y=float(h["y_center_mm"])
        s=s.cut(Part.makeCylinder(dia/2,t+2,V(x,y,-1)))
    return s.removeSplitter()

def pocket_local(p, radial, axial):
    t=p["plate_thickness"]
    s=cross_plate(p,t+axial,radial)
    s.translate(V(p["arm_cross_center_offset_x"],p["arm_cross_center_offset_y"],0))
    hub_depth=p["raised_hub_height_above_plate"]+axial
    if hub_depth>0:
        s=s.fuse(Part.makeCylinder(p["raised_hub_od"]/2+radial,hub_depth,V(0,0,t)))
    # Full center aperture keeps the original horn-retaining screw and driver accessible.
    access=max(p["retaining_driver_access_diameter"],p["retaining_screw_head_od"]+2*radial)
    through=Part.makeCylinder(access/2,t+hub_depth+2,V(0,0,-1))
    return s.fuse(through).removeSplitter()

def legacy_star_clearance(depth):
    s=Part.makeCylinder(4.25,depth)
    for angle in [0,72,144,216,288]:
        arm=Part.makeBox(12.25,4.1,depth,V(0,-2.05,0))
        arm.rotate(V(0,0,0),V(0,0,1),angle)
        s=s.fuse(arm)
    return s.removeSplitter()

def placed(shape,base,rot):
    q=shape.copy(); q.Placement=App.Placement(base,rot); return q

def make_coupon_document(p):
    # Four discrete, labeled clearances; these are calibration choices, not a selected fit.
    doc=App.newDocument("CrossHorn_Pocket_Clearance_Coupon")
    objects=[]
    L=p["long_tip_to_tip"]; S=p["short_tip_to_tip"]
    wall=3.0+max(abs(p["arm_cross_center_offset_x"]),abs(p["arm_cross_center_offset_y"])); pitchx=L+2*wall+4; pitchy=S+2*wall+4
    for i,c in enumerate(CLEARANCE_CANDIDATES):
        col=i%2; row=i//2; ox=col*pitchx; oy=row*pitchy
        block=Part.makeBox(L+2*wall,S+2*wall,p["plate_thickness"]+p["raised_hub_height_above_plate"]+wall)
        # Recess arms at the top face to plate depth; hub counterbore extends farther.
        top=block.BoundBox.ZMax
        armcut=cross_plate(p,p["plate_thickness"]+AXIAL_CANDIDATE,c)
        armcut.translate(V((L+2*wall)/2,(S+2*wall)/2,top-p["plate_thickness"]-AXIAL_CANDIDATE))
        block=block.cut(armcut)
        hub_depth=p["raised_hub_height_above_plate"]+AXIAL_CANDIDATE
        if hub_depth>0:
            hub=Part.makeCylinder(p["raised_hub_od"]/2+c,hub_depth+0.02,V((L+2*wall)/2,(S+2*wall)/2,top-hub_depth))
            block=block.cut(hub)
        access=max(p["retaining_driver_access_diameter"],p["retaining_screw_head_od"]+2*c)
        block=block.cut(Part.makeCylinder(access/2,block.BoundBox.ZLength+2,V((L+2*wall)/2,(S+2*wall)/2,-1)))
        block.translate(V(ox,oy,0))
        obj=doc.addObject("PartDesign::Feature","ClearanceVariant%02d"%(i+1));obj.Label="Cross pocket radial clearance %.2f mm"%c;obj.Shape=block
        obj.addProperty("App::PropertyLength","RadialClearance","FitTest");obj.RadialClearance=c
        obj.addProperty("App::PropertyString","FitStatus","FitTest");obj.FitStatus="PROVISIONAL - ABS fit test required"
        objects.append(obj)
    doc.recompute()
    compound=Part.makeCompound([o.Shape for o in objects])
    bb=compound.BoundBox
    if bb.XLength>260 or bb.YLength>260 or bb.ZLength>260:
        raise RuntimeError("Cross-horn coupon variants exceed the K2 260 mm build envelope; split the bed")
    if not all(o.Shape.isValid() and len(o.Shape.Solids)==1 for o in objects):
        raise RuntimeError("A generated cross-horn pocket coupon is not one valid solid")
    doc.saveAs(str(COUPON_DOC))
    mesh=MeshPart.meshFromShape(Shape=compound,LinearDeflection=0.08,AngularDeflection=0.12,Relative=False)
    mesh.write(str(COUPON_STL))
    return doc

def update_assembly(p, radial=0.25):
    d=App.openDocument(str(SOURCE)); a=d.getObject("EyeTraceNativeAssembly")
    if float(d.getObject("RepairParameters").CameraPitchX.Value)!=21 or float(d.getObject("RepairParameters").CameraPitchZ.Value)!=14:
        raise RuntimeError("Source camera pattern is not 21x14; refusing to modify candidate")
    d.getObject("CameraPlate_Cut007").Label="Camera mounting plate -21x14mm HOLE CENTERS"
    panrot=App.Rotation(); tiltrot=App.Rotation(V(0,1,0),90)
    for hornname,carriername,base,rot,olddepth,accessdiam in [
        ("Pan_OriginalStar_PROVISIONAL","PanYoke_EarBracket_KeyedDrive",V(0,0,35),panrot,2.3,8.0),
        ("Tilt_OriginalStar_PROVISIONAL","TiltCradle_KeyedHorn_CameraFrame",V(-41,0,78),tiltrot,2.2,7.0)]:
        carrier=d.getObject(carriername); oldhorn=d.getObject(hornname)
        # Restore the source star-shaped cavity to solid before cutting the measured cross profile.
        fill=placed(legacy_star_clearance(olddepth),base,rot)
        recess=placed(pocket_local(p,radial,AXIAL_CANDIDATE),base,rot)
        carrier.Shape=carrier.Shape.fuse(fill).cut(recess).removeSplitter()
        horn=placed(horn_solid(p),base,rot)
        if not horn.isValid() or len(horn.Solids)!=1:
            raise RuntimeError("Measured horn parameters produced a disconnected or invalid horn solid")
        oldhorn.Shape=horn; oldhorn.Label=hornname.replace("OriginalStar_PROVISIONAL","MeasuredCrossHorn_PROVISIONAL")
        if not hasattr(oldhorn,"FitStatus"): oldhorn.addProperty("App::PropertyString","FitStatus","Engineering")
        oldhorn.FitStatus="PROVISIONAL - printed horn pocket coupon and physical fit required"
        if not hasattr(carrier,"HornProfileParameters"): carrier.addProperty("App::PropertyString","HornProfileParameters")
        carrier.HornProfileParameters=json.dumps({"profile":"two-pair cross horn","measurements":p,"radial_clearance_candidate_mm":radial,"axial_clearance_candidate_mm":AXIAL_CANDIDATE})
        if not hasattr(carrier,"FitStatus"): carrier.addProperty("App::PropertyString","FitStatus","Engineering")
        carrier.FitStatus="PROVISIONAL - cross-horn fit not physically verified"
        # Preserve or enlarge the shaft/screw access bore; existing axis location is retained.
        access=max(accessdiam,p["retaining_driver_access_diameter"],p["retaining_screw_head_od"]+2*radial)
        if hornname.startswith("Pan"):
            carrier.Shape=carrier.Shape.cut(Part.makeCylinder(access/2,14,V(0,0,31)))
        else:
            carrier.Shape=carrier.Shape.cut(Part.makeCylinder(access/2,12,V(-43,0,78),V(1,0,0)))
        carrier.Shape=carrier.Shape.removeSplitter()
        if not carrier.Shape.isValid() or len(carrier.Shape.Solids)!=1:
            raise RuntimeError("Cross-horn pocket produced an invalid drive carrier: "+carriername)
    # Refresh the rigid-body compounds so native joints and simulations reference revised solids.
    for bodyname in ["PanRotorBody","PanHornBody","TiltCradleBody","TiltHornBody"]:
        body=d.getObject(bodyname)
        body.Shape=Part.makeCompound([d.getObject(name).Shape for name in body.RigidMembers])
    d.recompute()
    if a.solve()!=0: raise RuntimeError("native assembly solver failed")
    if len([j for j in d.getObject("Joints").Group if getattr(j,"JointType","")=="Revolute"])!=2:
        raise RuntimeError("expected two revolute joints")
    for sim in d.getObject("Simulations").Group:
        a.generateSimulation(sim)
        if a.numberOfFrames()<2: raise RuntimeError("native motion simulation produced too few frames: "+sim.Label)
        a.updateForFrame(0)
    d.recompute()
    # Candidate output is separate; do not alter or promote source/full-print projects.
    d.saveAs(str(OUT_CAD))
    try:
        import Import
        Import.export([d.getObject("EyeTraceNativeAssembly")],str(OUT_STEP))
    except Exception as e:
        print("STEP export requires GUI/import exporter:",e)
    for name,path in [("PanYoke_EarBracket_KeyedDrive",PAN_STL),("TiltCradle_KeyedHorn_CameraFrame",TILT_STL)]:
        shape=d.getObject(name).Shape
        mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=0.08,AngularDeflection=0.12,Relative=False)
        mesh.write(str(path))
    return d

def main():
    p=load_parameters()  # preflight must pass before source assembly is even opened
    clear=p.get("fit_clearance_parameter")
    radial=float(clear) if isinstance(clear,(int,float)) and clear>0 else 0.25
    make_coupon_document(p)
    d=update_assembly(p,radial)
    print("Built separate PROVISIONAL cross-horn candidate. Coupon fit and full collision validation remain required.")

if __name__=="__main__": main()
