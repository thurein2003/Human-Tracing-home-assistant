# Development history

Original file names, revision directories, content hashes and filesystem timestamps are indexed in the [recovery manifest](../archive/recovery-manifest.csv). Timestamps are archival clues and can reflect copying. The sequence below follows documented design dependencies and the builder’s bring-up account.

| Phase | Evidence and engineering decision |
| --- | --- |
| Initial CAD and structure | The original timestamped CAD tree contains editable part models, candidate assemblies and print layouts. |
| SG90 integration | Candidate and SG90 reference revisions compare servo envelopes, recover positive horn engagement and correct tab, boss and fastener interference. Unknown spline and clone dimensions are called out. |
| Integrated prototype | Integrated Candidate 01 combined revised servo references, the 13-piece assembly and initial 21 × 16 mm camera plate. |
| Motion and clearance | Final Engineering adds sampled motion audits, alternate assemblies and clearance test records. Camera rear envelope and cable routing remain physical fit items. |
| Camera correction | The revised plate, coupon and K2 bed move from nominal 21 × 16 mm to 21 × 14 mm. Native FreeCAD and STL assets preserve both generations. |
| ABS manufacturing | Creality Print projects and G-code record settings, brim/support footprints and time/filament estimates. Fit-test beds and horn tests isolate high-risk interfaces before committing to larger prints. |
| Later mechanical experiments | R15–R31 and cross-horn prototype directories preserve packaging, mount, plate and horn-pocket refinements. R31 increases a 1.70 mm horn recess to 2.00 mm with a thinner roof awaiting physical load/fit verification. |
| Camera and GPIO bring-up | The builder reports CSI camera operation and servo instability resolved by restoring a shared signal ground. Harness and audio path need readback. |
| Manual web control and OpenCV | The builder reports a working dashboard, face capture, manual positioning and movement via OpenCV. The current source and endpoint methods await collection. |
| Physical autonomous searching | The prototype searched for a complete face. A partial head at the bottom of the frame motivated changes to the search method. |
| Ollama migration and tunneling | The builder moved inference to Windows, then established a loopback reverse tunnel for the Pi and a local forward for the browser. |
| Multimodal inference | Historical text, image and structured JSON results are reproduced in the results directory. |
| Offline voice | Selected messages used the physical speaker and eSpeak NG. Event mapping, queue behavior and cooldowns require source review. |
| Target locking and investigation | The V5 record introduces a lock/unlock zone, confirmation and delayed reacquisition, plus the observe–think–move approach for partial-person cues. |
| Physical demonstration | The local MP4 shows the assembled device, changes in pan/tilt and the bench setup. The observed motions do not identify the active control mode. |

For engineering differences, consult [mechanical design](mechanical.md) and [tracking results](../results/tracking-results.md). Physical build revision, fitted hardware dimensions and dates are pending evidence.
