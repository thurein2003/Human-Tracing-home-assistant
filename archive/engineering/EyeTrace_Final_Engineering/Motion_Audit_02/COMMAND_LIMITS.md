# Motion audit 02: command range

Joint values in r03 are CAD joint angles relative to the neutral assembly pose.

| Axis | Audit range | Sampling | Selection basis | Hardware command mapping |
|---|---:|---:|---|---|
| Pan | -90° to +90° | 2° (91 positions) | Modeled structural clearance against the base/stator over sampled sweep. | Unverified; no SG90 pulse calibration or wire sweep. |
| Tilt | -30° to +30° | 1° (61 positions) | Soft limit. Camera board/yoke gap at +30° is 2.813 mm; gap declines to 0.157 mm at +41° and collision begins near +42°. | Unverified; no SG90 pulse calibration or physical stop check. |

Combined collision screen sampled 91 pan/tilt grid combinations (pan every 15°, tilt every 10°). These are CAD ranges only. There is no verified PWM microsecond mapping, no calibrated servo center, and no modeled physical stop. Cable routing may reduce pan travel. Begin physical checks unpowered and by hand; once energized, begin near neutral and use a small range, increasing only after clearance is confirmed. Do not stall the servos against stops.
