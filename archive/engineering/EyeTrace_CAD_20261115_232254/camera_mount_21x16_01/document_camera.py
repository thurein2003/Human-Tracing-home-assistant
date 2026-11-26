import os,json,shutil,hashlib,csv
import FreeCAD as A,Part,Mesh
H=os.path.join(os.path.dirname(os.path.abspath(__file__)),'validated');S=os.path.join(os.path.dirname(os.path.dirname(H)),'sg90_interface_repair_01')
d=A.openDocument(os.path.join(H,'EyeTrace_Camera_21x16.FCStd'));plate=d.getObjectsByLabel('Camera mounting plate -21x16mm HOLE CENTERS')[0]
st=Part.read(os.path.join(H,'parts',plate.Name+'.step'));holes=sorted(set((round(f.Surface.Center.x,6),round(f.Surface.Center.z-76,6)) for f in st.Faces if type(f.Surface).__name__=='Cylinder' and abs(f.Surface.Radius-1.2)<1e-6));expected=[(-10.5,-8),(-10.5,8),(10.5,-8),(10.5,8)]
assert holes==expected and st.isValid();diff=plate.Shape.cut(st).Volume+st.cut(plate.Shape).Volume;assert diff<.001
shutil.copy2(os.path.join(H,'parts',plate.Name+'.stl'),os.path.join(H,'CameraPlate_HoleCenters_21x16.stl'));shutil.copy2(os.path.join(H,'parts',plate.Name+'.step'),os.path.join(H,'CameraPlate_HoleCenters_21x16.step'))
previous=[]
for line in open(os.path.join(S,'manifest.sha256')):
 digest,p=line.rstrip('\n').split('  ',1);assert hashlib.sha256(open(os.path.join(S,p),'rb').read()).hexdigest()==digest;previous.append(p)
q={'step_readback_hole_centers_relative_XZ_mm':holes,'horizontal_center_spacing_mm':21,'vertical_center_spacing_mm':16,'step_symmetric_difference_mm3':diff,'source':'USER supplied nominal mounting-hole centers','original_manifest_files_unchanged':len(previous),'physical_fit':'UNVERIFIED'}
json.dump(q,open(os.path.join(H,'checks','independent_plate_readback_and_preservation.json'),'x'),indent=2)
rows=[['Horizontal mounting-hole center spacing',21,'mm','USER SUPPLIED NOMINAL','CameraPitchX'],['Vertical mounting-hole center spacing',16,'mm','USER SUPPLIED NOMINAL','CameraPitchZ'],['PCB outside width',38,'mm','UNVERIFIED prior assumption, independent of pitch','CameraPCBWidth'],['PCB outside height',38,'mm','UNVERIFIED prior assumption, independent of pitch','CameraPCBHeight'],['PCB thickness',1.6,'mm','UNVERIFIED','CameraPCBThickness'],['Actual PCB hole diameter',2.2,'mm','UNVERIFIED','CameraPCBMountHoleDiameter'],['Printed plate clearance-hole diameter',2.4,'mm','DESIGN CHOICE, physical fit unverified','CameraPlateHoleDiameter'],['Lens reference envelope diameter',14,'mm','UNVERIFIED','CameraLensEnvelopeDiameter'],['Lens projection',10,'mm','UNVERIFIED','CameraLensProjection'],['Printed plate lens clearance diameter',18,'mm','DESIGN CHOICE, actual optical/mechanical fit unverified','CameraLensClearanceDiameter']]
with open(os.path.join(H,'camera_dimensions.csv'),'x',newline='') as f:w=csv.writer(f);w.writerow(['Dimension','Value','Unit','Source/status','Independent native parameter']);w.writerows(rows)
text='''# Camera correction:21 x16mm HOLE-CENTER spacing

The horizontal21mm and vertical16mm distances are USER-SUPPLIED NOMINAL CENTER-TO-CENTER mounting dimensions. They are NOT PCB outside dimensions. The former28x28 example has been replaced in this separate revision. The previous sg90_interface_repair_01 assembly and all273 files in its recorded manifest remain unchanged.

Open EyeTrace_Camera_21x16_Assembly.FCStd (colored) or EyeTrace_Camera_21x16.FCStd. The fixed printed camera plate has four PCB attachment bores at X=+/-10.5mm and vertical Z=+/-8mm about the mounting-pattern center. The four separate M3 frame joints are NOT the PCB mounting pattern. The camera plate's own outside dimensions are56x32x3mm; these also are not the PCB dimensions.

Native RepairParameters keeps the following separate: CameraPitchX=21, CameraPitchZ=16; CameraPCBWidth/Height/Thickness; CameraPCBMountHoleDiameter; CameraPlateHoleDiameter; CameraLensEnvelopeDiameter/Projection/ClearanceDiameter and lens offsets. Only the21x16 center spacing is user-supplied. PCB38x38x1.6, PCB hole2.2, lens14 diameter/10 projection are retained UNVERIFIED reference assumptions. Printed2.4 clearance holes and18 lens opening are design choices, not measurements of your hardware. See camera_dimensions.csv.

The two old slotted rails were replaced by a single fixed four-hole plate. The frame slots were extended to accept16mm vertical spacing. Use BOTH the new camera plate and the revised TiltCradle_KeyedHorn_CameraFrame STL; the old frame's vertical slots did not accept16mm. Spacers, PCB holes and fasteners follow the new centers. Lens clearance is independently parameterized and was not derived from mounting pitch. The rest of the mechanism geometry is retained; checks/changed_geometry.json lists actual changes.

## Validation

- Native plate AND PCB hole centers measured21x16; spacer/fastener alignment checked.
- Plate STEP read-back measured the same four centers and agrees with native volume by Boolean difference.
- All13 printable components and the21x16 diagnostic gauge passed closed-mesh, manifold, connectivity, normal and self-intersection checks. Individual STL/STEP files are under parts/. Convenience plate exports are CameraPlate_HoleCenters_21x16.stl/.step.
-169 operating poses,198744 component-pair tests. No unintended penetration among nominal hardware solids was detected.
- The OLD unmeasured rear component box overlaps the new plate and four spacer/fastener locations:9 uncertainty-envelope conflicts. It was preserved and labeled UNKNOWN, not shrunk or represented as confirmed material. These conflicts require rear-component/standoff evidence and physical checking; they are NOT a clearance PASS. See checks/collision_motion.json.

No supplied camera photo/dimension establishes PCB outside size, hole diameter, lens or rear component clearance. M2 hardware is still conditional on the actual PCB holes; never force it. The updated gauge has its own30x25mm outside size, four2.4mm holes on21x16 centers, and an8mm center opening. Gauge size does not describe the PCB and the gauge center opening does not define lens clearance. Print/test it before full printing, using100% scale in mm. Check all real standoffs, screw intrusion, lens/IR and cable keep-outs.

This is a corrected nominal CAD interface, not production-ready or physically verified. Further actual dimensions may require updated spacers/fasteners/clearances;21x16 remains the supplied nominal pattern unless you provide a different nominal.
'''
open(os.path.join(H,'README.md'),'x').write(text)
# Dimension diagram: shows ONLY mounting-hole centers, no implied PCB outline.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="850" height="550" viewBox="0 0 850 550"><style>text{font:20px sans-serif;fill:#14374e}.h{fill:none;stroke:#14374e;stroke-width:2}.d{fill:none;stroke:#b14f16;stroke-width:2}</style><rect width="850" height="550" fill="white"/><text x="30" y="40">USER NOMINAL: four mounting-hole CENTERS</text><circle class="h" cx="220" cy="170" r="12"/><circle class="h" cx="535" cy="170" r="12"/><circle class="h" cx="220" cy="410" r="12"/><circle class="h" cx="535" cy="410" r="12"/><path class="d" d="M220 170V105 M535 170V105 M220 120H535 M535 170H635 M535 410H635 M620 170V410"/><text x="320" y="100">21 mm C-C</text><text x="640" y="290">16 mm C-C</text><path class="h" d="M365 290H390 M377.5 277.5V302.5"/><text x="30" y="490">Offsets about pattern center: X +/-10.5 mm; vertical +/-8 mm.</text><text x="30" y="525">No PCB outline shown. PCB size, hole diameter and lens are separate.</text></svg>'''
open(os.path.join(H,'hole_center_diagram.svg'),'x').write(svg)
print('Independent STEP hole centers:',holes,'Original manifest entries unchanged:',len(previous))
