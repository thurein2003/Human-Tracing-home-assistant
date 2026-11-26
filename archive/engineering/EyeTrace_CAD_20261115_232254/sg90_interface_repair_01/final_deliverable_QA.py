import os,json,hashlib,re
import FreeCAD as A
from PySide import QtGui
H=os.path.dirname(os.path.abspath(__file__));sel=json.load(open(os.path.join(H,'renders','report_selection.json')));qa={}
for n,caption in sel:
 p=os.path.join(H,'renders',n+'.png');im=QtGui.QImage(p);assert not im.isNull(),p
 nonwhite=0
 for y in range(0,im.height(),12):
  for x in range(0,im.width(),12):
   c=im.pixelColor(x,y)
   if min(c.red(),c.green(),c.blue())<235:nonwhite+=1
 assert nonwhite>20,n
 qa[n]={'nonwhite_samples':nonwhite,'resolution':[im.width(),im.height()]}
# Keep superseded raw render passes, but remove their ambiguous names from the current gallery directory.
raw=os.path.join(H,'renders','superseded_raw_pass');os.makedirs(raw,exist_ok=False)
for n in ['pan_ear_installation','pan_positive_star_pocket','complete_print_layout','fit_coupons']:
 a=os.path.join(H,'renders',n+'.png');b=os.path.join(raw,n+'.png');assert os.path.commonpath([os.path.abspath(a),H])==H and os.path.commonpath([os.path.abspath(b),H])==H;os.rename(a,b)
base=A.openDocument(os.path.join(H,'EyeTrace_Repair.FCStd'));colored=A.openDocument(os.path.join(H,'EyeTrace_Repair_Assembly.FCStd'))
a={o.Name:o for o in base.Objects if hasattr(o,'KinematicGroup')};b={o.Name:o for o in colored.Objects if hasattr(o,'KinematicGroup')};assert set(a)==set(b) and len(a)==50
geom={}
for n,o in a.items():
 x,y=o.Shape,b[n].Shape;v=abs(x.Volume-y.Volume);bounds=max(abs(getattr(x.BoundBox,k)-getattr(y.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax']);assert v<1e-6 and bounds<1e-6
 geom[n]={'volume_difference_mm3':v,'bounds_difference_mm':bounds,'colored_shape_valid':y.isValid()};assert y.isValid()
assert len([o for o in a.values() if o.Printable])==14
report=open(os.path.join(H,'REPORT.html'),encoding='utf-8').read();missing=[]
for p in re.findall(r'(?:href|src)="([^"]+)"',report):
 if '://' not in p and not os.path.exists(os.path.join(H,p)):missing.append(p)
assert not missing,missing
q={'selected_renders':qa,'colored_native_matches_geometry_snapshot':geom,'report_missing_links':missing,'current_print_STL_count':len([x for x in os.listdir(os.path.join(H,'parts')) if x.endswith('.stl')]),'source_preservation_evidence':'previous_artifact_preservation.json','physical_fit':'UNVERIFIED','production_ready':False}
with open(os.path.join(H,'checks','deliverable_QA.json'),'x') as f:json.dump(q,f,indent=2)
entries=[]
for parent,ds,fs in os.walk(H):
 for n in fs:
  if n=='manifest.sha256':continue
  p=os.path.join(parent,n);entries.append(hashlib.sha256(open(p,'rb').read()).hexdigest()+'  '+os.path.relpath(p,H))
with open(os.path.join(H,'manifest.sha256'),'x') as f:f.write('\n'.join(sorted(entries))+'\n')
print('Selected CAD views:',len(qa),'Native components:',len(a),'Printed STLs:',q['current_print_STL_count'],'Report missing links:',missing,'Manifest files:',len(entries))
