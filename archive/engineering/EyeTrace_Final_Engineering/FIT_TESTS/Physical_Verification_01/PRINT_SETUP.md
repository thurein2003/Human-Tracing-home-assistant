# Print this FIRST
PRINT_FIRST_FitTests_Optimized.stl contains ALL SEVEN pieces. Do not print the full assembly bed. Existing files/release status are unchanged.

No coupon is redundant:01 body/ears;02 positive torque before clamp friction;03 retention/nuts;04 camera centers;05+06 actual full-diameter pan pair;07 reusable tilt sleeve. New06 adds a matching5.2mm bore through2.5mm material. Horn coupons nest inside ring openings with minimum9mm actual surface gap. No mating rings touch in the print layout.

Bed159.3x115.6x4.2mm, seven grounded/watertight shells, fits260mm K2. Bounding rectangle about20.7% smaller than old192.6x120.6mm. Only new female-ring tab changes coupon geometry; original ring material/ID are preserved. Six other BReps remain identical.

## K2 PETG process
Select Creality K2, NOT Plus/Pro;0.4mm nozzle. Import SLICER/EyeTrace_FitTest_K2_020_process.json as user process if configuration import is supported; otherwise duplicate0.20mm Standard @Creality K2 0.4 nozzle and apply settings_to_apply.csv. Preset keys match installed process. GUI import/toolpaths have NOT been certified. Geometry3MF does not contain printer/material settings.

- Scale100%, mm. Flat Z0 face DOWN, pockets/hex seats UP. Keep relative arrangement, optionally center entire group. Do not auto-arrange shells independently.
-0.20mm layer and first layer;0.45mm line width, Arachne/variable-width walls,3 wall loops,5 top/5 bottom,100% rectilinear infill.0.9mm sleeve wall may fit TWO lines; three is maximum count, not three forced lines.
- Supports OFF, raft OFF. CAD has no elevated downward-facing surfaces requiring support; all pockets open UP. No support inside bores or pockets.
- BY LAYER, NEVER sequential/by-object with nested parts. Single material, prime tower OFF. Outer brim3mm, object gap0.15mm; minimum9mm surfaces leave3mm even if TWO brims extend into the gap. Inspect actual preview.
- First layer20mm/s, outer30, inner50, infill60, top30; acceleration2000mm/s2, outer1000, first500 as conservative starting values. Keep filament-maker flow/cooling settings.
- No global scaling, XY-hole/contour or elephant-foot compensation for first diagnostic print. Installed Generic PETG profile defaults250C nozzle/70C textured or hot bed. These are installed defaults, NOT your filament's verified settings: use only within actual filament/bed-surface maker guidance, otherwise select that filament's proper K2 profile.

Inspect preview:7 bodies, open hex pockets, open1.9/2.4/3.2/5.2mm holes, two continuous sleeve-wall tracks.1.5mm cover web and1.1mm flange may round at0.20mm layers: measure real print. Optional0.10mm precision preset keeps0.20mm first layer if preview drops features. Record chosen profile and reproduce it on future critical parts. One profile's result never validates another profile.

Cool PETG before removal. Support thin rings while peeling brim. Remove loose strings/brim only for initial test; record sanding/reaming separately and repeat after finishing. Measure above elephant foot. For0.10mm-clearance decisions, use suitable gauges/calipers with target uncertainty <=0.05mm; a ruler photo is insufficient. If not measurable, recordUNMEASURED rather than PASS.

Sources: installed K2 process/filament filenames and SHA256 in CHECKS/slicer_profile_evidence.json; https://github.com/CrealityOfficial/CrealityPrint and https://help.prusa3d.com/article/petg_2059 . All physical tests remain NOT PERFORMED.
