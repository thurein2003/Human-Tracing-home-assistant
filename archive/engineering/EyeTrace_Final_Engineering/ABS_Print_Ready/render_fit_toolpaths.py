import re,math
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent
p=r/'TOOLPATHS'/'fit'/'plate_1.gcode'
lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
bounds={k:float(v) for k,v in re.findall(r'^; (MINX|MINY|MAXX|MAXY) = ([\d.-]+)', '\n'.join(lines[:25]), re.M)}
objects=[]
for s in lines:
 m=re.match(r'^EXCLUDE_OBJECT_DEFINE NAME=(\S+) CENTER=([\d.-]+),([\d.-]+)',s)
 if m: objects.append((m.group(1),float(m.group(2)),float(m.group(3))))
roles={'Brim':('#888888',2),'Outer wall':('#165f9e',3),'Inner wall':('#4b90c4',2),'Bottom surface':('#273d55',2),'Support':'#e88016','Support interface':'#edab23'}
segments=[];x=y=z=e=0.;xyzabs=True;eabs=False;active=False;role='Custom';obj=''
rx=re.compile(r'([XYZEFIJ])\s*(-?(?:\d*\.\d+|\d+)(?:[eE][+-]?\d+)?)')
for line in lines:
 if line.startswith(';LAYER_CHANGE'):
  if active: break
  active=True; continue
 if not active: 
  if line=='G91': xyzabs=False
  elif line=='G90': xyzabs=True
  elif line=='M83':eabs=False
  elif line=='M82':eabs=True
  elif line.startswith('G92'):
   q=dict((k,float(v)) for k,v in rx.findall(line));e=q.get('E',e);x=q.get('X',x);y=q.get('Y',y)
  continue
 if line.startswith(';TYPE:'):role=line[6:].strip();continue
 if line.startswith('EXCLUDE_OBJECT_START '):obj=line.split('NAME=',1)[1].split()[0];continue
 if line.startswith(('G90','G91','M82','M83')): xyzabs=line.startswith('G90'); eabs=line.startswith('M82'); continue
 if line.startswith('G92'):
  q=dict((k,float(v)) for k,v in rx.findall(line));e=q.get('E',e);x=q.get('X',x);y=q.get('Y',y);continue
 m=re.match(r'^(G[0123])(?:\s|$)',line)
 if not m: continue
 q=dict((k,float(v)) for k,v in rx.findall(line.split(';')[0]))
 nx=q.get('X',x) if xyzabs else x+q.get('X',0); ny=q.get('Y',y) if xyzabs else y+q.get('Y',0)
 de=(q.get('E',e)-e) if eabs else q.get('E',0)
 e=q.get('E',e) if eabs else e+q.get('E',0)
 if de>1e-8 and role!='Custom':
  pts=[(x,y),(nx,ny)]
  if m.group(1) in ('G2','G3') and ('I' in q or 'J' in q):
   cx=x+q.get('I',0);cy=y+q.get('J',0);rad=math.hypot(x-cx,y-cy);a0=math.atan2(y-cy,x-cx);a1=math.atan2(ny-cy,nx-cx)
   sweep=(a1-a0)%(2*math.pi) if m.group(1)=='G3' else -((a0-a1)%(2*math.pi))
   if abs(nx-x)+abs(ny-y)<1e-7:sweep=2*math.pi if m.group(1)=='G3' else -2*math.pi
   pts=[(cx+rad*math.cos(a0+sweep*i/12),cy+rad*math.sin(a0+sweep*i/12)) for i in range(13)]
  segments.append((pts,role,obj))
 x,y,z=nx,ny,q.get('Z',z)
W,H=1200,900; pad=65; sx=(W-2*pad)/(bounds['MAXX']-bounds['MINX']); sy=(H-2*pad)/(bounds['MAXY']-bounds['MINY']); sc=min(sx,sy)
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
d.text((30,20),'Eye Trace ABS fit bed - actual Creality Print first-layer toolpaths',fill='#162b40')
d.rectangle((pad, pad, W-pad,H-pad),outline='#777777',width=2)
def tr(pt):return (pad+(pt[0]-bounds['MINX'])*sc,H-pad-(pt[1]-bounds['MINY'])*sc)
for pts,role,obj in segments:
 color,width=roles.get(role,('#234e72',2))
 d.line([tr(p0) for p0 in pts],fill=color,width=width)
for i,(name,cx,cy) in enumerate(objects,1):
 X,Y=tr((cx,cy));d.ellipse((X-10,Y-10,X+10,Y+10),fill='white',outline='#222',width=2);d.text((X-4,Y-7),str(i),fill='#111')
legend='Blue=part extrusion   Gray=brim   Orange=support/interface'
d.text((30,H-30),legend,fill='#273d55')
out= r/'FIT_TESTS'/'IMAGES'/'ABS_FitBed_FirstLayer_ActualToolpaths.png'
im.save(out)
print({'output':str(out),'first_layer_segments':len(segments),'objects':len(objects),'bounds':bounds})
