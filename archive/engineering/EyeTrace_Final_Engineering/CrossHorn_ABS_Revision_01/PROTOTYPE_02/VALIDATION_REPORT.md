# Cross-horn Prototype 02 validation

**Status: PROVISIONAL FIT TEST. Physical fit is not verified.** Previous prototypes and the complete pan/tilt assembly were not modified.

## Geometry used

- User-confirmed horn baseline: 35 mm long span, 18 mm short span, and 7 mm hub diameter.
- Pocket lateral clearance target: 0.20 mm total (0.10 mm per side).
- Long-arm cavity: tapered, with provisional 6.0 mm root width and 4.0 mm tip width before the 0.20 mm total clearance; rounded tips. Pocket span is 35.2 mm including clearance.
- Short-arm change: +1 mm at each distal end, producing 20 mm nominal extent from the 18 mm baseline; pocket span is 20.2 mm with clearance. Width also increases by 1 mm per side, separately from clearance. With the current provisional 4.0/3.0 mm root/tip widths, cavity widths are 6.2/5.2 mm respectively.
- Center hub seat: 7.2 mm diameter, 2.7 mm depth. Central retaining-screw access is a 4.5 mm through opening.
- No secondary attachment holes are included because the actual horn-hole coordinates have not been measured.

The local reference `REFERENCES\download.jpg` guided the tapered, rounded long-arm outline only. Numeric arm widths, end radii, hub centering, horn plate thickness (1.5 mm), hub height (2.5 mm), screw access (4.5 mm), and axial seat depth remain provisional. The photo is not dimensionally calibrated and was not used to extract exact measurements. The 20 mm short pocket span intentionally exceeds the 18 mm horn baseline by the requested 1 mm per end; this is a fit-test allowance, not a claim that the horn itself is 20 mm long.

## Software checks

- FreeCAD 1.1.4 reopened `CrossHorn_Single_FitTest_02.FCStd`: one valid BRep solid.
- Exported STEP reopens as one valid solid.
- STL reopens in FreeCAD as a solid mesh: 3,080 facets; 43 x 27 x 4.35 mm bounding box.
- The coupon bounding box is within the Creality K2 260 x 260 x 260 mm build envelope.
- 3MF archive integrity passes; it contains one model object and 3,080 triangles matching the STL.
- ABS project starting settings: 0.20 mm layers, four walls, 255 C nozzle, 100 C bed, 4 mm brim, supports disabled. Confirm filament and printer limits before printing.

Creality Print 7.2 is installed and the 3MF project was packaged. A sliced toolpath preview/G-code was not produced or inspected in this run. Open the 3MF in Creality Print and review Preview before printing.

## Remaining physical checks

Print this single coupon and lower the real white horn into the recess without force. Check both long arms and both short arms seat, the horn plate rests flat, the hub seats without bottoming, and the original retaining screw/driver can pass through the center opening. Record rocking, gaps, and removal force. Do not tighten the retaining screw to pull the horn into the coupon.

For an accurate production profile, measure actual long-arm root and tip widths, short-arm root and tip widths, each arm end from the hub center, horn plate thickness, hub height, hub offset, and retaining-screw head/driver clearance. Physical ABS fit and torque transfer remain unverified; do not update the assembly or production print set from this coupon alone.
