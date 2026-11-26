# Assembly and service instructions
Status: engineering candidate. Perform measurements and fit tests first. Use printed_part_inventory.csv and renders/exploded.png to identify parts; the exploded view is an identification aid, not an order of assembly. Hardware quantities are in FASTENER_BOM.csv. Do not force a servo gearbox, overtighten PCB fasteners or substitute M3 in small factory holes.

1. Confirm both actual SG90 case/ear patterns and original horns against the coupons. Establish each servo's safe electrical neutral using its own controller/data; the CAD zero angle is not a guaranteed PWM setting. Remove power for assembly.
2. Load the four small nuts into the captive ear supports as required. Insert pan motor from above into the base. Thread its real cable separately. Fit two appropriate small mounting screws with washers through original ears; nominal candidate is M1.6 x 8. Verify no case crushing and full nut engagement.
3. Locate the replaceable pan thrust ring on its three locators. Load four M3 nuts into the pan horn cover. Place cover over output, seat original star horn and use the original factory retaining screw. Lower the yoke onto the positive-profile pocket. Fit four M3 x 10 from above. Confirm cover capture without horn damage, bottoming or unintended clamping of stationary parts.
4. Leave right idler pillar off. Insert tilt servo from the fork's right toward its left through the tab opening. Fit its two small ear screws/washers/nuts. Cable threading and strain relief require real-hardware inspection.
5. Load four M3 nuts in tilt horn cover. Fit cover, original star horn and original retaining screw. With camera module and four drive bolts absent, slide cradle axially from the right onto the star interface. Fit four M3 x 10 from inside the fork. Pocket walls must engage the real horn profile; axial covers alone are not acceptable torque transfer.
6. Seat sleeve flange into right cradle cheek register. Slide removable pillar from right over sleeve neck onto yoke foot. Fit two M3 x 10 foot joints. Add idler M3 washer, M3 x 12 and locknut. Tighten against sleeve only. Check wall remains free and no hard rubbing develops. The user's M3 x 10 is not the specified idler bolt.
7. Attach camera PCB to plate with four 3 mm standoffs and four suitably sized screws/nuts (nominal M2 x 12, conditional on actual holes/components). Hole centers are 21 x 16 mm. Standoff height, component footprints and screw intrusion must be checked. Attach plate to moving cradle frame through four independent M3 x 10 joints. Never infer PCB outline or lens position from hole spacing.
8. Route real camera lead/ribbon with strain relief and a free service loop. Slowly check whole intended travel without power, without back-driving or forcing gearboxes. Check actual cables, connector, lens field, rear electronics and moving hardware. Only then perform conservative powered checks with a safe controller range.

## Nominal fastener stacks (mm)
| Joint | Grip | Nut height | Nominal protrusion |
|---|---:|---:|---:|
| M3 x 10 horn covers | 5.5 | 2.4 | 2.1 |
| M3 x 10 plate/frame and pillar | 6 | 2.4 | 1.6 |
| M1.6 x 8 ear, including washer | 5.5 | 1.3 | 1.2 |
| M2 x 12 PCB/spacer/plate | 7.6 | 1.6 | 2.8 |
| M3 x 12 idler, including washer | 6.8 | 4 | 1.2 |

These are geometric thread-envelope projections, not verified purchased bolt dimensions, thread engagement strength or torque settings. Extra camera screw projection must not contact live components.

## Disassembly and retaining-screw access
Reverse stages while supporting moving parts. Pan ear screws require upper yoke/horn removal. Tilt ear screws require cradle/horn removal. Camera module slides forward off frame with its four M3 joints removed; module approach was checked in CAD. Pan factory screw has a nominal diameter-5 driver path through a diameter-6 cradle service opening with camera module/lead removed. Tilt factory screw access requires support of cradle, removal of idler bolt/washer and pillar, then sleeve removal; a diameter-5 tool passes through the diameter-5.2 coaxial cheek hole.

Tilt cover bolts were checked using a nominal 50 mm stubby tool with diameter-5 bit and diameter-11 body after camera removal; pan cover bolts with camera/cradle removed; pillar joints with a long narrow shaft from above. Real tools must match these envelopes. CAD checks cover stated rigid tool approach stages, not fingers, flexible cable threading or all possible tool shapes.
