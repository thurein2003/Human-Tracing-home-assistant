#!/usr/bin/env bash
set -euo pipefail
packages=(python3 python3-picamera2 python3-opencv python3-numpy python3-flask python3-gpiozero python3-lgpio python3-requests espeak-ng curl)
sudo apt-get update
sudo apt-get install -- "${packages[@]}"
dpkg-query -W -- "${packages[@]}"
