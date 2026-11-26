# Tracking results

The builder observed that the conventional face detector did not acquire a complete face when a partial head entered the bottom of the frame. The later investigation approach analyzes a stable image and can recommend a downward look for that cue, then hands control back to local face detection once a complete face is confirmed. The current Pi source and logs are needed to verify which upgrade is deployed.

The intended target-lock behavior uses separate centering and unlock boundaries to reduce motion while centered. Target loss starts a brief hold before resuming search. The builder’s recording shows the physical rig changing position. There is no independent track ground truth, success rate, FPS or verified end-to-end latency measurement. See [tracking architecture and historical settings](../docs/ai-tracking-voice.md).
