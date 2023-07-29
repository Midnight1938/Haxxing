#!/bin/bash
#podman build -t kali-box .
## podman run -p 5900:5900 -i -t -v ~/Documents/Dev/Haxxing/container:/root/data/ kali-box
podman start 1a37661e08a1
notify-send "Ready" "VNC into localhost:5900\npwd: kallie"
podman exec -i -t 1a37661e08a1 /bin/bash
notify-send "Reminder" "Container is still active!"