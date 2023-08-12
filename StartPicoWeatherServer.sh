#!/bin/bash
##
## Shell script to start PicoWeatherServer.py as a daemon that listens for
## connections from a client (typically a Raspberry Pi Pico W) that has a BME280
## weather sensor and is running the PicoWeather app. The Pico will be sending 
## data every 10 minutes to PicoWeatherServer.py running on the server.
#

LOG=/tmp/PicoWeatherServer.log
ps_name="PicoWeatherServer.py"
PicoScript=/weather/pico_weather/PicoWeatherServer.py
host=192.168.1.33
port=5000

# Kill any script currently running
pico=$(ps -ef | grep "$ps_name" | grep -v grep)
if [[ "$pico" != "" ]]; then
    pico_pid=$(echo $pico | cut -f1)
    if [[ "$pico_pid" != "" ]]; then
        kill $pico_pid && sleep 2 && kill -1 $pico_pid && sleep 2 && kill -9 $pico_pid
    fi
fi

# Start the weather server
nohup $PicoScript $host $port > $LOG 2>&1 &
