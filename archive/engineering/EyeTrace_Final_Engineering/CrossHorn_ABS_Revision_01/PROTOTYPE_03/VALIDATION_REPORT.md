# Prototype 03 ultra-low-filament ABS fit test

**Status: SOFTWARE GEOMETRY PASS; PHYSICAL FIT UNVERIFIED.** This package contains one compact coupon. Earlier prototypes and the full assembly were not modified.

## Geometry and print orientation

- Outer boundary is a rounded cross following the four-arm pocket with a nominal 2.7 mm material margin. The large rectangular plate is removed.
- The long-arm recess remains tapered and rounded; the short-arm recess retains the Prototype 02 correction, including 1 mm extension per end from the Prototype 01 18 mm baseline.
- User-confirmed nominal horn spans remain 35 mm long and 18 mm short; hub is 7.0 mm nominal.
- Pocket lateral allowance is 0.20 mm total. Hub seat is 7.4 mm diameter x 2.7 mm deep. A separate 4.5 mm through opening retains screw/driver access.
- Base thickness is 4.2 mm. This leaves a 1.5 mm floor under the 2.7 mm hub recess and a 2.5 mm floor under the 1.7 mm arm recess. A 3.0 mm base would leave only 0.3 mm under the hub recess, so thickness was increased to preserve a robust floor.
- Print flat with the recess facing up. Support is off. The 4 mm brim is retained because the compact cross arms have limited ABS bed contact.
- Coupon bounding box is 40.60 x 25.60 x 4.20 mm, well inside the Creality K2 260 mm cube.

All unmeasured horn widths, radii, center offset, hub projection and screw/tool geometry remain provisional. The 7.4 mm seat diameter and 2.7 mm depth are test parameters, not verified physical fit.

## CAD and mesh checks

- FreeCAD 1.1.4 reopened the FCStd; it contains one valid solid feature.
- STL mesh is a single watertight solid with 3,872 facets.
- BRep volume is 1,820.32 mm^3.
- 3MF archive CRC/integrity passes; it contains one model object and 3,872 triangles matching the STL.
- Hub and arm floors meet their minimums (1.5 mm and 2.5 mm respectively). No separate/disconnected bosses or supports are present.

## ABS slicer setup

The 3MF starts with 0.20 mm layers, 3 walls, 12% gyroid infill, 255 C nozzle, 100 C bed, supports off and a 4 mm brim. Confirm the spool's specified ABS temperatures and printer limits.

Creality Print 7.2 is installed, but the attempted command-line slice/export invocation produced no G-code. A sliced toolpath preview was therefore not produced or inspected in this run. The 3MF settings and structural mesh checks are not a sliced-preview validation. Open the 3MF in Creality Print, slice it, and inspect first-layer adhesion, pocket floors, walls and infill before printing.

## Prototype 01 comparison (estimates, not slicer output)

Prototype 01 CAD contains three 43 x 27 x 4 mm coupons with a combined BRep volume of 12,892.95 mm^3. Its 3MF settings specify 100% infill and four walls. Prototype 03 BRep volume is 1,820.32 mm^3; its project specifies 12% infill and three walls.

Using assumed ABS density 1.04 g/cm^3, Prototype 01's estimated material mass is about 13.41 g. Prototype 03's estimated mass is approximately 1.04-1.51 g, using a broad 55-80% effective material fraction to account for perimeters and solid top/bottom layers around 12% sparse infill. Estimated filament reduction is approximately 88.7-92.2%.

Estimated print time is about 91 minutes for Prototype 01 and 12-15 minutes for Prototype 03. This estimate uses 2.5 mm^3/s effective extrusion flow plus five minutes for travel/setup overhead; actual K2/Creality Print time may differ substantially. These figures have not been verified by slicing.

## Physical test

Use the actual white horn without forcing it into the pocket. Check the tapered long arms, both extended/widened short arms, hub entry and depth, retaining screw/driver access, flat seating and removal. Record any rocking or gaps. Do not update production pan/tilt components until this coupon passes physically.
