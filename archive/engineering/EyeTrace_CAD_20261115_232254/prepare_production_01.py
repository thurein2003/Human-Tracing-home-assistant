import os,json,math,shutil,csv,hashlib
import FreeCAD as A, Part, Mesh, MeshPart
from FreeCAD import Vector as V
BASE=os.path.dirname(os.path.abspath(__file__));SRC=os.path.join(BASE,'candidate_02');OUT=os.path.join(BASE,'production_candidate_01')
os.makedirs(OUT,exist_ok=False)
for sub in ['checks','coupons','renders','measurements']:os.makedirs(os.path.join(OUT,sub))
# Retain the native assembly, not a new design.
for f in ['EyeTrace_Assembly.FCStd','EyeTrace.FCStd','assembly.step','single_bed.stl','parameters.json']:shutil.copy2(os.path.join(SRC,f),os.path.join(OUT,f))
shutil.copytree(os.path.join(SRC,'parts'),os.path.join(OUT,'parts'))
doc=A.openDocument(os.path.join(SRC,'EyeTrace_Assembly.FCStd'))
names=['Base','PanServoRetainer','TiltServoRetainer','PanYoke','TiltCameraCradle','PanHornClamp','TiltHornClamp']
audit={}
for n in names:
 s=doc.getObject(n).Shape;step=Part.read(os.path.join(SRC,'parts',n+'.step'))
 p=s.copy()
 if n in ['TiltCameraCradle','TiltHornClamp']:p.rotate(V(),V(0,1,0),90)
 b=p.BoundBox;p.translate(V(-b.XMin,-b.YMin,-b.ZMin))
 m=Mesh.Mesh(os.path.join(SRC,'parts',n+'.stl'));verts=m.Topology[0]
 err=max(Part.Vertex(v).distToShape(p)[0] for v in verts)
 delta=s.cut(step).Volume+step.cut(s).Volume
 audit[n]={'native_valid':s.isValid(),'native_solids':len(s.Solids),'step_symmetric_difference_mm3':delta,'stl_closed':m.isSolid(),'components':m.countComponents(),'nonmanifold':m.hasNonManifolds(),'self_intersections':m.hasSelfIntersections(),'normals_inconsistent':m.hasNonUniformOrientedFacets(),'all_stl_vertices_surface_error_mm':err,'volume_relative_error':abs(m.Volume-p.Volume)/p.Volume,'bounds_error_mm':max(abs(getattr(m.BoundBox,k)-getattr(p.BoundBox,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])}
 assert s.isValid() and len(s.Solids)==1 and delta<0.001 and m.isSolid() and err<0.01 and audit[n]['volume_relative_error']<0.002,n
bed=Mesh.Mesh(os.path.join(SRC,'single_bed.stl'));audit['bed']={'closed':bed.isSolid(),'components':bed.countComponents(),'self_intersections':bed.hasSelfIntersections()}
assemblystep=Part.read(os.path.join(SRC,'assembly.step'));audit['assembly_STEP']={'valid':assemblystep.isValid(),'solids':len(assemblystep.Solids)}
audit['scope']='All STL vertices checked against bed-oriented native BRep surface; volume and bounds also checked. Not a full Hausdorff proof.'
json.dump(audit,open(os.path.join(OUT,'checks','native_export_comparison.json'),'w'),indent=2)
# Reuse the existing generator tests on the loaded native shapes. No geometry rebuild.
src=open(os.path.join(BASE,'build_candidate_02.py'),encoding='utf-8-sig').read()
scope={'A':A,'Part':Part,'Mesh':Mesh,'MeshPart':MeshPart,'V':V,'os':os,'json':json,'doc':doc,'ROOT':OUT,'parts':[doc.getObject(n) for n in names],'fixtures':[],'P':json.load(open(os.path.join(SRC,'parameters.json')))}
for var,n in [('base','Base'),('yoke','PanYoke'),('cradle','TiltCameraCradle'),('cam','Camera_ASSUMED_38x38x30'),('tilt','TiltServo_ASSUMED')]:scope[var]=doc.getObject(n)
fg={o.Name:('fixed' if o.Name.startswith('PanRetainer_M3') else 'tilt' if o.Name.startswith('TiltHorn_M3') or o.Name=='Idler_M3' else 'pan') for o in doc.Objects if '_M3' in o.Name};scope['fastener_groups']=fg
scope['report']={};exec(src[src.index('collisions=[]'):src.index('Part.export(parts+fixtures')],scope)
json.dump(scope['report'],open(os.path.join(OUT,'checks','motion_rerun.json'),'w'),indent=2)
# Explicit local running clearances, not just intersection tests.
clear={}
for label,n,m in [('idler_axial_gap','PanYoke','TiltCameraCradle'),('pan_horn_to_retainer','PanHornClamp','PanServoRetainer')]:clear[label]=doc.getObject(n).Shape.distToShape(doc.getObject(m).Shape)[0]
clear['pan_head_to_retainer']=min(doc.getObject('PanHorn_M3_'+str(i)).Shape.distToShape(doc.getObject('PanServoRetainer').Shape)[0] for i in range(4))
clear['tilt_head_to_yoke_neutral']=min(doc.getObject('TiltHorn_M3_'+str(i)).Shape.distToShape(doc.getObject('PanYoke').Shape)[0] for i in range(4))
json.dump(clear,open(os.path.join(OUT,'checks','local_clearances_mm.json'),'w'),indent=2)
# Exact-interface small coupons. These do not pretend that unmeasured camera pitch is known.
cd=A.newDocument('EyeTrace_Fit_Coupons');coupons={}
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,V(x,y,z))
def cyl(r,h,x=0,y=0,z=0):return Part.makeCylinder(r,h,V(x,y,z))
coupons['ServoBodyGauge_24p2x13p2']=box(0,0,0,28.2,17.2,6).cut(box(2,2,-1,24.2,13.2,8))
for name in ['PanHornClamp','TiltHornClamp']:
 s=doc.getObject(name).Shape.copy()
 if name=='TiltHornClamp':s.rotate(V(),V(0,1,0),90)
 b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));coupons[name+'_Exact']=s
for name,r,t in [('PanHornMatingFace',18,2),('TiltHornMatingFace',14,2)]:
 s=cyl(r+4,t).cut(cyl(4,t+2,0,0,-1))
 for i in range(4):s=s.cut(cyl(1.65,t+2,r*math.cos(i*math.pi/2),r*math.sin(i*math.pi/2),-1))
 b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,0));coupons[name+'_Diagnostic']=s
rail=box(0,0,0,60,14,2).cut(box(5,5.35,-1,40,3.3,4))
for y,d in [(3,2.2),(7,2.6),(11,3.3)]:rail=rail.cut(cyl(d/2,4,53,y,-1))
coupons['CameraSlotRail_A']=rail;coupons['CameraSlotRail_B']=rail.copy()
coupons['CameraWidthGauge_38p4']=box(0,0,0,42.4,8,3).fuse(box(0,0,0,2,8,8)).fuse(box(40.4,0,0,2,8,8))
cr={};packed=[];x=0;y=0;row=0
for n,s in coupons.items():
 s=s.removeSplitter();o=cd.addObject('PartDesign::Feature',n);o.Shape=s
 Part.export([o],os.path.join(OUT,'coupons',n+'.step'))
 mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=0.06,AngularDeflection=0.15,Relative=False);path=os.path.join(OUT,'coupons',n+'.stl');mesh.write(path);m=Mesh.Mesh(path)
 cr[n]={'valid':s.isValid(),'solids':len(s.Solids),'closed':m.isSolid(),'components':m.countComponents(),'self_intersections':m.hasSelfIntersections(),'nonmanifold':m.hasNonManifolds(),'normals_inconsistent':m.hasNonUniformOrientedFacets()}
 assert s.isValid() and len(s.Solids)==1 and m.isSolid() and not m.hasSelfIntersections(),n
 if x+s.BoundBox.XLength>220:x=0;y+=row+6;row=0
 q=s.copy();q.translate(V(x,y,0));packed.append(q);x+=s.BoundBox.XLength+6;row=max(row,s.BoundBox.YLength)
cd.recompute();cd.saveAs(os.path.join(OUT,'coupons','FitCoupons.FCStd'))
MeshPart.meshFromShape(Shape=Part.makeCompound(packed),LinearDeflection=0.06,AngularDeflection=0.15,Relative=False).write(os.path.join(OUT,'coupons','coupon_bed.stl'))
json.dump(cr,open(os.path.join(OUT,'checks','coupon_audit.json'),'w'),indent=2)
# Source snapshot and measurement IDs for both physical units separately.
shutil.copy2(os.path.join(BASE,'build_candidate_02.py'),os.path.join(OUT,'measurements','inherited_dimensions_source.py'))
rows=[('S1','Case length / width / height','23 / 12 / 23','Measure main case excluding ears, then record all bulges'),('S2','Pan shaft center from short end / side','6 / 6','Measure to shaft center; use diameter midpoint'),('S3','Tilt shaft center above case bottom / across width','17 / 6','Case rotated end-on; do not reuse pan offset blindly'),('S4','Output envelope diameter / pan extension / tilt extension','6 / 8 / 7','Measure spline, boss and shoulder separately; current cylinders combine them'),('S5','Ear pitch / pilot diameter','32 / 2.2','Ears omitted from case model; measure ear length,width,thickness,height and hole offsets'),('S6','Horn contact plane relative case top/end','Pan +6; tilt +6','Measure installed horn underside and top with original center screw seated'),('S7','Case clearance per side / openings','0.6; 24.2x13.2; tilt 13.2x24.2','Check cable strain relief and entire insertion path'),('S8','Cable exit envelope and bend radius','Unknown; base relief 11x5x8','Measure exit location, connector, free cable bend radius'),('H1','Star arms / angular pitch','5 / 72 deg','Trace BOTH actual horns at 1:1 with a scale'),('H2','Arm radial rectangle length / width','12 / 3.6','Model envelope reaches about 12.134 mm radius at corners; measure each arm and actual tip radius'),('H3','Web thickness / center hub envelope diameter','2 / 8','Measure web and BOTH raised hub faces, total thickness, flat contact annulus'),('H4','Spline cavity / original center screw','Not modeled','Measure engagement depth, hub bore, center screw head and reach; keep original spline'),('H5','Original horn hole centers and diameters','Unknown; not used as mounting pattern','Trace coordinates relative shaft, even if sandwich retained'),('H6','Pan clamp OD / ID / thickness / bolt radius','44 / 8 / 1.5 / 18','Nominal printed interfaces; four M3 holes diameter3.3; mating effective thickness2'),('H7','Tilt clamp OD / ID / thickness / bolt radius','34 / 8 / 1.5 / 14','Nominal printed interfaces; four M3 holes diameter3.3; cradle access center diameter7'),('C1','Camera total envelope X / Y / height','38 / 38 / 30','Include IR PCB, rear components, LEDs, heatsinks and connectors'),('C2','Four-hole center spacing Px / Py','UNKNOWN - ABSENT FROM CAD','Measure center-to-center; also measure both diagonals and all edge offsets'),('C3','Four hole diameters / board thickness','UNKNOWN','Measure all four separately; identify plated/grounded holes and screw type'),('C4','Lens OD / forward protrusion','14 / 10','Measure focus ring and required focus-adjustment sweep'),('C5','Lens axis offset X / above bottom','0 centered / 17','Existing lens center world Z74 with camera bottom Z57; front is Y=-19'),('C6','Mounting face to rear/front keep-outs / standoffs','UNKNOWN','Measure allowed contact areas and screw intrusion before selecting M3x10'),('C7','Mass / center of mass / cable bend / optical FOV','UNKNOWN','Weigh camera; record cable force and IR LED optical keep-outs'),('F1','M3 head OD / height / nut AF / thickness','5.6 / 3 / 5.5 / 2.4','Measure actual hardware; screw length assumed10 under head'),('F2','Printed bore / nut recess / idler gap','3.3 / diameter7 / 0.5','PETG calibration and secure nonbinding pivot required')]
with open(os.path.join(OUT,'measurements','checklist.csv'),'w',newline='') as f:
 w=csv.writer(f);w.writerow(['ID','Dimension','CAD assumption mm unless noted','How to measure','Pan or horn A measured','Tilt or horn B measured','Camera measured','Test print result']);w.writerows([list(r)+['','','',''] for r in rows])
# Code-native measurement diagrams; dimension IDs refer directly to CSV.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="850" viewBox="0 0 1100 850"><style>text{font:17px sans-serif;fill:#163049} .s{fill:#edf4f9;stroke:#163049;stroke-width:2} .d{stroke:#c14d15;stroke-width:2;fill:none} .n{font:14px sans-serif}</style><rect width="1100" height="850" fill="white"/><text x="30" y="30">Measure actual hardware — schematic diagrams, NOT scale templates. Record mm in checklist.csv.</text><text x="30" y="70">SERVO: top and side (measure both units)</text><rect class="s" x="70" y="110" width="230" height="120"/><circle class="s" cx="130" cy="170" r="24"/><path class="d" d="M70 95H300 M55 110V230 M70 170H130"/><text x="150" y="91">S1 length</text><text x="10" y="260">S1 width; S2 shaft center to each case edge</text><rect class="s" x="365" y="110" width="230" height="120"/><rect class="s" x="400" y="82" width="48" height="28"/><path class="d" d="M610 110V230 M365 245H595"/><text x="620" y="175">S1 height</text><text x="380" y="75">S4 boss/spline</text><text x="350" y="275">S5 ears; S6 installed horn stack; S8 cable</text><text x="30" y="325">STAR HORN: trace both sides and every hole</text><circle class="s" cx="175" cy="440" r="75"/><circle class="s" cx="175" cy="440" r="25"/><path class="d" d="M175 440H250 M150 440H200"/><text x="265" y="410">H1 arms; H2 tip radius + width</text><text x="265" y="440">H3 hub OD, raised faces, web thickness</text><text x="265" y="470">H4 spline engagement + center screw</text><text x="265" y="500">H5 trace all original holes</text><text class="n" x="75" y="540">Circle is tip envelope, not a horn profile.</text><text x="650" y="325">CAMERA: actual four-hole mounting face</text><rect class="s" x="700" y="360" width="250" height="200"/><g fill="white" stroke="#163049" stroke-width="2"><circle cx="725" cy="385" r="8"/><circle cx="925" cy="385" r="8"/><circle cx="725" cy="535" r="8"/><circle cx="925" cy="535" r="8"/></g><circle class="s" cx="825" cy="460" r="32"/><path class="d" d="M725 345H925 M975 385V535 M725 385L925 535"/><text x="780" y="341">C2 Px</text><text x="980" y="465">C2 Py</text><text class="n" x="660" y="590">C3 hole diameters, board thickness, edge offsets, diagonals</text><text class="n" x="660" y="615">Hole positions drawn schematically; no pitch is assumed.</text><text x="30" y="635">CAMERA SIDE</text><rect class="s" x="100" y="675" width="190" height="90"/><rect class="s" x="65" y="700" width="35" height="40"/><path class="d" d="M65 785H100 M305 675V765"/><text x="20" y="815">C4 lens diameter/projection; C5 lens center offsets</text><text x="400" y="700">C1 full envelope and C6 component keep-outs</text><text x="400" y="735">C2/C3 all four holes required before screw-mount design</text><text x="400" y="770">C7 mass, center of mass, cable and IR/light paths</text></svg>'''
open(os.path.join(OUT,'measurements','hardware_diagrams.svg'),'w').write(svg)
print('Existing native geometry retained. Parts:',len(names),'motion collisions:',scope['report']['motion']['collision_count'],'coupon parts:',len(coupons),'clearances:',clear)
