# Windows Ollama

Install Ollama from its [Windows download](https://ollama.com/download/windows). Start the desktop app on loopback. If you use a foreground server instead, set OLLAMA_HOST before running ollama serve. Gemma 3 4B supports text and image inference in a local Ollama instance. [Gemma 3 model card](https://ollama.com/library/gemma3).

```powershell
$env:OLLAMA_HOST = '127.0.0.1:11434'
ollama serve
```

Use a separate PowerShell window for the following commands. Replace the placeholder with the SSH account and host verified locally. Compare the host key fingerprint against the Pi console before enrolling a new host key. The script requires an enrolled host key.

```powershell
$env:EYETRACE_SSH_TARGET = 'pi-user@pi-host'
$entry = '.\software\windows\EyeTrace.ps1'
& $entry -Action Check
& $entry -Action Model
& $entry -Action Pi
& $entry -Action Text
& $entry -Action Vision -ImagePath '.\media\CAD-renders\corrected-assembly.png'
& $entry -Action Tunnel
```

If Ollama is absent, & $entry -Action Install -ApproveInstall opens the vendor download for manual installation. Keep the tunnel open. From another Windows window run:

```powershell
.\software\windows\EyeTrace.ps1 -Action Dashboard
```

The default forwards are Pi 127.0.0.1:11435 → Windows 127.0.0.1:11434, and Windows 127.0.0.1:8081 → Pi 127.0.0.1:8080. The equivalent SSH command with your selected target is:

```powershell
ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -R 127.0.0.1:11435:127.0.0.1:11434 -L 127.0.0.1:8081:127.0.0.1:8080 $env:EYETRACE_SSH_TARGET
```

Use Ctrl+C in the tunnel console to release the forwards. Use the variables shown in [example configuration](../config/eyetrace.env.example) for port overrides. If modifying a port, confirm the authoritative Pi controller honors or matches it.

## Troubleshooting

- **Ollama API unavailable** • Inspect Get-NetTCPConnection -LocalPort 11434 and confirm the listener is on loopback. Leave the server process or desktop app running.
- **SSH fails** • Confirm the current Pi address, the host key and your selected account. Preserve strict host-key checking. A reverse forward needs the Pi SSH server to permit forwarding with loopback-only binding.
- **Remote port collision** • Check both end hosts for active listeners. Close only your own obsolete tunnel after identifying it. Keep GatewayPorts disabled for the Pi tunnel.
- **No model output** • Run the local text test first, then the Pi forwarded tags check. A model load can take longer than a cached response.
