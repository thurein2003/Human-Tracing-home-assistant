import struct, collections, json
from pathlib import Path

root = Path(r"EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01")
files = [root/"FIT_TESTS"/"ABS_Circular_Clearance_Calibration_Bed.stl"] + sorted((root/"STL").glob("*.stl"))
results = []
def vertex(v): return tuple(round(x, 5) for x in v)
for p in files:
    b = p.read_bytes()
    if len(b) < 84: raise ValueError("truncated STL: "+str(p))
    n = struct.unpack_from("<I", b, 80)[0]
    if len(b) != 84 + 50*n: raise ValueError("unexpected or truncated binary STL: "+str(p))
    edges = collections.Counter()
    xs=[]; ys=[]; zs=[]; off=84
    for _ in range(n):
        v=[vertex(struct.unpack_from("<3f", b, off+12+12*j)) for j in range(3)]
        off += 50
        for x,y,z in v: xs.append(x); ys.append(y); zs.append(z)
        for j in range(3): edges[tuple(sorted((v[j],v[(j+1)%3])))] += 1
    nonmanifold=sum(c != 2 for c in edges.values())
    result={"file":str(p.relative_to(root)),"bytes":len(b),"triangles":n,"edge_incidence_non2":nonmanifold,
            "bounds_mm":[round(min(xs),3),round(min(ys),3),round(min(zs),3),round(max(xs),3),round(max(ys),3),round(max(zs),3)],
            "watertight_edge_test":nonmanifold==0}
    results.append(result)
if any(not x["watertight_edge_test"] for x in results): raise SystemExit("FAIL: mesh edge-incidence check")
bed=results[0]["bounds_mm"]
out={"status":"PASS" if len(results)==21 else "FAIL", "files_checked":len(results), "bed_xy_span_mm":[round(bed[3]-bed[0],3),round(bed[4]-bed[1],3)], "k2_260mm_xy_fit":bed[3]-bed[0] <= 260 and bed[4]-bed[1] <= 260,"stls":results}
(root/"CHECKS"/"coupon_mesh_validation.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
