from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json, zipfile, xml.etree.ElementTree as ET, struct, math
out=Path(r'EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01\PROTOTYPE_03_REVISION_02')
root=out.parent
geom=json.loads((out/'geometry_validation.json').read_text(encoding='utf-8'))
# Side-by-side visual reference review; scales are intentionally not normalized.
files=[(out/'CrossHorn_Horn3_FitTest_03R02_Top.png','FreeCAD coupon top view'),(out/'Horn3_Detail_Crop.png','Published SG90 Horn #3 drawing detail'),(root/'REFERENCES'/'download.jpg','Actual white horn in physical test photo (scale/perspective not used for dimensions)')]
W,H=1680,760; canvas=Image.new('RGB',(W,H),(247,248,250)); d=ImageDraw.Draw(canvas)
try: font=ImageFont.truetype('arial.ttf',24); small=ImageFont.truetype('arial.ttf',16)
except: font=small=ImageFont.load_default()
for i,(path,label) in enumerate(files):
    x=i*560; d.text((x+16,12),label,fill=(15,22,34),font=font)
    im=Image.open(path).convert('RGB')
    if i==2: im=im.crop((150,650,950,1530))
    im.thumbnail((528,700),Image.Resampling.LANCZOS)
    canvas.paste(im,(x+16,55))
    d.rectangle((x+8,48,x+552,760),outline=(160,167,178),width=2)
canvas.save(out/'CrossHorn_Horn3_Profile_Comparison.png')
# Independently inspect STL binary structure and 3MF package contents.
stl=out/'CrossHorn_Horn3_FitTest_03R02.stl'; data=stl.read_bytes(); tri=struct.unpack_from('<I',data,80)[0]
assert len(data)==84+tri*50, 'STL binary length mismatch'
model3mf=out/'CrossHorn_Horn3_FitTest_03R02.3mf'
with zipfile.ZipFile(model3mf) as z:
    assert z.testzip() is None, '3MF CRC failure'
    model=ET.fromstring(z.read('3D/3dmodel.model'))
    ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    objs=model.findall('.//c:resources/c:object',ns)
    meshes=[obj.find('c:mesh',ns) for obj in objs]
    meshes=[x for x in meshes if x is not None]
    assert len(meshes)==1, f'Expected one printable object, got {len(meshes)}'
    triangles=meshes[0].find('c:triangles',ns).findall('c:triangle',ns)
    assert len(triangles)==tri, '3MF triangle count does not match STL'
    settings=json.loads(z.read('Metadata/project_settings.config'))
# K2 bed plus brim envelope
bx,by,bz=geom['bbox_mm']; bedx=bx+8; bedy=by+8
assert bx<=260 and by<=260 and bz<=260 and bedx<=260 and bedy<=260
p01_volume=12892.9488; p01_mass=p01_volume*1.04/1000.0
vol=geom['solid_volume_mm3']; low_mass=vol*.55*1.04/1000; high_mass=vol*.80*1.04/1000
p01_time=p01_volume/2.5/60+5; low_time=vol*.55/2.5/60+5; high_time=vol*.80/2.5/60+5
reduction=(1-high_mass/p01_mass)*100, (1-low_mass/p01_mass)*100
validation={
 'freecad_brep':{'valid':geom['solid_valid'],'solids':geom['solid_count'],'volume_mm3':vol},
 'stl':{'binary_length_valid':True,'triangles':tri,'freecad_mesh_is_solid':geom['mesh_is_solid'],'bbox_mm':geom['bbox_mm']},
 '3mf':{'zip_crc_ok':True,'printable_object_count':len(meshes),'triangles':len(triangles),'stl_triangle_match':True,'file_bytes':model3mf.stat().st_size},
 'creality_k2_bed':{'usable_build_volume_mm':[260,260,260],'part_bbox_with_4mm_brim_mm':[bedx,bedy,bz],'fits':True},
 'motion_or_full_assembly_tests':'Not applicable: coupon only; production pan/tilt assembly unchanged',
 'slicer_toolpath':'NOT VERIFIED: project metadata prepared; actual Creality Print sliced preview/G-code not inspected',
 'physical_horn_fit':'UNVERIFIED: coupon not yet printed/tested'
}
(out/'validation_results.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
report=f'''# Prototype 03 Revision 02 — Horn #3 profile fit coupon

**Release status: provisional fit-test coupon only. Physical fit is UNVERIFIED.** No production pan/tilt parts, assembly files, or earlier prototypes were changed.

## Files

- Editable FreeCAD: `CrossHorn_Horn3_FitTest_03R02.FCStd`
- STL: `CrossHorn_Horn3_FitTest_03R02.stl`
- Creality Print project: `CrossHorn_Horn3_FitTest_03R02.3mf`
- FreeCAD viewport screenshots: `CrossHorn_Horn3_FitTest_03R02_Top.png`, `CrossHorn_Horn3_FitTest_03R02_Isometric.png`
- Visual comparison: `CrossHorn_Horn3_Profile_Comparison.png`
- Parameter source: `parameters.json`; generation macro: `build_prototype_03_revision_02.FCMacro`

## Reference comparison and dimensional choices

The cited Auselectronics Direct SG90 drawing is available at [TA0132 SG90 servo and horn drawings](https://www.auselectronicsdirect.com.au/assets/brochures/TA0132.pdf). Page 4 is the servo-body drawing; page 5 shows Horn #3. The downloaded source and rendered pages are retained in this folder. The body drawing is not used to set the removable horn hub dimensions.

The top-view CAD profile was visually compared against the actual white horn photo in `REFERENCES/download.jpg` and the Horn #3 page. Both show a four-arm unequal cross, rounded tips, broad-to-narrow long arms and unequal long reaches. The photograph and drawing are shown side-by-side in the comparison image; image scale/perspective was not used to infer physical dimensions.

| Feature | Revision 02 value | Provenance / confidence |
|---|---:|---|
| Long overall span | 35.0 mm user measurement | Confirmed nominal by user; actual measurement tolerance not supplied |
| Short span baseline | 18.0 mm user measurement | Confirmed nominal by user |
| Horn center hub | 7.0 mm user measurement | Confirmed nominal by user; distinct from servo shaft/boss |
| Horn #3 long reach either side of hub | 16.0 / 18.5 mm on drawing (34.5 mm total); normalized to 16.25 / 18.75 mm to preserve user 35 mm span | Published similar-horn drawing; provisional offset X = -1.25 mm |
| Horn #3 short span | 16.3 mm drawing; not substituted for user's 18 mm | Reference only |
| Long arm taper angles | 6.3° / 8.0° on drawing, interpreted as total width-convergence angles | Profile guidance; interpretation provisional |
| Long root width | 7.0 mm nominal estimate; 7.2 mm pocket | Scaled/profile estimate, not a dimension explicitly called out on the drawing |
| Long tip widths | CAD pocket 5.406 / 4.565 mm | Derived from the provisional root estimate, arm reaches and interpreted drawing angles |
| Short arm width | 3.2 mm nominal profile estimate; 3.4 mm pocket | Provisional scaled drawing/profile estimate; wider than Prototype 01's 3.0 mm assumption |
| Lateral pocket clearance | 0.20 mm total | User target; CAD parameter, not ABS process compensation validation |
| Short pocket end extension | +1.0 mm each end from 18 mm baseline; pocket span 20.2 mm including 0.20 mm clearance | User requirement plus nominal allowance |
| Hub recess | Ø7.4 × 2.7 mm deep | Provisional; Ø7.0 hub supplied by user and +0.4 diametral recess allowance retained |
| Separate screw access | Ø4.5 mm through | Carried forward as provisional driver/retaining-screw access; not horn spline or shaft geometry |
| Base / floor | 4.2 mm base; 1.5 mm under hub, 2.5 mm under arms | CAD-measured; floor intentionally not pierced except separate center access bore |
| Perimeter | Approximately 2.7 mm around recess | Rounded-cross envelope expansion; local perimeter varies at arm intersections |

**All arm widths, radii, local contour, hub offset, hub depth and screw-access size remain PROVISIONAL.** The published page 5 also depicts a 6.9 mm horn hub and 2.5 mm raised height; these are reference values only. User's measured 7.0 mm hub supersedes 6.9 mm. The 2.7 mm recess depth follows 2.5 mm reference height plus 0.2 mm provisional axial allowance. No secondary horn holes are modeled because their positions were not measured.

## CAD and mesh validation

- FreeCAD 1.1.4 generated and saved one valid BRep solid; BRep volume **{vol:.2f} mm³**.
- The exported STL contains **{tri} facets**; FreeCAD reports the mesh as solid/watertight.
- 3MF ZIP CRC passes, contains exactly one printable mesh object and has the same **{tri} triangles** as the STL.
- Bounding box: **{bx:.2f} × {by:.2f} × {bz:.2f} mm**. With 4 mm brim allowance: **{bedx:.2f} × {bedy:.2f} mm**, within the Creality K2 260 × 260 × 260 mm volume.
- Blind hub recess leaves **{geom['hub_floor_mm']:.2f} mm** floor; arm pocket leaves **{geom['arm_floor_mm']:.2f} mm**. Center access hole remains a separate through-feature.
- The coupon is one continuous solid with no detached geometry. Flat base on bed, pocket upward; supports disabled.

Full machine slicing is not confirmed. Creality Print 7.2 is installed, but this run did not produce or inspect sliced layers/G-code. Open the 3MF, slice it, and inspect the first layer, perimeter, pocket floors and center opening before printing.

## ABS project starting settings

0.20 mm layers, 3 walls, 12% gyroid infill, supports off, 4 mm outer brim, 255 °C nozzle and 100 °C bed. Verify these against the filament maker's range and printer configuration. The brim can be reduced after an adhesion calibration; do not scale the complete model for ABS shrinkage without measured calibration.

## Consumption and time estimates (not slicer output)

Prototype 01 reference: three coupons, combined CAD volume 12,892.95 mm³; prior project used 100% infill and 4 walls. At assumed ABS density 1.04 g/cm³, estimated mass is **{p01_mass:.2f} g**. Prototype 03 Revision 02 BRep volume is {vol:.2f} mm³. With a broad 55–80% effective material fraction for 12% infill plus walls/top/bottom, estimated mass is **{low_mass:.2f}–{high_mass:.2f} g**, or about **{reduction[0]:.1f}–{reduction[1]:.1f}% less** than the three-coupon Prototype 01 package.

Estimated time uses 2.5 mm³/s effective flow plus 5 minutes handling/travel overhead: **{p01_time:.0f} minutes** for Prototype 01 versus **{low_time:.0f}–{high_time:.0f} minutes** for this coupon. These are rough geometry-based estimates only; actual filament and time remain unknown until sliced in Creality Print.

## Physical test / remaining verification

Use the actual white horn, centered on the separate hub recess. It should sit fully into the rounded tapered pocket without force, show no arm interference or forced bending, allow the hub to seat without bottoming, and leave the original retaining screw accessible through the separate opening. Remove it by hand without prying the horn. Record arm gaps, rocking, insertion feel and whether any ABS strings need cleanup; do not sand the horn or enlarge the coupon before recording the result.

If it fails, provide a straight-down photo of the horn alongside a ruler/calipers and measure: (1) long-arm width at the root and 2–3 distances toward each tip, (2) short-arm width, (3) hub outer diameter and height above the horn plate, (4) long and short end reach from the hub center, including center offset, and (5) retaining-screw head diameter / screwdriver access requirement. Production pan/tilt drive parts remain untouched pending coupon fit.
'''
(out/'VALIDATION_REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps({'comparison_image':str(out/'CrossHorn_Horn3_Profile_Comparison.png'),'validation':validation,'estimated_mass_g':[low_mass,high_mass],'estimated_time_min':[low_time,high_time],'p01_estimated_mass_g':p01_mass,'estimated_filament_reduction_percent':reduction},indent=2))
