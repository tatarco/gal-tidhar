#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for f in hero-*.html; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=1200,630 --virtual-time-budget=1500 \
    --screenshot="${f%.html}.png" "file://$PWD/$f" 2>/dev/null
done
echo "rendered $(ls hero-*.png | wc -l | tr -d ' ') PNGs"
