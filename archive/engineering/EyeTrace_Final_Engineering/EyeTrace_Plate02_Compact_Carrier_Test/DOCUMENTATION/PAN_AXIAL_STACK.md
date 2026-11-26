# Pan axial stack — compact carrier candidate

Coordinate: the unchanged R17 assembly global Z axis. The pan rotation axis remains at X=0, Y=0, parallel to +Z.

| Feature | Source geometry | Compact candidate |
|---|---:|---:|
| Carrier overall Z range | 33.0–103.0 mm | 35.2–103.0 mm |
| Carrier height | 70.0 mm | 67.8 mm |
| Lower circular layer removed | Z 33.0–35.2 = 2.2 mm | Removed |
| Remaining circular support land | Z 35.2–41.0 = 5.8 mm | Retained |
| R15 pocket entrance | Z 33.0 mm | Z 35.2 mm |
| R15 pocket floor | Z 35.2 mm at inspected long-arm point (2.2 mm locally) | Z 36.9 mm |
| R15 recess | 2.2 mm at the inspected section | 1.7 mm |
| Servo reference output cylinder | Z 33.0–36.3 mm, modeled Ø5 mm cylindrical region | Same position; 0.6 mm below the pocket floor at its top |
| Horn proxy axial range | Z 32.5–36.5 mm, uniform 4.0 mm proxy | Unchanged; proxy overlap with candidate is 5.655 mm³ |
| Retainer axial range | Z 30.8–35.0 mm; modeled thickness 4.2 mm | Unchanged; 0.2 mm gap to new carrier underside |
| Screw centers | (±18,0), (0,±18) mm | Unchanged |

The source over-depth is present in the editable carrier and its STL, so it is not an STL export artifact. The local 0.5 mm excess came from an overlapping relief beneath the nominal R15 floor. The redesign removes the entire lower 2.2 mm circular layer and places the new R15 pocket in the upper support’s Z=35.2 mm face. The R15 cutter is applied directly from the master BREP; the center bore is Ø8 mm through.

A temporary full restoration in the old position was not used: it intersected the old placed cover and horn proxy. In the candidate stack, the retainer remains separate and the measured CAD gap is 0.2 mm. The horn proxy still has a small positive-volume overlap, so axial fit is **PROVISIONAL** pending the actual horn/servo stack measurement.

**Measured model clearances:** retainer 0.20 mm; pan servo 1.50 mm; unchanged base thrust support 0.30 mm; thrust-ring contact 0.00 mm (intended); each modeled screw 0.20 mm. These are static CAD checks, not a motion sweep or physical fit test.

The output-axis model is centered at X=0, Y=0. Its CAD cylinder is not an exact spline representation, and its 3.3 mm projection is a reference-model value, not a measurement of the user’s servo.
