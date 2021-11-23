# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

import socket 
import sys
import math
from time import sleep
import datetime
import time
import struct

accelerate_rate = 10
dist_mars_to_sun = 227940000 #kilometers
dist_satellite_mars = 3400 #kilometers
satellite_angle_speed = 0.002555 #kilometer/second
mars_angle_speed = 0.000000105860934  #kilometer/second angle_
initial_time = time.time()


def get_Location():
    time_passed = (time.time() - initial_time)*accelerate_rate
    mars_location_x = dist_mars_to_sun * math.sin(mars_angle_speed * time_passed)
    mars_location_y = dist_mars_to_sun * math.cos(mars_angle_speed * time_passed)
    satellite_location_x = dist_satellite_mars * math.sin(satellite_angle_speed * time_passed) + mars_location_x
    satellite_location_y = dist_satellite_mars * math.cos(satellite_angle_speed * time_passed) + mars_location_y
    coordinate = [satellite_location_x,satellite_location_y,mars_location_x,mars_location_y]
    coordinate = struct.pack('<4f',*coordinate)
    return coordinate

try:
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 	# Socket creation. 
	print('Socket Creation successful')

except socket.error as err: 
	print('Socket creation failed with %s '%(err))

server_port = 33000
server_ip = '127.0.1'   					 # Server ip and portno. 

s.connect((server_ip,server_port))  					# Connecting to server

while True:
    try:
        coordinate = get_Location()
        print(coordinate)
        s.send(coordinate)
        #s.send(msg.replace('tstmp',time_now()).encode('utf-8'))						# Sending message to server, infinite loop. 
        sleep(5)																	# Simulates delay in sending messages.

    except socket.error as err: 													# Catches errors encoutered while sending. 
        print('ERROR: '+ str(err))
        break

s.close()
