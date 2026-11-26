# SG90 compatibility audit
| Dimension | Both actual CAD models mm | Source / confidence | Status |
|---|---:|---|---|
| Main case length x width |22.7 x12.2|BRep section at localZ5; TowerPro nominal body dimensions with detailed community datum|PASS CAD / PROVISIONAL clone fit|
| Main case height |22.7|Juan Fenoy reference detailed case|PROVISIONAL|
| Entire case/ears/output bounding dimensions |32.3 x12.2 x30.3|Actual canonical BRep bounds, both references|PASS CAD / PROVISIONAL hardware|
| Ear bottom / thickness |15.9 /2.5|Community native geometry; manufacturer datumF ambiguous|PROVISIONAL|
| Ear hole pitch / diameter / open slot |27.2 /2.0 /1.3|Community drawing/native model|PROVISIONAL|
| Output shoulder / top above base |27 /30.3|Manufacturer dimension labels; headline29 conflicts with detailed datum|PROVISIONAL|
| Axis from near case end |5.9|Canonical section and community output datum|PROVISIONAL|
| Gear boss diameter / height |12.2 /4.3|Manufacturer width plus community height datum|PROVISIONAL|
| Output smooth envelope diameter / height |5 /3.3|Rounded community envelope; no exact tooth shape|PROVISIONAL; not spline dimensions|
| Wire exit notch W/H/base height |3.6 /1.2 /4.5|Community native sketch|PROVISIONAL|

Both references are consistent SG90-sized geometry, with ears, holes, bosses, smooth outputs and wire exits. They are not MG90S/MG995 replacements. Canonical BRep comparison is below0.001mm3; actual dimensions/cylinder surfaces are in TESTS/results/actual_servo_dimensions.json. Manufacturer tolerances were not published; no dimensional tolerance or clone equivalence is inferred. See DIMENSIONAL_AUDIT.csv and historical_servo_dimension_comparison.csv for full sources and low-confidence details.

Original star-horn proxy: five arms at0/72/144/216/288 degrees,12mm tip lengths,3.6mm widths,2mm web,8mm hub diameter. None was measured on the user's original horns. Socket and retaining-screw proxies are not thread or spline specifications. Exact spline teeth are not modeled. Preserve original horn-to-servo pairing and original factory retaining screws; M3 is never assumed to fit the horn.

Both original horns are axially captured by covers and four M3 structural joints, with0.25mm nominal side allowance and2.2mm pocket depth. Proxy engagement probes show free at+/-1 degree and positive wall engagement by+/-2 degrees. This demonstrates a plausible positive torque path in the modeled profile, not measured backlash, load capacity or physical fit. Both horn and output/screw reference solids were included in all-pair interference tests; no positive-overlap whitelist.

Both motor installation/removal routes, original ear seating, ear bolt axes and staged retaining-screw tool paths were checked. Ear mounts provisionally require M1.6x8 with small nuts/washers, conditional on measured original holes. M3 stock is for structural joints only. The small ear coupon and two-piece positive horn coupon are essential before full printing.
