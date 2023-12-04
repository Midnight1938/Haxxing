#!/bin/bash
# podman build -t kali-box .
##Alt: podman pull quay.io/midnight1938/kali-box
## podman run -p 5900:5900 -i -t -v ~/Documents/Dev/Haxxing/container:/root/data/ kali-box
podman start d390723adb65
notify-send "Ready" "VNC into localhost:5900\npwd: kallie"
podman exec -i -t d390723adb65 /bin/bash
notify-send "Reminder" "Container is still active!"
