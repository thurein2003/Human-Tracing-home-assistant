# Hardware fit and assembly — prototype only

The mechanism has been modeled and exported, but a functional hardware fit has NOT been validated. Do not treat the STLs as a production release. Camera resolution and 3.6 mm focal length do not specify mounting geometry.

| Required measurement | Modeled assumption / acceptance question |
|---|---|
| SG90 main case, both units | 23 x 12 x 23 mm case envelope; flange ears, case bulges and strain relief omitted |
| Pan case to shaft and flange offsets | Shaft axis at X=0, case X=-6..17; actual shoulder and horn seating height must be checked |
| Tilt shaft height and axial offset | X axis through Y=0, Z=78; case X=-70..-47, Z=61..84 |
| Star horn shape, hub and thickness | Five-arm visual envelope radius 12 mm, 2 mm flat clamped web, 8 mm central clearance; actual raised hubs may prevent clamping |
| Horn-to-spline screw | Original servo-specific center screws required, not M3; availability and length unconfirmed |
| M3 hardware | Assumed 10 mm under head, 5.6 mm head diameter, 3 mm head height, 5.5 mm nut across flats, 2.4 mm nut thickness; no washers |
| Camera body and boards | Assumed 38 x 38 x 30 mm block; measure IR boards, lens, LEDs, connector, cable exit, mounting holes and keep-out areas |
| Lens projection | Assumed 14 mm diameter, 10 mm protrusion; optical field of view and IR reflections not checked |
| Camera retention | Two straps through shelf slots; straps are additional hardware not confirmed available; neither screw-hole fit nor exposed PCB pressure is verified |
| Payload | Camera mass, center of mass, wire drag, servo torque and thermal duty cycle unknown |
| Printer / PETG | Confirm selected K2 profile, actual material shrinkage, screw-hole and nut-pocket fit |

The nominal screw-head relief has only 0.2 mm axial running clearance in the pan and tilt reliefs. These are CAD dimensions, not verified PETG clearances; inspect actual print tolerances before motion. The nominal modeled idler axial air gap is 0.5 mm. M3 is a plain pivot envelope, not a modeled precision bearing. A 10 mm screw leaves 1.6 mm nominal thread projection beyond a 2.4 mm nut for the 6 mm idler grip. Nut retention against loosening, bearing friction, backlash and wear need physical testing. Do not tighten the idler enough to bind the cheeks. A verified locking method may require different hardware; none is claimed to be supplied.

Horn sandwiches use four M3 x 10 fasteners each, with a nominal 5.5 mm grip and 2.1 mm nut-side projection. They clamp the original horns rather than attempting to print servo splines. Torque transmission depends on friction and the real horn profile. Clamp force, PETG creep, horn slip and allowable tightening torque have not been validated. M3 does not replace the original center spline screw. Retainer joints have 5 mm nominal grip and 2.6 mm projection. Screw access is represented by bores, but actual tool access with servo cables and real hardware must be checked.

## Bill of materials

- One each of the seven printed parts listed in README.md.
- Two SG90 position servos with their two original star horns.
- Thirteen M3 x 10 screws and thirteen nominal 2.4 mm M3 nuts: four pan horn, four tilt horn, one idler, two pan retainer, two tilt retainer. Screw and nut quantity on hand is unknown.
- Two original servo-specific horn center screws, availability unconfirmed.
- Camera-retention straps and suitable padding, not confirmed on hand.
- Base fastening to the intended support: four 3.4 mm clearance holes, support thickness and fastening hardware unspecified.
- Suitable servo power source and controller, not modeled.

## Assembly sequence after measuring the hardware

1. Check every critical dimension above. Revise the generator before printing if any mounting geometry differs. Do not assume the SG90 label determines case or horn fit.
2. Slice a fit sample or check the relevant printed holes with your actual M3 screws and nuts. Inspect PETG parts for support scars, cracks and warping.
3. Seat the pan servo in the base with a clear cable exit. Fit the pan retainer with two M3 joints; prevent case distortion.
4. Electrically center each servo using its own safe operating range, then disconnect power. Attach the original horns using the correct original center screws.
5. Sandwich the pan star horn between its clamp and the yoke platform. Fit four M3 screws from below, with nuts in the top recesses. Check access to the original spline screw and verify no horn slip.
6. Seat the tilt servo in the outboard cage. Fit the tilt retainer using two M3 joints. Keep the cable clear of the moving cradle.
7. Sandwich the tilt star horn between its clamp and cradle flange using four M3 joints. Use the wall bores for head access. Fit the M3 idler through the coaxial right holes with the nominal 0.5 mm axial gap; check free motion and reliable nut retention.
8. Secure the camera using measured, suitable straps and padding that avoid PCB components, IR LEDs and ventilation needs. Route a relaxed cable loop around both axes and provide strain relief.
9. With servo power off, slowly check the entire intended range using the real cables, fasteners and camera. Confirm balance, no rubbing and no hidden head or wire interference. Stop on contact; never force servo gears.
10. Test powered motion gradually under the real payload. Measure backlash, idle/stall behavior, current, horn slip and temperature. There are no mechanical end stops. The sampled +/-60 degree pan and +/-30 degree tilt range is a CAD test envelope, not a guaranteed safe servo command range.

## PETG slicing notes

Use candidate_02/single_bed.stl at 100% scale in millimeters. It contains seven independent shells; split into objects in the slicer if needed. All parts have a minimum Z of zero within floating-point tolerance. There is at least 8 mm between their axis-aligned packing boxes. Bed fit is for the part geometry only; brims, supports, purge towers and exclusion zones must also fit.

The base and yoke are upright; the cradle is on its side; both thin horn clamps lie flat. The yoke's outboard servo cage and parts of the cradle need supports. Review every layer and keep support scars out of horn seating faces, nut seats and pivot bores. The pan retainer includes a 1.3 mm residual web at its screw-head relief; inspect its layers and verify its stiffness under clamp load. The 1.5 mm horn clamp plates are thin and need a sound first layer and full solid thickness. Their strength and long-term PETG creep are unverified. Choose PETG temperatures and cooling from the filament manufacturer's profile; no generic temperature is asserted as tested. Print settings, strength, dimensional accuracy and actual print quality have not been validated.

Manufacturer references used for context only, not hardware fit: [TowerPro SG90](https://towerpro.com.tw/product/sg90-analog/) and [Creality K2 series](https://www.creality.com/products/k2-series-3d-printer). The SG90 manufacturer lists overall dimensions; the simplified local case model does not establish flange, shaft or horn dimensions.
