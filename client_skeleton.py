# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

import socket 
import sys
from time import sleep
import datetime 

def time_now():							# To insert timestamp into data.

	now = datetime.datetime.now()	
	return (now.strftime("%Y%m%d%H%M%S"))

msg = "Hello World from Sensor 1" + " tstmp"

try:
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 	# Socket creation. 
	print('Socket Creation successful')

except socket.error as err: 
	print('Socket creation failed with %s '%(err))

#server_port = 33000
#server_ip = '10.35.70.21'   							# Server ip and portno (rpi). 
server_ip = '127.0.0.1' 								# Server ip, localhost.
server_port = 8888										# Server portno, localhost. 

s.connect((server_ip,server_port))  					# Connecting to server

while True:			
	try: 
		s.send(msg.replace('tstmp',time_now()).encode('utf-8'))						# Sending message to server, infinite loop. 
		sleep(1)																	# Simulates delay in sending messages.
	
	except socket.error as err: 													# Catches errors encoutered while sending. 
		print('ERROR: '+ str(err))
		break

s.close()												
