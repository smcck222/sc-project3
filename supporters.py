#!/usr/bin/env python
# coding: utf-8

# In[2]:

import json
import random
import math

class info_Manager:
    client_info = []                # List of slave rovers.
    rover_info = {}                 # ip: [x,y]
    
    def __init__():
        pass
    
    def update_client_info(client,port,rover):
        temp = (client,port,rover)
        if client not in info_Manager.client_info: 
            info_Manager.client_info.append(temp)
        
    # Updates rover_info dict, with ip, location_x, location_y.
    def update_rover_info(addr,data):
        info_Manager.rover_info[data['rover']] = [data['location_x'], data['location_y'], addr[1]]  # rover_no:[x,y, portno]
        # Adds new + replaces old. 
   
    def broadcast(server_port):
        for i in range(0,len(info_Manager.client_info)):
            msg = {'type':'new_port','port': server_port}
            info_Manager.client_info[i][0].send(json.dumps(msg).encode('utf-8'))

    def find_rover_port(rover_index):
        for i in range(0,len(info_Manager.client_info)):
            if info_Manager.client_info[i][2] == rover_index:
                return info_Manager.client_info[i][1]
            
    def clear_all_info():
        info_Manager.client_info.clear()
        info_Manager.rover_info.clear()
        
    def get_client_info():
        return info_Manager.client_info
    
    def get_rover_info():
        return info_Manager.rover_info


class task_Generator:
    
    def generate_simple_task(task, server_port):
        Task = {'type':task,'port':server_port}
        Task = json.dumps(Task).encode('utf-8')
        return Task

    # Generates move task - for healthy rover.
    def generate_move_task(location_x,location_y):
    
        task_distance = random.uniform(50,100) # The distance that the rover is going to move.
        task_direction = random.uniform(0,360) * math.pi / 180 # The direction that the rover is going to move.
        task_location_x = location_x + math.cos(task_direction)*task_distance # Calculate Task Coordinate.
        task_location_y = location_y + math.sin(task_direction)*task_distance # Calculate Task Coordinate.

        task = {'type': 'move+collect','task_location_x': task_location_x,'task_location_y': task_location_y}
        task = json.dumps(task).encode('utf-8')
        return task



