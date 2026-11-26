# R17 horn cleanup — geometry and assembly validation

## Scope

New revision created from `EyeTrace_Final_2_PLATES_R16_COMPACT_SERVO/CAD/EyeTrace_R16_CompactServo_Assembly_HOLD.FCStd`. Previous candidates and the R15 master were left unchanged.

## Repaired features

- Removed the obsolete square/rectangular and overlapping horn-slot cuts in both motor-drive seating regions.
- Re-established a Ø41.0 mm circular seating land local to each carrier, then cut the exact R15 master horn profile to 1.7 mm depth.
- Retained four separate Ø3.3 mm horn-retainer bores and the Ø8.0 mm center opening.
- Did not change camera plate geometry, R15 master, separate horn retainers, or other printable components.

## CAD results

| Component | BREP valid | Solids | Volume before (mm³) | Volume after (mm³) | Added material (mm³) | R15 void delta (mm³) |
|---|---:|---:|---:|---:|---:|---:|
| PanYoke_EarBracket_KeyedDrive | Yes | 1 | 42,345.826 | 45,847.222 | 3,501.396 | 0 extra / 0 missing |
| TiltCradle_KeyedHorn_CameraFrame | Yes | 1 | 24,528.290 | 24,742.035 | 213.745 | 0 extra / 0 missing |

The material increase restores the local circular seating land after removal of the old cutouts; it is not a global scale operation. The assembly component bounding boxes remain the same as the source carriers.

### Mesh results

| Export | Watertight/solid mesh | Faces | Mesh volume (mm³) | BREP volume (mm³) |
|---|---:|---:|---:|---:|
| Pan print mesh | Yes | 27,036 | 45,845.016 | 45,847.222 |
| Tilt print mesh | Yes | 20,976 | 24,743.135 | 24,742.035 |

Mesh/BREP volume differences are tessellation error, approximately 0.005% pan and 0.004% tilt. The 13 component STL inventory is present; no temporary trial meshes are included in `STL/`.

The source camera mounting plate was carried through unchanged; the nominal pattern remains 21 × 14 mm center-to-center. No camera-hole diameter, PCB envelope, or camera fit claim is made here.

## Two-plate project integrity

Both saved 3MF archives reopened as ZIP/XML packages. Each contains 13 mesh resources and 13 component resources. Plate 01 has one build item; Plate 02 has twelve. Total: 13 components once across two jobs. The updated pan and tilt mesh resources are the only replaced component meshes.

The current printed mesh bounds are inside the K2 XY envelope. This file/package check does not prove that slicer supports, brims, or actual toolpaths are conflict-free.

## Assembly validation status

- Pan and tilt BREP solids: **PASS**
- Exact R15 pocket BREP comparison: **PASS**
- Updated STL mesh closure: **PASS**
- Two 3MF package/component-count integrity: **PASS**
- Camera pattern carried unchanged: **PASS (source geometry retained)**
- Assembly-wide motion, axis alignment, and pairwise collision sweep: **NOT RUN in this cleanup**
- Physical horn fit on these rebuilt carrier parts: **NOT TESTED**
- Creality Print slicing, ABS temperatures/build surface, support/brim/toolpath verification: **NOT RUN**

## Release

**CAD GEOMETRY VERIFIED; PRINT STATUS HOLD.** Open and slice both HOLD 3MFs in Creality Print 7.2, inspect the actual toolpaths and ABS/build-surface profile, and resolve any support/brim conflicts before printing. Do not treat the geometrical R15 comparison as physical validation.

## Final-file reopen and package checks

The saved `CAD/EyeTrace_R17_HornCleanup_Assembly.FCStd` was reopened in FreeCAD 1.1.4. The document contains 54 objects, including 52 non-null shaped objects; the assembly root and printed-parts group report valid shapes. This verifies document readability and shape validity, not assembly-wide pairwise clearance or motion.

A fresh FreeCAD mesh audit was run on the final `STL/` folder: all 13 STL files report closed solid meshes. Both updated 3MF archives were fully read from end to end, and their model XML was parsed: each has 13 mesh resources and 13 component resources; build-item counts are 1 and 12. The package CRC/read pass completed. No slicer toolpaths were generated.
