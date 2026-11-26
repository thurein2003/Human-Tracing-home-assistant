# Raspberry Pi setup

The builder’s system used a Pi 4B, Debian 13 Trixie, system Python, Picamera2, OpenCV, NumPy, Flask, GPIO Zero, LGPIO and eSpeak NG. The original package versions are pending Pi access. Use a Trixie image with the Raspberry Pi camera packages available. The dependency script reports the package versions on the target. [Raspberry Pi camera documentation](https://www.raspberrypi.com/documentation/accessories/camera-software.html).

## Clean installation

On a fresh Pi, enable SSH using your own key, record its host-key fingerprint, and transfer the project through a trusted channel. GPIO initialization can move the mechanism depending on the original application, so keep servo power physically isolated while validating startup.

```bash
cd software/raspberry-pi
bash install.sh
bash camera-test.sh
bash speaker-test.sh
/usr/bin/python3 ollama-test.py
/usr/bin/python3 ollama-test.py --structured
```

The camera script lists devices. If the image lacks rpicam-hello, use sudo apt-get install rpicam-apps-lite on Raspberry Pi OS Lite or sudo apt-get install rpicam-apps on the desktop image. Connect the Windows tunnel before the Ollama test. The structured test sends a synthetic text prompt with no camera image.

Restore the current verified manual_web.py, intelligence.py and voice.py and any local modules/templates into this folder from the original Pi backup. Review the original entry point, ensuring the restored controller starts idle or manual with tracking disabled and never enables movement automatically. The loopback launcher assumes the source starts Flask through Flask.run. Verify that signature in the restored code before executing it and confirm the listening address afterward. The launcher cannot enforce idle behavior inside unknown source code.

```bash
bash start.sh
journalctl --user -u eye-trace-dashboard.service -n 50
ss -ltn
bash health-check.sh
bash stop.sh
```

These wrappers manage only the service named eye-trace-dashboard.service for the logged-in user. Restarting a separately installed service or invoking an old migration script can affect the original robot. Keep the original installation intact during archival. If the user systemd manager is unavailable, diagnose the login session and run the same reviewed launcher in the foreground from a local console with servo power isolated for the first check.

## Calibration and first run

1. Isolate servo power and check neutral horn installation, ribbon slack and enclosure clearance.
2. Use the planner with the bench-verified bounds. Example angles below only illustrate command format.
3. With tracking off, reapply servo power with the mechanism clear. Test one small manual move per axis at a time from neutral. Record direction, safe bounds, detach behavior and measured clearances. Reverse axis configuration only after reviewing the recovered controller.
4. Confirm stop and release behavior before explicitly enabling autonomy. PWM detachment can allow loaded axes to sag. Continuous PWM holding has thermal and mechanical implications and is a separate design choice.

```bash
/usr/bin/python3 calibration-plan.py pan 85 90 95 1
/usr/bin/python3 calibration-plan.py tilt 85 90 95 1
```

## Dashboard and prior routes

The builder reports an MJPEG stream, crosshair, target box, centering zone, commanded angles, tracking state, manual movement and stop/release. Reported paths are /video, /api/tracking, /api/move, /api/stop, /api/intelligence and /api/voice. Methods, request formats and current availability await source inspection. Screenshots from the real application also await access. Treat routes as unauthenticated and restrict listeners to loopback behind SSH.

## Troubleshooting

- **Camera absent** • Shut down before reseating CSI at each end. Use the camera listing before launching any app. Ensure the active image provides camera packages and the camera device is free.
- **Jerky motion** • Isolate servo power. Check shared ground continuity, peak supply behavior, connector orientation, horn binding and commanded limits.
- **Web access** • Confirm the Pi service and its loopback listener, then check the Windows forwarding process. A port conflict can stop the tunnel.
- **AI requests fail** • Run the forwarded tags check and the Windows local Check action. Confirm the same model name, exact endpoint and configured timeouts.
- **No audio** • Verify local output routing with the known working physical speaker. eSpeak NG produces audio through the selected system output. Record the interface and device before documenting its wiring.

If migration away from a Pi Ollama install is desired, inspect it first with systemctl status ollama.service. On a rebuild where Windows inference has been confirmed, sudo systemctl disable --now ollama.service stops and disables the Pi service while retaining installed files. That command was not run on the original Pi.


[Read-only recovery instructions](recovery.md).
