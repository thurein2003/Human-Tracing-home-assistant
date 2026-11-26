# Eye Trace — R15 All-in-One K2 Layout Validation

## Release status

**CAD/layout package: validated for geometry and file integrity.**  
**Physical fit: provisional.** The R15 horn coupon has not passed a physical fit test, so the pan/tilt horn interfaces and complete assembly are not physically verified.  
**Sliced job: not verified.** The supplied Creality Print project contains printer/material/process and per-object support settings, but no sliced toolpaths or slicer-derived time/filament estimate were produced in this run. Open the 3MF in Creality Print, slice it, and inspect Preview before printing.

## Main file

`EyeTrace_K2_ABS_All_In_One_R15.3mf`

This is the Creality K2 260 × 260 mm project with 13 placed printable objects. The combined arranged STL is `STL/EyeTrace_K2_ABS_All_In_One_R15.stl`. Editable assembly/layout and STEP files are in `CAD/`. Individual parts are in `STL/individual/`.

## Source and integration

- Assembly source: `Camera_21x14_Correction_01/CAD/EyeTrace_Final_Assembly_21x14.FCStd`.
- Horn-profile source: `CrossHorn_ABS_Revision_01/PROTOTYPE_04_REVISION_15/CrossHorn_UltraMinimal_FitTest_04R15.FCStd`.
- The R15 rounded unequal four-arm cavity profile and Ø8 mm through-hole were applied to the actual pan yoke and tilt cradle drive regions. The coupon itself was not placed as a substitute for the functional parts.
- Existing placements/joint alignment and 13-part inventory were retained.
- Camera hole centers remain 21 × 14 mm center-to-center at (±10.5, ±7) mm about the pattern center. PCB outside dimensions remain a separate model envelope.

## Printable part inventory

1. `Base_EarMount_ThrustSupport`
2. `Pan_Replaceable_ThrustRing`
3. `PanYoke_EarBracket_KeyedDrive` — R15 cavity integrated
4. `Tilt_Removable_IdlerPillar`
5. `Pan_KeyedHorn_Cover`
6. `TiltCradle_KeyedHorn_CameraFrame` — R15 cavity integrated
7. `Tilt_KeyedHorn_CaptiveCover`
8. `Tilt_Journal_FlangedSleeve`
9. `PCB_Spacer_Lower_Left`
10. `PCB_Spacer_Lower_Right`
11. `PCB_Spacer_Upper_Left`
12. `PCB_Spacer_Upper_Right`
13. `CameraPlate_21x14`

## Geometry and export checks

- FreeCAD 1.1.4 assembly opens; 13 printable solids found, each valid and single-solid.
- Pan yoke and tilt cradle modified solids are valid.
- Print-layout FreeCAD document opens with 13 valid placed solids.
- Assembly STEP reopens and is valid (76 solids, including nonprintable reference hardware); arranged STEP reopens as 13 solids.
- All 13 individual STL meshes are one connected watertight component each.
- Combined STL: 44,994 facets, 13 connected components, all watertight.
- 3MF archive integrity passes; 13 mesh objects and 13 build items; the two updated drive objects are present.
- Layout bounds: X 10–207 mm, Y 10–202.6 mm, Z approximately 0–77 mm. It is within the 260 × 260 mm K2 bed footprint. The layout audit reports no pairwise overlaps and a 10 mm arranged margin.
- Estimated summed CAD solid volume is 135,913.875 mm³. At an assumed solid ABS density of 1.04 g/cm³, this corresponds to about **141.35 g net model material**. This excludes slicer-generated supports, brim, purge, and process losses; it is not a slicer estimate.

See `CHECKS/geometry_packaging_validation.json`, `CHECKS/3mf_structure_validation.json`, `CHECKS/3mf_package_validation.json`, and `CHECKS/readback_validation.json` for machine-readable results.

## 3MF print setup

Embedded project settings identify Creality K2 with a 0.4 mm nozzle, ABS, 0.20 mm layers, 4 walls, 35% gyroid infill, 255 °C nozzle, 100 °C bed, and 5 mm brim. Tree/slim support is configured per object: enabled on the base, pan yoke, and tilt cradle; disabled on the remaining parts. These are project settings, not proof that support placement or resulting toolpaths are suitable. Inspect support contacts and critical faces in Creality Print Preview.

The installed Creality Print command-line slice attempt did not emit G-code, so this package has no verified toolpath, layer preview, slicer mass, or print-time result. Do not treat the 141.35 g CAD estimate as the final job estimate.

## Horn interface and physical risk

The R15 profile is integrated into the functional pan yoke and tilt cradle. CAD checks confirm valid solids and approximately 0.10 mm nominal side clearance against the modeled R15 profile. The cross-pocket walls are intended to provide positive torque transfer. The Ø8 mm central passage leaves clearance around the nominal 7 mm horn hub; no secondary horn fastener holes were added because their positions and sizes are not established. The reference horn and retaining-screw geometry are provisional, and the original SG90 spline/retaining screw fit has not been physically demonstrated. The 0.10 mm CAD clearance also does not account for ABS shrinkage or printer-specific dimensional error.

**Print the R15 horn fit-test coupon and test the actual white horn before relying on the integrated pan/tilt interfaces.** Confirm it seats without force, lies against the intended seating face, permits retaining-screw access, and has acceptably low rotational backlash. If it fails, revise the interface and regenerate the functional drive parts before printing the full set.

## Files to inspect

- Build-plate overview: `RENDERS/Creality_K2_R15_Build_Plate.png`
- Machine-readable read-back: `CHECKS/readback_validation.json`
- Geometry/layout audit: `CHECKS/geometry_packaging_validation.json`
- 3MF structure: `CHECKS/3mf_structure_validation.json`
- 3MF package/layout: `CHECKS/3mf_package_validation.json`
