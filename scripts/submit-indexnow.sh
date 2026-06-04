#!/usr/bin/env bash
set -euo pipefail
HOST="gal.tidhar.org.il"
KEY="6ba1cae03c1ec6ba61a2f3b19421056a"
JSON=$(cat <<EOF
{"host":"$HOST","key":"$KEY","keyLocation":"https://$HOST/$KEY.txt","urlList":["https://$HOST/","https://$HOST/gal-tidhar-cv.pdf"]}
EOF
)
curl -sS -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json" -d "$JSON"
echo
curl -sS -X POST "https://www.bing.com/indexnow" -H "Content-Type: application/json" -d "$JSON"
echo
