import FreeCAD as A, Part, json, os, sys, traceback
from FreeCAD import Vector as V, Placement
ROOT=r'EyeTrace_Final_Engineering'; OUT=os.path.join(ROOT,'Camera_21x14_Correction_01')
sys.path.append(r'D:\App files\Mod\Assembly')
try:
    p=os.path.join(ROOT,'Motion_Audit_02','Native_Simulations','EyeTrace_Final_Assembly_Native_Simulation_r02.FCStd')
    d=A.openDocument(p); rp=d.getObject('RepairParameters')
    rp.CameraPitchX=21.0; rp.CameraPitchZ=14.0; rp.CameraCenterZ=76.0
    if not hasattr(rp,'CameraPlateHeight'): rp.addProperty('App::PropertyLength','CameraPlateHeight','Camera correction')
    rp.CameraPlateHeight=32.0
    d.getObject('CameraPlate_Blank').setExpression('Height','RepairParameters.CameraPlateHeight')
    d.getObject('CameraPlate_Blank').setExpression('Placement.Base.z','RepairParameters.CameraCenterZ - RepairParameters.CameraPlateHeight / 2')
    for name,val in [('CameraHoleSpacingHorizontal',21.0),('CameraHoleSpacingVertical',14.0),('CameraHoleCenterZ',76.0)]:
        if not hasattr(rp,name): rp.addProperty('App::PropertyLength',name,'Camera correction')
        setattr(rp,name,val)
    d.recompute()
    # Rebuild all rigid-body compounds from their updated source feature members.
    bodies=[]
    for bodyname in ['BaseBody','PanServoBody','PanRotorBody','PanHornBody','TiltServoBody','TiltCradleBody','TiltHornBody']:
        body=d.getObject(bodyname)
        if body is None: raise RuntimeError('Missing rigid body '+bodyname)
        members=list(body.RigidMembers)
        shapes=[d.getObject(n).Shape.copy() for n in members]
        body.Shape=Part.makeCompound(shapes); bodies.append(body)
    d.recompute()
    asm=d.getObject('EyeTraceNativeAssembly'); solved=asm.solve()
    if solved!=0: raise RuntimeError('native solve failed '+str(solved))
    links={o.Name:o for o in asm.Group if o.TypeId=='App::Link'}
    simgroup=d.getObject('Simulations'); sim_results=[]
    for sim in simgroup.Group:
        asm.generateSimulation(sim); n=asm.numberOfFrames()
        if n<10: raise RuntimeError('insufficient frames for '+sim.Label+': '+str(n))
        asm.updateForFrame(n//4)
        pan=links['PanRotorBodyLink'].Placement.Rotation.Angle>1e-5
        rel=links['PanRotorBodyLink'].Placement.inverse().multiply(links['TiltCradleBodyLink'].Placement)
        tilt=rel.Rotation.Angle>1e-5
        sim_results.append({'label':sim.Label,'frames':n,'motion_count':len(sim.Group),'pan_rotated_at_quarter':pan,'tilt_relative_rotated_at_quarter':tilt})
        for l in links.values(): l.Placement=Placement()
        d.recompute()
    solved2=asm.solve(); d.recompute()
    # Geometry evidence from final linked body compounds.
    solid_results={b.Name:{'valid':b.Shape.isValid(),'solids':len(b.Shape.Solids)} for b in bodies}
    out=os.path.join(OUT,'CAD','EyeTrace_Final_Assembly_Native_21x14.FCStd'); d.saveAs(out)
    report={'source':p,'output':out,'solver_return_before_and_after_sim':[solved,solved2],'grounded':getattr(d.getObject('GroundedBase'),'ObjectToGround',None).Name,'joint_names':[o.Name+':'+str(getattr(o,'JointType','')) for o in d.getObject('Joints').Group if hasattr(o,'JointType')],'intended_rotational_dof':2,'simulation_results':sim_results,'rigid_bodies':solid_results,'camera_pattern_xz_mm':[[-10.5,69],[-10.5,83],[10.5,69],[10.5,83]],'physical_fit':'UNVERIFIED'}
    with open(os.path.join(OUT,'CHECKS','native_motion_validation.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
except Exception:
    with open(os.path.join(OUT,'CHECKS','native_motion_error.txt'),'w') as f:f.write(traceback.format_exc())
    raise
finally:
    for n in list(A.listDocuments()): A.closeDocument(n)
