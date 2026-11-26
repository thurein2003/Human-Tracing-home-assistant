# R17 final print validation — PASS/HOLD

## Overall: HOLD — neither plate is approved to print

The exact R17 projects are copied into this folder with HOLD filenames; the source revisions were not overwritten. Both ZIP/3MF archives passed a full read/CRC check. Each includes 13 mesh resources and 13 object definitions, but the build list correctly allocates **one printable object to Plate 01** and **twelve to Plate 02** (13 unique printable components total across the jobs). The 13 standalone STL meshes report closed solid meshes in FreeCAD.

The isolated pan and tilt pocket voids match the R15 master BREP (39.2 × 20.2 mm envelope, 1.7 mm depth, Ø8 mm center). However, the rebuilt pan carrier has newly introduced BREP intersections with its modeled horn, cover, and four screws (details in `FREECAD_ASSEMBLY_VALIDATION.md`). The pan assembly therefore fails mechanical clearance. No full assembly motion/interference sweep was completed.

Creality Print 7.2 was unavailable for slicing in this environment. The project metadata is authored in Creality Print 7.3.1.6378 and records a 70 °C first-layer bed value. Actual support paths, bridge support, first layers, brims, ABS thermal settings, toolpath conflicts, filament mass, and print time were not verified.

| Plate | Build items | Slicing / support | Filament and time | Verdict |
|---|---:|---|---|---|
| Plate 01 | 1 (base) | Not sliced; 23.3 mm bridge support unverified | Not available | **HOLD** |
| Plate 02 | 12 | Not sliced; pan carrier clearance fails | Not available | **HOLD** |

The BREP-derived pocket drawings in `../RENDERS/` are not slicer screenshots. No physical fit claim is made for the rebuilt carriers.
