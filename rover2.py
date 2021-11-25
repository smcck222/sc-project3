# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

from json import decoder
import socket 
import sys
import math
from time import sleep
import datetime
import time
import struct
import random
import json
import threading
import rover_sensors

overheating_rate = 0.5 # 0.5 degree / seconds when doing task
decreasing_rate = 5 # 5 degree / seconds when sleeping
status = 1  #Activate:1, Sleep:0, Leader:3
temperature = 40
rover_speed = 10 
location_x = random.uniform(0,500)
location_y = random.uniform(0,500)

initial_time = time.time()
server_port = 8888             # localhost
server_ip = '127.0.0.1'        # localhost
#server_ip = '10.35.70.21'     # rpi
#server_port = 33000           # rpi

def do_task(task):
    global rover_speed, location_x, location_y, temperature, overheating_rate, status
    
    if task['type'] == 'move+collect':
        target_x = task['task_location_x']
        target_y = task['task_location_y']

        # Finding distance to dest location + time taken to get there. 
        dist_x = target_x - location_x
        dist_y = target_y - location_y
        total_dist = math.sqrt(math.pow(dist_x,2)+math.pow(dist_y,2))
        task_require_time = total_dist/rover_speed
        msg = "ROVER2: Heading to Location (" + str(target_x) + ", " + str(target_y) + "), ETA: " + str(task_require_time) + " seconds"
        print(msg)
        
        # Increasing temp of rover as it moves, include after sensor data if that counts in task_require_time.
        temperature = temperature + overheating_rate * task_require_time
        if temperature > 90:    # Overheat threshold.
            temperature = 91
            status = 0

        # Simulating the rover moving.
        sleep(task_require_time)

        # Collecting sensor data on the way to the location/ a fixed number of sensor data values at the location?
        # Should we include this to task_require_time/ does the rover heat up during this part?
        s = rover_sensors.rover_sensors()
        for i in range(10):
            sensor_data = s.generate_sensor_data()
            print(sensor_data)
        
        location_x = target_x
        location_y = target_y
        print("ROVER2: Task Completed!")
    
def start():
   
    task = init()
    global status, temperature, decreasing_rate
    while True:
        if status == 1:         # healthy rover, and is not the leader.
            if task == None:
                task = init()
            else:
                do_task(task)
                task = init()
        elif status == 0:       # Rover is overheated and needs to be put to sleep.
            task_require_time = ((temperature-40)//decreasing_rate)    # Time to cool down = (diff in temp/cooling rate)/2
            print("ROVER 2: Coolinig down for: " + str(task_require_time ) + "seconds")
            sleep(task_require_time)
            temperature = 40  #reset temp.
            status = 1       
            task = None   

def init():
    global location_x, location_y, temperature
    health_report = {'rover': 2,
                     'type': 'health_report',
                     'temperature': temperature, 
                     'location_x': location_x, 
                     'location_y': location_y}
    try:
        task_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 	# Socket creation. 
        print('Socket Creation successful')
        task_socket.connect((server_ip,server_port))  					# Connecting to server/ leader rover.
        task_socket.send(json.dumps(health_report).encode('utf-8'))
        print("ROVER 2: successfully sent health data")
        sleep(1)
        msg=task_socket.recv(1024)     # Waiting for task from server/leader rover.
        task = msg.decode('utf-8')
        task = json.loads(task)
        print(task)
        print("ROVER2: successfully recieved task")
        task_socket.close()
        return task

    except socket.error as err: 
        print('Socket creation failed with %s '%(err))
    

if __name__ == '__main__':
    start()