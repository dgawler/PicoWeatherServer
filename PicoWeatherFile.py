#!/usr/bin/python
#
# Takes a string of weather data that has been received from a weather client 
# and writes it to our data file.
#
# Author : Dean Gawler, 2014
# Changes: 2020-01-16 Updated for AM2302 sensor
#          2020-11-07 Tidy up code, increase delta in next reading
#          2023-03-22 Changed for the Pico and the BME280 sensor
#
#

__author__ = 'Dean Gawler'

## import subprocess
import time
import os

# Are we in DEBUG mode
DEBUG=1
DEBUG=0

# Need to know if this temp and humidity read is the first for today. Assume no for now.
BASEDIR='/weather/temps/'

def SaveWeatherData(data):
    # Get the current date and time
    localtime = time.localtime(time.time())
    YYYY=localtime[0]
    MON='%02d' % localtime[1]
    DAY='%02d' % localtime[2]
    TDATE=str(MON) + '/' + str(DAY) + '/' + str(YYYY-2000)
    
    # Construct the file name that we will use for logging
    TEMPFILE=BASEDIR + str(YYYY) + '-' + str(MON) + '-' + str(DAY) + "-pico.temps"
    
    # Start by checking for the existence of the file. If it does not exist, then
    # create it, then create the symlink to it.
    #
    if not os.path.exists(TEMPFILE):
        try:
            f = open(TEMPFILE, 'w')
            f.close()
        except:
            print(f"Cannot create temperature file: {TEMPFILE}")

    # Write data string to file
    #
    if DEBUG:
        print(f"Writing Pico weather date {data} to {TEMPFILE}")
    
    try:
	    output = open(TEMPFILE,'a')
	    output.write(data)
	    output.write('\n')
	    output.close()
    except:
        print(f"Cannot write temperature data >>{data} to file: {TEMPFILE}")

