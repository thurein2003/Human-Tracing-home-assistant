import FreeCAD as A, json, re
from pathlib import Path
root=Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
d=A.openDocument(str(root/"FIT_TESTS"/"ABS_Clearance_Calibration.FCStd"))
objs=[o for o in d.Objects if hasattr(o,"Shape") and not o.Shape.isNull()]
def overlap(a,b):
    x,y=a,b
    return x.XMin<=y.XMax and x.XMax>=y.XMin and x.YMin<=y.YMax and x.YMax>=y.YMin and x.ZMin<=y.ZMax and x.ZMax>=y.ZMin
checks=[]; ncommon=0
for i,a in enumerate(objs):
    for b in objs[i+1:]:
        if not overlap(a.Shape.BoundBox,b.Shape.BoundBox): continue
        ncommon+=1
        inter=a.Shape.common(b.Shape)
        vol=inter.Volume if not inter.isNull() else 0.0
        checks.append({"a":a.Label,"b":b.Label,"intersection_volume_mm3":round(vol,8),"pass":vol<1e-6})
bad=[x for x in checks if not x["pass"]]
result={"status":"PASS" if not bad else "FAIL","solids":len(objs),"bbox_candidate_pairs_checked":ncommon,"pairs_with_solid_intersection":len(bad),"pair_results":checks}
(root/"CHECKS"/"coupon_pair_interference.json").write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!="pair_results"},indent=2))
if bad: raise SystemExit("solid intersections detected")
