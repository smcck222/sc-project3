# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

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

Overheating_rate = 0.5 # 0.5 degree / seconds when doing task
Decreasing_Rate = 5 # 5 degree / seconds when sleeping
Status = 1  #Activate:1,Sleep:0, Leader:3
Temperature = 40
Rover_Speed = 10 
Location_x = random.uniform(0,500)
Location_y = random.uniform(0,500)
initial_time = time.time()

server_port = 3040
server_ip = '127.0.1'


def listen_to_Broadcast():
    try:
        Broadcast_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 	# Socket creation. 
        print('Broadcast_Socket Creation successful')
        Broadcast_socket.connect((server_ip,server_port))  					# Connecting to server
        addr = Broadcast_socket.getsockname()
        addr_report = {'Type':'addr_report','IP':addr[0],'Port':addr[1]}
        Broadcast_socket.send(json.dumps(addr_report).encode('utf-8'))
        while True:
            Broadcast_socket.recv(1024)
            print("Receive Broadcast")
        
    except socket.error as err: 
        print('Socket creation failed with %s '%(err))
    
def doTask(task):
    global Rover_Speed, Location_x, Location_y, Temperature, Overheating_rate, Status
    task_type = task['Type']
    if task_type == 'Task':
        target_x = task['Task_Location_x']
        target_y = task['Task_Location_y']
        dist_x = target_x - Location_x
        dist_y = target_y - Location_y
        total_dist = math.sqrt(math.pow(dist_x,2)+math.pow(dist_y,2))
        task_require_time = total_dist/Rover_Speed
        msg = "Heading to Location (" + str(target_x) + ", " + str(target_y) + "), require " + str(task_require_time) + " seconds"
        print(msg)
        
        sleep(task_require_time)
        Temperature = Temperature + Overheating_rate * task_require_time
        if Temperature > 90:
            Temperature = 91
  
        Location_x = target_x
        Location_y = target_y
        print("Task completed!")
    
def start():
    try:
        thread_1 = threading.Thread(target=listen_to_Broadcast)
        thread_1.start()
    except:
        print ("Error: Thread Error")
        
    Task = init()
    global Status
    while True:
        if Status == 1: #Runs normally, and is not the leader
            if Task == None:
                Task = init()
            else:
                doTask(Task)
                Task = init()
        elif Status == 0:
            time_counter = time.time()
            global Temperature, Decreasing_Rate
            Temperature = 40
            Status = 1
            
def init():
    global Location_x, Location_y, Temperature
    health_report = {'Type': 'Health_Report',
                     'Temperature': Temperature, 
                     'Location_x': Location_x, 
                     'Location_y': Location_y}
    try:
        Task_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 	# Socket creation. 
        print('Socket Creation successful')
        Task_socket.connect((server_ip,server_port))  					# Connecting to server
        Task_socket.send(json.dumps(health_report).encode('utf-8'))
        print("Successfully send health data")
        sleep(1)
        msg=Task_socket.recv(1024)
        task = msg.decode('utf-8')
        task = json.loads(task)
        print(task)
        print("Successfully get Task")
        return task

    except socket.error as err: 
        print('Socket creation failed with %s '%(err))
    
    
if __name__ == '__main__':
    start()