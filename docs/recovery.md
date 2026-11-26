# Read-only Raspberry Pi recovery

The original Pi project directory is `~/EyeTrace`. In the November 26, 2026 recovery attempt, the recorded local hostname failed to resolve and all three recorded addresses timed out on SSH. A comparison against the saved Pi host key found no match among 15 visible Wi-Fi neighbors. The configured Tailscale SSH alias reached a separate Linux workstation, where a read-only search found no Eye Trace project or controller files.

The authoritative `manual_web.py`, `intelligence.py`, `voice.py`, calibration scripts and historical backups remain pending. Recovery did not reach the Pi or access the dashboard. The attempt used SSH connectivity and read-only file queries.

Set EYETRACE_SSH_TARGET to the verified Pi account and current address. After comparing the SSH server host key with the local console, verify connectivity and the project path from Windows PowerShell.

```powershell
$target = $env:EYETRACE_SSH_TARGET
ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=yes $target 'test -d "$HOME/EyeTrace" && printf "%s\n" EyeTrace'
```

For recovery, create a fresh owner-only directory outside the Git worktree and launch SFTP from it after the SSH check succeeds.

```powershell
sftp -o BatchMode=yes -o StrictHostKeyChecking=yes $target
```

At the SFTP prompt run `get -pR EyeTrace`. This reads the original tree into the current local directory and preserves file times. The running Pi application, services, networking and GPIO are unaffected. Keep the recovered tree local until its code, configuration and media are reviewed.

Preserve manual_web.py from the Pi as the current baseline. Collect intelligence.py, voice.py, helpers, templates, static assets and historical backups. Record hashes before modifying release copies. Compare manual_web.py to upgrade scripts and historical snapshots without executing them. Inspect the active service state, listening sockets, package versions and audio devices using read-only queries. Never call a movement, tracking-start or stop endpoint during collection. Review route handlers before testing even ostensibly read-only endpoints.

The [Pi setup guide](raspberry-pi.md) describes the clean rebuild after recovery. The [security review](security-review.md) describes what belongs in the Git commit.
