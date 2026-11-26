import os,json,csv,html,hashlib
import FreeCAD as A
from PySide import QtGui
H=os.path.join(os.path.dirname(os.path.abspath(__file__)),'validated');d=A.openDocument(os.path.join(H,'EyeTrace_Camera_21x16_Assembly.FCStd'))
before={o.Name:(o.Shape.Volume,[getattr(o.Shape.BoundBox,k) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax']]) for o in d.Objects if hasattr(o,'KinematicGroup')}
d.getObject('Verification_HOLD').Label='HOLD:21x16 centers USER NOMINAL; PCB/hole/lens/rear dimensions unverified; physical test required'
d.getObject('PCB_Cut003').Label='PCB reference:21x16 hole centers USER NOMINAL; outside size unverified'
d.recompute();d.saveAs(os.path.join(H,'EyeTrace_Camera_21x16_Reviewed.FCStd'))
for n,(v,b) in before.items():
 s=d.getObject(n).Shape;assert abs(s.Volume-v)<1e-6 and max(abs(getattr(s.BoundBox,k)-b[i]) for i,k in enumerate(['XMin','XMax','YMin','YMax','ZMin','ZMax']))<1e-6
old=os.path.join(H,'README.md');os.rename(old,os.path.join(H,'README_initial.md'));t=open(os.path.join(H,'README_initial.md')).read().replace('Open EyeTrace_Camera_21x16_Assembly.FCStd (colored) or EyeTrace_Camera_21x16.FCStd.','Open EyeTrace_Camera_21x16_Reviewed.FCStd (current colored assembly, corrected source/status labels). Earlier geometry snapshots remain preserved.')
with open(old,'x') as f:f.write(t)
rows=list(csv.reader(open(os.path.join(H,'camera_dimensions.csv'))));tbl='<table>'+''.join('<tr>'+''.join(('<th>' if i==0 else '<td>')+html.escape(s)+('</th>' if i==0 else '</td>') for s in r)+'</tr>' for i,r in enumerate(rows))+'</table>'
pngs=['assembly_21x16','plate_21x16'];qa={}
for n in pngs:
 im=QtGui.QImage(os.path.join(H,'renders',n+'.png'));assert not im.isNull();c=0
 for y in range(0,im.height(),12):
  for x in range(0,im.width(),12):
   q=im.pixelColor(x,y)
   if min(q.red(),q.green(),q.blue())<235:c+=1
 assert c>20;qa[n]=c
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eye Trace:21x16mm mounting-hole centers</title><style>body{font:17px/1.5 system-ui;max-width:1100px;margin:30px auto;padding:18px;color:#183549}img{max-width:100%}td,th{border:1px solid #abc;padding:8px;text-align:left}table{border-collapse:collapse}pre{white-space:pre-wrap;font:inherit}.hold{color:#a34115}</style><h1>21 x16mm mounting-hole CENTER spacing</h1><p>User-supplied nominal: horizontal21mm, vertical16mm. These are not PCB outside dimensions.</p><p class="hold">Physical fit unverified. Rear-component clearance remains unresolved.</p><p><a href="EyeTrace_Camera_21x16_Reviewed.FCStd">Current FreeCAD assembly</a> | <a href="CameraPlate_HoleCenters_21x16.stl">Fixed plate STL</a> | <a href="parts/TiltCradle_KeyedHorn_CameraFrame.stl">Revised frame/cradle STL</a> | <a href="coupons/Camera_HoleCenters_21x16_Gauge.stl">21x16 fit gauge</a></p><img src="hole_center_diagram.svg">'+tbl+'<h2>Actual FreeCAD plate view</h2><p>Inner four small holes: PCB mounting pattern21x16. Outer four larger holes: separate frame fasteners.</p><img src="renders/plate_21x16.png"><h2>Actual assembled CAD</h2><img src="renders/assembly_21x16.png"><h2>Validation and remaining checks</h2><pre>'+html.escape(t)+'</pre></html>'
with open(os.path.join(H,'REPORT.html'),'x') as f:f.write(page)
with open(os.path.join(H,'checks','final_QA.json'),'x') as f:json.dump({'render_nonwhite_samples':qa,'reviewed_native_geometry_unchanged':True,'hole_spacing_mm':[21,16],'spacing_source':'USER NOMINAL CENTER-TO-CENTER','physical_fit':'UNVERIFIED'},f,indent=2)
entries=[]
for p,ds,fs in os.walk(H):
 for n in fs:
  path=os.path.join(p,n);entries.append(hashlib.sha256(open(path,'rb').read()).hexdigest()+'  '+os.path.relpath(path,H))
with open(os.path.join(H,'manifest.sha256'),'x') as f:f.write('\n'.join(sorted(entries))+'\n')
print('Current reviewed native, report and manifest saved. Hole centers21x16; physical fit UNVERIFIED.')
