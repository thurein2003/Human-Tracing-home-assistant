# Eye Trace R23 — Unified Bottom Mount Block

## Result

The bottom pan-yoke mounting structure has been rebuilt as one connected printable solid. The circular pan thrust land is integrated into the yoke mesh; the separate thrust-ring print item is absent from the R23 assembly and Plate 02 layout. The already printed base (Plate 01) remains unchanged.

The edit is limited to the pan-yoke/thrust interface. The vertical frame, top/tilt structure, camera mount, servo positions, screw locations, and R15 horn geometry were carried forward from R22 without edits.

## Measured CAD changes

| Feature | R22 source | R23 result |
|---|---:|---:|
| Rectangular pan-yoke web at X=40, Y=20 mm | 2.5 mm | 2.5 mm |
| Circular annular land at X=34, Y=0 mm | 2.5 mm | 2.5 mm |
| Local flange screw bosses | 4.0 mm | 4.0 mm retained |
| M3 clearance holes | Ø3.30 mm, centers (32.5, ±23.5) mm | unchanged; both bores remain clear |
| R22 yoke volume | 27,162.3103 mm³ | — |
| Integrated R23 yoke + thrust land volume | — | 27,995.8377 mm³ |
| Separate thrust-ring volume incorporated | 833.5274 mm³ | incorporated into yoke |
| Pan-axis/base interface | — | 0 mm³ intersection; 0 mm CAD surface distance (intended contact) |

The R23 union adds the existing thrust-ring geometry to the yoke as a single BREP solid. It does not scale, simplify, or re-mesh the source parts before fusion. The two parts had zero positive-volume intersection and their union validates as one solid.

## Validation evidence

- R23 FCStd reopened in FreeCAD 1.1.4; unified yoke is one valid solid.
- Assembly printed-part group has 12 components, one fewer than the R22 assembly because the thrust ring is incorporated into the yoke.
- Plate 02 contains 11 printable objects; the unchanged base remains on Plate 01 and is not included in this Plate 02 job.
- Yoke STL: watertight, 80,190 facets, connected to one mesh component.
- R23 3MF reopened in Creality Print and sliced. The saved exact 3MF has a valid ZIP CRC, 11 model objects/build items/instances, and the fused yoke mesh.
- No positive-volume collision with the unchanged base; their interface is intended contact.
- Flange screw bores at (32.5, ±23.5) mm remain unobstructed in the BREP.
- Yoke footprint remains within the existing Plate 02 placement; no other part placements or meshes were changed.

## Slicer result and release status

Creality Print 7.3.2.6412 completed slicing the R23 project with the Creality K2, textured PEI plate, 0.4 mm standard nozzle, and the project’s ABS filament profile.

- Slicer estimate: **83.30 g**, **9 h 31 min**.
- Slicer warning: **Pan_KeyedHorn_Cover has a floating cantilever; reorient or enable support generation.**
- The floating-cantilever warning remains unresolved in this focused correction. The R23 project is therefore **HOLD**, not approved for printing.
- CAD checks do not establish printed ABS strength, physical servo/horn fit, or long-term thrust-surface wear.

## Files

- Editable assembly: `CAD/EyeTrace_R23_UnifiedBottomBlock.FCStd`
- Unified component STEP: `CAD/PanYoke_R23_UnifiedBottomBlock.step`
- Full assembly STEP: `CAD/EyeTrace_R23_FullAssembly.step` (reimported; 74 solids; volume delta 1.2e-9 mm³)
- Unified component STL: `STL/PanYoke_R23_UnifiedBottomBlock.stl`
- Openable unsliced Creality project: `PRINT/Plate02_R23_UnifiedBottomBlock_IMPORTFIX_UNSLICED.3mf`
- Sliced Creality project: `PRINT/Plate02_R23_UnifiedBottomBlock_SLICED_HOLD.3mf`
- Same-angle assembled CAD view: `SCREENSHOTS/R23_UnifiedBottomBlock_Isometric.png`
- Genuine Creality sliced preview: `SCREENSHOTS/R23_CrealityPrint_Sliced_HOLD.png`

## Physical verification

The part remains a CAD/slicer candidate. Check the pan rotation and thrust contact after printing, and verify the retained SG90 horn/retainer hardware physically. No physical-fit or structural test is claimed.
