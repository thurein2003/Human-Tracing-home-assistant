# Plate 02 assembly repair — engineering status

## Verdict
**MECHANICAL REPAIR CANDIDATE: PASS for the local pan-carrier BREP correction only. COMPLETE ASSEMBLY: HOLD. PLATE 02 PRINT: HOLD.** Plate 01 and its 3MF were not opened or written by the repair build; the circular base shape and pan-axis transform were preserved from R16.

## Root cause
The R17 horn-cleanup carrier was produced with a broad disk-fill operation. It added a Ø41 mm × 3.8 mm region (reported added volume 3501.396 mm³) where the R16 carrier had relief. The assembly transforms were unchanged. This caused the pan carrier to occupy volume belonging to the horn proxy, retainer, and four screws. The R17 intersections reproduced against the R16 source were: horn 291.272 mm³; retainer 1655.771 mm³; screw intersections 4.017–8.413 mm³ each. This evidence points to changed carrier Boolean geometry, not a component-placement shift.

The screws' small overlaps cannot automatically be called faults: the horn is retained by screws, so intended fastening engagement is possible. Actual white-horn hole sizes/positions and whether the modeled M3 hardware is compatible remain unmeasured. The carrier-to-cover overlap is not an intended fastening contact and was removed in the candidate.

## Repair applied
Built a selective local carrier repair from the R16 editable carrier. The R15 master cutter was used for the horn recess; the full Ø41 fill was not retained. The regenerated main carrier is one valid solid, volume 43453.582 mm³, versus source carrier volume 42345.826 mm³ (net +1107.756 mm³). Two disconnected Boolean scraps (130.812 and 129.085 mm³) were excluded. The candidate was checked against the exact R15 pocket cutter, cover, four modeled screws, servo body, unchanged base support, and thrust ring. Calculated positive-volume intersections for those carrier pairs are zero. The carrier's intersection with the exact R15 void is zero.

## Dimensions and fit caveats
R15 master BREP: pocket envelope 39.2 × 20.2 mm; recess depth 1.7 mm; center bore Ø8.0 mm. The matching cut is preserved in the pan carrier. Tilt carrier is retained from R17 and is a valid one-solid BREP with nominal R15 envelope values recorded as 39.2 × 20.2 × 1.7 mm and Ø8 mm. The supplied checks did not produce a numerical BREP distance/deviation comparison for every curved face; therefore exact surface identity for the tilt pocket is **not independently certified** here.

The reference horn model is a provisional uniform 4 mm-thick proxy, not an axial-accurate scan. Its clipped R15 fit-envelope intersects the pan servo reference by 55.439 mm³; center shaft/horn engagement is intended, but its axial seating and spline/retaining screw geometry remain provisional. The tilt horn proxy intersects its servo reference by 73.264 mm³, also consistent with intended output engagement, not proof of correct fit. Tilt horn proxy also overlaps two M3 screws by 10.603 mm³ each; actual hardware placement/compatibility must be checked. Do not interpret these proxy intersections as validated physical engagement.

## Assembly status
The candidate uses the R16 component placements and leaves the pan axis transform unchanged. Local static checks show the repaired pan carrier has no positive-volume overlap with the checked cover, screws, servo housing, base support, or thrust ring. Tilt carrier and local components have zero measured overlap in the recorded checks, except modeled horn-to-output and two horn-to-fastener overlaps described above. A complete constrained-joint or sampled-motion sweep was not executed by this build, so motion clearance and disassembly sequence remain **HOLD / unverified**.

Camera mounting coordinates remain the existing 21 × 14 mm pattern by source parameter/check record; no camera geometry was modified.

## Files
- Editable assembly: `CAD/EyeTrace_R17_Plate02_Repaired_HOLD.FCStd`
- STEP assembly: `CAD/EyeTrace_R17_Plate02_Repaired_HOLD.step`
- Plate 02 project: `PRINT/EyeTrace_R17_Plate_02_ABS_HOLD.3mf`
- Individual Plate 02 meshes: `STL/` (12 files)

## Remaining blockers
1. Confirm physical horn center/underside heights and actual retaining screw engagement; the CAD horn is an axial proxy.
2. Measure actual white horn small-hole diameters and centers; confirm whether M3 screws are appropriate. Do not force M3 into horn holes.
3. Verify tilt drive/retainer assembly physically and through the intended motion range.
4. Slice the exact 3MF in Creality Print 7.2 and inspect supports, brim/first-layer clearance, precision pocket layers, ABS profile, and complete toolpaths. Slicer was unavailable for this repair run; no filament or time estimate is asserted.
5. Assemble against the unchanged base and verify fastener access and free pan rotation. No physical fit test is implied.
