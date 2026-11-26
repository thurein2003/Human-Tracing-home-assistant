# FreeCAD Python console helper. Load the R15 assembly and apply placement-only motion samples.
# Passed angles are study poses, not servo limits or approved travel limits.
import FreeCAD as App
from FreeCAD import Vector, Rotation, Placement

def set_pan_tilt_angles(pan_deg=0.0, tilt_deg=0.0, doc=None):
    if doc is None:
        doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError('Open EyeTrace_R15_Full_Assembly.FCStd first')
    rp = Rotation(Vector(0,0,1), float(pan_deg))
    rt = Rotation(Vector(1,0,0), float(tilt_deg))
    cp = Vector(0,0,0)
    ct = Vector(-41,0,78)
    tp = cp - rp.multVec(cp)
    tt = ct - rt.multVec(ct)
    pan_xf = Placement(tp, rp)
    combined_rot = rp.multiply(rt)
    combined_translation = rp.multVec(tt) + tp
    combined_xf = Placement(combined_translation, combined_rot)
    for obj in doc.Objects:
        kg = str(getattr(obj, 'KinematicGroup', ''))
        if kg not in ('fixed','pan','tilt') or not hasattr(obj,'Placement'):
            continue
        rest = getattr(obj, '_et_nominal_placement', None)
        if rest is None:
            rest = obj.Placement
            obj.addProperty('App::PropertyPlacement','_et_nominal_placement','Motion','Nominal placement used by the angle helper')
            obj._et_nominal_placement = rest
        if kg == 'fixed':
            obj.Placement = rest
        elif kg == 'pan':
            obj.Placement = pan_xf.multiply(rest)
        else:
            obj.Placement = combined_xf.multiply(rest)
    doc.recompute()
    return doc

# Example:
# exec(open(r'C:\path\to\Set_Pan_Tilt_Angles.py').read())
# set_pan_tilt_angles(pan_deg=20, tilt_deg=-10)
