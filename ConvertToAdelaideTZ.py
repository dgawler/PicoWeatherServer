#!/usr/bin/python3
#
# Python program to convert the UTC time that the Raspberry Pi Pico will have
# obtained from the network into Australia/Adelaide timezone. I cannot find an
# easier way to get localtime on the Pico correct, as there does not seem to be
# an available timezone module for MicroPython on the Pico as yet.
#
# This is ugly, but works. Does not take into account daylight savings time, but
# you could hack this if needed. I will wait for someone to provide a decent, 
# easy to use timezone module for MicroPython on the Pico.
#
# Dean Gawler
# August 2023
#

from datetime import datetime, timedelta

def ConvertPicoDate(pico_datetime):
	# First step is to convert the datetime string into proper datetime format
	#
	pico_converted_datetime = datetime.strptime(pico_datetime, '%m/%d/%y %H:%M')

	# Forget daylight savings and just assume Adelaide is 9.5 in front of UTC
	#
	pico_localtime = str(pico_converted_datetime + timedelta(hours = 9.5))
	
	# Now convert proper datetime back into strings, and manipulate as needed
	# Will be in a format of -> 2023-03-22 18:04:00+10:30
	#
	conv_month=pico_localtime[5:7]
	conv_day=pico_localtime[8:10]
	conv_year=pico_localtime[2:4]

	converted_date=conv_month + "/" + conv_day + "/" + conv_year
	converted_time=pico_localtime[11:16]
	
	converted_datetime=converted_date + " " + converted_time
	#### print("Converted date: >>", converted_date)
	#### print("Converted time: >>", converted_time)
	#### print(f"Converted date time: >>{converted_datetime}<<")

    # Return to the calling routine (string)
	return converted_datetime
