import FreeCAD as A, Part, MeshPart, Mesh, json, math, os, shutil, traceback
from FreeCAD import Vector as V, Rotation, Placement
ROOT=r'EyeTrace_Final_Engineering'
OUT=os.path.join(ROOT,'Camera_21x14_Correction_01')
SRC=os.path.join(ROOT,'CAD','EyeTrace_Final_Assembly.FCStd')

def revise_doc(doc):
    # Hole and spacer placements are expression-driven by these shared master parameters.
    rp=doc.getObject('RepairParameters')
    rp.CameraPitchX=21.0
    rp.CameraPitchZ=14.0
    rp.CameraCenterZ=76.0
    if not hasattr(rp,'CameraPlateHeight'): rp.addProperty('App::PropertyLength','CameraPlateHeight','Camera correction')
    rp.CameraPlateHeight=32.0
    blank=doc.getObject('CameraPlate_Blank')
    blank.setExpression('Height','RepairParameters.CameraPlateHeight')
    blank.setExpression('Placement.Base.z','RepairParameters.CameraCenterZ - RepairParameters.CameraPlateHeight / 2')
    for name,val in [('CameraHoleSpacingHorizontal',21.0),('CameraHoleSpacingVertical',14.0),('CameraHoleCenterZ',76.0)]:
        if not hasattr(rp,name): rp.addProperty('App::PropertyLength',name,'Camera correction')
        setattr(rp,name,val)
    doc.recompute()
    plate=doc.getObject('CameraPlate_Cut007')
    plate.Label='Camera mounting plate -21x14mm HOLE CENTERS'
    plate.PrintFileName='CameraPlate_21x14'
    # Ensure parameter data for future edits is directly visible on the plate.
    if not hasattr(plate,'HoleSpacingHorizontal'): plate.addProperty('App::PropertyLength','HoleSpacingHorizontal','Camera pattern')
    if not hasattr(plate,'HoleSpacingVertical'): plate.addProperty('App::PropertyLength','HoleSpacingVertical','Camera pattern')
    plate.HoleSpacingHorizontal=21.0; plate.HoleSpacingVertical=14.0
    return plate

def mesh_for(shape, path):
    m=MeshPart.meshFromShape(Shape=shape,LinearDeflection=0.08,AngularDeflection=0.12,Relative=False)
    m.write(path)
    return m

def main():
    d=A.openDocument(SRC)
    plate=revise_doc(d)
    assert plate.Shape.isValid() and len(plate.Shape.Solids)==1
    centers=[]
    for prefix in ('PlatePCB_Hole','PCB_Hole'):
        objs=[o for o in d.Objects if o.Name.startswith(prefix)]
        centers=[(round(o.Placement.Base.x,4),round(o.Placement.Base.z,4)) for o in objs]
        assert sorted(centers)==[(-10.5,69.0),(-10.5,83.0),(10.5,69.0),(10.5,83.0)],(prefix,centers)
    # Preserve the 38 x 38 x 1.6 PCB reference and every independent optical/cable reservation.
    pcb=d.getObject('CameraPCB_Blank').Shape.BoundBox
    assert round(pcb.XLength,4)==38 and round(pcb.ZLength,4)==38 and round(pcb.YLength,4)==1.6
    report={'cad_version':A.Version()[:4],'source':SRC,'pattern_center_xyz_mm':[0,-30.4,76], 'hole_centers_xz_mm':sorted(centers),'horizontal_pitch_mm':21,'vertical_pitch_mm':14,'plate_valid':plate.Shape.isValid(),'plate_solids':len(plate.Shape.Solids),'plate_volume_mm3':plate.Shape.Volume,'old_plate_volume_mm3':4449.355830897155,'pcb_envelope_mm':[pcb.XLength,pcb.YLength,pcb.ZLength], 'camera_plate_outside_mm':[plate.Shape.BoundBox.XLength,plate.Shape.BoundBox.YLength,plate.Shape.BoundBox.ZLength],'lens_envelope_diameter_mm':14,'lens_clearance_diameter_mm':18,'lens_projection_mm':10,'rear_envelope_mm':[20,24.4,20],'ribbon_reservation_mm':[20,1,18],'physical_fit':'UNVERIFIED'}
    d.recompute(); d.saveAs(os.path.join(OUT,'CAD','EyeTrace_Final_Assembly_21x14.FCStd'))
    # CAD STEP: full source assembly's moving/fixed component geometry.
    obs=[o for o in d.Objects if hasattr(o,'KinematicGroup') and hasattr(o,'Shape') and not o.Shape.isNull()]
    Part.export(obs,os.path.join(OUT,'CAD','EyeTrace_Final_Assembly_21x14.step'))
    plate_step=os.path.join(OUT,'CAD','CameraPlate_21x14.step'); Part.export([plate],plate_step)
    plate_stl=os.path.join(OUT,'STL','CameraPlate_21x14.stl'); mesh_for(plate.Shape,plate_stl)
    # Recreate the exact existing 13-component bed with the corrected plate at its original slot.
    bed=A.openDocument(os.path.join(ROOT,'CAD','K2_PrintLayout.FCStd'))
    bo=bed.getObject('CameraPlate_21x16')
    assert bo is not None
    sh=plate.Shape.copy(); sh.rotate(V(0,0,0),V(1,0,0),90); sh.translate(V(88,252.6,27.4));
    # CAD layout's old camera plate occupies x60..116, y160.6..192.6, z0..3.
    sh.translate(V(0,0,0)); bo.Shape=sh; bo.Label='CameraPlate_21x14'
    objs=[x for x in bed.Objects if hasattr(x,'Shape') and not x.Shape.isNull()]
    assert len(objs)==13
    bboxes={x.Name:[x.Shape.BoundBox.XMin,x.Shape.BoundBox.YMin,x.Shape.BoundBox.ZMin,x.Shape.BoundBox.XMax,x.Shape.BoundBox.YMax,x.Shape.BoundBox.ZMax] for x in objs}
    bed.saveAs(os.path.join(OUT,'CAD','K2_PrintLayout_21x14.FCStd'))
    compound=Part.makeCompound([x.Shape.copy() for x in objs]); mm=mesh_for(compound,os.path.join(OUT,'STL','EyeTrace_Final_K2_SingleBed_21x14.stl'))
    report.update({'printable_components':len(objs),'print_layout_bounds_mm':[min(v[0] for v in bboxes.values()),min(v[1] for v in bboxes.values()),max(v[3] for v in bboxes.values()),max(v[4] for v in bboxes.values())],'bed_components':bboxes,'single_bed_stl_facets':len(mm.Facets),'single_bed_stl_watertight_component_mesh':'FreeCAD tessellation from 13 CAD solids; STL format has no solid topology'})
    # Minimal flat camera spacing coupon: 29 x 22 x 2 mm, 4 x 2.4 mm holes, 21 x 14 pitch.
    coupon=Part.makeBox(29,22,2,V(-14.5,-11,0))
    for x in (-10.5,10.5):
        for y in (-7,7): coupon=coupon.cut(Part.makeCylinder(1.2,2,V(x,y,0)))
    coupon=coupon.removeSplitter(); assert coupon.isValid() and len(coupon.Solids)==1
    cstl=os.path.join(OUT,'FIT_TESTS','Camera_Hole_Pattern_21x14_ABS.stl'); mesh_for(coupon,cstl)
    report['coupon']={'size_mm':[29,22,2],'hole_centers_xy_mm':[[-10.5,-7],[-10.5,7],[10.5,-7],[10.5,7]],'hole_diameter_mm':2.4,'valid':coupon.isValid(),'solids':len(coupon.Solids),'purpose':'spacing and screw/pass-through screening; not lens, PCB envelope, rear clearance, or cable validation'}
    # Step-export the layout itself as optional engineering reference.
    Part.export([x for x in objs],os.path.join(OUT,'CAD','K2_PrintLayout_21x14.step'))
    # Additional parameterized source copy to make the correction reproducible.
    with open(os.path.join(OUT,'CAD','camera_21x14_parameters.json'),'w') as f:
        json.dump({'hole_spacing_center_to_center_mm':{'horizontal':21,'vertical':14},'center_xz_mm':[0,76],'hole_centers_xz_mm':sorted(centers),'pcb_envelope_mm':{'width':38,'height':38,'thickness':1.6,'status':'provisional envelope kept separate from hole pitch'},'pcb_hole_diameter_mm':2.2,'plate_hole_diameter_mm':2.4,'lens':{'envelope_diameter_mm':14,'clearance_diameter_mm':18,'projection_mm':10,'status':'provisional'},'rear_component_envelope_mm':[20,24.4,20],'ribbon_reservation_mm':[20,1,18],'physical_fit':'unverified'},f,indent=2)
    with open(os.path.join(OUT,'CHECKS','cad_geometry_validation.json'),'w') as f: json.dump(report,f,indent=2)
    print(json.dumps({'complete':True,'report':report},indent=2))

try: main()
except Exception:
    with open(os.path.join(OUT,'CHECKS','generation_error.txt'),'w') as f:f.write(traceback.format_exc())
    raise
finally:
    for n in list(A.listDocuments()): A.closeDocument(n)






