# AI, tracking and voice

## Architecture and authority

Use the Raspberry Pi for Picamera2 capture, OpenCV face detection, the Flask dashboard, GPIO servo control and offline speaker output. The Windows laptop serves Ollama with gemma3:4b. It analyzes selected stable frames and sends an observation to the Pi. Treat the observation as a suggestion. Only the Pi controller can authorize movement.

The intended investigation loop is Observe → Think → Move → Observe Again. A partial head near the bottom can merit a bounded downward investigation if the result is fresh and the direction agrees with calibrated tilt. A complete face is confirmed using local computer vision. Centering needs hysteresis to avoid repeated corrections. Hold inside the lock zone, wait briefly after loss, and resume an appropriate scan or investigation when the timeout expires.

Current source readback is pending. The V5 record describes Manual, Observing, AI observing/thinking, Scanning, Investigating, Confirming target, Centering, Target locked, Holding target and Limit/check. Source verification is needed for exact display strings and state transitions.

| Historical V5 setting | Value |
| --- | --- |
| Autonomous pan / tilt windows | 80–100° each |
| Centering dead zone | 45 px horizontal, 35 px vertical |
| Unlock thresholds | 65 px horizontal, 50 px vertical |
| Correction / search intervals | 0.30 s / 0.85 s |
| Target lost timeout | 3 s |
| Maximum tracking correction | 1.5° |
| Confirmation threshold | Three consecutive detections |

Those are historical software values. Physically measure allowable motion and servo polarity. PWM detachment can cause sag under load.

## AI observation

| Field | Meaning |
| --- | --- |
| person_visible | Complete or visible person reported by the model |
| possible_person | Possible person or partial human cues |
| horizontal | Estimated left, center or right |
| vertical | Estimated up, center or down |
| action | Suggested next investigation action |
| confidence | Model’s self-reported score |
| reason | Short rationale |
| speech | Optional speech text |

A safe controller attaches a capture timestamp and command generation to the frame, checks for a changed mode or target, validates the action and confidence, clamps movement to calibrated bounds, and cancels stale or invalid results. This is the intended validation contract. Current implementation, observation memory retention and deduplication remain unverified. Short-term context can guide direction after a partial glimpse. It provides no identity evidence or persistent biometric memory.

## Voice

The builder reports a physical speaker driven by offline eSpeak NG. The historical design uses a background queue, duplicate-message suppression and event cooldowns. Actual hookups, timing and audio output routing require the recovered voice.py and installed setup.

| Intended event | Recorded announcement |
| --- | --- |
| Startup | Eye Trace online. All systems ready. |
| Scan | I am searching for you. |
| Suspected person | I think I see someone. |
| Investigation | Let me take a closer look. |
| Confirmed target | I found you! |
| Correction | Let me adjust my position. |
| Tracking | I am following you now. |
| Loss | I lost sight of you. |
| Resuming search | Let me find you again. |
| Reacquisition | There you are! |
| Manual | Manual control activated. |
| Stop | Okay. I will stop moving. |
| AI unavailable | My AI brain is temporarily disconnected. |

The historical speaker test and model output are in [AI vision results](../results/AI-vision-results.md). Browser microphone conversation and natural neural speech remain future work pending source evidence.
