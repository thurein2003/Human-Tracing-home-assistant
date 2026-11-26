#!/usr/bin/env bash
set -u
status=0
for package in picamera2 cv2 numpy flask gpiozero lgpio; do
    /usr/bin/python3 -c 'import importlib.util, sys; sys.exit(importlib.util.find_spec(sys.argv[1]) is None)' "$package" \
        && printf '%s present\n' "$package" || { printf '%s missing\n' "$package"; status=1; }
done
command -v espeak-ng >/dev/null || { printf 'espeak-ng missing\n'; status=1; }
for endpoint in "${EYETRACE_PI_WEB_PORT:-8080}/" "${EYETRACE_PI_OLLAMA_PORT:-11435}/api/tags"; do
    port=${endpoint%%/*}
    if [[ ! $port =~ ^[0-9]{1,5}$ ]] || (( 10#$port < 1 || 10#$port > 65535 )); then
        printf 'Invalid port %s\n' "$port" >&2; status=1; continue
    fi
    curl --noproxy '*' --silent --show-error --fail --max-time 5 --output /dev/null "http://127.0.0.1:$endpoint" \
        && printf 'HTTP available at %s\n' "$endpoint" || status=1
done
exit "$status"
