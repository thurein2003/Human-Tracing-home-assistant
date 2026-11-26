# AI vision results

The following are historical observations recorded by the builder. They were not rerun during archival.

1. The Pi discovered the Windows Ollama API through the SSH reverse forward.
2. Gemma 3 4B answered a text inference request.
3. An image inference test described low light and reported a visible person in the lower-right quadrant.
4. A subsequent structured test produced the response below.
5. Offline eSpeak NG announcements played through a physical speaker.

```json
{
  "person_visible": true,
  "possible_person": true,
  "horizontal": "center",
  "vertical": "center",
  "action": "follow",
  "confidence": 0.8,
  "reason": "A person is clearly visible in the center of the frame. I will follow this individual.",
  "speech": ""
}
```

No raw camera input, timestamps or screenshot were recovered for independent position verification. Model confidence is self-reported. The test provides no calibrated accuracy estimate.
