# SERVER SIDE SCRIPT TO HANDLE MULTIPLE CLIENTS.

import asyncio
import socket
import json
import random
import math
import threading
import security

clients_info_lock = threading.Lock()
client_info = []              # List of slave rovers.
rover_info = {}                 # ip: [x,y]
WAIT_TIME_SECONDS = 10
gateway_address = ('10.35.70.21',33333)
#gateway_address = ('127.0.0.1', 9999)

gateway_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Updates client_info list.
def update_client_info(client):
    global clients_info_lock
    global client_info
    if client not in client_info: 
        with clients_info_lock:
            client_info.append(client)
               

# Updates rover_info dict, with ip, location_x, location_y.
def update_rover_info(addr,data):
    global rover_info
    
    rover_info[str(data['rover']) + '10.35.70.21'] = [data['location_x'], data['location_y'], addr[1]]  # rover_no:[x,y, portno]
    # Adds new + replaces old. 

# Generates sleep task - for overheated rover.
def generate_sleep_task():
    
    task = {'type':'sleep'}
    task = json.dumps(task).encode('utf-8')
    return task

# Generates move task - for healthy rover.
def generate_move_task(location_x,location_y):
    
    task_distance = random.uniform(50,100) # The distance that the rover is going to move. 
    task_direction = random.uniform(0,360) * math.pi / 180 # The direction that the rover is going to move.
    task_location_x = location_x + math.cos(task_direction)*task_distance # Calculate Task Coordinate.
    task_location_y = location_y + math.sin(task_direction)*task_distance # Calculate Task Coordinate.
    
    task = {'type': 'move+collect','task_location_x': task_location_x,'task_location_y': task_location_y}
    task = json.dumps(task).encode('utf-8')
    return task

# if the temperature of the rover is greater than 90, send "sleep" task.
# else send "move+collect" task.
def check_rover_temperature(temperature):
    overheat_threshold = 90
    if temperature >= overheat_threshold:
        return 0
    else:
        return 1

async def send_mesg_at_timeout(timeout, func):
    while True:
        await asyncio.sleep(timeout)
        await func()

async def start_stream():
    global gateway_socket
    global rover_info
    try:
        if bool(rover_info):
            public_key = security.read_public_key()
            msg = json.dumps(rover_info).encode('utf-8')
            encrypted_msg = security.encrypt_data(msg, public_key)
            gateway_socket.sendall(encrypted_msg)  

    except Exception as e:
        print(e)
        pass

def connectToGateway(address):
    global gateway_socket
    socket_address = address
    gateway_socket.connect(socket_address)
    gateway_socket.setblocking(False)

# This function is used for receiving the data from gateway and send it to all other rovers.
async def receiveGatewayData(loop):
    global client_info
    global gateway_socket
    while True:
        try:
            msg = await loop.sock_recv(gateway_socket,4096)
            print('Data Received from Gateway')
            #data = msg.decode('utf-8')
            #data = json.loads(data)

            private_key = security.read_private_key()
            decrypted_msg = security.decrypt_data(msg, private_key).decode('utf-8')
            print("DATA FROM GATEWAY: ", json.loads(decrypted_msg))


            #if not msg:
            #    break
            #else:
            #    if client_info:
            #        for client in client_info:
            #            task = {'type':'UpdateMessageFromNetwork1'}
            #            print('Sending data to rover ',client)
            #    else:
            #        break
        except Exception as e:
            print(e)
            pass

async def handle_client(address, loop):
    # Initial socket setup
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    sock.bind(address) 
    sock.listen(6)           
    print('Server listening')
    sock.setblocking(False)                              # Setting to non blocking sockets
    connectToGateway(gateway_address)

    loop.create_task(send_mesg_at_timeout(WAIT_TIME_SECONDS, start_stream))
    loop.create_task(receiveGatewayData(loop))
    while True:                                                                     
        try:
            client,addr = await loop.sock_accept(sock)   # Accepting connections from clients
            print('Connection from',addr)
            update_client_info(client)
            loop.create_task(handle_client_data(client,loop,addr))
        
        except socket.error as err:
             print('ERROR:  %s'%(err))

async def handle_client_data(client, loop, addr):
    global rover_info
    while True: 
        try:
            
            msg = await loop.sock_recv(client,4096)      # Receiving data from clients
            data = msg
            
            if not data:				                 # If no data message is recieved
                break
            else: 
                data = data.decode('utf-8')
                data = json.loads(data)
                update_rover_info(addr, data) # - is this useful because the port number keeps changing?
                # print(rover_info)
                print('Data recevied from ', addr)
                print(data)
                #print(addr[0] + str(addr[1]))
                info_type = data['type']
                if info_type == 'health_report':
                    update_rover_info(addr,data)
                    if check_rover_temperature(data['temperature']) == 1:   # If temp is below overheat.
                        client.send(generate_move_task(data['location_x'],data['location_y'])) # Send move+collect task to rover.
                    else:
                        client.send(generate_sleep_task())  # If temp above overheat, send sleep task to rover.
                        
                        # --SEND TASK TO ANOTHER ROVER THAT IS FREE--

                elif info_type == 'addr_report': # Will this happen once in the beginning, doesn't the rover have to send health_report too?
                    update_client_info(client)
                    print("Added rover to client_info")
                        
        except socket.error as err:
             print('ERROR:  %s'%(err))                   # Includes accidental disconnect of client 
             break      
        
    print('Connection closed',addr)                      # Includes no data recieved, parse error and keyboard interrupt as well
    client.close() 


if __name__ == '__main__':
    
    loop=asyncio.get_event_loop()
    security.create_keys()
    loop.run_until_complete(handle_client(('127.0.0.1',8888),loop))
    #loop.run_until_complete(handle_client(('10.35.70.21',33000),loop)) 

    #ip and port no. RPI: 10.35.70.21, 10.35.70.22 , 33000
    loop.close()



















