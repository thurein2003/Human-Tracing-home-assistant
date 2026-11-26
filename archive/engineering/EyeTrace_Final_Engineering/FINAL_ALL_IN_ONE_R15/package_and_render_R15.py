import json,struct,zipfile,xml.etree.ElementTree as ET,math,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(r'EyeTrace_Final_Engineering\FINAL_ALL_IN_ONE_R15')
template=Path(r'EyeTrace_Final_Engineering\Camera_21x14_Correction_01\Creality_Print\EyeTrace_K2_ABS_Full_21x14.3mf')
target=p/'EyeTrace_K2_ABS_All_In_One_R15.3mf'; report=json.loads((p/'CHECKS/geometry_packaging_validation.json').read_text())
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'; ET.register_namespace('',ns); tag=lambda x:'{%s}%s'%(ns,x)
def stlread(path):
 b=Path(path).read_bytes(); n=struct.unpack_from('<I',b,80)[0]; off=84; vs=[];faces=[];lut={}
 def vi(v):
  v=tuple(round(float(x),6) for x in v)
  if v not in lut:lut[v]=len(vs);vs.append(v)
  return lut[v]
 tris=[]
 for i in range(n):
  pts=[struct.unpack_from('<3f',b,off+12+12*j) for j in range(3)];off+=50;idx=tuple(vi(v) for v in pts);faces.append(idx);tris.append(pts)
 return vs,faces,tris
with zipfile.ZipFile(template) as z:
 model=ET.fromstring(z.read('3D/3dmodel.model')); settings=json.loads(z.read('Metadata/project_settings.config')); ms=ET.fromstring(z.read('Metadata/model_settings.config')); files={f:z.read(f) for f in z.namelist() if f not in ('3D/3dmodel.model','Metadata/project_settings.config','Metadata/model_settings.config')}
resources=model.find(tag('resources')); objs={o.attrib.get('id'):o for o in resources.findall(tag('object'))}
for oid,name in [('3','PanYoke_EarBracket_KeyedDrive'),('6','TiltCradle_KeyedHorn_CameraFrame')]:
 verts,faces,_=stlread(p/'STL/bed_components'/f'{name}.stl'); obj=objs[oid]
 for child in list(obj):obj.remove(child)
 mesh=ET.SubElement(obj,tag('mesh')); vr=ET.SubElement(mesh,tag('vertices'))
 for x,y,z in verts: ET.SubElement(vr,tag('vertex'),{'x':'%.9g'%x,'y':'%.9g'%y,'z':'%.9g'%z})
 fs=ET.SubElement(mesh,tag('triangles'))
 for a,b,c in faces:ET.SubElement(fs,tag('triangle'),{'v1':str(a),'v2':str(b),'v3':str(c)})
 obj.attrib['name']=name
# update project identity while keeping vendor printer/material/support profiles intact
settings['project_name']='EyeTrace K2 ABS All-in-One R15'
changes={'3D/3dmodel.model':ET.tostring(model,encoding='utf-8',xml_declaration=True),'Metadata/project_settings.config':json.dumps(settings,indent=2).encode(),'Metadata/model_settings.config':ET.tostring(ms,encoding='utf-8',xml_declaration=True)}
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for f,b in files.items():z.writestr(f,b)
 for f,b in changes.items():z.writestr(f,b)
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 mm=ET.fromstring(z.read('3D/3dmodel.model')); mo=mm.findall('.//'+tag('resources')+'/'+tag('object')); meshobjs=[o for o in mo if o.find(tag('mesh')) is not None]; build=mm.findall('.//'+tag('build')+'/'+tag('item'))
 assert len(meshobjs)==13 and len(build)==13,(len(meshobjs),len(build))
# actual mesh-derived build plate image (top orthographic projection)
W=1600; margin=120; scale=(W-2*margin)/260; H=W; im=Image.new('RGB',(W,H),(246,248,250));d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
for mm in range(0,261,20):
 x=margin+mm*scale;y=margin+mm*scale;d.line((x,margin,x,H-margin),fill=(220,225,230),width=1);d.line((margin,y,W-margin,y),fill=(220,225,230),width=1)
d.rectangle((margin,margin,W-margin,H-margin),outline=(25,40,55),width=3)
colors=[(90,145,200),(200,130,70),(80,165,135),(180,105,145),(145,130,200),(190,175,80),(75,155,175),(185,115,85),(110,165,95),(140,115,175),(195,140,120),(80,130,180),(180,165,110)]
for idx,part in enumerate(report['printable_components']):
 name=part['name']; vs,faces,tris=stlread(p/'STL/bed_components'/f'{name}.stl')
 # sort back-to-front by height so upper faces occlude lower projections
 for tri in sorted(tris,key=lambda t:sum(v[2] for v in t)/3):
  pts=[(margin+v[0]*scale,margin+(260-v[1])*scale) for v in tri]
  d.polygon(pts,fill=colors[idx%len(colors)])
 bb=part['bed_bbox'];cx=(bb[0]+bb[3])/2;cy=(bb[1]+bb[4])/2;screen=(margin+cx*scale,margin+(260-cy)*scale)
 d.text((screen[0],screen[1]),str(idx+1),fill=(20,20,20),font=font,anchor='mm',stroke_width=2,stroke_fill='white')
d.text((60,35),'Eye Trace — Creality K2 ABS Full Bed / R15 integrated candidate',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',28),fill=(20,35,50));d.text((60,H-55),'260 × 260 mm bed • 13 printable parts • 10 mm minimum arranged margin • pocket fit remains provisional',font=small,fill=(40,50,60));im.save(p/'RENDERS/Creality_K2_R15_Build_Plate.png')
# mesh geometry summary
allvol=sum(x['volume_mm3'] for x in report['printable_components']);summary={'3mf':str(target),'zip_valid':True,'mesh_objects':13,'build_items':13,'component_names':[x['name'] for x in report['printable_components']],'modified_object_ids':['3','6'],'bounds_bed_mm':report['bed_bounds_mm'],'all_parts_inside_260mm_bed':report['within_bed'],'overlap_pairs':report['pairwise_print_intersections'],'sum_solid_volume_mm3':allvol,'approx_net_abs_mass_g_at_density_1.04':round(allvol/1000*1.04,2),'slicer_toolpath':'not yet sliced'}
(p/'CHECKS/3mf_package_validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))

