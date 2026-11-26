# Camera 21 × 14 mm correction audit

## Authoritative pattern

The user supplied the four-hole center-to-center pitch as **21 mm horizontal × 14 mm vertical**. The pattern center remains X=0, Z=76 mm in the assembly coordinate system. The four centers are (−10.5, 69), (−10.5, 83), (+10.5, 69), and (+10.5, 83) mm in X/Z. These are hole centers, not PCB outside dimensions.

The previous 21 × 16 mm pattern was wrong. The correction is isolated in this revision and does not change any source candidate.

## What changed

- `CameraPlate_Cut007` hole centers and the four corresponding plate bores now use 21 × 14 mm.
- Four camera PCB reference holes, four spacers, and four modeled camera fasteners were moved with the pattern.
- The plate outside envelope remains 56 × 32 × 3 mm. A new independent 32 mm plate-height parameter prevents outside height from following the vertical pitch.
- PCB envelope remains a separate 38 × 38 × 1.6 mm provisional parameter. Its outline is not inferred from either pitch.
- Lens, rear-component, and ribbon reservations were retained independently.
- The new fit coupon is 29 × 22 × 2 mm, with four 2.4 mm bores at the corrected centers. This checks pattern placement and hole access only.

## CAD checks

FreeCAD 1.1.4 reports the corrected plate as one valid solid. The full source assembly contains 49 valid kinematic shapes and 13 printable parts. The generated STEP plate reopens as one valid solid. Both pan/tilt revolute joints solve and the three existing native simulation definitions regenerate 52 frames each. Dense collision sampling returned no unintended moving-body overlaps across the audited ranges.

The camera lens envelope is 5.016 mm from the plate B-rep, and the PCB reference is 3 mm from the plate at the modeled stand-off. Modeled screw shanks align with the new pattern and pass through the 2.4 mm plate holes in CAD. These results do not establish physical camera/screw fit.

## Known rear clearance uncertainty

The estimated rear-component envelope is not measured from the actual camera. In the current B-rep it intersects all four provisional camera screw/nut assemblies by approximately 13.03 mm³ each. This is a **known uncertainty-envelope overlap**, not evidence that actual electronics collide. Measure/photograph the camera rear and fastener locations before full printing. Do not force or shorten screws against camera components.

The ribbon reservation has no modeled intersection with the camera plate or cradle at neutral. The cable itself and its flex through motion remain physically unverified. Motion collision samples are not cable-bend or strain-relief tests.

## Confidence

| Dimension / feature | Value | Source | Status |
|---|---:|---|---|
| Horizontal hole-center pitch | 21 mm | User supplied | Nominal input; CAD matches; physical fit not tested |
| Vertical hole-center pitch | 14 mm | User supplied | Nominal input; CAD matches; physical fit not tested |
| PCB outside envelope | 38 × 38 mm | Existing project parameter | Provisional; measure actual PCB |
| PCB thickness | 1.6 mm | Existing project parameter | Provisional |
| PCB hole diameter | 2.2 mm | Existing project parameter | Provisional; measure actual holes |
| Plate bore diameter | 2.4 mm | Existing design parameter | CAD verified; physical print clearance untested |
| Plate outside envelope | 56 × 32 × 3 mm | Corrected CAD parameter/B-rep | CAD verified; independent of pitch |
| Lens / rear / ribbon envelopes | Existing parameterized reservations | Existing project; no new camera measurement | Provisional; rear envelope overlaps modeled camera fasteners |
| Camera fasteners | 4 × M2 × 12 modeled | Existing design assumption | Provisional; confirm actual PCB hole and rear clearance |

See `../CHECKS/final_validation.json` and `../CHECKS/motion_collision_validation.json` for machine-readable results.

