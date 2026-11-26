#!/usr/bin/env bash
set -euo pipefail
# Listing probes camera availability without saving images or initializing GPIO.
exec rpicam-hello --list-cameras
