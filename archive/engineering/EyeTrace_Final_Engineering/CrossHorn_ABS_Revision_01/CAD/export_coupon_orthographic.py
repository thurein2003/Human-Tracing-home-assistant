import FreeCAD as App, os, html
from pathlib import Path

root=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
doc=App.openDocument(str(root/"FIT_TESTS"/"ABS_Clearance_Calibration.FCStd"))
items=[o for o in doc.Objects if hasattr(o,"Shape") and not o.Shape.isNull()]
bb=doc.Objects[0].Shape.BoundBox
for o in items[1:]: bb.add(o.Shape.BoundBox)
W,H,margin=756,488,24
scale=min((W-2*margin)/bb.XLength,(H-2*margin)/bb.YLength)
def pt(x,y): return margin+(x-bb.XMin)*scale, H-margin-(y-bb.YMin)*scale
colors={"PAN Female":"#4386c5","PAN Male":"#e38f37","TILT Bore":"#4fa66b","TILT Journal":"#c87c42"}
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#fafbfd"/>',
       '<text x="18" y="22" font-family="Arial" font-size="15" font-weight="bold" fill="#17212b">ABS pivot-clearance calibration — FreeCAD BRep projection</text>']
for o in items:
    color=next((c for k,c in colors.items() if o.Label.startswith(k)),"#606a75")
    for e in o.Shape.Edges:
        try: pts=e.discretize(Deflection=0.15)
        except: pts=e.discretize(Number=24)
        if len(pts)<2: continue
        coords=[pt(v.x,v.y) for v in pts]
        d="M "+" L ".join("%.2f %.2f"%v for v in coords)
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"/>')
    b=o.Shape.BoundBox
    cx,cy=pt((b.XMin+b.XMax)/2,(b.YMin+b.YMax)/2)
    if o.Label.startswith("PAN Female"):
        label=o.Label.replace("PAN Female ","")
    elif o.Label.startswith("TILT Bore"):
        label=o.Label.replace("TILT Bore ","")
    else:
        label=""
    if label: parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" font-family="Arial" font-size="8" fill="#1b2832">{html.escape(label)}</text>')
parts.append('<text x="18" y="480" font-family="Arial" font-size="9" fill="#263746">Blue pan bores • orange male/journal controls • green tilt bores • 1–5 holes/notches identify variants.</text>')
parts.append('</svg>')
(root/"RENDERS"/"ABS_clearance_coupon_top.svg").write_text("\n".join(parts),encoding="utf-8")
print("wrote BRep projection",root/"RENDERS"/"ABS_clearance_coupon_top.svg","objects",len(items))
