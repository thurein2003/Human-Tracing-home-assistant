# Validation summary

| Check | Result |
| --- | --- |
| Diagnostic unit tests | 11 passed, 0 failures, 0 skips |
| Bash parser | Six Pi setup and diagnostics scripts passed |
| PowerShell parser | Five new and recovered scripts passed |
| FreeCAD readback | Four selected FCStd files and four STL files opened, with zero invalid shape objects in the four native documents |
| Selected STL integrity | Four closed meshes, all below the K2 build-volume dimensions |
| Source preservation | All 2,851 originals rehashed against the local inventory. The primary ZIP matched its supplied SHA-256. |
| Windows Ollama | gemma3:4b discovery, text inference and image inference passed over loopback |
| Demonstration preview | Extracted H.264 stream SHA-256 matched the original video stream |

The unit suite covers the new diagnostics, observation schema, malformed JSON, mocked timeout and connection failures, calibration-plan bound checks and the loopback launcher. Run these checks from the root of a checkout.

```bash
python3 -m unittest discover -s tests -v
python3 tests/validate-repository.py
git fsck --full
for script in software/raspberry-pi/*.sh; do bash -n "$script"; done
```

GitHub Actions defines the same hardware-free checks and the PowerShell parser run. The workflow awaits the first private push.

## Hardware and source limitations

Pi SSH timed out at the last recorded address and the previous hostname did not resolve. The original controller, AI, voice, calibration and historical Python files remain unrecovered. Controller-specific tests for stale decisions, mocked movement limits, target lock/loss, queue cooldown and Flask endpoints require that source. Physical GPIO, camera, speaker, live dashboard and end-to-end tunnel checks were skipped. No servos were actuated during collection.
