# Prototype 04 Revision 04 — Second Center-Recess Depth Update

## Status
Provisional ABS physical fit gauge only. The real white SG90 horn has not been tested in this revision. This is not a production drive component and does not approve the pan/tilt assembly for printing.

## Changed geometry
- Rear/backside center recess: **Ø5.5 mm nominal × 0.8 mm deep**. This is +0.5 mm from the preceding prototype's 0.3 mm depth.
- Front hub recess: **Ø7.4 mm nominal × 2.7 mm deep**, provisional.
- Separate central servo-retaining-screw/tool access: **Ø4.5 mm through**; not enlarged by the rear recess change.
- To retain a 0.8 mm web, a **Ø10.2 mm local center pad** is raised by **0.5 mm**. Overall thickness is 3.8 mm away from the pad and 4.3 mm locally.
- Remaining center web between the two recess floors: **0.8 mm**. Front hub floor elevation is 1.6 mm above the datum; arm-pocket floor is 2.1 mm above datum.
- Tapered long-arm recess, widened short-arm recesses, 1.0 mm end extension per end, and overall outline are retained from the prior version. The confirmed horn span baseline remains 35 mm long, 18 mm short, and Ø7 mm nominal hub.

## Engineering interpretation
The second-recess depth is independently adjustable in the editable FreeCAD model (`BackHubRecessDepth`). The front recess depth is separate (`FrontHubRecessDepth`). The rear Ø5.5 mm recess is a stepped bearing/relief feature and remains distinct from the Ø4.5 mm retaining-screw access opening.

Without local reinforcement, increasing the rear recess from 0.3 to 0.8 mm would reduce the center web from 0.8 to 0.3 mm. The model instead adds 0.5 mm only at the central pad; it does not thicken the entire coupon. Geometry reports one valid solid. The local pad and remaining thin ring/web still require sliced-layer and physical handling checks.

## Validation results
- FreeCAD saved-document reopen: **PASS** — one valid solid; volume 1013.656 mm³; bounding box 38.000 × 23.000 × 4.300 mm.
- FreeCAD mesh export: **PASS** — STL is one closed solid mesh, 6,260 facets.
- 3MF package: **PASS** — single coupon/object; packaged mesh matches the STL triangle count; archive integrity checked.
- Build volume: **PASS** — coupon footprint is within the 260 × 260 mm K2 build area. A 4 mm brim envelope is approximately 46 × 31 mm.
- Nominal modeled center dimensions: **PASS** — front Ø7.4 mm, rear Ø5.5 mm, rear depth 0.8 mm, screw access Ø4.5 mm, center web 0.8 mm.
- CAD section: **PASS** — section model is valid; shown in the included section image.
- Slicer toolpath: **NOT CHECKED** — this revision's 3MF carries starting settings (ABS, 0.20 mm layers, 2 walls, 0% infill, supports off, 4 mm brim, 255 °C nozzle/100 °C bed). No actual Creality Print slice/toolpath inspection was performed for this revision.
- Physical horn seating: **UNVERIFIED** — requires printing and trying the user's actual horn. No physical-fit claim is made.

## Remaining risks / physical check
The 0.8 mm web and the annular material near the central access opening are thin features. Confirm the coupon slices as continuous perimeters/solid layers, then seat the horn by hand without force. Check that the hub bottoms neither on the recess floor nor the screw/tool path, and that the horn plate rests in its arm pocket. Do not use the coupon as a structural part.

## Files
- `CrossHorn_UltraMinimal_FitTest_04R04.FCStd` — editable FreeCAD model
- `CrossHorn_UltraMinimal_FitTest_04R04.stl` — single coupon mesh
- `CrossHorn_UltraMinimal_FitTest_04R04.3mf` — single-object ABS fit-test job
- `CrossHorn_UltraMinimal_FitTest_04R04_Section_Dimensions.png` — actual FreeCAD section with dimensions
- `geometry_validation.json`, `fcstd_reopen_validation.json`, `section_validation.json`, `parameters.json` — machine-readable evidence and assumptions

Print only the 3MF after checking the ABS profile against the filament manufacturer's specification and confirming the preview preserves the thin central web. Test with the actual servo horn; this coupon does not replace the servo or retaining screw.
