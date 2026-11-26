import os,json,csv,math,hashlib,html
import FreeCAD as A,Part,Mesh,MeshPart
from FreeCAD import Vector as V
B=os.path.dirname(os.path.abspath(__file__));S=os.path.join(B,'production_candidate_01');R=os.path.join(B,'sg90_interface_audit_01');os.makedirs(R,exist_ok=False)
for sub in ['checks','renders']:os.makedirs(os.path.join(R,sub))
d=A.openDocument(os.path.join(S,'EyeTrace_Assembly.FCStd'));names=['Base','PanServoRetainer','TiltServoRetainer','PanYoke','TiltCameraCradle','PanHornClamp','TiltHornClamp'];result={}
for n in ['PanServo_ASSUMED','TiltServo_ASSUMED']:
 s=d.getObject(n).Shape
 fs=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and any(type(e.Curve).__name__=='Line' for e in f.Edges)]
 b=Part.makeCompound(fs).BoundBox;bb=s.BoundBox
 cylinders=[]
 for f in s.Faces:
  if type(f.Surface).__name__=='Cylinder':
   u=f.Surface;cylinders.append({'radius':u.Radius,'axis':[u.Axis.x,u.Axis.y,u.Axis.z],'axis_point':[u.Center.x,u.Center.y,u.Center.z],'length_from_area':f.Area/(2*math.pi*u.Radius)})
 result[n]={'body_bounds':{k:getattr(b,k) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax']},'body_world_xyz_mm':[b.XLength,b.YLength,b.ZLength],'whole_world_xyz_mm':[bb.XLength,bb.YLength,bb.ZLength],'cylinders':cylinders,'valid':s.isValid(),'solids':len(s.Solids),'tabs_present':False,'mounting_holes_present':False,'spline_present':False,'center_screw_bore_present':False}
for hn,sn in [('PanStarHorn_ASSUMED','PanServo_ASSUMED'),('TiltStarHorn_ASSUMED','TiltServo_ASSUMED')]:
 h=d.getObject(hn).Shape;s=d.getObject(sn).Shape
 result[hn]={'world_bounds_mm':[h.BoundBox.XLength,h.BoundBox.YLength,h.BoundBox.ZLength],'solid_count':len(h.Solids),'cylindrical_faces':sum(type(f.Surface).__name__=='Cylinder' for f in h.Faces),'shaft_horn_overlap_mm3':h.common(s).Volume,'original_horn_holes_present':False,'spline_socket_present':False}
result['interpretation']='Bodies are generic micro-servo-sized envelopes, not verified SG90 models. Physical product identity cannot be inferred from geometry or label.'
json.dump(result,open(os.path.join(R,'checks','geometry_extraction.json'),'w'),indent=2)
# Existing native assembly tests, no new printable geometry or printing exports.
src=open(os.path.join(B,'build_candidate_02.py'),encoding='utf-8-sig').read();scope={'A':A,'Part':Part,'Mesh':Mesh,'MeshPart':MeshPart,'V':V,'os':os,'json':json,'doc':d,'ROOT':R,'report':{}}
for var,n in [('base','Base'),('yoke','PanYoke'),('cradle','TiltCameraCradle'),('cam','Camera_ASSUMED_38x38x30'),('tilt','TiltServo_ASSUMED')]:scope[var]=d.getObject(n)
scope['fastener_groups']={o.Name:('fixed' if o.Name.startswith('PanRetainer_M3') else 'tilt' if o.Name.startswith('TiltHorn_M3') or o.Name=='Idler_M3' else 'pan') for o in d.Objects if '_M3' in o.Name}
exec(src[src.index('collisions=[]'):src.index('Part.export(parts+fixtures')],scope);json.dump(scope['report'],open(os.path.join(R,'checks','limited_motion_rerun.json'),'w'),indent=2)
checks={}
for n in names:
 s=d.getObject(n).Shape;m=Mesh.Mesh(os.path.join(S,'parts',n+'.stl'));st=Part.read(os.path.join(S,'parts',n+'.step'))
 checks[n]={'solid_valid':s.isValid(),'solids':len(s.Solids),'stl_closed':m.isSolid(),'stl_components':m.countComponents(),'self_intersections':m.hasSelfIntersections(),'nonmanifold':m.hasNonManifolds(),'bad_normals':m.hasNonUniformOrientedFacets(),'step_valid':st.isValid(),'step_difference_volume_mm3':s.cut(st).Volume+st.cut(s).Volume}
checks['full_hardware_collision_status']='FAIL: positive-volume shaft/horn reference intersections, excluded by inherited motion test; see geometry_extraction.json'
json.dump(checks,open(os.path.join(R,'checks','solid_mesh_export_rerun.json'),'w'),indent=2)
# Correct the misleading identity/status metadata, without inventing physical dimensions.
for n in ['PanServo_ASSUMED','TiltServo_ASSUMED','PanStarHorn_ASSUMED','TiltStarHorn_ASSUMED']:
 o=d.getObject(n);o.Label='UNVERIFIED generic envelope - '+n;o.FitStatus='FAIL reference completeness; SG90 physical fit UNVERIFIED'
o=d.addObject('App::DocumentObjectGroup','CompatibilityHold');o.Label='HOLD - SG90 interface audit failed completeness; no production release'
d.recompute();d.saveAs(os.path.join(R,'SG90_Audit_Hold.FCStd'))
rows=[['Body envelope both','23 x 12 x 23','Derived planar-face bounds','SG90 manufacturer overall 23 x 12.2 x 29; not identical datums','UNVERIFIED'],['Overall pan along output axis','31','Native solid bounding box','Manufacturer overall29; other branded sheet approx31','UNVERIFIED'],['Overall tilt along output axis','30','Native solid bounding box','Differs from pan by1 for supposedly identical hardware','FAIL reference consistency'],['Width both','12','Native planar bounds','Manufacturer12.2; delta -0.2; no published tolerance','FAIL nominal source match; actual fit UNVERIFIED'],['Mounting tabs and holes','ABSENT','Exactly6 body planes + cylinder/cap; no tabs or bores','Documented SG90 drawings have tabs','FAIL reference completeness'],['Base pilot pitch / bore','32 / 2.2','Inherited structure dimensions; NOT measured servo holes','32.2 in circulated drawing is overall tab span, not proven hole pitch','UNVERIFIED; previous pitch assumption unsupported'],['Tilt pilot pitch / bore','32 / 2.2','Inherited wall pilots z56.5..88.5','Actual holes unknown; pilot heights not matched to ear plane','UNVERIFIED'],['Pan output axis','X0 Y0; 6 from short end and side','Cylinder axis + case bounds','Manufacturer source does not specify this datum','UNVERIFIED'],['Tilt output axis','Y0 Z78;17 above bottom and6 across width','Cylinder axis + case bounds','Manufacturer table F17 has ambiguous axis mapping without drawing','UNVERIFIED'],['Output cylinder diameter','6 both','Cylindrical radius3','Plain cylinders combine shoulder/spline; no tooth profile','UNVERIFIED'],['Output cylinder length','Pan8 / tilt7','Cylinder area divided by2piR','Same intended servo but inconsistent references','FAIL reference consistency'],['Horn height from case end','Pan6 to underside8 to top; tilt6 to underside8 to top','Face coordinates','Pan shaft reaches top, tilt ends1 before horn top','UNVERIFIED'],['Horn web / hub / arms','2 / diameter8 / five arms','Native envelope; inherited source arms12 x3.6 at72deg','No manufacturer dimensional horn drawing found','UNVERIFIED'],['Horn spline socket and center screw','ABSENT','Native solid, no hole','Original horns need actual spline socket and retaining screw','FAIL reference completeness'],['Shaft/horn engagement','Positive solid overlap','Boolean common measured in geometry_extraction.json','Could represent unmodeled spline engagement; cannot count as valid clearance','FAIL full CAD mating; physical UNVERIFIED'],['M3 hole fit in original horn','No horn holes modeled','Native horn shapes','M3 compatibility must NOT be assumed','UNVERIFIED'],['M3 structural clamp joints','10 long; grip5.5;nut2.4;nominal projection2.1','Nominal structural stack, not horn-hole engagement','No washer, real hub or screw-head tolerances','UNVERIFIED'],['M3 idler','Grip6; projection1.6; gap0.5','Native stack','Retention, wear, loosening, threads as bearing not validated','UNVERIFIED'],['Load capacity and bearing reactions','UNKNOWN','No mass/inertia/bearing-load rating','Manufacturer stall torque is not bearing or continuous-duty rating','UNVERIFIED; release blocked']]
with open(os.path.join(R,'comparison.csv'),'w',newline='') as f:
 w=csv.writer(f);w.writerow(['Feature','CAD mm unless noted','Measurement source','Document comparison','Status']);w.writerows(rows)
text='''# SG90 interface audit — production STOPPED

The audit reads production_candidate_01/EyeTrace_Assembly.FCStd directly. No geometry was resized and no printing package was generated. SG90_Audit_Hold.FCStd changes identity/status labels only: generic motor/horn references are explicitly UNVERIFIED. The geometry lacks the detail needed for an exact replacement. No evidence justifies choosing a new shaft, ear or horn dimension as a correction to your real units.

## Result

FAIL as an exact SG90 reference assembly. Both cases are micro-servo-sized, but this does NOT verify SG90 identity or exclude another micro-servo family with similar dimensions. There is no evidence of a larger-servo case being modeled. Actual identity comes from your two SG90 units; their fit remains UNVERIFIED. Both references have the same23x12x23 case, but output extensions8 and7 produce different overall axial envelopes31 and30. The original model contains NO mounting tabs: close-ups cannot truthfully show tabs that do not exist. Missing tabs, holes, splines and center screws are exposed in the screenshots instead of fabricated.

## Sources and tolerance treatment

[Manufacturer SG90 page](https://towerpro.com.tw/product/sg90-analog/) lists overall23x12.2x29mm and a separate A-F table without a usable mapping in its page text. It does not publish dimensional tolerances or star-horn interface dimensions. [TowerPro-branded SG90 sheet hosted by University Hamburg](https://tams.informatik.uni-hamburg.de/lehre/2019ss/vorlesung/es/doc/sg90.pdf) lists approximately22.2x11.8x31mm and shows tabs. These are conflicting nominal references, NOT a tolerance band. Do not interpret32.2 overall tab span as mounting-hole center distance. Exact ear-plane height, ear hole pitch/diameter, shoulder, spline and your original star profile require your measurements.

CAD numerical comparisons use0.001mm3 intersection threshold; extracted coordinate precision is not manufacturing tolerance. Neither quoted source gives manufacturing tolerances for the interfaces being checked. All hardware manufacturing tolerance, PETG dimensional error and load capacity are UNKNOWN. PASS in mesh/solid tests means digital integrity only. FAIL nominal match identifies source disagreement without asserting that a physical part cannot fit.

## Horn attachment and fasteners

The original horns cannot be verified from the reference stars: their modeled hubs are solid and have no spline cavity, center-screw bore or original arm holes. Boolean tests show shaft/horn positive-volume intersections; the inherited motion test excludes these parts and therefore its zero collisions does not mean a valid full hardware assembly. They might stand in for spline engagement, but no mating geometry exists to prove that interpretation.

The design uses a four-bolt sandwich around each original star, not M3 screws through original horn holes. Those M3 bolts join printed rings and printed yoke/cradle. True compatibility depends on horn web thickness, raised hub faces, contact annulus, tip radius and access to the servo-specific original center screw. The model has2mm flat horns and8mm hub envelopes only. No original SG90 horn hole is assumed to take M3. Original retaining screw thread and head are unknown and MUST NOT be replaced by M3 by assumption. Nominal M3 hardware is modeled as smooth envelopes, without threads. Nuts are2.4mm thick and heads5.6mm diameter x3mm high; actual tolerances and quantities are unconfirmed.

Pan structural holes diameter3.3 lie at radius18; tilt at radius14. The drawn star tip corner radius is sqrt(12^2+1.8^2), about12.134. This leaves only a nominal radial envelope difference0.216 between tip radius and the inward edge of a tilt structural hole (14-1.65). That is an envelope comparison, not a measured actual nearest distance or a proven fit. The flat friction sandwich has no positive anti-rotation key. Creep and slip remain unknown.

## Load path

Pan has NO external bearing or thrust support: the output shaft/horn carries the yoke, offset tilt motor/cage, cradle, camera and cables. The left motor is offset substantially from the pan axis, so pan bending depends on the complete center of mass even at rest. Tilt has an opposite M3 idler but no precision bushing; the servo still transmits torque and shares support load. Whether these unsupported loads are excessive is UNVERIFIED: camera mass, printed-part mass, acceleration, cable drag, bearing load rating and continuous-duty torque are unknown. Calculate force=m*g, bending moment=sum(m*g*horizontal offset), and tilt torque about the X axis using measured masses/centers and dynamics. Stall torque cannot approve these bearing or duty-cycle loads. No stress/torque safety factor has been demonstrated.

## Evidence and remaining estimates

comparison.csv gives measured CAD values, sources and status. checks/geometry_extraction.json contains world bounds, cylinder axes/radii/lengths and overlap volumes. Existing native solids, STEP files and STL files were rechecked without creating new printing exports. checks/limited_motion_rerun.json contains the inherited169-pose test; full hardware compatibility FAILS completeness despite that test's lack of detected intersections. checks/solid_mesh_export_rerun.json records the digital integrity results.

All hardware dimensions remain estimated: both case bodies, boss/spline cylinder, axis offsets, shoulder and seated horn height; all omitted ear dimensions/holes and cable strain reliefs; all star arm widths/lengths/angles, hub raises, spline and screw geometry, horn holes and thickness; actual M3 threads, head/nut dimensions, printed clearances; camera envelope/lens/holes/standoffs, mass/center of mass and cable loads. The previous production_candidate_01/measurements/checklist.csv remains the complete pending measurement list; its blanks are not approvals. Printed dimensions are design choices rather than hardware measurements. Camera four-hole pattern is still absent.

Confirmed errors corrected here are the misleading identity/compatibility metadata and the production-readiness interpretation. The physical geometry errors cannot be responsibly dimension-corrected from inconsistent incomplete references. Obtain measurements of BOTH SG90s, BOTH original horns and original center screws before making a new physical interface revision. Then model the real tabs/holes/shoulders/splines or explicitly bounded mating envelopes, resolve retention/load support, and rerun complete assembly/collision/export checks including all hardware. Until then: no full-print release.
'''
open(os.path.join(R,'AUDIT.md'),'w').write(text)
table='<table><tr><th>Feature</th><th>CAD mm</th><th>Source</th><th>Comparison</th><th>Status</th></tr>'+''.join('<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'
open(os.path.join(R,'REPORT.html'),'w').write('<!doctype html><html><meta charset="utf-8"><style>body{font:16px/1.5 system-ui;max-width:1200px;margin:30px auto}td,th{border:1px solid #aaa;padding:8px}table{border-collapse:collapse}img{max-width:100%}pre{white-space:pre-wrap}</style><h1>SG90 compatibility audit: HOLD</h1>'+table+''.join('<h2>'+n.replace('_',' ')+'</h2><img src="renders/'+n+'.png">' for n in ['pan_installation','pan_horn_interface','tilt_installation','tilt_horn_interface'])+'<pre>'+html.escape(text)+'</pre></html>')
print(json.dumps(result,indent=2));print('Motion collisions in limited inherited set:',scope['report']['motion']['collision_count'])
