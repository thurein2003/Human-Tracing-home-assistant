import struct,zipfile,re,json
from pathlib import Path
p=Path(r'EyeTrace_Final_Engineering\EyeTrace_R21_SinglePanMountPlate')
for stl in [p/'STL'/'PanYoke_R20_LowProfile_PrintOrientation.stl',p/'STL'/'PanYoke_R20_LowProfile.stl']:
 if stl.exists():
  b=stl.read_bytes();n=struct.unpack_from('<I',b,80)[0];vs=[]
  for i in range(n):
   v=struct.unpack_from('<12fH',b,84+i*50)
   vs += [v[3:6],v[6:9],v[9:12]]
  bb=[[min(v[k] for v in vs),max(v[k] for v in vs)] for k in range(3)]
  print(stl.name, 'facets',n,'bbox',bb)
q=p/'PRINT'/'Plate02_R21_SingleMountPlate_SLICED_HOLD.3mf'
with zipfile.ZipFile(q) as z:
 for nm in ['3D/Objects/object_2.model','Metadata/model_settings.config']:
  s=z.read(nm).decode()
  if 'object_2.model' in nm:
   v=re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',s)
   bb=[[min(float(a[k]) for a in v),max(float(a[k]) for a in v)] for k in range(3)]
   print(nm,'bbox',bb)
  else:
   i=s.find('value="PanYoke_EarBracket_KeyedDrive"')
   print('yoke settings',s[i-100:i+800])
