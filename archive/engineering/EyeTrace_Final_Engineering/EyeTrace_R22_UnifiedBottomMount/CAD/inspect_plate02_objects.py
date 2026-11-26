import zipfile,re,json
from pathlib import Path
p=Path(r'EyeTrace_Final_Engineering\EyeTrace_R22_UnifiedBottomMount\PRINT\Plate02_R22_UnifiedBottomMount_UNSLICED.3mf')
with zipfile.ZipFile(p) as z:
 cfg=z.read('Metadata/model_settings.config').decode()
 print(cfg)
 for n in z.namelist():
  if n.startswith('3D/Objects/') and n.endswith('.model'):
   t=z.read(n).decode(errors='ignore'); name=re.search(r'<object[^>]*name="([^"]*)"',t)
   print(n,'name=',name.group(1) if name else '?','v=',len(re.findall(r'<vertex ',t)),'tri=',len(re.findall(r'<triangle ',t)))
