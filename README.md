# BatteryProbe.collect

## Server

### Usage
To build and run the influxdb and grafana containers, use:
```
$ docker-compose -f server/docker-compose.yml up --build -d
```

## Client

### Daemon

To start the daemon, simply launch the program "client.py"

Example:
``` 
$ python3 client/client.py --mac_os 
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

#### Logs
Client logs are located in "logs/error_logs.txt"




