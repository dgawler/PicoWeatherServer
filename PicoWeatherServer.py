#!/usr/bin/python3
#
# Weather server to read data from a Raspberry Pi Pico. This will be stored in a text
# file for processing.
#
# File format is the same as for the external temperature Pi:
# mm/dd/yy,hh:mm,humidity,temperature
#
# Dean Gawler, March 2023
#
# August 2023   :   Added syslogging capability for the server
#
#

import socket
import sys
import syslog
from ConvertToAdelaideTZ import ConvertPicoDate
from PicoWeatherFile import SaveWeatherData


def ProcessPicoWeatherData(pico_data):
    # The Pico weather data is in the format -> mm/dd/yy,hh:mm,humidity,temperature
    # but the date and time is in UTC time, as the Pico does not have timezone info.
    #
    # So will separate the date and time from the weahter data, and convert the date
    # and time to local Adelaide time.
    #
    date, time, humidity, temperature = pico_data.split(',')

    ### Converts from UTC to Adelaide
    converted_datetime = ConvertPicoDate(str(date + " " + time))
    date, time = converted_datetime.split(" ")
    pico_weather_data = date + "," + time + "," + humidity + "," + temperature

    # Store the data in the Pico weather file. This will roll the file over when it
    # is a new day.
    #
    SaveWeatherData(pico_weather_data)
    return


def server_program(program_args):
    bytes_read = 0
    host, port = program_args[1], int(program_args[2])

    # Open the socket and keep receiving data from the client until the
    # keyboard interrupts us...
    #
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            server_socket.bind((host, port))  # bind host address and port together
            server_socket.listen(3) # how many clients can the server listen to concurrently
            print(f"Server listening on {host}:{port}...")
            syslog.syslog(syslog.LOG_INFO,f"Server listening on {host}:{port}...")

            while True:
                # Wait for an incoming client connection to arrive
                conn, address = server_socket.accept()  # accept new connection
                syslog.syslog(syslog.LOG_INFO,f"Received connection from {address}")

                # Receive data stream up to 1024 bytes. This is a blocking call so the
                # program hangs at this point until it receives data from the client.
                #
                data = conn.recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                bytes_read += len(data)

                # Send the data back to the client to prove we got it
                conn.sendall(data.encode())  # send data to the client
                conn.close()  # close the connection

                # Process the Pico weather data and store in a file
                ProcessPicoWeatherData(data)
        except KeyboardInterrupt:
                print("\nServer quitting now...")
                print(f"Read a total of {bytes_read} bytes from clients")
                syslog.syslog(syslog.LOG_INFO,f"Server quitting now...")
                syslog.syslog(syslog.LOG_INFO,f"Read a total of {bytes_read} bytes from clients")
        finally:
            server_socket.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    server_program(sys.argv)
