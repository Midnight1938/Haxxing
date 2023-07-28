podman build -t kali-box .
podman run -p 5900:5900 --rm -i -t -v ~/Documents/Dev/Haxxing/container:/root/data/ kali-box
notify-send "Ready" "VNC into localhost:5900\npwd: kallie"