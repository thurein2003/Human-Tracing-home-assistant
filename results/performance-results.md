# Performance results

The builder recorded one historical text inference using local Windows Ollama.

| Metric | Recorded value |
| --- | --- |
| Model | gemma3:4b |
| Parameters | Approximately 3.9 billion |
| Quantization | Q4_K_M |
| Model size | 3,350,272,403 bytes |
| Generated tokens | 160 |
| Total duration | 12.7745659 s |
| Generation duration | 6.081061 s |
| Generation speed | Approximately 26.31 tokens/s, calculated as 160 ÷ 6.081061 |

This run provides a single historical observation. GPU settings, laptop load, response variance, image processing latency and tracking-loop FPS were not recorded.

The [new Windows loopback smoke tests](local-ollama-smoke.json) returned the expected text and processed the recovered CAD render. The vision response identified a rotating head and likely optical opening and described some internal parts unsupported by the image. Both calls completed successfully. Their elapsed times describe these smoke tests only.
