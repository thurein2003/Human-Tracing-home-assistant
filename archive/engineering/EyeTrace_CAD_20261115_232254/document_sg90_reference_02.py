import os,json,hashlib,csv,html
import FreeCAD as A,Part,Mesh,MeshPart
B=os.path.dirname(os.path.abspath(__file__));R=os.path.join(B,'sg90_reference_revision_02');S=os.path.join(B,'production_candidate_01');D=os.path.join(B,'sg90_reference_revision_01','sources')
d=A.openDocument(os.path.join(R,'EyeTrace_SG90_Reference_01.FCStd'));out={}
os.makedirs(os.path.join(R,'checks','mesh_roundtrip'),exist_ok=True)
for n in ['Base','PanServoRetainer','PanYoke','TiltServoRetainer']:
 s=d.getObject(n).Shape;m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.06,AngularDeflection=.15,Relative=False);p=os.path.join(R,'checks','mesh_roundtrip',n+'_VALIDATION_ONLY.stl');m.write(p);re=Mesh.Mesh(p)
 out[n]={'closed':re.isSolid(),'components':re.countComponents(),'self_intersections':re.hasSelfIntersections(),'nonmanifold':re.hasNonManifolds(),'bad_normals':re.hasNonUniformOrientedFacets()}
 assert re.isSolid() and re.countComponents()==1 and not re.hasSelfIntersections() and not re.hasNonManifolds(),n
for n in ['PanServo_ASSUMED','TiltServo_ASSUMED','PanStarHorn_ASSUMED','TiltStarHorn_ASSUMED','PanOriginalScrew_PROVISIONAL','TiltOriginalScrew_PROVISIONAL']:
 s=d.getObject(n).Shape;cs=[]
 for f in s.Faces:
  surf=f.Surface
  if type(surf).__name__=='Cylinder':cs.append({'radius_mm':surf.Radius,'axis':[surf.Axis.x,surf.Axis.y,surf.Axis.z],'point':[surf.Center.x,surf.Center.y,surf.Center.z]})
 out[n]={'valid':s.isValid(),'solid_count':len(s.Solids),'world_bounds_mm':[s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength],'cylindrical_surfaces':cs}
 assert s.isValid() and len(s.Solids)==1,n
# Confirm both new smooth output axes from actual cylindrical faces.
assert any(abs(c['radius_mm']-2.5)<1e-7 and abs(c['point'][0])<1e-7 and abs(c['point'][1])<1e-7 and abs(c['axis'][2])>.999 for c in out['PanServo_ASSUMED']['cylindrical_surfaces'])
assert any(abs(c['radius_mm']-2.5)<1e-7 and abs(c['point'][1])<1e-7 and abs(c['point'][2]-78)<1e-7 and abs(c['axis'][0])>.999 for c in out['TiltServo_ASSUMED']['cylindrical_surfaces'])
for fn in os.listdir(os.path.join(R,'coupons')):
 if fn.endswith('.step'):
  s=Part.read(os.path.join(R,'coupons',fn));out[fn]={'step_valid':s.isValid(),'solids':len(s.Solids)};assert s.isValid() and len(s.Solids)==1
json.dump(out,open(os.path.join(R,'checks','native_alignment_and_STL_readback.json'),'x'),indent=2)
changed=[];count=0
for line in open(os.path.join(S,'manifest.sha256')):
 h,p=line.rstrip('\n').split('  ',1);count+=1
 if hashlib.sha256(open(os.path.join(S,p),'rb').read()).hexdigest()!=h:changed.append(p)
assert not changed
json.dump({'original_files_checked':count,'changed':changed},open(os.path.join(R,'checks','preservation.json'),'x'),indent=2)
# Actual per-file license supersedes a generic repository description for selected native model.
attribution='''# Reference attribution and source selection

SG90 community source: Juan Fenoy, Servo sg90.fcstd / Servo-sg90.step, FreeCAD community Parts Library:
https://github.com/FreeCAD/FreeCAD-library/tree/master/Electrical%20Parts/Servos/SG-90

The downloaded native document explicitly names Juan Fenoy and CreativeCommons Attribution-ShareAlike, https://creativecommons.org/licenses/by-sa/4.0/ . Its model-specific README is empty. The repository-level README describes a general CC-BY3.0 policy; this revision follows the more specific native-file attribution/license declaration. The derived reference assembly declares CC BY-SA4.0. No endorsement by the author or manufacturer is implied. Changes: independently rebuilt parameterized case/tab/boss envelopes from cited drawing and native dimensions; no community spline tooth profile copied as a verified physical spline. New clearances, horn/screw proxy geometry and bracket modifications are identified in the dimension ledger. Source files remain unchanged in ../sg90_reference_revision_01/sources; SHA-256 hashes are recorded here.

Manufacturer: https://towerpro.com.tw/product/sg90-analog/ . Product photograph and A-F dimension-label image were inspected; cached research images belong to their original owner. The manufacturer has not supplied a STEP file here. No claim is made that this nominal drawing describes the user's two SG90 clones.

Other researched CAD leads: https://kernelcad.com/standards/micro-servo/ explicitly describes its catalog model as community reference and credits Juan Fenoy; it is not independent corroboration. https://colinsradiocontrol.com/index.php?catid=74&id=38&view=article advertises an SG90 STEP but could not be fetched, so no dimensions were adopted from it. GrabCAD SG90 listings were considered community models, not manufacturer evidence, and were not used.
'''
open(os.path.join(R,'ATTRIBUTION.md'),'x').write(attribution)
json.dump({n:hashlib.sha256(open(os.path.join(D,n),'rb').read()).hexdigest() for n in os.listdir(D)},open(os.path.join(R,'checks','source_hashes.json'),'x'),indent=2)
text='''# SG90 mechanical reference revision 02 — HOLD

This is a continuation of the original Eye Trace assembly. It replaces BOTH simplified motor references in EyeTrace_SG90_Reference_01.FCStd, preserves production_candidate_01 unchanged, and does not release a complete printing package. Revision01 is retained as a failed intermediate; revision02 is the current reference study. The filename's final01 identifies the native reference model, not a production release.

## What is and is not accurate

The external envelope is DRAWING-BASED with a per-dimension confidence ledger in dimension_comparison.csv. It is not a verified model of your specific SG90 clones. The official A-F drawing/table is given priority for clear overall/width/length dimensions; incomplete details come from Juan Fenoy's dimensioned native community model. Case height22.7, ear bottom15.9/thickness2.5 and mounting-hole details are community dimensions, not manufacturer-certified dimensions. The manufacturer F17 flange datum remains unresolved; it was not silently used as a different ear height. The nominal table A30.3 conflicts with the product headline29; neither was treated as a tolerance. All manufacturing tolerances are unspecified, and all physical fit remains UNVERIFIED.

Both references now have the SAME geometry and include a main case, full flange/tabs, diameter2 open mounting holes, cable notch, gear bosses and a separate distinguishable smooth output envelope. The case is22.7 long x12.2 wide x22.7 high; shoulder top27 and output top30.3 above the base; tabs span32.3, hole pitch27.2, ear thickness2.5. The output axis is5.9 from the nearest case end. Pan remains on globalZ atX=Y=0; tilt on globalX atY=0,Z=78. Actual saved cylindrical faces were checked for these axes.

NO spline tooth count/profile is modeled or asserted. The smooth diameter5 output is a clearance envelope derived conservatively from community geometry, not a spline dimension specification. Its1.7 axial bore comes from that community model, not a verified thread specification. Original retaining screws are represented by explicitly PROVISIONAL smooth envelopes: shank1.6, length5, head3.5 diameter x1 high, all unmeasured and not an M1.6 specification. They do not establish engagement or thread compatibility.

The original five-arm stars remain explicitly PROVISIONAL because no measured trace was provided. The exterior is inherited, not made accurate by its label. A stepped smooth socket (5.2 diameter x1.4 deep,1.9 through) makes the provisional assembly geometrically coherent; it is NOT a spline socket and is NOT a design for printing replacement horns. The real horn arm holes remain unknown and omitted. Both original horns and retaining screws must be measured before claiming any physical attachment. M3 is used only in printed structural sandwich joints, not assumed to fit the original horn holes or shaft thread.

## Bracket corrections and results

With the complete reference envelopes in the inherited brackets, four neutral collisions were detected: pan base184.64mm3, pan retainer195.70mm3, tilt retainer70.65mm3, tilt yoke83.56mm3. Tabs intersected the base/end floor and cap; the large/secondary bosses intersected the caps. The first correction missed two remaining boss contacts; its evidence is preserved in revision01. Revision02 resolves them by cutting tab clearance pockets with0.3mm nominal added clearance, clearing the pan cap to diameter12.8 plus the secondary boss relief, and clearing the tilt cap around the main boss. These are corrections to PRINTED clearance, not distortion of the servo to fit old brackets.

The case-height/datum changes required small pressure/seating lands: pan retainer0.3mm, tilt lower seat0.2mm and tilt upper cap0.1mm. These thin features must be reviewed against actual PETG layer height and dimensions; their precise CAD contacts are not a physical clamp validation. Source servo flange details and these lands need an insertion/retention test before any full bracket print. The inherited unused32mm-pitch/2.2 pilot bores are NOT the revised27.2 tab pattern and must not be used as if they align; the mechanism still retains the servos by its caps. New actual tab holes are diameter2, so M3 is not a compatible tab fastener.

The expanded motion test now includes BOTH motor bodies, BOTH horn proxies and BOTH original-screw proxies, plus all printed parts and nominal M3 envelopes. It checks169 poses over pan +/-60deg/tilt +/-30deg. Zero positive-volume collisions were detected after correction, with threshold0.001mm3. Intended camera-to-shelf contact is excluded. Other coincident contact is allowed. Discrete motion and provisional smooth mating envelopes cannot verify actual spline engagement, running gap, cable/connector clearance, tool access, optics, friction, load capacity or continuous motion. The pan still lacks a separate load bearing; this reference revision does not approve that structural load path.

All seven printed BReps are single valid solids; their in-memory meshes pass closure, connectivity, manifold, normal and self-intersection checks. The FOUR changed printed parts additionally have serialized STL read-back checks in checks/mesh_roundtrip; those files are validation artifacts, not a manufacturing package. The three unchanged printed parts were not re-exported. No final mechanism bed was generated. Both motors, both stars and the provisional original screws are valid single solids. The coupon STLs and STEP read-back also pass. See checks/*.json for exact evidence.

## Small interface tests only

Print only the three files under coupons first, at100% scale in mm and with intended PETG/nozzle/layer settings. Source hardware remains unverified, so tests may legitimately FAIL. These are standalone small tests, no full mount package.

1. SG90_TabMount_Test.stl: a2mm seating plate with23.3x12.8 body window,27.2 hole pitch and2.3 plate holes. Slide the REAL servo case through the window until its tabs seat, without forcing the body/strain relief. Measure the printed window, pitch, tab contact, cable clearance and insertion path. Test both servos separately. The servo's modeled holes are2.0; use only the verified original small mounting hardware, NEVER force M3 through it. This plate does not test complete cage insertion, cap clamping height, boss clearance or actual screw-thread fit. Record actual ear bottom height, thickness, hole centers and all case protrusions.
2. StarHorn_Clamp_Test.stl plus StarHorn_MatingFace_Test.stl: two rings with8mm central clearance and four3.3mm structural holes at14mm radius. Put the actual original star horn between the1.5mm clamp and2mm mating ring. Use four M3x10 structural screws/nuts around it; these do NOT pass through original horn holes. Check flat web contact, hub interference, star-tip interference, access to original center screw, available thread projection and gentle unpowered hand-slip behavior. A nominal2mm horn gives5.5mm grip; actual thickness must be measured. This is the smaller tilt-radius test; it does not certify surrounding bracket/tool clearance or long-term PETG friction/creep. Never print the provisional spline-free reference star as a replacement horn.

Please return both case sizes, ear bottom height/thickness/span, hole diameter/pitch, shaft center/shoulder/top heights, horn traces and thickness/raised hub, and original screw diameter/head/length plus both coupon results. Then update the reference/mount in a NEW revision and rerun all tests. Camera four-hole mounting geometry, actual payload and bearing loads are separate unresolved blockers. Full printing remains on HOLD.
'''
open(os.path.join(R,'README.md'),'x').write(text)
rows=list(csv.reader(open(os.path.join(R,'dimension_comparison.csv'))));table='<table>'+''.join('<tr>'+''.join(('<th>' if i==0 else '<td>')+html.escape(x)+('</th>' if i==0 else '</td>') for x in row)+'</tr>' for i,row in enumerate(rows))+'</table>'
imgs=['assembly_reference_replacement','pan_tabs_and_horn','tilt_tabs_and_horn','reference_case_tabs_output','reference_tab_holes']
page='<!doctype html><html lang="en"><meta charset="utf-8"><title>SG90 reference revision02 HOLD</title><style>body{font:16px/1.5 system-ui;max-width:1250px;margin:30px auto;padding:15px}td,th{border:1px solid #abc;padding:8px}table{border-collapse:collapse}pre{white-space:pre-wrap}img{max-width:100%}</style><h1>SG90 reference replacement — physical compatibility UNVERIFIED</h1><p><a href="EyeTrace_SG90_Reference_01.FCStd">Native revised assembly</a> | <a href="dimension_comparison.csv">Dimension/confidence table</a> | <a href="ATTRIBUTION.md">Sources and attribution</a></p>'+table+''.join('<h2>'+n.replace('_',' ')+'</h2><img src="renders/'+n+'.png">' for n in imgs)+'<pre>'+html.escape(text)+'</pre></html>'
open(os.path.join(R,'REPORT.html'),'x').write(page)
print('Documentation complete; original files unchanged:',count)
