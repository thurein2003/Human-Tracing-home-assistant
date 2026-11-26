# Motion and collision validation
PASS nominal components: 1266 distinct sampled poses, 1488816 component-pair checks, 230646 unique relative-transform checks; zero unintended nominal-component penetrations. Nine rear uncertainty conflicts remain BLOCKED as explained in CAMERA_MOUNTING_AUDIT.md.

All49 tagged components participate: both motor housings/ears/bosses/output envelopes, original horn proxies, covers, factory screw proxies, all structural/camera fastener solids, PCB, lens, frame, pillar, sleeve and cable reservations. No positive penetration whitelist. Compounds also receive internal-solid pair checks.

Main grid: pan-60..60 and tilt-30..30 in2.5-degree increments (1225 combinations). Additional off-grid and one-degree-spaced guard positions near+/-60..62 and+/-30..32 produce1266 distinct poses. Both independent axes and simultaneous motion are included. Exact BRep volume is computed after bounding-box screening; only invariant relative transforms are cached. Reporting threshold0.001mm3. Numerical thresholds are not hardware tolerances. This discrete sampling is not a continuous swept-volume guarantee.

Proposed initial command window: pan+/-55deg, tilt+/-25deg relative to a physically established neutral. This gives5-degree margin inside the main tested envelope; actual cable/servo limits can be smaller. Guard positions are not an expanded command range. No full180-degree travel is claimed. CAD zeros are not guaranteed electrical neutral PWM values. There are no newly certified external hard stops; original servo internal stops and exact electrical endpoints remain unknown. Never use a gearbox stop as a calibration force limit.

Contact classes: zero-distance ear seats, nut seats, spacer/PCB and plate/frame contacts are intentional bearing/fastening contacts; horn pocket wall drive is separately probed as designed engagement; unintended nominal penetration is a FAIL; rear-box overlap is unverified possible camera material, explicitly retained as BLOCKED. No coincident smooth shaft/socket geometry establishes physical spline engagement.

17-frame motion GIF and source images in RENDERS use positions on the tested grid. They show rigid CAD motion only. True cable bend, connector strain, backlash, wear and powered repeatability require physical checks.
