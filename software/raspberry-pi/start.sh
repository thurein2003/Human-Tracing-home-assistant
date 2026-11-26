#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
for source in manual_web.py intelligence.py voice.py; do
    if [[ ! -f $source ]]; then
        printf 'Restore and review the authoritative Pi source first. Missing %s\n' "$source" >&2
        exit 1
    fi
done
port=${EYETRACE_PI_WEB_PORT:-8080}
exec systemd-run --user --unit=eye-trace-dashboard.service --collect --setenv="EYETRACE_PI_WEB_PORT=$port" \
    --property="WorkingDirectory=$PWD" /usr/bin/python3 "$PWD/launch_dashboard.py"
