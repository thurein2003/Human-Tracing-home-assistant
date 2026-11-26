import json,os,math
from PIL import Image,ImageDraw,ImageFont
root=r'EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R15_GEOMETRY_REPAIR'; sec=json.load(open(root+r'\CHECKS\fresh_section_paths.json')); grid=json.load(open(root+r'\CHECKS\pocket_grid_comparison.json'));out=root+r'\RENDERS';W,H=2400,1800
try: font=ImageFont.truetype('arial.ttf',42); small=ImageFont.truetype('arial.ttf',30)
except: font=small=ImageFont.load_default()
for part,key,view in [('PanYoke_EarBracket_KeyedDrive','pan','Top'),('PanYoke_EarBracket_KeyedDrive','pan','Bottom'),('TiltCradle_KeyedHorn_CameraFrame','tilt','Top'),('TiltCradle_KeyedHorn_CameraFrame','tilt','Bottom')]:
 data=sec[key]; samples=grid[part]; img=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(img);cx,cy=W/2,H/2+15;scale=51.0
 d.text((90,55),f'{part} — R15 interface {view} view',font=font,fill='#172b43')
 pl='Z=35.85 mm' if key=='pan' else 'X=−40.15 mm'
 d.text((90,115),f'FreeCAD BREP section {pl}; 0.25 mm occupancy grid compared with R15 master cutter',font=small,fill='#334a63')
 def xy(pt):
  x,y=pt
  if view=='Bottom': y=-y
  return cx+x*scale,cy-y*scale
 # Master profile boundary in orange dashed lines.
 for path in data['master_profile_section']:
  pts=[xy(p) for p in path]
  for a,b in zip(pts,pts[1:]):
   dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
   if L<1: continue
   ux,uy=dx/L,dy/L;pos=0
   while pos<L:
    e=min(pos+9,L);d.line((a[0]+ux*pos,a[1]+uy*pos,a[0]+ux*e,a[1]+uy*e),fill='#d77d30',width=4);pos+=16
 # Actual BREP occupancy points: green=void, red=unexpected material intrusion.
 rad=3
 for x,y,material in samples['points']:
  px,py=xy((x,y));c='#d84a4a' if material else '#347b65';d.ellipse((px-rad,py-rad,px+rad,py+rad),fill=c)
 r=4*scale;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#367c67',width=3)
 d.line((cx-22*scale,cy,cx+22*scale,cy),fill='#dfe5eb',width=2);d.line((cx,cy-12*scale,cx,cy+12*scale),fill='#dfe5eb',width=2)
 d.text((90,H-205),f"R15 interior sample points: {samples['tested_profile_points']}  |  intrusion count: {samples['intruding_material_points']}  |  master cavity: 39.2 × 20.2 mm",font=small,fill='#172b43')
 d.ellipse((90,H-135,112,H-113),fill='#347b65');d.text((128,H-146),'Actual carrier is void at sampled R15 pocket points',font=small,fill='#172b43')
 d.line((900,H-124,958,H-124),fill='#d77d30',width=4);d.text((976,H-146),'R15 master profile boundary',font=small,fill='#172b43')
 d.rectangle((W-650,H-155,W-260,H-145),fill='#172b43');d.text((W-650,H-130),'10 mm',font=small,fill='#172b43')
 d.text((90,H-70),'Inspection render from actual FreeCAD BREP occupancy and master cutter; no geometry changed.',font=small,fill='#586574')
 img.save(os.path.join(out,f'{part}_R15_{view}_Section.png'))
