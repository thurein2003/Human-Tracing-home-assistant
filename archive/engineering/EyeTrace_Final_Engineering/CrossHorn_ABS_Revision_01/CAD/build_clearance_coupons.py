import FreeCAD as App
import Part, MeshPart, math, os

ROOT = r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01"
OUT = os.path.join(ROOT, "FIT_TESTS")
STL = os.path.join(ROOT, "STL")
doc = App.newDocument("ABS_Clearance_Calibration")
objects = []

def add(label, shape, color=(0.78, 0.78, 0.82)):
    obj = doc.addObject("PartDesign::Feature", "Coupon")
    obj.Label = label
    obj.Shape = shape
    if obj.ViewObject:
        obj.ViewObject.ShapeColor = color
    objects.append(obj)
    return obj

def annulus(ro, ri, h):
    return Part.makeCylinder(ro, h).cut(Part.makeCylinder(ri, h))

# Pan ring pairs: documented CAD male OD64/ID60 and female OD70.6.
# Five diametral clearances include the original 0.60 mm control.
pan_gaps = [0.10, 0.20, 0.30, 0.40, 0.60]
step_x, step_y = 82.0, 75.0
for i, gap in enumerate(pan_gaps):
    col, row = i % 3, i // 3
    x, y = col * step_x, row * step_y
    female_id = 64.0 + gap
    f = annulus(35.3, female_id/2.0, 2.0)
    # tab and its one-to-five identification perforations
    tab = Part.makeBox(9.0, 8.0, 2.0, App.Vector(33.0, -4.0, 0))
    f = f.fuse(tab)
    for n in range(i+1):
        hole = Part.makeCylinder(0.75, 2.2, App.Vector(35.0 + n*1.35, 0, -0.1))
        f = f.cut(hole)
    f.translate(App.Vector(x, y, 0))
    add("PAN Female C%d ID%.2f" % (i+1, female_id), f, (0.30,0.56,0.83))
    m = annulus(32.0, 30.0, 2.0)
    m.translate(App.Vector(x, y, 0))
    add("PAN Male Control OD64 ID60 C%d" % (i+1), m, (0.88,0.58,0.25))

# Tilt journal calibration: through-bore blocks and a 5.00 mm journal plug.
# Hole axis Z for easy printing and measurement; the CAD functional pair is
# a 5 mm sleeve in a 5.2 mm bore, so 5.20 is retained as the control.
tilt_bores = [5.05, 5.10, 5.15, 5.20, 5.30]
base_y = 155.0
for i, bore in enumerate(tilt_bores):
    x = i * 24.0
    block = Part.makeBox(20.0, 16.0, 6.0)
    block = block.cut(Part.makeCylinder(bore/2.0, 6.2, App.Vector(10,8,-0.1)))
    # number of edge notches marks the variant while leaving the bore intact
    for n in range(i+1):
        notch = Part.makeBox(1.2, 2.0, 6.2, App.Vector(2+n*2.3, 14, -0.1))
        block = block.cut(notch)
    block.translate(App.Vector(x, base_y, 0))
    add("TILT Bore T%d ID%.2f" % (i+1, bore), block, (0.34,0.70,0.47))
    pin = Part.makeCylinder(2.5, 6.0)
    pin.translate(App.Vector(x+10, base_y+8, 0))
    add("TILT Journal Control OD5 T%d" % (i+1), pin, (0.85,0.57,0.32))

doc.recompute()
doc.saveAs(os.path.join(OUT, "ABS_Clearance_Calibration.FCStd"))
for obj in objects:
    shape = obj.Shape.copy()
    import re
    m = re.search(r"PAN (?:Female|Male) C(\d+)", obj.Label)
    t = re.search(r"TILT (?:Bore|Journal Control).*T(\d+)", obj.Label)
    if m:
        idx=int(m.group(1))-1; shape.translate(App.Vector(-(idx%3)*step_x, -(idx//3)*step_y, 0))
    elif t:
        idx=int(t.group(1))-1; shape.translate(App.Vector(-idx*24.0, -base_y, 0))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.08, AngularDeflection=0.12, Relative=False)
    mesh.write(os.path.join(STL, obj.Label.replace(" ", "_").replace(".", "p") + ".stl"))

# Separate single-bed layout of test coupons, all on z=0. Extents: <230 x 220.
combined = Part.makeCompound([o.Shape for o in objects])
combined.translate(App.Vector(35.4, 35.4, 0))
mesh = MeshPart.meshFromShape(Shape=combined, LinearDeflection=0.08, AngularDeflection=0.12, Relative=False)
mesh.write(os.path.join(OUT, "ABS_Circular_Clearance_Calibration_Bed.stl"))
doc.recompute()
print("GENERATED", len(objects), "objects", "bbox", combined.BoundBox)
