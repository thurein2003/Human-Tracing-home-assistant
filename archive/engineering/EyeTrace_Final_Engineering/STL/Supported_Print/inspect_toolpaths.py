from pathlib import Path
import json,re,math,sys,collections
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy import ndimage
r=Path(__file__).resolve().parent;version=sys.argv[1] if len(sys.argv)>1 else 'v03';path=r/'TOOLPATHS'/version/'plate_1.gcode';out=r/'CHECKS'/('toolpath_'+version);out.mkdir(exist_ok=True)
header_layer_count=None
roles=[];names=[];layers=collections.defaultdict(list);role_volume=collections.Counter();obj_volume=collections.Counter();counts=collections.Counter();x=y=z=e=0.;xyzabs=True;eabs=False;active=False;role='Custom';obj='';width=.45;height=.2;arcs=0;layerchange=0;metadata={};params=re.compile(r'([XYZEF])\s*(-?(?:\d*\.\d+|\d+)(?:[eE][+-]?\d+)?)')
with path.open(encoding='utf-8') as f:
 for lineno,line in enumerate(f,1):
  if line.startswith('; total layer number:'):header_layer_count=int(line.rsplit(':',1)[1])
  elif line.startswith(';LAYER_CHANGE'):active=True;layerchange+=1
  elif line.startswith(';TYPE:'):role=line[6:].strip()
  elif line.startswith(';WIDTH:'):width=float(line[7:])
  elif line.startswith(';HEIGHT:'):height=float(line[8:])
  elif line.startswith('EXCLUDE_OBJECT_START '):obj=re.sub(r'_id_\d+_copy_\d+$','',line.strip().split('NAME=',1)[1])
  elif line.startswith('; estimated printing time') or line.startswith('; filament used') or line.startswith('; total filament used'):metadata[line[2:].split(' = ',1)[0]]=line.strip().split(' = ',1)[1]
  elif line.startswith('M83'):eabs=False
  elif line.startswith('M82'):eabs=True
  elif line.startswith('G90'):xyzabs=True
  elif line.startswith('G91'):xyzabs=False
  elif line.startswith('G92'):
   p=dict((k,float(v)) for k,v in params.findall(line.split(';')[0]));e=p.get('E',e)
   if 'X' in p:x=p['X']
   if 'Y' in p:y=p['Y']
   if 'Z' in p:z=p['Z']
  elif re.match(r'^G[0123](?: |\n)',line):
   p=dict((k,float(v)) for k,v in params.findall(line.split(';')[0]));nx=(p['X'] if xyzabs else x+p['X']) if 'X' in p else x;ny=(p['Y'] if xyzabs else y+p['Y']) if 'Y' in p else y;nz=(p['Z'] if xyzabs else z+p['Z']) if 'Z' in p else z
   de=(p['E']-e if eabs else p['E']) if 'E' in p else 0.;e=(p['E'] if eabs else e+de) if 'E' in p else e
   if active and de>1e-7 and math.hypot(nx-x,ny-y)>1e-6 and role!='Custom':
    if line.startswith(('G2 ','G3 ')):arcs+=1
    if role not in roles:roles.append(role)
    if obj not in names:names.append(obj)
    rid=roles.index(role);oid=names.index(obj);layers[round(nz,3)].append([x,y,nx,ny,rid,oid,width,height]);role_volume[role]+=de*math.pi*(1.75/2)**2;obj_volume[obj]+=de*math.pi*(1.75/2)**2;counts[role]+=1
   x,y,z=nx,ny,nz
assert len(names)==13 and arcs==0,(names,arcs)
info=json.loads((r/'CHECKS/orientation_support_inventory_v02.json').read_text());inv={p['name']:np.array(p['inverse_matrix']).reshape(4,4) for p in info['parts']};support_ids={i for i,v in enumerate(roles) if v.startswith('Support')};brim_ids={i for i,v in enumerate(roles) if v in ['Skirt','Brim']};model_ids=set(range(len(roles)))-support_ids-brim_ids;bridge_ids={i for i,v in enumerate(roles) if 'Bridge' in v or 'bridge' in v};violations=[];support_samples=0;support_by_obj=collections.Counter()
def protected(name,pts):
 a,b,c=pts.T;tests={}
 if name=='Base_EarMount_ThrustSupport':
  for i,x in enumerate([-8.15,19.05]):tests['ear/nut '+str(i)]=((a-x)**2+b*b<1.65**2)&(c>17.75)&(c<22.0)
  tests['thrust face']=(a*a+b*b>27.4**2)&(a*a+b*b<32.1**2)&(c>35.85)&(c<36.65)
 elif name=='PanYoke_EarBracket_KeyedDrive':
  tests['pan horn/mating flange']=(a*a+b*b<16.1**2)&(c>34.85)&(c<37.45)
  tests['radial journal/thrust']=(a*a+b*b>31.8**2)&(a*a+b*b<35.5**2)&(c>32.8)&(c<37.3)
  for i,zz in enumerate([58.95,86.15]):tests['SG90 ear/nut '+str(i)]=(b*b+(c-zz)**2<2.0**2)&(a>-58.4)&(a<-49.3)
  for i,(xx,yy) in enumerate([(18,0),(-18,0),(0,18),(0,-18),(32.5,-23.5),(32.5,23.5)]):tests['pan/foot screw '+str(i)]=((a-xx)**2+(b-yy)**2<1.5**2)&(c>32.8)&(c<41.3)
 elif name=='TiltCradle_KeyedHorn_CameraFrame':
  tests['tilt horn/drive']=(b*b+(c-78)**2<21.1**2)&(a>-41.2)&(a<-36.8)
  tests['idler pivot/flange']=(b*b+(c-78)**2<3.6**2)&(a>31.8)&(a<36.2)
  tests['pan service bore']=(a*a+b*b<2.8**2)&(c>53.8)&(c<60.1)
  for i,xx in enumerate([-24,24]):tests['camera frame slots '+str(i)]=(np.abs(a-xx)<1.45)&(b>-24.7)&(b<-21.1)&(((c>58.3)&(c<69.7))|((c>82.3)&(c<93.7)))
 return tests
# Conservative bead envelope bounds and sampled3D support void/precision checks.
mins=np.array([1e9,1e9]);maxs=-mins;obj_layers=collections.defaultdict(set)
for zz,segs in layers.items():
 arr=np.array(segs);xy=arr[:,:4].reshape(-1,2);bead=max(arr[:,6])/2;mins=np.minimum(mins,xy.min(axis=0)-bead);maxs=np.maximum(maxs,xy.max(axis=0)+bead)
 for row in segs:
  if row[4] in model_ids:obj_layers[names[row[5]]].add(zz)
  if row[4] not in support_ids:continue
  name=names[row[5]];support_by_obj[name]+=1;n=max(2,int(math.hypot(row[2]-row[0],row[3]-row[1])/.25)+1);t=np.linspace(0,1,n);points=np.column_stack((row[0]+(row[2]-row[0])*t,row[1]+(row[3]-row[1])*t,np.full(n,zz-row[7]/2)));matrix=inv[name];points=points@matrix[:3,:3].T+matrix[:3,3];support_samples+=n
  for feature,mask in protected(name,points).items():
   if mask.any() and len(violations)<40:violations.append({'object':name,'feature':feature,'nozzle_Z':zz,'example_source_point':points[np.flatnonzero(mask)[0]].round(4).tolist()})
assert np.all(mins>=0) and np.all(maxs<=260),(mins,maxs)
# All-layer raster screening,0.20mm pixels. Intended support-contact air gaps are allowed.
scale=5;size=1301;history=collections.deque();rows=[];islands=[];maxbridge=0;bridge_fail=[];preview=[]
for seq,(zz,segs) in enumerate(sorted(layers.items())):
 images={k:Image.new('1',(size,size)) for k in ['model','support','brim']};draw={k:ImageDraw.Draw(v) for k,v in images.items()}
 for a,b,c,d,rid,oid,w,h in segs:
  kind='support' if rid in support_ids else 'brim' if rid in brim_ids else 'model';draw[kind].line((round(a*scale),round(b*scale),round(c*scale),round(d*scale)),fill=1,width=max(1,round(w*scale)))
 model=np.array(images['model'],dtype=bool);support=np.array(images['support'],dtype=bool)
 while history and zz-history[0][0]>.51:history.popleft()
 anchor=np.zeros_like(model)
 for z0,m0,s0 in history:
  if zz-z0<=.261:anchor|=m0
  if zz-z0<=.50:anchor|=s0
 anchor=ndimage.binary_dilation(anchor,iterations=1);labels,num=ndimage.label(model,structure=np.ones((3,3)));anchored=set(np.unique(labels[anchor]));new=[]
 if zz>.201:
  sizes=np.bincount(labels.ravel())
  for k in range(1,num+1):
   if k not in anchored and sizes[k]>=7:
    ys,xs=np.where(labels==k);event={'nozzle_Z':zz,'area_mm2':round(float(sizes[k])/25,3),'centroid_xy':[round(float(xs.mean())/5,3),round(float(ys.mean())/5,3)]};new.append(event);islands.append(event)
 longest=0
 for a,b,c,d,rid,oid,w,h in segs:
  if rid not in bridge_ids:continue
  length=math.hypot(c-a,d-b);n=max(2,int(length/.2)+1);ts=np.linspace(0,1,n);xs=np.clip(np.rint((a+(c-a)*ts)*scale).astype(int),0,size-1);ys=np.clip(np.rint((b+(d-b)*ts)*scale).astype(int),0,size-1);unsupported=~anchor[ys,xs];longrun=run=0
  for v in unsupported:run=run+1 if v else 0;longrun=max(longrun,run)
  span=min(length,longrun*length/max(n-1,1));longest=max(longest,span)
  if span>8.5 and len(bridge_fail)<30:bridge_fail.append({'nozzle_Z':zz,'object':names[oid],'unsupported_bridge_mm':round(span,3)})
 maxbridge=max(maxbridge,longest);rows.append({'Z':zz,'model_segments':sum(q[4] in model_ids for q in segs),'support_segments':sum(q[4] in support_ids for q in segs),'unanchored_components':len(new),'longest_sampled_bridge_gap_mm':round(longest,3)});history.append((zz,model,support))
 preview.append({'z':zz,'s':[[round(a,3),round(b,3),round(c,3),round(d,3),rid,oid] for a,b,c,d,rid,oid,w,h in segs]})
 if seq%50==0:print('inspected Z planes',seq,'of',len(layers),flush=True)
fine_reviews=[]
for event in islands:
 zz=event['nozzle_Z'];cx,cy=event['centroid_xy'];x0,y0=cx-4,cy-4;sz=161;sc=20;ims=[Image.new('1',(sz,sz)) for _ in range(3)];dr=[ImageDraw.Draw(im) for im in ims]
 for z0,segments in layers.items():
  if z0>zz+1e-5 or zz-z0>.51:continue
  for a,b,c,d,rid,oid,w,h in segments:
   if max(a,c)<x0 or min(a,c)>x0+8 or max(b,d)<y0 or min(b,d)>y0+8:continue
   kind=0 if abs(z0-zz)<1e-5 and rid in model_ids else 1 if rid in model_ids and zz-z0<=.261 else 2 if rid in support_ids else -1
   if kind>=0:dr[kind].line(((a-x0)*sc,(b-y0)*sc,(c-x0)*sc,(d-y0)*sc),fill=1,width=max(1,round(w*sc)))
 cur=np.array(ims[0],bool);anc=ndimage.binary_dilation(np.array(ims[1],bool)|np.array(ims[2],bool),iterations=4);lab,n=ndimage.label(cur,structure=np.ones((3,3)));anch=set(np.unique(lab[anc]));sizes=np.bincount(lab.ravel());bad=[{'label':i,'area_mm2':round(float(sizes[i])/400,4)} for i in range(1,n+1) if i not in anch and sizes[i]>=16]
 fine_reviews.append({'coarse_event':event,'resolution_mm':.05,'unanchored_local_components':bad})
report={'Gcode':str(path.relative_to(r)),'declared_model_layers':header_layer_count,'actual_layer_change_events':layerchange,'extrusion_Z_planes':len(layers),'extrusion_segments':sum(counts.values()),'role_segment_counts':dict(counts),'roles':roles,'objects':names,'object_model_layer_counts':{n:len(obj_layers[n]) for n in names},'support_segments_by_object':dict(support_by_obj),'filament_metadata':metadata,'role_filament_volume_cm3':{k:v/1000 for k,v in role_volume.items()},'role_filament_mass_g_at1p27':{k:v*.00127 for k,v in role_volume.items()},'support_centerline_samples':support_samples,'protected_region_intrusions':violations,'bead_XY_bounds_mm':[mins.tolist(),maxs.tolist()],'unanchored_model_components':islands,'longest_sampled_unsupported_bridge_mm':round(maxbridge,3),'bridge_spans_above8p5mm':bridge_fail,'raster_resolution_mm':.2,'fine_island_reviews':fine_reviews,'fine_reviews_with_flags':sum(bool(q['unanchored_local_components']) for q in fine_reviews),'limits':'Raster extrusion screening is not continuous3D physics. Support-air-gap reach0.50mm, model interlayer reach0.261mm; one-pixel XY allowance. Protected void checks sample support centerlines every<=0.25mm; not full bead-volume metrology. Physical PETG bridge sag, adhesion and mating fit unverified.'}
(out/'report.json').write_text(json.dumps(report,indent=2));(out/'layer_checks.json').write_text(json.dumps(rows,indent=2));(r/'IMAGES'/('layer_data_'+version+'.js')).write_text('window.TOOLPATH='+json.dumps({'roles':roles,'objects':names,'layers':preview},separators=(',',':'))+';',encoding='utf-8')
# Selected actual-toolpath layer images, no CAD-imagined supports.
for target in [.2,1.0,1.6,3,4.2,14,17.8,19.4,26.8,35,39.8,40,41,45,57,67.2]:
 zz=min(layers,key=lambda z:abs(z-target));im=Image.new('RGB',(1041,1081),'white');dr=ImageDraw.Draw(im);dr.rectangle((0,40,1040,1080),outline='#777');dr.text((12,10),f'{version}: actual extrusion paths, Z={zz:.3f}mm (blue=model orange=support gray=brim)',fill='black')
 for a,b,c,d,rid,oid,w,h in layers[zz]:dr.line((a*4,1080-b*4,c*4,1080-d*4),fill='#df7010' if rid in support_ids else '#aaaaaa' if rid in brim_ids else '#1263a0',width=max(1,round(w*4)))
 im.save(r/'IMAGES'/f'layer_{version}_{target:05.1f}.png')
print(json.dumps({k:report[k] for k in ['declared_model_layers','extrusion_Z_planes','extrusion_segments','object_model_layer_counts','support_segments_by_object','protected_region_intrusions','bead_XY_bounds_mm','longest_sampled_unsupported_bridge_mm','bridge_spans_above8p5mm']},indent=2));print('Unanchored model components:',len(islands),islands[:8])
