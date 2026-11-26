import FreeCAD as A, Part, Mesh, MeshPart, json, os, re, zipfile, xml.etree.ElementTree as ET, hashlib, traceback
from FreeCAD import Vector as V
ROOT=r'EyeTrace_Final_Engineering'; OUT=os.path.join(ROOT,'Camera_21x14_Correction_01')
NS={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}; TAG='{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
def gcode_info(path):
    head={}; layer_changes=0; support_comments=0; e_moves=0; first_layer_extrusions=0; in_layer=False; xs=[]; ys=[]
    with open(path,'r',errors='ignore') as f:
        for line in f:
            if line.startswith(';LAYER_CHANGE'): layer_changes+=1; in_layer=True
            if line.startswith(';TYPE:Support'): support_comments+=1
            if line.startswith('; total layer number:'): head['layer_count']=int(line.split(':',1)[1])
            for key in ['MINX','MINY','MINZ','MAXX','MAXY','MAXZ']:
                if line.startswith('; '+key+' ='): head[key.lower()]=float(line.split('=',1)[1])
            if line.startswith('; filament used [g] ='): head['filament_g']=float(line.split('=')[1])
            if line.startswith('; estimated printing time (normal mode) ='): head['estimated_time']=line.split('=',1)[1].strip()
            if line.startswith('; nozzle_temperature ='): head['nozzle_C']=int(float(line.split('=',1)[1]))
            if line.startswith('; first_layer_bed_temperature ='): head['bed_C']=int(float(line.split('=',1)[1]))
            if line.startswith('G1') and ' E' in line:
                if in_layer:
                    mx=re.search(r'X(-?\d+(?:\.\d+)?)',line); my=re.search(r'Y(-?\d+(?:\.\d+)?)',line)
                    if mx: xs.append(float(mx.group(1)))
                    if my: ys.append(float(my.group(1)))
                e_moves+=1
                if in_layer and layer_changes==1: first_layer_extrusions+=1
    head['extrusion_xy_bounds_mm']=[min(xs),min(ys),max(xs),max(ys)] if xs and ys else None
    head.update({'layer_change_markers':layer_changes,'support_feature_regions':support_comments,'extrusion_moves':e_moves,'first_layer_extrusion_moves':first_layer_extrusions,'gcode_bytes':os.path.getsize(path)})
    return head

def main():
    doc=A.openDocument(os.path.join(OUT,'CAD','EyeTrace_Final_Assembly_21x14.FCStd'))
    objs=[o for o in doc.Objects if hasattr(o,'KinematicGroup') and hasattr(o,'Shape') and not o.Shape.isNull()]
    invalid=[o.Name for o in objs if not o.Shape.isValid() or len(o.Shape.Solids)==0]
    pr=doc.getObject('RepairParameters'); plate=doc.getObject('CameraPlate_Cut007')
    centers=sorted([[round(o.Placement.Base.x,4),round(o.Placement.Base.z,4)] for o in doc.Objects if o.Name.startswith('PlatePCB_Hole')])
    expected=[[-10.5,69.0],[-10.5,83.0],[10.5,69.0],[10.5,83.0]]
    assert centers==expected,(centers,expected)
    # Deliberate CAD clearances/known provisional overlap intersections, from actual final B-reps.
    def pair(a,b):
        x=doc.getObject(a).Shape;y=doc.getObject(b).Shape
        return {'intersection_mm3':float(x.common(y).Volume),'minimum_distance_mm':float(x.distToShape(y)[0])}
    pair_checks={
      'plate_to_lens':pair('CameraPlate_Cut007','Camera_Lens_PROVISIONAL'),
      'plate_to_PCB_reference':pair('CameraPlate_Cut007','PCB_Cut003'),
      'plate_to_camera_fastener_lower_left':pair('CameraPlate_Cut007','Camera_M2x12_Lower_Left'),
      'plate_to_camera_fastener_upper_left':pair('CameraPlate_Cut007','Camera_M2x12_Upper_Left'),
      'rear_uncertainty_to_lower_left_fastener':pair('Camera_RearComponents_KEEP_OUT','Camera_M2x12_Lower_Left'),
      'rear_uncertainty_to_upper_left_fastener':pair('Camera_RearComponents_KEEP_OUT','Camera_M2x12_Upper_Left'),
      'rear_uncertainty_to_all_four_camera_fasteners':{n:pair('Camera_RearComponents_KEEP_OUT',n) for n in ['Camera_M2x12_Lower_Left','Camera_M2x12_Lower_Right','Camera_M2x12_Upper_Left','Camera_M2x12_Upper_Right']},
      'ribbon_reservation_to_cradle':pair('Camera_WireExit_KEEP_OUT','TiltCradle_KeyedHorn_CameraFrame'),
      'ribbon_reservation_to_plate':pair('Camera_WireExit_KEEP_OUT','CameraPlate_Cut007')}
    shape_report={'cad_version':A.Version()[:4],'object_count':len(doc.Objects),'kinematic_shape_count':len(objs),'printable_component_count':sum(bool(getattr(o,'Printable',False)) for o in objs),'invalid_solids':invalid,'camera_hole_pattern':{'pitch_mm':[pr.CameraPitchX.Value,pr.CameraPitchZ.Value],'centers_xz_mm':centers,'source':'user-supplied nominal','PCB_envelope_mm':[pr.CameraPCBWidth.Value,pr.CameraPCBThickness.Value,pr.CameraPCBHeight.Value],'plate_outside_mm':[plate.Shape.BoundBox.XLength,plate.Shape.BoundBox.YLength,plate.Shape.BoundBox.ZLength],'plate_height_parameter_mm':pr.CameraPlateHeight.Value,'plate_hole_diameter_mm':pr.CameraPlateHoleDiameter.Value,'PCB_hole_diameter_assumed_mm':pr.CameraPCBMountHoleDiameter.Value},'clearances_and_uncertainty_intersections':pair_checks,'physical_fit':'UNVERIFIED'}
    assert not invalid and len(objs)==49 and shape_report['printable_component_count']==13
    # Reopen STEP outputs in FreeCAD's Part kernel.
    step_results={}
    for fname in ['EyeTrace_Final_Assembly_21x14.step','CameraPlate_21x14.step','K2_PrintLayout_21x14.step']:
        s=Part.read(os.path.join(OUT,'CAD',fname)); step_results[fname]={'valid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume,'bbox_mm':[s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength]}; assert s.isValid() and len(s.Solids)>0
    # Validate and export an STL layout exactly matching the corrected 13-object Creality project.
    project=os.path.join(OUT,'Creality_Print','EyeTrace_K2_ABS_Full_21x14.3mf')
    with zipfile.ZipFile(project) as z:
        model=ET.fromstring(z.read('3D/3dmodel.model'))
        direct=[o for o in model.findall('.//c:resources/c:object',NS) if o.find('c:mesh',NS) is not None]
        names=[]; mesh_checks=[]; merged=Mesh.Mesh()
        for o in direct:
            mesh=o.find('c:mesh',NS); vs=mesh.find('c:vertices',NS); fs=mesh.find('c:triangles',NS)
            points=[V(float(v.attrib['x']),float(v.attrib['y']),float(v.attrib['z'])) for v in vs]
            facets=[]
            part=Mesh.Mesh()
            for t in fs:
                a,b,c=(int(t.attrib[k]) for k in ('v1','v2','v3')); tri=(points[a],points[b],points[c]); facets.append(tri); part.addFacet(*tri); merged.addFacet(*tri)
            names.append(o.attrib.get('name',''))
            mesh_checks.append({'name':o.attrib.get('name',''),'facets':part.CountFacets,'closed_solid':part.isSolid(),'bbox_mm':[part.BoundBox.XMin,part.BoundBox.YMin,part.BoundBox.ZMin,part.BoundBox.XMax,part.BoundBox.YMax,part.BoundBox.ZMax]})
        assert len(direct)==13 and len(model.findall('.//c:build/c:item',NS))==13
        assert 'CameraPlate_21x14' in names and sum(bool(m['closed_solid']) for m in mesh_checks)==13,mesh_checks
        stlout=os.path.join(OUT,'STL','EyeTrace_Final_K2_SingleBed_21x14.stl'); merged.write(stlout)
        check=Mesh.Mesh(stlout)
        stl_report={'project_mesh_count':len(direct),'project_names':names,'per_part_mesh_checks':mesh_checks,'combined_facets':check.CountFacets,'combined_components':check.countComponents(), 'combined_closed':check.isSolid(),'bounds_mm':[check.BoundBox.XMin,check.BoundBox.YMin,check.BoundBox.ZMin,check.BoundBox.XMax,check.BoundBox.YMax,check.BoundBox.ZMax],'bed_xy_mm':[260,260],'inside_bed':check.BoundBox.XMin>=0 and check.BoundBox.YMin>=0 and check.BoundBox.XMax<=260 and check.BoundBox.YMax<=260}
        assert stl_report['inside_bed'] and check.isSolid() and check.countComponents()==13
        ms=ET.fromstring(z.read('Metadata/model_settings.config'))
        support={}
        for o in ms.findall('object'):
            name='';enabled='';style=''
            for m in o.findall('metadata'):
                if m.attrib.get('key')=='name':name=m.attrib.get('value')
                if m.attrib.get('key')=='enable_support':enabled=m.attrib.get('value')
                if m.attrib.get('key')=='support_style':style=m.attrib.get('value')
            if name:support[name]={'enabled':enabled,'style':style}
    # Validate the camera coupon STL and all fresh sliced toolpaths.
    coupon=Mesh.Mesh(os.path.join(OUT,'FIT_TESTS','Camera_Hole_Pattern_21x14_ABS.stl'))
    coupon_mesh={'facets':coupon.CountFacets,'closed_solid':coupon.isSolid(),'components':coupon.countComponents(),'bounds_mm':[coupon.BoundBox.XMin,coupon.BoundBox.YMin,coupon.BoundBox.ZMin,coupon.BoundBox.XMax,coupon.BoundBox.YMax,coupon.BoundBox.ZMax]}
    full_gcode=gcode_info(os.path.join(OUT,'CHECKS','SLICE_FULL','plate_1.gcode')); fit_gcode=gcode_info(os.path.join(OUT,'CHECKS','SLICE_CAMERA','plate_1.gcode'))
    assert full_gcode['layer_count']==599 and full_gcode['maxx']<=260 and full_gcode['maxy']<=260 and full_gcode['support_feature_regions']>0
    assert fit_gcode['layer_count']==10 and fit_gcode['support_feature_regions']==0 and fit_gcode['maxx']<=260 and fit_gcode['maxy']<=260
    # Source and legacy file hashes demonstrate preservation and identify previous pattern artifacts.
    old_paths=[os.path.join(ROOT,'CAD','EyeTrace_Final_Assembly.FCStd'),os.path.join(ROOT,'ABS_Print_Ready','Creality_Print','EyeTrace_K2_ABS_Supported_Project_v2.3mf'),os.path.join(ROOT,'ABS_Print_Ready','STL','EyeTrace_K2_ABS_SingleBed.stl'),os.path.join(ROOT,'STL','individual','CameraPlate_21x16.stl'),os.path.join(ROOT,'CAD','individual_STEP','CameraPlate_21x16.step'),os.path.join(ROOT,'FIT_TESTS','Camera_21x16_HoleCenter_Gauge.stl'),os.path.join(ROOT,'ABS_Print_Ready','FIT_TESTS','Creality_Print','EyeTrace_ABS_FitTest_Project_v5.3mf')]
    preserved={os.path.relpath(p,ROOT):{'exists':os.path.isfile(p),'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest() if os.path.isfile(p) else None} for p in old_paths}
    report={'CAD_geometry':shape_report,'STEP_readback':step_results,'full_print_mesh':stl_report,'camera_coupon_mesh':coupon_mesh,'Creality_support_configuration':support,'sliced_full_print':full_gcode,'sliced_camera_coupon':fit_gcode,'preserved_old_21x16_file_hashes':preserved,'overall_software_validation':'PASS with provisional physical fit; see known rear-envelope intersection','physical_camera_fit':'UNVERIFIED'}
    with open(os.path.join(OUT,'CHECKS','final_validation.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps({'CAD':shape_report,'STEP':step_results,'STL':{k:stl_report[k] for k in ['project_mesh_count','combined_facets','combined_components','combined_closed','bounds_mm','inside_bed']},'sliced_full_print':full_gcode,'sliced_coupon':fit_gcode,'support':support},indent=2))
    A.closeDocument(doc.Name)
try: main()
except Exception:
    with open(os.path.join(OUT,'CHECKS','validation_error.txt'),'w') as f:f.write(traceback.format_exc())
    raise
finally:
    for n in list(A.listDocuments()): A.closeDocument(n)





