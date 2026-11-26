# Eye Trace R19 — Thin Pan Mount Plate

## Release status

**CAD candidate: geometry/export checks pass.**  
**Mechanical release: HOLD. Print release: HOLD.** The plate has been materially reduced and the FreeCAD/STEP/STL/3MF outputs validate, but the modified ABS structure has not been physically load-tested and the exact R19 3MF has not been sliced in Creality Print. No physical SG90 fit or structural strength is claimed.

## Target and function

The edited component is `PanYoke_EarBracket_KeyedDrive` from the latest R18 circular-mount correction. It is the moving pan carrier; its broad horizontal mounting plate sits below the vertical frame. The source plate supports the R15 pan horn interface and carries the vertical frame, the four PanDrive M3 screw locations, the pan shaft opening, and a circular support land mating with the replaceable thrust ring.

CAD geometry identifies:

- Central shaft opening: Ø8.0 mm.
- Four existing mount bores: Ø7.0 mm, centered at (−18,0), (+18,0), (0,−18), (0,+18) mm in the pan-carrier XY plane. Their cylindrical wall spans Z=39–41 mm (2 mm depth) and aligns with the four `PanDrive_M3x10` references. These are retained exactly; actual screw/head seating remains a physical-fit check.
- Circular land: outer radius 35.3 mm and inner boundary radius 32.3 mm. The full-height land and its thrust-ring contact surface were retained.
- R15 pocket: the exact prior pocket geometry is retained. Symmetric-difference volume below Z=37.7 mm is 0.0 mm³. The nominal 1.7 mm pocket and Ø8 opening were not changed.

## Change made

The broad horizontal plate was relieved from its upper side. The main web is now 2.5 mm thick; the R15 pocket retains 2.5 mm of material above its pocket floor. I used an exact R15 pocket-profile prism to preserve the required material directly over the horn cavity.

Localized reinforcement remains at the central shaft boss, four screw pads, the circular outer land, and three narrow tie rails to the vertical-frame foot. The main vertical frame and all attachment positions remain in place. The new pad radii and tie-rail layout are design choices for this candidate, not measured hardware dimensions or a strength certification.

| Measure | R18 C1 source | R19 candidate |
|---|---:|---:|
| Ordinary plate section at XY=(10,10) | 5.8 mm (Z=35.2…41.0) | 2.5 mm (Z=35.2…37.7) |
| Material above R15 pocket floor at XY=(10,0) | 4.1 mm (Z=36.9…41.0) | 2.5 mm (Z=36.9…39.4) |
| Four screw-pad wall section | 4.0 mm | 4.0 mm retained |
| Outer circular land section | 5.8 mm | 5.8 mm retained |
| Yoke volume | 38,324.180 mm³ | 30,038.906 mm³ |

The yoke loses 8,285.274 mm³ (21.62% of its R18 C1 volume). At an assumed ABS density of 1.04 g/cm³, that is about 8.62 g of solid-material equivalent; actual slicer savings are unknown. Overall yoke envelope and vertical height remain unchanged.

## Validation evidence

- FreeCAD 1.1.4 model recomputes; edited yoke is one valid solid.
- Measured plate web and R15 floor backing are each 2.5 mm by direct section probes.
- Existing four Ø7 mm bore centers, central Ø8 mm opening, outer circular land, and complete lower horn region remain unchanged.
- The R19 yoke is a strict subtractive subset of the R18 C1 yoke. No material was added and no component placement or axis moved.
- Pan-yoke static BREP distances: base 0.30 mm; replaceable thrust ring 0.00 mm intentional contact; pan servo 1.50 mm; pan retainer 0.20 mm; four pan screws 0.20 mm each; tilt cradle 2.00 mm; tilt cover 0.40 mm. The tilt servo and idler pillar are at modeled contact with zero positive-volume penetration.
- The simplified pan horn proxy still overlaps by 5.655 mm³, unchanged from R18 C1. It is a proxy/interface uncertainty, not proof of physical horn collision or fit.
- Sampled yoke checks: 37 pan poses from −90° to +90° in 5° steps, 19 tilt poses from −45° to +45° in 5° steps, and 49 combined poses. No positive-volume yoke intersections were found against the checked stationary or moving reference components. These are exploratory CAD ranges, not established servo travel limits; cable motion and structural load response are not covered.
- Carrier STL reimport: one closed component, 51,972 facets, no nonmanifold edges or self-intersections.
- Carrier STEP reimport: one valid solid. Full assembly STEP reimport: 13 valid solids.
- Plate 02 3MF archive integrity: PASS; exactly 12 unique build objects. All 11 non-yoke STL files match their R18 C1 hashes. The replacement yoke retains its prior build placement. Bed XY bounds are within 260 × 260 mm, no component XY bounding-box intersections were found, and the minimum envelope gap is 16 mm.
- The 21 × 14 mm camera mounting plate is unchanged. Plate 01 and its files were not modified.

## Deliverables

- `CAD/EyeTrace_R19_ThinMountPlate.FCStd` — editable R19 FreeCAD assembly
- `CAD/EyeTrace_R19_Assembly.step` — 13 printable assembly solids
- `CAD/PanYoke_R19_ThinMountPlate.step` — redesigned yoke
- `STL/PanYoke_R19_ThinMountPlate.stl` — redesigned yoke in existing print-bed orientation
- `STL/` — 11 other Plate 02 component STLs, copied unchanged
- `PRINT/Plate02_R19_ThinMountPlate.3mf` — updated 12-part plate project
- `SCREENSHOTS/R18_R19_ThinPlate_Comparison.png` — same isometric projection for both exported meshes
- `SCREENSHOTS/R19_PanYoke_ThinPlate_Isometric.png`
- `DOCUMENTATION/r19_geometry.json`, `r19_validation.json`, `r19_static_clearances.json`, `r19_motion_clearance.json`, `r19_package_validation.json`, `r19_assembly_step_check.json`

The comparison graphic is a shaded render of the exported CAD meshes, not a FreeCAD UI capture. Its camera approximates the saved R18 axonometric view. The newest user screenshot was not present among the project’s local reference files, so an exact camera-angle match to that image cannot be claimed.

## Remaining checks

1. Slice the exact R19 3MF in Creality Print with the intended K2 ABS profile. Inspect first layers, walls around the raised pads/rails, overhangs and horn-pocket layers; actual filament and time estimates are not available yet.
2. Physically check mounting screw seating, horn/shaft engagement, and the locally reinforced plate after printing.
3. Test the ABS yoke under the real camera/servo load and repeated motion. The 2.5 mm web has not been strength- or fatigue-certified.
4. Confirm actual SG90 operating angles and cable clearance; the reported movement samples are CAD screening only.

**Recommendation: review this R19 geometry and comparison render, then keep the part on HOLD until slicer inspection and physical checks pass.**
