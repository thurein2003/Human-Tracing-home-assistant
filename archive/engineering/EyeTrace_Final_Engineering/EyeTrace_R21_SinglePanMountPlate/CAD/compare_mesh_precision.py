import zipfile,xml.etree.ElementTree as ET,json
from pathlib import Path
ns={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
files=[Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate\PRINT\Plate02_R21_SingleMountPlate_UNSLICED.3mf'),Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate\PRINT\Plate02_R21_SingleMountPlate_SLICED_HOLD.3mf')]
def get(p):
 with zipfile.ZipFile(p) as z:
  root=ET.fromstring(z.read('3D/Objects/object_4.model'));m=root.find('.//c:mesh',ns)
  vs=[tuple(float(v.attrib[k]) for k in ('x','y','z')) for v in m.find('c:vertices',ns)]
  fs=[tuple(int(t.attrib[k]) for k in ('v1','v2','v3')) for t in m.find('c:triangles',ns)]
  return vs,fs
a,fa=get(files[0]);b,fb=get(files[1])
maxd=max(max(abs(x-y) for x,y in zip(p,q)) for p,q in zip(a,b)) if len(a)==len(b) else None
print(json.dumps({'vertex_count_equal':len(a)==len(b),'triangle_count_equal':len(fa)==len(fb),'face_connectivity_identical':fa==fb,'max_coordinate_delta_mm':maxd,'position_transform_unchanged':'see preserved assemble_item','within_0.001_mm':maxd is not None and maxd<=0.001},indent=2))
