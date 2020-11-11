systemctl stop batteryprobe.service
sudo kill $(cat /run/battery_probe.pid)
