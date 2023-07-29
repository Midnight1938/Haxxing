#!/bin/bash
#podman build -t kali-box .
## podman run -p 5900:5900 -i -t -v ~/Documents/Dev/Haxxing/container:/root/data/ kali-box
podman start b168bf0ff62e
podman exec -i -t b168bf0ff62e /bin/bash
notify-send "Ready" "VNC into localhost:5900\npwd: kallie"