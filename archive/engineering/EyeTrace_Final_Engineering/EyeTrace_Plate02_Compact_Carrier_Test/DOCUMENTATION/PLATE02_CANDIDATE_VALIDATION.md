# Plate 02 compact-carrier candidate validation

**Status: HOLD — not sliced or released for printing.** This candidate changes only the PanYoke mesh from the existing Plate 02 HOLD project. It does not alter Plate 01 or its files.

## Files

- Candidate 3MF: `PRINT\EyeTrace_Plate02_CompactCarrier_ABS_CANDIDATE.3mf`
- Editable assembly source: `CAD\EyeTrace_CompactCarrier_Candidate.FCStd`
- Replacement pan yoke STL: `STL\PanYoke_Compact_R15_Carrier_Candidate.stl`
- Existing CAD views: `SCREENSHOTS\Carrier_Before_After_{Isometric,Top,Bottom,Side,Axial_Section}.png`
- Input project: `EyeTrace_R17_PLATE_02_ASSEMBLY_REPAIR\PRINT\EyeTrace_R17_Plate_02_ABS_HOLD.3mf`

## CAD and interface findings

The compact part is `PanYoke_EarBracket_KeyedDrive`. Its lower axial thickness was reduced by 2.2 mm: original Z extent 33.0–103.0 mm (70.0 mm), candidate 35.2–103.0 mm (67.8 mm). The retained annular land is 5.8 mm tall (Z 35.2–41.0 mm); the local material above the R15 pocket floor is 4.1 mm at the sampled central web. These are CAD measurements, not strength certification.

The pocket is cut from the R15 master. Candidate CAD/STL checks report 39.2 mm long-axis envelope, 20.2 mm short-axis envelope, 1.7 mm pocket depth, and Ø8.0 mm center opening. An independent STL section ray found the long-arm floor at 1.70000005 mm below the entrance. The master cutter's common volume with the candidate pocket void and the center-bore check were both 0.0 mm³. The R15 master file was not changed.

The prior simplified pan-horn proxy still overlaps the carrier by **5.655 mm³**. This is not silently treated as a verified physical collision or waived as harmless: the project proxy lacks confirmed dimensions for the actual white horn's axial thickness and front/rear hub profile. Therefore physical horn seating and retention remain provisional. The source candidate's CAD clearance checks also show 0.2 mm to the removable cover, 1.5 mm to the simplified pan-servo reference, 0.3 mm to the base support, and 0.2 mm to each of four pan-drive screw models. The thrust-ring contact is intentional. These clearances depend on the supplied CAD references and do not establish clone hardware fit.

## Motion screen

No intended travel limits or mechanical stops are defined in the source CAD. Exploratory independent sweeps used pan −90° to +90° in 5° steps (37 positions) and tilt −45° to +45° in 5° steps (19 positions). A corrected simultaneous transform screen checked a **91-state** grid (13 pan values × 7 tilt values): pan −90° to +90° in 15° steps and tilt −45° to +45° in 15° steps. It found no positive-volume intersections among the checked transformed tilt-moving parts versus the stationary base/pan-servo references. Independent-axis screens likewise found no other positive-volume intersections in the modeled groups.

The modeled horn/servo overlap is 73.264 mm³ per axis and represents the simplified proxy's modeled output engagement; it is not proof of fit. The tilt horn proxy also has reported 10.603 mm³ overlaps with each of two screw solids; the actual horn-hole positions and diameters are undocumented, so those pairs remain unresolved. The grid is a CAD collision screen only, not a continuous sweep, cable check, verified safe range, or servo command recommendation. Several camera cable/lens and camera fastener references are provisional or placed as placeholders, so cable and camera hardware clearance through motion is not validated.

## Mesh and print-bed checks

- Candidate 3MF ZIP CRC test: passed; XML parsed; 12 build items resolve to 12 named mesh components. The 11 non-pan printable meshes are unchanged from the input package; the unbuilt base reference mesh is also unchanged.
- Candidate 3MF build coordinates: all 12 component bounds are within 260×260 mm; all minimum Z values are 0.0 mm.
- Component XY bounding boxes do not intersect; minimum XY bounding-box gap is 16.0 mm. This geometric gap does not include unverified slicer support/brim footprints.
- The candidate pan footprint is unchanged (X 13.0–115.2, Y 13.0–83.6 mm) and its maximum Z is 67.8 mm.
- All 12 final component STLs, including the replacement pan-yoke STL, passed a triangle-edge incidence check (each undirected mesh edge appears exactly twice). This supports watertight/manifold mesh status; it is not a slicer or dimensional-accuracy test.
- Pan yoke is one valid solid in FreeCAD; the replacement STL was independently reopened and its R15 section checked.
- The CAD-derived local center web is 4.1 mm. Minimum wall thickness throughout all 12 components has not been measured by a dedicated thickness analysis.

## Existing slicer profile metadata

The candidate 3MF retains the source project metadata: Creality K2, 0.4 mm nozzle, ABS profile label `EyeTrace ABS 255C K2 100C`, 255 °C nozzle, 100 °C bed/plate entries, 3 wall loops, 20% gyroid, tree-auto support, and 5 mm global brim (the pan object has an 8 mm object-level brim entry in its model settings). Metadata retention is not verification that the installed slicer selected the correct build surface or that the actual ABS manufacturer permits these settings.

## Slicer and estimate status

Creality Print 7.2 is installed, but the current interactive GUI session could not be brought to the foreground/opened on this exact modified 3MF. No slice completed for this candidate and no actual candidate toolpaths were inspected. Consequently, there are no verified candidate filament, support-mass, or print-time estimates; prior project estimates do not apply. The first layer, support reach, brim/support clearance, pocket layers, small features, ABS process compatibility, and actual sliced object inventory remain HOLD.

## Physical measurements still needed

To resolve the 5.655 mm³ proxy overlap and confirm the interface, measure the actual horn's overall thickness at the arms, raised front hub diameter and protrusion, rear hub diameter and protrusion, and retaining-screw head/shaft envelope. If using optional horn-to-retainer screws, measure the actual horn-hole diameters and their center coordinates; none are modeled as confirmed. For real motion-range claims, also supply servo mechanical limits/stops and the installed ribbon-cable route/bend envelope.

## Release decision

**CAD candidate: PASS for the stated 2.2 mm height reduction and R15 pocket geometry.**

**Assembly/physical fit: PROVISIONAL / HOLD.** The proxy overlap and unmeasured servo/horn geometry remain unresolved.

**Printability/slicing: HOLD.** No candidate slice or toolpath inspection was completed. Do not print from this 3MF until the exact project is opened, sliced, and inspected in Creality Print with the actual ABS/build-surface profile.

