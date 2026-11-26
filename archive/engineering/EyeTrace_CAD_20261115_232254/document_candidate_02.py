import os,json,hashlib,html,datetime
ROOT=os.path.dirname(os.path.abspath(__file__));R=os.path.join(ROOT,'candidate_02')
v=json.load(open(os.path.join(R,'checks','validation.json')));audit=json.load(open(os.path.join(R,'checks','export_audit.json')))
assert v['motion']['collision_count']==0
for n,d in audit.items():
 if n.endswith('.stl'):assert d['closed'] and not d['nonmanifold'] and not d['self_intersections'] and not d['nonuniform_orientation'], n
assert os.path.exists(os.path.join(R,'renders','render_status.json'))
def write(path,txt):
 with open(path,'x',encoding='utf-8') as f:f.write(txt)
inv='''# Initial project inventory

Inspected location:  on 2026-11-15 (Asia/Bangkok).

The initial directory listing, including hidden entries, and recursive file listing were empty. There were no subfolders, STL, STEP/STP, FCStd, ZIP, reference images, CAD scripts, or project instruction files. No Heavy Duty Pan & Tilt for FPV archive was present. No reference archive was extracted, geometry copied, or third-party CAD imported. All generated geometry was independently constructed with FreeCAD primitives and Boolean operations. No license terms from an unavailable reference can be asserted.

FreeCAD was located using the Windows uninstall registry and Start menu shortcut: D:/App files/bin/FreeCAD.exe. The installed FreeCADCmd.exe reports 1.1.4 revision 20260928. Bundled Python is D:/App files/bin/python.exe (Python 3.11). Importing FreeCAD, Part and MeshPart succeeded; a 1 x 2 x 3 mm OpenCascade solid returned 6 mm3. Mesh requires importing FreeCAD first in this environment. The actual GUI rendered the final geometry using Coin3D.

All created files are under EyeTrace_CAD_20261115_232254. Earlier revisions are preserved for traceability and are superseded. Revision 2 contains a disconnected flange and must not be printed. Only candidate_02 is the current candidate. The folder final_prototype has failed fastener motion checks; release_candidate has a failed yoke mesh audit. These are retained and superseded. No original project files existed to alter.
'''
write(os.path.join(ROOT,'INVENTORY.md'),inv)
measure='''# Hardware fit and assembly — prototype only

The mechanism has been modeled and exported, but a functional hardware fit has NOT been validated. Do not treat the STLs as a production release. Camera resolution and 3.6 mm focal length do not specify mounting geometry.

| Required measurement | Modeled assumption / acceptance question |
|---|---|
| SG90 main case, both units | 23 x 12 x 23 mm case envelope; flange ears, case bulges and strain relief omitted |
| Pan case to shaft and flange offsets | Shaft axis at X=0, case X=-6..17; actual shoulder and horn seating height must be checked |
| Tilt shaft height and axial offset | X axis through Y=0, Z=78; case X=-70..-47, Z=61..84 |
| Star horn shape, hub and thickness | Five-arm visual envelope radius 12 mm, 2 mm flat clamped web, 8 mm central clearance; actual raised hubs may prevent clamping |
| Horn-to-spline screw | Original servo-specific center screws required, not M3; availability and length unconfirmed |
| M3 hardware | Assumed 10 mm under head, 5.6 mm head diameter, 3 mm head height, 5.5 mm nut across flats, 2.4 mm nut thickness; no washers |
| Camera body and boards | Assumed 38 x 38 x 30 mm block; measure IR boards, lens, LEDs, connector, cable exit, mounting holes and keep-out areas |
| Lens projection | Assumed 14 mm diameter, 10 mm protrusion; optical field of view and IR reflections not checked |
| Camera retention | Two straps through shelf slots; straps are additional hardware not confirmed available; neither screw-hole fit nor exposed PCB pressure is verified |
| Payload | Camera mass, center of mass, wire drag, servo torque and thermal duty cycle unknown |
| Printer / PETG | Confirm selected K2 profile, actual material shrinkage, screw-hole and nut-pocket fit |

The nominal modeled idler axial air gap is 0.5 mm. M3 is a plain pivot envelope, not a modeled precision bearing. A 10 mm screw leaves 1.6 mm nominal thread projection beyond a 2.4 mm nut for the 6 mm idler grip. Nut retention against loosening, bearing friction, backlash and wear need physical testing. Do not tighten the idler enough to bind the cheeks. A verified locking method may require different hardware; none is claimed to be supplied.

Horn sandwiches use four M3 x 10 fasteners each, with a nominal 5.5 mm grip and 2.1 mm nut-side projection. They clamp the original horns rather than attempting to print servo splines. Torque transmission depends on friction and the real horn profile. Clamp force, PETG creep, horn slip and allowable tightening torque have not been validated. M3 does not replace the original center spline screw. Retainer joints have 5 mm nominal grip and 2.6 mm projection. Screw access is represented by bores, but actual tool access with servo cables and real hardware must be checked.

## Bill of materials

- One each of the seven printed parts listed in README.md.
- Two SG90 position servos with their two original star horns.
- Thirteen M3 x 10 screws and thirteen nominal 2.4 mm M3 nuts: four pan horn, four tilt horn, one idler, two pan retainer, two tilt retainer. Screw and nut quantity on hand is unknown.
- Two original servo-specific horn center screws, availability unconfirmed.
- Camera-retention straps and suitable padding, not confirmed on hand.
- Base fastening to the intended support: four 3.4 mm clearance holes, support thickness and fastening hardware unspecified.
- Suitable servo power source and controller, not modeled.

## Assembly sequence after measuring the hardware

1. Check every critical dimension above. Revise the generator before printing if any mounting geometry differs. Do not assume the SG90 label determines case or horn fit.
2. Slice a fit sample or check the relevant printed holes with your actual M3 screws and nuts. Inspect PETG parts for support scars, cracks and warping.
3. Seat the pan servo in the base with a clear cable exit. Fit the pan retainer with two M3 joints; prevent case distortion.
4. Electrically center each servo using its own safe operating range, then disconnect power. Attach the original horns using the correct original center screws.
5. Sandwich the pan star horn between its clamp and the yoke platform. Fit four M3 screws from below, with nuts in the top recesses. Check access to the original spline screw and verify no horn slip.
6. Seat the tilt servo in the outboard cage. Fit the tilt retainer using two M3 joints. Keep the cable clear of the moving cradle.
7. Sandwich the tilt star horn between its clamp and cradle flange using four M3 joints. Use the wall bores for head access. Fit the M3 idler through the coaxial right holes with the nominal 0.5 mm axial gap; check free motion and reliable nut retention.
8. Secure the camera using measured, suitable straps and padding that avoid PCB components, IR LEDs and ventilation needs. Route a relaxed cable loop around both axes and provide strain relief.
9. With servo power off, slowly check the entire intended range using the real cables, fasteners and camera. Confirm balance, no rubbing and no hidden head or wire interference. Stop on contact; never force servo gears.
10. Test powered motion gradually under the real payload. Measure backlash, idle/stall behavior, current, horn slip and temperature. There are no mechanical end stops. The sampled +/-60 degree pan and +/-30 degree tilt range is a CAD test envelope, not a guaranteed safe servo command range.

## PETG slicing notes

Use candidate_02/single_bed.stl at 100% scale in millimeters. It contains seven independent shells; split into objects in the slicer if needed. All parts have a minimum Z of zero within floating-point tolerance. There is at least 8 mm between their axis-aligned packing boxes. Bed fit is for the part geometry only; brims, supports, purge towers and exclusion zones must also fit.

The base and yoke are upright; the cradle is on its side; both thin horn clamps lie flat. The yoke's outboard servo cage and parts of the cradle need supports. Review every layer and keep support scars out of horn seating faces, nut seats and pivot bores. The pan retainer includes a 1.3 mm residual web at its screw-head relief; inspect its layers and verify its stiffness under clamp load. The 1.5 mm horn clamp plates are thin and need a sound first layer and full solid thickness. Their strength and long-term PETG creep are unverified. Choose PETG temperatures and cooling from the filament manufacturer's profile; no generic temperature is asserted as tested. Print settings, strength, dimensional accuracy and actual print quality have not been validated.

Manufacturer references used for context only, not hardware fit: [TowerPro SG90](https://towerpro.com.tw/product/sg90-analog/) and [Creality K2 series](https://www.creality.com/products/k2-series-3d-printer). The SG90 manufacturer lists overall dimensions; the simplified local case model does not establish flange, shaft or horn dimensions.
'''
write(os.path.join(R,'BUILD_AND_FIT.md'),measure)
rows='\n'.join('| '+n+' | '+str(d['solids'])+' | '+str(d['valid'])+' |' for n,d in v['solids'].items())
b=v['bed']['bounds_mm'];mc=v['motion']['collision_count']
readme=f'''# Eye Trace — FreeCAD two-axis prototype

**Physical hardware fit NOT VALIDATED. This is a reviewable prototype, not a print-released functional assembly.**

Created with installed FreeCAD 1.1.4 using its Python/OpenCascade geometry engine. Start with [EyeTrace_Assembly.FCStd](EyeTrace_Assembly.FCStd), the colored assembly with separate printed and nominal hardware groups. [EyeTrace.FCStd](EyeTrace.FCStd) is the headless build snapshot. [assembly.step](assembly.step) exchanges the positioned assembly. Individual STEP and bed-oriented STL files are in [parts](parts/). The [single-bed STL](single_bed.stl) contains all seven printed parts, without the hardware.

![Actual FreeCAD assembly render](renders/assembly_isometric.png)

The pan axis is global Z through X=Y=0. The tilt axis is global X through Y=0, Z=78 mm, carried by the pan yoke. The original star horns are retained by printed sandwich clamps; M3 is used for structural fastening and the opposite idler. No printed splines are claimed to fit the servos. Servo retention uses printed caps. Camera retention is provisionally by straps.

## Verified digitally

| Printed part | Solid count | BRep valid |
|---|---:|---|
{rows}

All seven STL parts reload as one connected closed mesh apiece, without detected nonmanifold edges, self-intersections, or inconsistent face orientation. All seven STEP parts reload as one valid solid. The single-bed STL reloads as seven closed connected components with no detected self-intersections. Packed geometric dimensions: {b[0]:.1f} x {b[1]:.1f} x {b[2]:.1f} mm, minimum packing gap 8 mm; within the standard K2 260 x 260 mm bed before slicer additions.

Motion check: {v['motion']['sampled_poses']} sampled poses, +/-60 degree pan in 10 degree steps and +/-30 degree tilt in 5 degree steps. {v['motion'].get('pair_checks','not recorded')} pair checks, {mc} detected positive-volume collisions in the tested set. Nominal M3 shanks, heads and nuts are included in the final motion audit. Common pan rotation is reused mathematically for internal pair checks. Face contact is permitted; collision threshold is 0.001 mm3. See [validation.json](checks/validation.json) for the actual pairs and results and [export_audit.json](checks/export_audit.json) for independent export checks.

{'No sampled collisions were detected. This does not establish continuous clearance or hardware fit.' if mc==0 else 'UNRESOLVED COLLISIONS EXIST. Inspect the listed pairs before proceeding.'}

## Limits and next measurements

The camera is an assumed envelope, not a manufacturer CAD model. Servo ears, strain relief, cables, actual horn hubs, screw threads, real tool access, optical field of view and IR light paths are not fully represented. No print, torque, strength, creep, cable-bend, fastener-locking or physical motion test has been performed. No mechanical stops are included. The camera dimensions and horn profile are critical blockers. Read [BUILD_AND_FIT.md](BUILD_AND_FIT.md) for measurements, hardware requirements, assembly steps and PETG slicing notes.

The native file is a positioned BRep assembly with separate component objects, not a native Assembly workbench joint solver. Kinematics are explicit rigid transforms about the documented axes. The generator is editable Python with dimension assumptions in code; parameters.json records selected assumptions and is not a complete live parameter driver.

## Reproduce and inspect

Preserved scripts in the parent folder: build_candidate_02.py, audit_candidate_02.py and render_candidate_02.FCMacro. Run with the installed `D:/App files/bin/python.exe`. The builder intentionally refuses to recreate an existing candidate_02 output folder; choose a NEW output path in a copied script for another run. Do not delete or overwrite earlier output to rerun it. The render macro produces real FreeCAD GUI views from the same geometry source. Source units and STL units are millimeters (STL itself has no unit metadata).

Earlier revisions are retained as design history and must not be selected for printing. Initial project and FreeCAD discovery are recorded in [INVENTORY.md](../INVENTORY.md).

More views: [front](renders/assembly_front.png), [right](renders/assembly_right.png), [top](renders/assembly_top.png), [pan60 / tilt30](renders/pose_pan60_tilt30.png), [exploded printed parts](renders/exploded_printed_parts.png), [single bed](renders/single_bed.png). A self-contained local gallery page is [REPORT.html](REPORT.html).
'''
write(os.path.join(R,'README.md'),readme)
imgs=['assembly_isometric','assembly_front','assembly_right','assembly_top','pose_pan60_tilt30','exploded_printed_parts','single_bed']
gallery=''.join('<figure><img loading="lazy" src="renders/'+n+'.png"><figcaption>'+html.escape(n.replace('_',' '))+'</figcaption></figure>' for n in imgs)
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eye Trace CAD prototype</title><style>body{font:16px/1.55 system-ui;margin:32px auto;max-width:1100px;padding:0 20px;color:#1b2733;background:#f6f8fa}header{background:#fff;padding:24px;border-left:6px solid #d77924}.status{font-weight:bold;color:#963d08}figure{background:white;padding:14px;margin:24px 0}img{width:100%;height:auto}figcaption{font-weight:600}a{color:#185b89}</style><header><h1>Eye Trace pan and tilt</h1><p class="status">Prototype — physical hardware fit NOT VALIDATED</p><p>Seven printable parts, nominal M3 fasteners, two SG90 envelopes and an assumed camera. Geometry generated and rendered in FreeCAD 1.1.4.</p><p>Sampled motion collisions: '+str(mc)+'; meshes: seven connected closed parts. See the actual reports for scope and limits.</p><nav><a href="README.md">CAD report</a> · <a href="BUILD_AND_FIT.md">Measurements and assembly</a> · <a href="checks/validation.json">Motion checks</a> · <a href="checks/export_audit.json">Export audit</a> · <a href="EyeTrace_Assembly.FCStd">FreeCAD assembly</a></nav></header>'+gallery+'</html>'
write(os.path.join(R,'REPORT.html'),page)
manifest=[]
for parent,dirs,files in os.walk(ROOT):
 for name in sorted(files):
  path=os.path.join(parent,name)
  if name=='manifest.sha256':continue
  with open(path,'rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
  manifest.append(digest+'  '+os.path.relpath(path,ROOT).replace('\\','/'))
write(os.path.join(ROOT,'manifest.sha256'),'\n'.join(sorted(manifest))+'\n')
print('Documentation and manifest created. Collision count:',mc)

