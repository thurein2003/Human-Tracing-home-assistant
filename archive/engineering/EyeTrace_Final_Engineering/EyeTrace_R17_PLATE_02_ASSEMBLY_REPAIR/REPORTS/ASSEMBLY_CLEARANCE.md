# Pan and tilt local clearance report

Source assembly: R16 CompactServo; R17 carrier compared; R15 master cutter used for pan repair. Values are positive-volume common volumes in mm³, not surface distance.

## Pan repaired candidate
| Pair | Common volume |
|---|---:|
| Carrier / exact R15 pocket void | 0.000 |
| Carrier / horn retainer cover | 0.000 |
| Carrier / each of four PanDrive M3 screws | 0.000 |
| Carrier / pan servo reference body | 0.000 |
| Carrier / unchanged base ear/thrust support | 0.000 |
| Carrier / replaceable thrust ring | 0.000 |

The exact R15 fit envelope intersects the pan servo by 55.439 mm³ at the output interface. This is a modeled shaft/horn engagement region and is classified **designed engagement, provisional**, because the horn axial geometry is simplified. No dimensional minimum gap was computed; zero common volume only means no positive-volume penetration for the checked pair.

## Tilt local checks
The recorded local BREP check reports zero carrier intersection with the tilt cover, four tilt-drive screws, servo housing, idler pillar, journal sleeve, idler bolt, and washer. The tilt horn proxy has 73.264 mm³ overlap with its servo reference and 10.603 mm³ with each of two screws. These are possible intended output/retention engagements but remain provisional pending hardware geometry and actual assembly confirmation.

## Motion and assembly
No verified native joint graph or full pan/tilt angular sweep is part of the generated checks. Do not infer a clear motion range from these static pair checks. Complete mechanism travel, cable clearance, assembly order, and disassembly access remain **UNVERIFIED**.

## Camera
Existing nominal hole-center spacing is 21 × 14 mm. No camera envelope or cable dimensions were changed or newly established in this repair.
