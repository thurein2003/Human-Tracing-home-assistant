from pathlib import Path
import struct,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).parent.parent
before_path=root.parent/'EyeTrace_R18_CircularMount_Correction_01'/'STL'/'PanYoke_CircularMount_R18C1.stl'
after_path=root/'STL'/'PanYoke_R19_ThinMountPlate.stl'
def read_stl(path):
 d=path.read_bytes(); n=struct.unpack_from('<I',d,80)[0]; a=np.empty((n,3,3),dtype=np.float32)
 for i in range(n):
  f=struct.unpack_from('<12fH',d,84+i*50); a[i]=[(f[3],f[4],f[5]),(f[6],f[7],f[8]),(f[9],f[10],f[11])]
 return a
def render(tris,size=(850,690),az=45,el=28):
 W,H=size; az=math.radians(az); el=math.radians(el)
 center=(tris.reshape(-1,3).min(axis=0)+tris.reshape(-1,3).max(axis=0))/2
 x=tris[:,:,0]-center[0]; y=tris[:,:,1]-center[1]; z=tris[:,:,2]-center[2]
 ca,sa,ce,se=math.cos(az),math.sin(az),math.cos(el),math.sin(el)
 u=ca*x-sa*y; up=-sa*se*x-ca*se*y+ce*z; dep=sa*ce*x+ca*ce*y+se*z
 umin,umax=float(u.min()),float(u.max()); vmin,vmax=float(up.min()),float(up.max())
 scale=min((W-70)/(umax-umin),(H-70)/(vmax-vmin)); px=(W-scale*(umin+umax))/2+u*scale; py=(H+scale*(vmin+vmax))/2-up*scale
 db=np.full((H,W),-1e30,dtype=np.float32); img=np.full((H,W,3),[246,248,251],dtype=np.uint8)
 # Flat, softly shaded CAD surfaces with a true per-pixel depth buffer (no triangle wire clutter).
 light=np.array([.30,.42,.86]); light/=np.linalg.norm(light)
 for i in range(len(tris)):
  xx=px[i]; yy=py[i]; dd=dep[i]
  xmin=max(0,int(math.floor(float(xx.min())))); xmax=min(W-1,int(math.ceil(float(xx.max())))); ymin=max(0,int(math.floor(float(yy.min())))); ymax=min(H-1,int(math.ceil(float(yy.max()))))
  if xmin>xmax or ymin>ymax: continue
  p1=np.array([xx[0],yy[0]]); p2=np.array([xx[1],yy[1]]); p3=np.array([xx[2],yy[2]])
  den=(p2[1]-p3[1])*(p1[0]-p3[0])+(p3[0]-p2[0])*(p1[1]-p3[1])
  if abs(den)<1e-8: continue
  gx,gy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
  w1=((p2[1]-p3[1])*(gx-p3[0])+(p3[0]-p2[0])*(gy-p3[1]))/den
  w2=((p3[1]-p1[1])*(gx-p3[0])+(p1[0]-p3[0])*(gy-p3[1]))/den
  w3=1-w1-w2; inside=(w1>=-1e-5)&(w2>=-1e-5)&(w3>=-1e-5)
  if not inside.any(): continue
  depth=w1*dd[0]+w2*dd[1]+w3*dd[2]
  sub=db[ymin:ymax+1,xmin:xmax+1]; mask=inside&(depth>sub)
  if not mask.any():continue
  a,b,c=tris[i]; n=np.cross(b-a,c-a); norm=np.linalg.norm(n)
  if norm<1e-12:continue
  shade=.30+.70*max(0,float(np.dot(n/norm,light)))
  base=np.array([174,184,197]); color=np.clip(base*shade,0,255).astype(np.uint8)
  sub[mask]=depth[mask]; tile=img[ymin:ymax+1,xmin:xmax+1];tile[mask]=color
 return Image.fromarray(img)
left=render(read_stl(before_path));right=render(read_stl(after_path))
W,H=1780,900; out=Image.new('RGB',(W,H),(232,235,239));d=ImageDraw.Draw(out)
try: font=ImageFont.truetype('arial.ttf',28); small=ImageFont.truetype('arial.ttf',20)
except: font=small=ImageFont.load_default()
d.text((35,18),'EYE TRACE R19 — PAN-YOKE PLATE REDUCTION',font=font,fill=(23,31,42));out.paste(left,(25,70));out.paste(right,(905,70))
d.text((55,775),'R18 C1 — 5.8 mm plate / 4.1 mm material above R15 pocket floor',font=small,fill=(23,31,42))
d.text((935,775),'R19 — 2.5 mm plate / 2.5 mm above R15 floor; local pads and land retained',font=small,fill=(23,31,42))
d.text((640,835),'Matched isometric projection from exported CAD meshes; approximate saved R18 axonometric angle.',font=small,fill=(75,83,94))
out.save(root/'SCREENSHOTS'/'R18_R19_ThinPlate_Comparison.png');right.save(root/'SCREENSHOTS'/'R19_PanYoke_ThinPlate_Isometric.png');print('saved z-buffered views')
