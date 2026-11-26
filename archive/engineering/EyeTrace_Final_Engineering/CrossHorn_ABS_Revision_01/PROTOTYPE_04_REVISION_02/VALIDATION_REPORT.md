# Prototype 04 Revision 02 — backside hub clearance update

**Status: CAD/export checks pass; physical horn fit remains UNVERIFIED.** This is one fit-test coupon only. Prototype 04, Prototype 03 and production assembly files were preserved.

## Geometry

The corrected Horn #3 profile remains unchanged outside the center interface. Long arms remain unequal, tapered and rounded; the short arms retain their widened profile and 1.0 mm extension at each end from the 18 mm baseline.

The center has three distinct coaxial features:

| Face / feature | Diameter | Depth | Status |
|---|---:|---:|---|
| Front hub recess | 7.4 mm | 2.7 mm | Provisional; editable parameter |
| Backside hub clearance recess | 8.0 mm | 0.3 mm | Provisional initial depth; editable parameter, not physically measured |
| Servo retaining-screw access | 4.5 mm | Through | Separate intentional through-opening |

Overall coupon thickness is **3.8 mm**. This leaves **1.1 mm** under the front hub recess, **2.1 mm** below the horn-arm pocket, and a **0.8 mm web** between the overlapping front and rear counterbores. The rear Ø8.0 recess is local to the center; it does not enlarge the cross-arm pocket. The outer horn-pocket wall remains nominally **1.4 mm**. Only the center access hole passes through; the front and rear recesses do not break through into one another or through the perimeter wall.

The 0.3 mm backside depth is a parameterized starting value because the actual rear hub protrusion depth has not been measured. If the horn bottoms out in the backside pocket, measure the protrusion from the horn plate seating plane with calipers; do not deepen this coupon without maintaining the minimum web or increasing thickness.

## Files

- Editable FreeCAD: `CrossHorn_UltraMinimal_FitTest_04R02.FCStd`
- STL: `CrossHorn_UltraMinimal_FitTest_04R02.stl`
- Creality Print project: `CrossHorn_UltraMinimal_FitTest_04R02.3mf`
- Actual FreeCAD screenshots: `CrossHorn_UltraMinimal_FitTest_04R02_Top.png`, `CrossHorn_UltraMinimal_FitTest_04R02_Bottom.png`, and `CrossHorn_UltraMinimal_FitTest_04R02_Isometric.png`
- Parameter file and builder: `parameters.json`, `build_prototype_04_revision_02.FCMacro`
- Validation data: `geometry_validation.json`, `fcstd_reopen_validation.json`, `validation_results.json`

## Checks

- FreeCAD 1.1.4 reopened the saved FCStd: valid BRep, one solid, volume **992.58 mm³**.
- STL: **5,960 facets**; FreeCAD reports a solid/watertight mesh.
- 3MF archive CRC passes; it contains one object with the same **5,960 triangles** as the STL.
- Bounding box **38.00 × 23.00 × 3.80 mm**; with the configured 4 mm brim it remains within the 260 mm K2 bed.
- Model has a continuous floor/web and no disconnected features. The center screw-access opening is intentional.
- Print setup: ABS, 0.20 mm layers, 2 walls, 0% sparse infill, supports off, 4 mm brim, 255 °C nozzle and 100 °C bed. Confirm the spool and printer limits; actual toolpaths have not been sliced/inspected for this revision.

**Physical fit is not verified.** Test with the actual horn without force. Confirm both faces' hub clearances, arm seating, screw access, and that the coupon remains intact around the 0.8 mm central web. The backside hub diameter and depth are still provisional despite the requested 8.0 mm nominal pocket diameter.
