from pathlib import Path
import json,math,csv,zipfile,xml.etree.ElementTree as E
import FreeCAD as A,Part,MeshPart,Mesh
from FreeCAD import Vector as V
r=Path(__file__).resolve().parent;base=r.parent.parent;d=A.openDocument(str(base/'CAD/EyeTrace_Final_Assembly.FCStd'));parts=[o for o in d.Objects if hasattr(o,'KinematicGroup') and o.Printable];layout=A.newDocument('Supported_Print_Layout');info=[];meshes=[];shapes=[]
# Only rigid printing orientations, no component geometry modifications.
placements={'Base_EarMount_ThrustSupport':(12,12),'PanYoke_EarBracket_KeyedDrive':(108,12),'Pan_Replaceable_ThrustRing':(12,98.6),'Tilt_Removable_IdlerPillar':(90,98.6),'Pan_KeyedHorn_Cover':(120,98.6),'Tilt_KeyedHorn_CaptiveCover':(182,98.6),'TiltCradle_KeyedHorn_CameraFrame':(12,176.6),'CameraPlate_21x16':(103,176.6),'Tilt_Journal_FlangedSleeve':(178,178),'PCB_Spacer_Lower_Left':(177,202),'PCB_Spacer_Lower_Right':(177,225),'PCB_Spacer_Upper_Left':(201,178),'PCB_Spacer_Upper_Right':(201,202)}
def refine(vertices,triangles):
 vs=[tuple(v) for v in vertices];ts=list(triangles)
 for iteration in range(6):
  marked={tuple(sorted((t[i],t[(i+1)%3]))) for t in ts for i in range(3) if sum((vs[t[i]][j]-vs[t[(i+1)%3]][j])**2 for j in range(3))>25}
  if not marked:break
  mids={}
  for a,b in marked:mids[(a,b)]=len(vs);vs.append(tuple((vs[a][i]+vs[b][i])/2 for i in range(3)))
  out=[]
  for t in ts:
   flags=[tuple(sorted((t[i],t[(i+1)%3]))) in marked for i in range(3)];count=sum(flags)
   def mid(a,b):return mids[tuple(sorted((a,b)))]
   if count==0:out.append(t)
   elif count==3:
    a,b,c=t;ab,bc,ca=mid(a,b),mid(b,c),mid(c,a);out.extend([(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)])
   elif count==1:
    i=flags.index(True);a,b,c=t[i],t[(i+1)%3],t[(i+2)%3];ab=mid(a,b);out.extend([(a,ab,c),(ab,b,c)])
   else:
    j=next(j for j in range(3) if flags[(j-1)%3] and flags[j]);a,b,c=t[(j-1)%3],t[j],t[(j+1)%3];ab,bc=mid(a,b),mid(b,c);out.extend([(b,bc,ab),(a,ab,c),(ab,bc,c)])
  ts=out
 return vs,ts
for o in parts:
 name=o.PrintFileName;s=o.Shape.copy();rot=A.Rotation()
 if name=='PanYoke_EarBracket_KeyedDrive':rot=A.Rotation(V(0,1,0),135)
 elif name=='Tilt_Journal_FlangedSleeve':rot=A.Rotation(V(0,1,0),-90)
 elif name=='Tilt_KeyedHorn_CaptiveCover':rot=A.Rotation(V(0,1,0),90)
 elif name=='Pan_KeyedHorn_Cover':rot=A.Rotation(V(1,0,0),180)
 elif name.startswith(('CameraPlate','PCB_Spacer')):rot=A.Rotation(V(1,0,0),90)
 # Cradle now upright on its broad floor. Idler/base retain upright orientation.
 pl=A.Placement(V(),rot);s.Placement=pl.multiply(s.Placement);bb=s.BoundBox;px,py=placements[name];offset=V(px-bb.XMin,py-bb.YMin,-bb.ZMin);s.translate(offset);transform=A.Placement(offset,rot);inverse=transform.inverse()
 assert s.isValid() and len(s.Solids)==1
 # Exact inverse proves no geometry edit.
 inv=s.copy();inv.Placement=inverse.multiply(inv.Placement);delta=inv.cut(o.Shape).Volume+o.Shape.cut(inv).Volume;assert delta<.001
 q=layout.addObject('PartDesign::Feature',name);q.Shape=s;q.addProperty('App::PropertyString','SourceComponent');q.SourceComponent=o.Name
 m=MeshPart.meshFromShape(Shape=o.Shape,LinearDeflection=.08,AngularDeflection=.15,Relative=False);vs,ts=m.Topology;vs=[tuple(transform.multVec(v)) for v in vs]
 if False:vs,ts=refine(vs,ts) # Keep validated part mesh intact; support painting never refines model geometry
 else:vs=[tuple(v) for v in vs]
 tags=[];counts={'enforcer':0,'blocker':0};area=0
 for tri in ts:
  a,b,c=[V(*vs[i]) for i in tri];p=inverse.multVec((a+b+c)/3);normal=(b-a).cross(c-a);normal=normal/normal.Length;orgnormal=rot.inverted().multVec(normal);enforce=False
  if name=='Base_EarMount_ThrustSupport':
   if orgnormal.z<-.99:
    if abs(p.z-17.8)<.01:enforce=True # exterior bottom rims, not hex ceilings
    elif abs(p.z-19.4)<.01 and all((p.x-x)**2+p.y**2>2.15**2 for x in [-8.15,19.05]):enforce=True
  elif name=='PanYoke_EarBracket_KeyedDrive':
   # Two small nonfunctional wall patches become organic stability braces.
   enforce=normal.z<-.1 and abs(p.x+43)<.01 and abs(abs(p.y)-21)<1.8 and abs(p.z-90)<2.5
  elif name=='TiltCradle_KeyedHorn_CameraFrame':
   enforce=orgnormal.z<-.99 and abs(p.z-94)<.01 and abs(p.x)<21.01 and -24.41<p.y<-21.39
  tags.append('4' if enforce else '8');counts['enforcer' if enforce else 'blocker']+=1
  if enforce:area+=(b-a).cross(c-a).Length/2
 mm=Mesh.Mesh([[V(*vs[i]) for i in t] for t in ts]);print('MESH',name,mm.isSolid(),mm.hasNonManifolds(),mm.hasSelfIntersections(),mm.hasNonUniformOrientedFacets(),flush=True);assert mm.isSolid() and not mm.hasNonManifolds() and not mm.hasSelfIntersections() and not mm.hasNonUniformOrientedFacets(),name
 mm.write(str(r/'STL'/(name+'.stl')));meshes.append((name,vs,ts,tags));shapes.append(s)
 opts={'enable_support':'1' if counts['enforcer'] else '0','support_type':'tree(manual)','support_style':'organic','extruder':'1'}
 if name=='PanYoke_EarBracket_KeyedDrive':opts.update({'brim_width':'8','brim_object_gap':'0','support_on_build_plate_only':'1'})
 if name not in ['Base_EarMount_ThrustSupport','PanYoke_EarBracket_KeyedDrive','TiltCradle_KeyedHorn_CameraFrame','Tilt_Removable_IdlerPillar']:opts['sparse_infill_density']='100%'
 bb=s.BoundBox;info.append({'name':name,'source':o.Name,'rotation_quaternion':list(rot.Q),'translation':list(offset),'inverse_matrix':list(inverse.toMatrix().A),'bbox':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'orientation_symmetric_difference_mm3':delta,'support_paint':counts,'enforced_area_mm2':area,'settings':opts,'facets':len(ts)})
 print(name,'supports',counts['enforcer'],'area',round(area,2),'facets',len(ts),flush=True)
for i,a in enumerate(shapes):
 for j,b in enumerate(shapes[i+1:],i+1):assert a.distToShape(b)[0]>8-1e-5,(info[i]['name'],info[j]['name'])
layout.recompute();layout.saveAs(str(r/'CAD/Supported_Print_Layout_v02.FCStd'));comp=Part.makeCompound(shapes);mm=MeshPart.meshFromShape(Shape=comp,LinearDeflection=.06,AngularDeflection=.12,Relative=False);mm.write(str(r/'STL/EyeTrace_Reoriented_13Parts_v02_UNSUPPORTED.stl'))
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',ns);model=E.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
for k,v in [('Application','Creality_Print V7.3.1.6378'),('BambuStudio:3mfVersion','1'),('BambuStudio:FdmSupportsPaintingVersion','0'),('Title','EyeTrace supported manufacturing candidate'),('Description','13 original parts; selected organic supports; physical hardware fit remains unverified')]:E.SubElement(model,'{'+ns+'}metadata',{'name':k}).text=v
resources=E.SubElement(model,'{'+ns+'}resources');build=E.SubElement(model,'{'+ns+'}build');config=E.Element('config')
for i,(name,vs,ts,tags) in enumerate(meshes,1):
 obj=E.SubElement(resources,'{'+ns+'}object',{'id':str(i),'type':'model','name':name});mesh=E.SubElement(obj,'{'+ns+'}mesh');vv=E.SubElement(mesh,'{'+ns+'}vertices');tt=E.SubElement(mesh,'{'+ns+'}triangles')
 for p in vs:E.SubElement(vv,'{'+ns+'}vertex',dict(zip(['x','y','z'],[format(0 if abs(v)<1e-8 else v,'.10g') for v in p])))
 for t,tag in zip(ts,tags):E.SubElement(tt,'{'+ns+'}triangle',dict(zip(['v1','v2','v3'],map(str,t)),paint_supports=tag))
 parent=E.SubElement(resources,'{'+ns+'}object',{'id':str(100+i),'type':'model','name':name});components=E.SubElement(parent,'{'+ns+'}components');E.SubElement(components,'{'+ns+'}component',{'objectid':str(i)});E.SubElement(build,'{'+ns+'}item',{'objectid':str(100+i),'printable':'1'})
 co=E.SubElement(config,'object',{'id':str(100+i)});E.SubElement(co,'metadata',{'key':'name','value':name})
 for k,v in info[i-1]['settings'].items():E.SubElement(co,'metadata',{'key':k,'value':v})
 part=E.SubElement(co,'part',{'id':str(i),'subtype':'normal_part'});E.SubElement(part,'metadata',{'key':'name','value':name})
plate=E.SubElement(config,'plate')
for k,v in [('plater_id','1'),('plater_name','EyeTrace13 PETG - hardware fit HOLD'),('locked','false'),('bed_type','Textured PEI Plate'),('print_sequence','by layer')]:E.SubElement(plate,'metadata',{'key':k,'value':v})
for i in range(1,14):
 instance=E.SubElement(plate,'model_instance')
 for k,v in [('object_id',str(100+i)),('instance_id','0'),('identify_id',str(i))]:E.SubElement(instance,'metadata',{'key':k,'value':v})
settings=(r/'SLICER/project_settings.json').read_bytes();creality=b'<config><metadata key="Company" value="Creality"/><metadata key="Application" value="Creality_Print"/><metadata key="AppVersion" value="7.3.1.6378"/></config>'
with zipfile.ZipFile(r/'EyeTrace_K2_PETG_Supported_Project_v02.3mf','w',compression=zipfile.ZIP_DEFLATED) as z:
 z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/model_settings.config',E.tostring(config,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/project_settings.config',settings);z.writestr('Metadata/creality.config',creality);z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="text/xml"/></Types>');z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/></Relationships>')
(r/'CHECKS/orientation_support_inventory_v02.json').write_text(json.dumps({'parts':info,'dimensions_mm':[comp.BoundBox.XLength,comp.BoundBox.YLength,comp.BoundBox.ZLength],'source_geometry_unchanged':True,'paint_encoding_source':'Official EnforcerBlockerType1/2 encoded unsplit nibble4/8','physical_fit':'UNVERIFIED'},indent=2))
print('Project prepared; dimensions',comp.BoundBox)
