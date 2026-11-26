# Prototype 04 Revision 03 — backside hole diameter correction

**Status: CAD/export checks pass; physical printed fit remains UNVERIFIED.** One lightweight coupon is present. Earlier revisions and production files are unchanged.

## Center interface parameters

| Feature | CAD diameter | Depth | Parameter status |
|---|---:|---:|---|
| Backside center recess | **5.5 mm nominal** | 0.3 mm | Diameter confirmed by user; depth remains provisional |
| Front hub recess | 7.4 mm | 2.7 mm | Provisional, independent parameter |
| Retaining-screw access | 4.5 mm | Through | Separate feature and parameter |

The previous 8.0 mm backside diameter is not used. The revised backside counterbore remains stepped from the front hub recess. The overlapping recesses leave a calculated 0.8 mm axial web; the front hub floor is 1.1 mm and the arm-pocket floor is 2.1 mm. The annular radial ligament between the Ø5.5 backside recess and Ø4.5 access bore is 0.5 mm. This is intentionally retained at the requested nominal dimensions; inspect its sliced toolpath and handle the printed test gently.

Long- and short-arm profiles, short-arm extension, and surrounding 1.4 mm walls are carried forward unchanged from Revision 02. The coupon envelope is 38.0 × 23.0 × 3.8 mm; with the configured 4 mm brim it fits the Creality K2 260 mm build area.

## Software validation

- FreeCAD 1.1.4 reopened the saved FCStd and confirmed one valid solid.
- The saved FreeCAD feature properties independently report front Ø7.4 mm, back Ø5.5 mm, front depth2.7 mm, backside depth0.3 mm, and separate Ø4.5 mm through access.
- STL contains 5,960 facets; FreeCAD reports a solid/watertight mesh.
- 3MF CRC passes and its single model mesh contains the same 5,960 triangles as the STL.
- The 3MF carries ABS starting settings: 0.20 mm layers, 2 walls, 0% sparse infill, supports off and 4 mm brim. Sliced toolpaths were not inspected in this revision.

## Files

- `CrossHorn_UltraMinimal_FitTest_04R03.FCStd`
- `CrossHorn_UltraMinimal_FitTest_04R03.stl`
- `CrossHorn_UltraMinimal_FitTest_04R03.3mf`
- `CrossHorn_UltraMinimal_FitTest_04R03_Top.png`
- `CrossHorn_UltraMinimal_FitTest_04R03_Bottom.png`
- `CrossHorn_UltraMinimal_FitTest_04R03_Isometric.png`
- `parameters.json`, `geometry_validation.json`, `fcstd_reopen_validation.json`, `validation_results.json`

**Physical fit remains unverified.** The 5.5 mm value is the nominal CAD diameter; ABS hole size and actual horn fit require slicing/printing and testing with the real horn.
