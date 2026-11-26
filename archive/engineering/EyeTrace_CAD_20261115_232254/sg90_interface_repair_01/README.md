# Eye Trace SG90 interface repair01 — physical verification pending

Start with REPORT.html and EyeTrace_Repair_Assembly.FCStd. This continues the existing project using sg90_interface_audit_01 as the authoritative baseline. All previous candidates/audits are preserved. This is NOT production-ready.

The repair supplies two consistent drawing/community-based SG90 references with ears/holes/bosses/wire exits; small-fastener ear mounts; positive star-profile carriers with accessible original screws; a removable right pillar; a replaceable journal sleeve with non-pinching locking stack; pan thrust/radial support; and an adjustable four-hole PCB interface. Clone fit, original horn outlines, actual camera geometry and physical performance remain unverified.

## Files

- EyeTrace_Repair_Assembly.FCStd: colored editable component assembly with live camera pitch properties. EyeTrace_Repair.FCStd is the geometry snapshot. This is a positioned BRep assembly with scripted rigid kinematics, not a native Assembly-workbench joint solver.
- EyeTrace_Assembly.step: full50-component/77-solid assembly, including separate hardware solids.
- parts/:14 printed STL/STEP components. PrintLayout.FCStd and prototype_print_layout.stl contain all14 packed parts, no motors/horns/hardware and no diagnostic coupons.
- coupons/:five small diagnostic pieces, native layout, STL and STEP files. Print these first.
- DIMENSIONAL_AUDIT.md and dimensional_audit.csv: sources, confidence and separate CAD/physical status.
- COLLISION_AND_MOTION.md and checks/: independent native-file checks, motion/contact classification, installation/service tests, mesh/export evidence.
- ASSEMBLY_AND_FASTENERS.md and hardware_BOM.csv: sequence and required additional hardware. The supplied M3 stock alone is insufficient.
- REMAINING_PHYSICAL_VERIFICATION.md and measurements/essential_hardware_results.csv: essential missing measurements/results.
- COUPON_AND_PRINT_GUIDE.md: diagnostic use, print orientation and limitations.

## Edits and history

In the native document, edit RepairParameters.CameraPitchX/CameraPitchZ over the mechanical20–32mm range. PCB holes, rails, spacers and fasteners are expression-linked. The camera is a provisional38mm PCB, not identified hardware. Check rear components as well as pitch: the placeholder keep-out conflicts at20x20; only default28x28 has full motion/export validation. Regenerate exports after edits; existing STLs do not update automatically.

Builders preserve existing targets. Regenerate using build_repair_v09.py with a NEW work-folder name and optional parameter JSON; run independent_validate_v02.py on it; use export_repair_v03.py work_folder new_export_folder. Other servo/horn stack dimensions need coordinated code/parameter changes when actual measurements differ. A changed horn thickness is not fixed by relabeling the model.

Earlier repair attempts remain in work_*/ and archived_packages/. Use only the CURRENT top-level deliverables for review. Previous candidates and authoritative audit remain byte-identical to their recorded checksums. Sources/attribution are in ATTRIBUTION.md and measurements/servo_reference_source_ledger.csv. No exact spline teeth were invented.
