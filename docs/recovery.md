# Read-only Raspberry Pi recovery

The original Pi project directory is EyeTrace under the SSH user’s home. The last recorded host and address were tested through SSH before starting a transfer. Both attempts failed before login.

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
