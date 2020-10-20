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
On MacOs, you need to install istats by yourself before trying to use batteryProbe.
This can be done with that command: 
``` 
gem install iStats
``` 
A sudo can be needed.

### Linux
To complete

### Go forther

If you want to go further, you can launch the client without launching the daemon

``` 
python3 client/client.py
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
Client logs are located in "logs/" for the client program
Daemon logs are located in "install/(OSX/UNIX)/" for the daemon logs.







