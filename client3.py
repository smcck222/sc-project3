# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

import socket 
import sys
import math
from time import sleep
import datetime
import time
import struct

distance = 228 
Period_of_revolution = 16487 #687 * 24 hours.
angle_speed = 0.021835 * math.pi / 180  # 360 degree / period_of_revolution, then transimit it to arc
initial_time = time.time()

def get_Location():
    time_passed = time.time() - initial_time
    location_x = distance * math.sin(angle_speed * time_passed)
    location_y = distance * math.cos(angle_speed * time_passed)
    coordinate = [location_x,location_y]
    coordinate = struct.pack('<2f',*coordinate)
    return coordinate

def time_now():# To insert timestamp into data.

    now = datetime.datetime.now()	
    return (now.strftime("%Y%m%d%H%M%S"))

msg = "Hello World from Sensor 1" + " tstmp"

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
