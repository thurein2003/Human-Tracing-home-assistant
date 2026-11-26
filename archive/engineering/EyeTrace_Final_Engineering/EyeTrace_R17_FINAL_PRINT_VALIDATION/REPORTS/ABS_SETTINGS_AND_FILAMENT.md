# ABS settings and filament comparison

The exact HOLD 3MF metadata records:

- Printer: Creality K2; 0.4 mm nozzle
- Material: Generic ABS
- Nozzle: 255 °C; first layer nozzle setting 250 °C
- Build surface: Textured PEI Plate
- First-layer bed temperature: **70 °C**
- Part cooling: minimum 0%, maximum 15%
- Walls: 3; infill: 20% gyroid
- Brim: 5 mm general; 6 mm override for the base object
- Plate 01 base support metadata: automatic slim tree, build-plate-only
- 3MF authoring metadata: Creality Print 7.3.1.6378

The 70 °C first-layer bed value is not verified for the intended ABS and is below the project's earlier 100–110 °C starting range. The requested Creality Print 7.2 executable was not found in the searched standard install locations and no slicer process was running. Thus the settings above are values stored in the project, not settings verified in the target application.

Neither plate was sliced. No toolpaths were inspected for the 23.3 mm base bridge, supports, first layers, brim contacts, mounting holes, or cleaned pockets. No actual filament mass, support mass, or print time can be reported. 10%, 15%, and 20% infill variants were not sliced and compared; the projects retain 20% gyroid. No filament savings are asserted.

Both projects remain **HOLD** until the pan interference is repaired and the exact 3MFs are sliced and inspected in the requested Creality Print version using a verified ABS/build-surface profile.
