import FreeCAD as A, FreeCADGui as G, Part, Mesh, os, traceback
from FreeCAD import Vector as V
from PySide import QtCore,QtWidgets
ROOT=r'EyeTrace_Final_Engineering\Camera_21x14_Correction_01'
try:
 G.showMainWindow()
 d=A.openDocument(os.path.join(ROOT,'CAD','EyeTrace_Final_Assembly_21x14.FCStd'))
 G.updateGui(); view=G.activeDocument().activeView()
 objs=d.Objects
 for o in objs:
  if hasattr(o,'Shape'): o.Visibility=bool(getattr(o,'Printable',False)) or o.Name in ('CameraPCB_Blank','Camera_Lens_PROVISIONAL')
  if o.Name=='CameraPCB_Blank': o.ViewObject.Transparency=65; o.ViewObject.ShapeColor=(0.15,0.55,0.25)
  elif o.Name=='Camera_Lens_PROVISIONAL': o.ViewObject.ShapeColor=(0.12,0.12,0.14)
  elif getattr(o,'PrintFileName','')=='CameraPlate_21x14': o.ViewObject.ShapeColor=(0.92,0.53,0.13)
  elif o.Name.startswith('PCB_Spacer'): o.ViewObject.ShapeColor=(0.15,0.65,0.35)
  elif o.Name.startswith('Camera_M2'): o.ViewObject.ShapeColor=(0.6,0.62,0.66)
 G.updateGui(); view.viewAxonometric(); view.fitAll(); G.updateGui(); view.saveImage(os.path.join(ROOT,'RENDERS','camera_mount_21x14_iso.png'),1400,1000,'White')
 # plate-only end view for visible 21 x 14 pattern
 for o in objs:
  if hasattr(o,'Shape'): o.Visibility=(o.Name=='CameraPlate_Cut007')
 view.viewFront(); view.fitAll(); G.updateGui(); view.saveImage(os.path.join(ROOT,'RENDERS','camera_plate_21x14_front.png'),1200,900,'White')
 # Full actual assembly neutral view.
 for o in objs:
  if hasattr(o,'Shape'): o.Visibility=bool(hasattr(o,'KinematicGroup') and 'KEEP_OUT' not in o.Name)
 view.viewAxonometric(); view.fitAll(); G.updateGui(); view.saveImage(os.path.join(ROOT,'RENDERS','assembly_21x14_iso.png'),1400,1000,'White')
 # Editable coupon document and its actual FreeCAD top view.
 cd=A.newDocument('CameraCoupon21x14')
 coupon=Part.makeBox(29,22,2,V(-14.5,-11,0))
 for x in (-10.5,10.5):
  for y in (-7,7): coupon=coupon.cut(Part.makeCylinder(1.2,2,V(x,y,0)))
 coupon=coupon.removeSplitter(); co=cd.addObject('PartDesign::Feature','CameraPatternCoupon'); co.Label='Camera 21x14 hole-pattern fit-test coupon'; co.Shape=coupon
 co.addProperty('App::PropertyLength','HorizontalPitch','Pattern'); co.HorizontalPitch=21
 co.addProperty('App::PropertyLength','VerticalPitch','Pattern'); co.VerticalPitch=14
 co.addProperty('App::PropertyLength','HoleDiameter','Pattern'); co.HoleDiameter=2.4
 cd.recompute(); cd.saveAs(os.path.join(ROOT,'FIT_TESTS','Camera_Hole_Pattern_21x14_coupon.FCStd'))
 Gui=G; Gui.activeDocument().activeView().viewTop(); Gui.activeDocument().activeView().fitAll(); Gui.updateGui(); Gui.activeDocument().activeView().saveImage(os.path.join(ROOT,'RENDERS','camera_coupon_21x14_top.png'),1100,800,'White')
 A.closeDocument(cd.Name)
 # Actual corrected single-bed STL in the Creality project's coordinates.
 bd=A.newDocument('CorrectedK2Bed'); mo=bd.addObject('Mesh::Feature','ThirteenPrintableComponents'); mo.Label='13 ABS printable parts - corrected 21x14 camera plate'; mo.Mesh=Mesh.Mesh(os.path.join(ROOT,'STL','EyeTrace_Final_K2_SingleBed_21x14.stl'))
 bd.recompute(); G.activeDocument().activeView().viewTop(); G.activeDocument().activeView().fitAll(); G.updateGui(); G.activeDocument().activeView().saveImage(os.path.join(ROOT,'RENDERS','k2_13_part_bed_21x14.png'),1200,1000,'White')
 A.closeDocument(bd.Name)
 print('rendered actual FreeCAD images')
except Exception:
 open(os.path.join(ROOT,'CHECKS','render_error.txt'),'w').write(traceback.format_exc()); raise
finally:
 for n in list(A.listDocuments()): A.closeDocument(n)



