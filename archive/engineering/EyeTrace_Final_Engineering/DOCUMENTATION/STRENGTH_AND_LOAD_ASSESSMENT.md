# Strength and load assessment — screening, not certification
TowerPro publishes1.8kgf cm stall torque at4.8V: https://towerpro.com.tw/product/sg90-analog/ . Converted nominal stall torque is0.17652Nm. Stall torque is not a continuous working rating, and it does not certify the user's clones. An analyst-selected25% working budget is0.04413Nm; it is a conservative screening assumption, not a manufacturer guarantee.

Mass/center estimates use actual CAD volumes and volume-weighted solid centroids. Printed parts are treated as100% solid PETG at1.27g/cm3 (illustrative Prusament material: https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf); nominal steel7.85g/cm3, horn nylon1.15g/cm3, SG90 mass9g. Solid printed mass bound is173.2g before supports/brim, not slicer filament consumption. Actual filament density, infill distribution, hardware masses and camera mass are unknown.

Assumed camera/lens combined mass10/25/50g at[0,-33,76]mm. Gravity torque is summed about tiltX atZ78 and maximized at0.5-degree samples within+/-30deg. Slow acceleration assumption1rad/s2 with conservative bounding-radius inertia. Tilt demand=2*maximum gravity+I*acceleration+0.005Nm cable allowance. Pan demand=mu*weight*radius+I*acceleration+0.005Nm, assuming mu0.30 and30mm effective thrust radius. A worse cable or bearing friction can exceed these assumptions.

|Camera assumption g|Tilt static Nm|Tilt screened demand Nm|Pan screened demand Nm|Assessment|
|---:|---:|---:|---:|---|
|10|0.0082|0.0215|0.0191|Within assumed tilt budget|
|25|0.0129|0.0309|0.0205|Within assumed tilt budget|
|50|0.0209|0.0470|0.0227|EXCEEDS assumed tilt budget|

At25g camera assumption: tilt moving mass82.47g, pan moving mass169.06g; neutral tilt CoM[-7.20,-15.40,73.78]mm. Pan neutral eccentricity13.02mm creates0.0216Nm overturning moment under gravity. The annular support has27.5/32mm radii; mean thrust pressure0.00197MPa is an area average, not peak pressure. Clearance/compliance can create partial contact and transfer residual moment into horn/shaft; no shaft bearing load rating was found. At50g the tilt screening budget is exceeded. No measured payload rating is issued.

Opposite tilt support nominal reaction at25g is about0.345N, giving projected pressure0.0276MPa on assumed5mm x2.5mm journal area. This simple rigid two-support split excludes bracket flexibility and dynamic loads. Sleeve/nut clamp separation is geometrically checked; a real freely turning journal and secure retaining nut remain test items.

Representative weak-axis PETG plate-strip calculation:2N at20mm lever,20mm effective width,2.5mm thickness and assumed1000MPa effective modulus yields1.92MPa bending stress and0.205mm deflection. This is a sensitivity example, not peak stress in the actual fork or FEA. Actual layer adhesion, local notches, bridges, print defects, nut preload and time/temperature creep are excluded. No numerical factor of safety or fatigue certification is claimed from generic PETG properties.

Retain the thrust wear ring, opposite pivot and removable pillar. Avoid heavier cameras or cable tension until measured. Verify low-speed operation without stalls, bracket deflection, settling/vibration, backlash, fastener loosening, bearing wear and creep under intended duty/temperature. Rebalance or revise only using actual camera mass/CoM evidence; arbitrary thickening raises servo inertia and material use.

Pan inertia bound includes the full tilt Y/Z radial envelope, not only its neutral XY projection. Apply ramped, low-acceleration commands rather than abrupt position jumps; actual controller dynamics and servo damping are unverified.
