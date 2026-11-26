# F625 Bearing Upgrade 01

This folder contains an optional alternative for the existing opposite-side tilt journal. It is not a new mount design and does not replace prior candidates.

- Authoritative alternative assembly: `CAD/EyeTrace_F625_Alternative_r02.FCStd`
- STEP: `CAD/EyeTrace_F625_Alternative_r02.step`
- Print the ABS bearing fit coupon first: `FIT_TESTS/F625_ABS_Fit_Coupon_r02.stl`
- Revised pillar STL (only after coupon passes): `STL/Tilt_IdlerPillar_F625_ABS_SeatAxisVertical_r02.stl`
- Retainer cap STL: `STL/F625_OuterRace_Retainer_ABS_r02.stl`
- Engineering comparison and release limits: `DOCUMENTATION/F625_BEARING_COMPARISON.md`
- Coupon procedure: `FIT_TESTS/F625_ABS_Fit_Guide.md`
- K2 ABS starting profile: `SLICER/F625_K2_ABS_Start_Settings.json`
- Machine-readable results: `CHECKS/f625_upgrade_validation.json`

The earlier unsuffixed F625 files are the first draft; r02 corrects the cradle clamp stack and is authoritative. Original assembly, native simulation, and ABS print files were preserved. The r02 outer bearing envelope is simplified; race internals and actual bearing tolerances are not inferred from nominal catalog sizes.

**Recommendation:** optional bearing upgrade, fit-test required. It may lower pivot friction/wear, but the existing plain journal may already be adequate for a light, intermittent-use camera. Do not full-print this alternative until the coupon, race-isolation, adapter fit and unpowered motion checks pass.
