# BatteryProbe.collect

## Server

### Usage
To build and run the influxdb and grafana containers, use:
```
$ docker-compose -f server/docker-compose.yml up --build -d
```

## Client

### MACOS
To initiate and load the daemon, simply launch the program "install.py"
``` 
$ python3 install/OSX/install.py
``` 
On MacOs, you need to install istats by yourself before trying to use BatteryProbe.
This can be done with that command: 
``` 
$ gem install iStats
``` 
Sudo rights can be needed.

#### Logs
Client logs are located in `logs/` for the client program
Daemon logs are located in `install/OSX/` for the daemon logs.

### Linux
On Linux, launch the bash script `install/UNIX/install.sh`

```
$ bash install/UNIX/install.sh
```

Sudo rights could be needed.

The script will create a directory in `/opt/batteryprobe` and add the file 
`install/UNIX/batteryprobe` to your `/etc/init.d`

If the install is successful, start the daemon:
```
$ systemctl start batteryprobe.service
```

To stop the daemon, use 
```
$ systemctl stop batteryprobe.service
$ sudo kill $(cat /run/battery_probe.pid)
```

### Go further

If you want to go further, you can launch the client without launching the daemon

``` 
$ python3 client/client.py
``` 

Different options are available: 
``` 
Data scrapping frequency (in seconds), default: 10
--interval

Database uri, default: localhost:8086
--database_uri

(Required)
Specify the OS
--linux
--mac_os

Set debug mode
--debug
``` 








