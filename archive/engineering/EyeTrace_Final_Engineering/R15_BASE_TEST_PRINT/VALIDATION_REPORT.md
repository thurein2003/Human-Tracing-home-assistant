# R15 Circular Base ABS Support Test — Validation Report

**Status: NOT APPROVED — localized bridge support was not generated in the inspected slice.**

## Source and scope

- Source layout: `FINAL_ALL_IN_ONE_R15_LAYOUT_FIXED/EyeTrace_K2_ABS_All_In_One_R15_Fixed.3mf`.
- A derived Creality Print session isolated only `Base_EarMount_ThrustSupport`; the source project was not edited.
- Slicer object inspection reported 80.00 × 70.00 × 36.50 mm, 50,567.1 mm³, 5,460 triangles.
- Internal rectangular bridge clear span: 23.3 mm (from the prior CAD section measurement).
- No horn coupon or other part was included in this base-only test.

## Slice result

- Creality Print completed slicing the isolated base.
- Estimated time: **3 h 26 min**.
- Estimated filament: **41.06 g / 16.41 m**.
- These are slicer estimates for the isolated base job.
- The preview at Z=19.20 mm and Z=19.80 mm showed model/bridge toolpaths, but no distinct support or support-interface paths beneath the span.
- The line-type list contained Bridge and Internal Bridge categories (plate-only totals: 0.02 g Bridge and 1.42 g Internal Bridge), but no Support or Support Interface category. These bridge-category amounts are not support material.
- One small enforcer mark was painted at the cavity bridge midpoint, clear of the visible mounting holes. After reslicing, it did not produce a verifiable support structure. Therefore the support top gap (profile value 0.24 mm) cannot be confirmed against an actual interface.

## Bed adhesion and ABS profile caveat

- The selected machine was Creality K2 and the filament type was ABS; nozzle temperature was 255 °C and layer height 0.20 mm.
- The visible build-plate selection was **Cool Plate**. A suitable ABS bed temperature was not exposed in the inspected project settings. This profile state is not sufficient evidence of an appropriate ABS bed setup.
- The first-layer preview showed the base footprint and an outer brim; no neighboring part or brim collision exists in this single-object plate. The screenshot layer is Z=0.20 mm.

## Decision

The 23.3 mm bridge is **not cleared for unsupported ABS printing** by this slice. The local enforcer failed to generate a visible support path, and the selected plate/profile state needs correction and confirmation. The project saved in this folder is deliberately named `R15_Circular_Base_ABS_Support_UNVERIFIED.3mf`; it is a diagnostic artifact, not an approved print file.

## Evidence screenshots

- `01_Base_Complete_Slice.png` — isolated base and slicer estimate.
- `02_Bridge_Z19.20.png` — bridge region at Z=19.20 mm.
- `03_Bridge_Z19.80.png` — bridge region at Z=19.80 mm.
- `04_First_Layer.png` — first-layer footprint and brim at Z=0.20 mm.

## Remaining blocker

A successful revision must produce visible support/interface toolpaths beneath the bridge at the target layers, with the interface gap confirmed and mounting holes unobstructed, using a verified ABS bed setup. Save the requested `R15_Circular_Base_ABS_Support_Verified.3mf` only after that evidence exists.
