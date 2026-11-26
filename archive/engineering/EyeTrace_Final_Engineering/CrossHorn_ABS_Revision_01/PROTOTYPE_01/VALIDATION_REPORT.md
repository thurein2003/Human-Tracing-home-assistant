# Prototype 01 validation

**Release class: PROVISIONAL TEST GEOMETRY ONLY.** No production part or full-bed project was changed.

## CAD evidence

- Generated with installed FreeCAD 1.1.4 command-line application.
- FreeCAD coupon document saved as a native FCStd file; independent reopen validation is recorded in `prototype_validation.json` after running the validation macro.
- Three independent coupon solids are valid, each has one solid, and FreeCAD mesh `isSolid()` check returned true.
- Binary STL bed contains 9,270 triangles; coupon components have 2,584, 3,088 and 3,598 facets respectively.
- Reference horn envelope is a valid single solid, nominal bounding dimensions 35 x 18 x 4 mm (the 4 mm height includes 1.5 mm plate plus 2.5 mm boss).
- STEP reference envelope exported by FreeCAD's Import exporter.
- Creality Print 3MF project ZIP passes archive CRC and its 3MF object triangle count matches the input STL (9,270).
- Camera pitch values recorded in parameters remain 21 x 14 mm center-to-center.

## Important limitations

- The rounded profile is a provisional gauge because actual arm widths, each arm's end location relative to the hub, end radii, and hub offset have not been measured.
- Current assumptions are stated in `prototype_parameters.json`: arm widths 3.2/3.0 mm, end radii 1.6/1.5 mm, centered hub, 1.5 mm plate, 2.5 mm hub height, 4.5 mm driver access, and 0.20 mm axial allowance.
- Published drawing values for a similar Horn #3 are provisional, not clone-specific. Its stated 34.5 mm overall length differs from user's 35 mm measured value.
- No small horn attachment holes were modeled. Their coordinates are unmeasured; the typical 1.0 mm drawing callout is not used to choose screws.
- This task generated coupon geometry and a slicer project only. It did not modify the assembly, pan/tilt drive components, motion simulation, or production print set.
- Creality Print 7.2 is installed. A valid 3MF project is prepared, but this run did not produce sliced toolpaths or G-code; open the project in Creality Print and inspect Preview before printing.
- ABS physical fit, shrinkage, retention, torque transfer, and camera/assembly fit remain unverified.
