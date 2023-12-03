#!/bin/bash
# podman build -t kali-box .
##Alt: podman pull quay.io/midnight1938/kali-box
## podman run -p 5900:5900 -i -t -v ~/Documents/Dev/Haxxing/container:/root/data/ kali-box
podman start c5db0b30a942
notify-send "Ready" "VNC into localhost:5900\npwd: kallie"
podman exec -i -t c5db0b30a942 /bin/bash
notify-send "Reminder" "Container is still active!"
