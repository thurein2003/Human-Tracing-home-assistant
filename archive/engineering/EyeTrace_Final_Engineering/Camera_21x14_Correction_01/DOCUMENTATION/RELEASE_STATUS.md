# Release status — Camera 21 × 14 mm correction

| Stage | Status | Evidence / acceptance still needed |
|---|---|---|
| CAD VERIFIED | PASS for corrected nominal pattern and software geometry | FreeCAD solids, coordinates, STEP readback, native solver and sampled moving-body collision report pass. Rear uncertainty-envelope overlap remains explicitly flagged. |
| FIT-TEST READY | PASS | Correct 21 × 14 mm coupon STL and Creality project sliced; print the coupon and check both real camera and screw clearance without force. |
| FULL-PRINT READY | BLOCKED | Must pass the corrected coupon and establish rear-component/screw clearance from the actual camera. Review the updated full project after coupon feedback. |
| PHYSICALLY VERIFIED | NOT COMPLETE | No physical print or hardware fit result has been supplied. |

**Release hold:** the new full-bed project is a software-validated candidate, not a released full-production print. Existing 21 × 16 mm files are superseded for camera-interface printing and remain preserved.
