# Eye Trace R31 horn-pocket depth

The saved Creality reference showed the tilt cradle and overhangs without an edge selection. All 14 edges that measured 1.700 mm in R30 are axial edges of the same SG90 horn pocket. R31 changes their shared depth to 2.000 mm. The comparison highlights the same physical edge on both solids at assembly Y=3.457118 mm and Z=75.987952 mm.

The R30 solid had no editable pocket history. R31 exposes the depth as HornPocketDepthTool.PocketDepth, which drives a native FreeCAD extrusion and cut. A reopen test changed the parameter to 1.850 mm, recomputed the feature, and restored it to 2.000 mm. The STEP matches the final solid on reimport. Both measured endpoints exist in the reopened STL and are 2.000 mm apart.

| Check | Result |
| --- | --- |
| Material removed | 61.27 mm³ within the 0.300 mm pocket-floor extension |
| R31 solid | One valid connected solid |
| Flat mounting web | 2.50 mm outside the keyed recess |
| Recess roof thickness | 0.50 mm, down from 0.80 mm |
| Fasteners and shaft | Four inherited Ø3.30 mm bores, Ø8 mm access and unchanged shaft axis |
| Camera frame and Plate 01 | Preserved |
| Static and sampled tilt clearance | Zero positive-volume interference at neutral and every 5° from −45° to +45° |

The horn mating plane, keyed contact against the provisional horn, and washer-bearing areas are preserved in CAD. The two holes intersecting the long-axis pocket continue to rely on the R30 removable spacer washers spanning the recess. The thinner 0.50 mm roof and physical horn fit have not been load-tested.

## K2 ABS slice

Creality Print generated a slice with a 0.4 mm nozzle, 0.12 mm nominal model layers, textured PEI, and automatic slim tree supports from the build plate. The project uses two top-interface layers and a 0.24 mm nominal support gap. No support geometry was added to the CAD solid or STL.

The exported toolpath was checked for support-interface extrusion under each of these regions.

| Region | Part underside | Highest support-interface path |
| --- | --- | --- |
| Upper plate | Z=74.00 mm | Z=73.76 mm |
| Upper frame opening | Z=62.00 mm | Z=61.76 mm |
| Lower frame crossbar | Z=13.00 mm | Z=12.80 mm |
| Recess roof | Z=2.00 mm | Z=1.76 mm |

The Creality estimate is 4 h 48 min and 29.56 g. The editable 3MF contains the exact revised STL mesh. The sliced 3MF passed its archive and embedded G-code checksums. No print was started.

[Measurements and toolpath verification](R31_Geometry_Validation.json)
