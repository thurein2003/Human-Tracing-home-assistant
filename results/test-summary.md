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

On November 26, 2026, the 11 hardware-free tests, all six Bash syntax checks and the Windows helper's PowerShell syntax check passed again. The archive scan passed with zero findings across 1,672 tracked files and 18,162 embedded files. It verified 1,625 unique manifest destinations. Git object integrity passed.

The unit suite covers the new diagnostics, observation schema, malformed JSON, mocked timeout and connection failures, calibration-plan bound checks and the loopback launcher. Run these checks from the root of a checkout.

```bash
python3 -m unittest discover -s tests -v
python3 tests/validate-repository.py
git fsck --full
for script in software/raspberry-pi/*.sh; do bash -n "$script"; done
```

GitHub Actions defines the same hardware-free checks and the PowerShell parser run.

## Hardware and source limitations

Pi SSH recovery remains blocked. See the [read-only recovery record](../docs/recovery.md) for the connection attempts and missing sources. Controller-specific tests for stale decisions, mocked movement limits, target lock/loss, queue cooldown and Flask endpoints require that source. Physical GPIO, camera, speaker, live dashboard and end-to-end tunnel checks were skipped. No servos were actuated during collection.
