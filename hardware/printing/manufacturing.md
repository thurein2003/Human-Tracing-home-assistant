# ABS printing and mechanical assembly

See the [printing file audit](../../PRINTING_FILES.md) for the complete candidate's parts, fit tests, and release holds. The corrected 21 × 14 mm candidate retains the earlier five-arm horn pockets. Check the archived white-horn pocket revisions separately when using four-arm horns.

The Creality K2 has a 260 × 260 × 260 mm nominal build volume. Use the project’s K2 profile and the documented 0.4 mm nozzle. Check filament condition and dry it per the manufacturer’s directions. Start with a clean compatible build plate, a draft-controlled enclosure, and appropriate ventilation for ABS. Confirm safe nozzle and bed limits for the actual spool and printer, let the enclosure equilibrate, retain the engineered brims, and let the bed cool before removal. [Creality K2 guide](https://wiki.creality.com/en/k2-flagship-series/k2).

| Recovered job | Settings | Historical slice |
| --- | --- | --- |
| Corrected 13-part ABS bed | 0.20 mm, 4 walls, 35% gyroid, selective tree slim support | 124.33 g, 11 h 45 m 59 s |
| Corrected camera coupon | 0.20 mm, 3 walls, 100% fill, 4 mm brim, supports off | 1.35 g, 8 m 34 s |
| Earlier seven-coupon ABS bed | Older tooling reference, 21 layers | 12.06 g, 1 h 21 m 12 s |

The corrected jobs’ G-code records 255 °C nozzle and 100 °C first-layer bed. Treat these as historical slice profiles. The older seven-coupon estimate does not specify the runtime of the optimized plate or corrected single coupon. Full-bed supports are set only for the base, pan yoke and tilt cradle. Keep the preserved orientations, holes and precision bores inspectable. Preview all per-object supports, brims and paths in Creality Print before exporting new machine G-code.

## Fit-test sequence

1. Open the corrected [camera coupon](../3d-models/fit-tests/Camera_21x14_ABS_FitTest.3mf). Verify both hole spacings with calipers and compare the physical PCB using nonconductive alignment pins, with power off. Inspect rear components, fastener protrusion, lens clearance and ribbon bend.
2. Print the [seven-piece diagnostic bed](../3d-models/fit-tests/PRINT_FIRST_FitTests_Optimized.stl) with supports off. Check fastener access, cross-horn seating, pan interface and tilt support. Use the [clearance calibration print](../3d-models/fit-tests/ABS_Circular_Clearance_Calibration_Bed.stl) if a fit is tight, loose, oval or rough.
3. Compare printed hole dimensions and sample diameters at room temperature. Record actual clearances and any seam bulge, elephant’s foot, warping or dimensional shift. Select the fitting coupon locally. Global scaling shifts the mounting pitch.
4. Review the [full 3MF](../3d-models/3MF/EyeTrace_K2_ABS_Full_21x14.3mf) after fit approval. Confirm the actual firmware, slicing profile and 260 mm build volume. The historical clearance record leaves the rear camera envelope open, so a physical fit check is required before an assembly print.

## Assembly

1. Clean brims and support contact surfaces without widening precision holes blindly. Dry-fit the base and pan thrust interface.
2. With power isolated, fit the SG90 bodies in their mounting pockets and align the pan yoke and tilt cradle. Confirm the measured horn matches both drive pockets before fitting the horns on the splined shafts with their original retaining screws. Verify that each horn seats without binding.
3. Attach the opposite tilt journal, and run both axes through the unpowered working arc. Use the assembly drawing for structural M3 joints and verify cable clearance.
4. Fit verified camera hardware and spacers. Route the ribbon with slack and strain relief in all tested poses, clear of screws and horn sweep. Never pull a PCB into alignment using the screws.
5. Confirm common ground and independent servo power before calibration. Begin with a small commanded movement on one axis and measure its direction and range. Keep the emergency power cutoff accessible.
