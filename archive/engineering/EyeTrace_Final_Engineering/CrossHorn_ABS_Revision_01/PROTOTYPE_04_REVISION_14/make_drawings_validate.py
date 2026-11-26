import json,struct,zipfile,xml.etree.ElementTree as ET, math, os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(r'EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01\PROTOTYPE_04_REVISION_14')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22); small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18); title=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',30)
def draw_paths(img, paths, box, color=(28,80,145), width=4):
 d=ImageDraw.Draw(img); x0,y0,x1,y1=box
 allp=[pt for path in paths for pt in path]
 xs=[v[0] for v in allp]; ys=[v[1] for v in allp]; loX,hiX=min(xs),max(xs); loY,hiY=min(ys),max(ys)
 s=min((x1-x0)/(hiX-loX),(y1-y0)/(hiY-loY)); ox=(x0+x1-s*(loX+hiX))/2; oy=(y0+y1+s*(loY+hiY))/2
 def tr(pt): return (ox+s*pt[0],oy-s*pt[1])
 for path in paths:
  if len(path)>1: d.line([tr(pt) for pt in path],fill=color,width=width,joint='curve')
 return tr,s
# top drawing from actual BRep top edges
paths=json.loads((p/'top_edges.json').read_text())
im=Image.new('RGB',(1500,1050),'white'); d=ImageDraw.Draw(im); d.text((60,30),'Eye Trace R14 — Top View / Actual FreeCAD BRep Edges',font=title,fill='black')
tr,s=draw_paths(im,paths,(250,170,1260,830)); d=ImageDraw.Draw(im)
# X dimension, two reaches and overall pocket
cx,cy=tr((0,0)); ydim=890; xL=tr((-19.6,0))[0]; xR=tr((19.6,0))[0]
def arrow(a,b,y,label):
 d.line((a,y,b,y),fill=(0,0,0),width=2); q=10
 d.polygon([(a,y),(a+q,y-5),(a+q,y+5)],fill='black'); d.polygon([(b,y),(b-q,y-5),(b-q,y+5)],fill='black'); d.text(((a+b)/2-95,y-34),label,font=font,fill='black')
arrow(xL,cx,ydim,'19.60 mm pocket reach'); arrow(cx,xR,ydim,'19.60 mm pocket reach')
d.text((60,955),'Nominal horn span: 39.00 mm (19.50 + 19.50)    |    Pocket envelope: 39.20 mm (0.10 mm per tip)',font=font,fill='black')
d.text((60,990),'Center bore Ø8.00 mm nominal, continuous through coupon; short-arm geometry carried forward unchanged.',font=small,fill='black')
im.save(p/'CrossHorn_04R14_Top_Dimensioned.png')
# center section from actual FreeCAD section edge coordinates
sec=json.loads((p/'vertical_section_brep.json').read_text())
im=Image.new('RGB',(1500,1050),'white'); d=ImageDraw.Draw(im); d.text((60,30),'Eye Trace R14 — Center X-Z Section / Actual FreeCAD Section',font=title,fill='black')
# custom scale view x -10..10, z -3..4.5
x0,y0,x1,y1=270,180,1230,820;s=min((x1-x0)/20,(y1-y0)/7.5); ox=(x0+x1)/2; oy=y0+3*s
trsec=lambda pt:(ox+s*pt[0],oy-s*pt[1])
for path in sec['paths']:
 if len(path)>1 and all(abs(pt[0])<=10 for pt in path):d.line([trsec(pt) for pt in path],fill=(28,80,145),width=4)
# annotate bore diameter and existing body extent wall
D=ImageDraw.Draw(im); xleft=trsec((-3.7,0))[0]; xright=trsec((3.7,0))[0]
D.line((xleft,850,xright,850),fill='black',width=2); D.polygon([(xleft,850),(xleft+9,845),(xleft+9,855)],fill='black'); D.polygon([(xright,850),(xright-9,845),(xright-9,855)],fill='black'); D.text((ox-65,860),'Ø8.00 mm',font=font,fill='black')
D.text((60,930),'Bore wall: x = ±4.00 mm from underside z = −2.20 to horn-seat plane z = +2.10.',font=font,fill='black')
D.text((60,970),'Above the seat plane, the bore opens into the preserved cross-horn pocket. No Ø5.50 restriction, shoulder, or ring remains.',font=small,fill='black')
D.text((60,1005),'Section generated from actual saved FreeCAD solid; overall coupon Z = 6.00 mm.',font=small,fill='black')
im.save(p/'CrossHorn_04R14_Center_Section_Dimensioned.png')
# STL topology and 3MF integrity
b=(p/'CrossHorn_UltraMinimal_FitTest_04R14.stl').read_bytes(); n=struct.unpack_from('<I',b,80)[0]; off=84; edges={}; verts=set()
for i in range(n):
 tri=[tuple(round(x,5) for x in struct.unpack_from('<3f',b,off+12+12*j)) for j in range(3)]; off+=50
 for v in tri: verts.add(v)
 for a,c in ((tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])):
  e=tuple(sorted((a,c)));edges[e]=edges.get(e,0)+1
with zipfile.ZipFile(p/'CrossHorn_UltraMinimal_FitTest_04R14.3mf') as z:
 bad=z.testzip(); model=ET.fromstring(z.read('3D/3dmodel.model')); ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}; obj=model.findall('.//m:object',ns); tri3=len(model.findall('.//m:triangle',ns));
report={'stl_triangles':n,'stl_unique_vertices':len(verts),'stl_closed_manifold_edge_incidence_all_2':all(v==2 for v in edges.values()),'3mf_zip_integrity':bad is None,'3mf_object_count':len(obj),'3mf_triangles':tri3,'3mf_triangle_count_matches_stl':tri3==n,'bbox_mm':[42.0,23.0,6.0],'approx_solid_volume_mm3':1211.5218,'minimum_net_abs_mass_g_at_1.04_g_cm3':round(1211.5218/1000*1.04,3),'slicer_toolpath_available':False}
(p/'mesh_export_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))



