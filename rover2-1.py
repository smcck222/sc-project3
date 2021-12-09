# CLIENT SIMULATION/SENSOR SENDING DATA TO MONITOR.

import asyncio
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
import security
from supporters import info_Manager as im
from supporters import task_Generator as tg

status = 3  # Activate:1, Sleep:0, Leader:3
flag = 0
temperature = 40
rover_index = 1

location_x = random.uniform(0, 500)
location_y = random.uniform(0, 500)

infoManager = im
taskGenerator = tg

threads = []

initial_time = time.time()
# server_port = 3030          # localhost
server_ip = '10.35.70.22'        # localhost
# server_ip = '127.0.0.2'  # rpi
server_port = 33000  # rpi
server_addr = (server_ip, server_port)
# clients_info_lock = threading.Lock()
gateway_address = ('10.35.70.21',33333)
gateway_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
WAIT_TIME_SECONDS = 10
gatewayClosed = False
own_server_port = 33000


# if the temperature of the rover is greater than 90, send "sleep" task.
# else send "move+collect" task.
def check_rover_temperature(temperature):
    overheat_threshold = 90
    if temperature >= overheat_threshold:
        return 0
    else:
        return 1


# listen to broadcast information from the server
def listen_to_Broadcast():
    global status, server_port, server_ip, server_addr, own_server_port, rover_index
    try:
        Broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket creation.
        Broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # print('Broadcast_Socket Creation successful')
        Broadcast_socket.connect(server_addr)  # Connecting to server
        addr_report = {'type': 'addr_report', 'Port': own_server_port, 'rover': rover_index}
        Broadcast_socket.send(json.dumps(addr_report).encode('utf-8'))
        while True:
            msg = Broadcast_socket.recv(1024)
            task = msg.decode('utf-8')
            task = json.loads(task)
            if task['type'] == 'new_port':
                server_port = task['port']
                server_addr = (server_ip, server_port)
                print("Receive Broadcast, new port", task['port'])
                Broadcast_socket.close()
                threads.clear()
                break
    except socket.error as err:
        print('Broadcast Socket creation failed with %s ' % (err))


def do_task(task):
    global location_x, location_y, temperature, status, server_ip, server_port, server_addr, own_server_port, rover_index

    overheating_rate = 0.5
    rover_speed = 15

    if task['type'] == 'move+collect':
        target_x = task['task_location_x']
        target_y = task['task_location_y']

        # Finding distance to dest location + time taken to get there.
        dist_x = target_x - location_x
        dist_y = target_y - location_y
        total_dist = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_y, 2))
        task_require_time = total_dist / rover_speed
        msg = "N" + str(rover_index) + " ROVER " + str(rover_index) + ": Heading to Location (" + str(
            target_x) + ", " + str(target_y) + "), ETA: " + str(task_require_time) + " seconds"
        print(msg)

        # Increasing temp of rover as it moves, include after sensor data if that counts in task_require_time.
        temperature = temperature + overheating_rate * task_require_time
        if temperature > 90:  # Overheat threshold.
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
        print("N" + str(rover_index) + " ROVER " + str(rover_index) + ": Task Completed!")

    elif task['type'] == 'exchange':
        status = 3
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket creation.
        temp_socket.connect((server_ip, server_port))  # Connecting to server/ leader rover.
        # print("server_addr",server_addr)
        task = {'type': 'test'}
        temp_socket.send(json.dumps(task).encode('utf-8'))
        temp_socket.close()
        server_port = own_server_port
        server_addr = (server_ip, server_port)


    elif task['type'] == 'redirect':
        server_port = task['port']
        server_addr = (server_ip, server_port)

    elif task['type'] == 'sleep':
        status = 0


def broadcast_controller():
    global status, threads
    while True:
        if len(threads) == 0 and status != 3:
            try:
                threads.append(threading.Thread(target=listen_to_Broadcast))
                threads[0].start()
            except threading.error as err:
                print("Error: Thread Error%s" % (err))
        else:
            sleep(1)


def relink():
    global server_ip, server_addr

    back_up = [33000, 34000, 33001, 33002, 33003]

    print('Re-link started')

    test_report = {'type': 're-link test'}

    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket creation.
    print('Test Socket Creation successful')

    for port in back_up:
        try:
            test_socket.connect((server_ip, port))  # Connecting to server/ leader rover.
            test_socket.send(json.dumps(test_report).encode('utf-8'))
            server_addr = (server_ip, port)
            print('relink successed, current server address: ', server_addr)
            test_socket.close()
            break
        except socket.error as err:
            print('Test Socket creation failed with %s ' % (err))


def start():
    global status, temperature, decreasing_rate, rover_index, flag

    decreasing_rate = 10

    thread_1 = threading.Thread(target=broadcast_controller)
    thread_1.start()

    loop = asyncio.get_event_loop()

    while True:
        if status == 1:  # healthy rover, and is not the leader.
            task = init()
            if task != None:
                do_task(task)

        elif status == 0:  # Rover is overheated and needs to be put to sleep.
            task_require_time = (
                        (temperature - 40) // decreasing_rate)  # Time to cool down = (diff in temp/cooling rate)/2
            print("N" + str(rover_index) + " ROVER " + str(rover_index) + ": Coolinig down for: " + str(
                task_require_time) + " seconds")
            sleep(task_require_time)
            temperature = 40  # reset temp.
            status = 1
            task = None

        elif status == 3:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            loop.run_until_complete(handle_client(server_addr, loop, server_sock))
            # ip and port no. RPI: 10.35.70.21, 10.35.70.22 , 33000
            server_sock.close()
            flag = 0
            print("Server Down")


def init():
    global location_x, location_y, temperature, rover_index
    health_report = {'rover': rover_index,
                     'type': 'health_report',
                     'temperature': temperature,
                     'location_x': location_x,
                     'location_y': location_y}
    try:
        task_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket creation.
        print('Socket Creation successful')
        task_socket.connect(server_addr)  # Connecting to server/ leader rover.
        task_socket.send(json.dumps(health_report).encode('utf-8'))
        print("N" + str(rover_index) + " ROVER " + str(rover_index) + ": successfully sent health data")
        sleep(1)
        msg = task_socket.recv(1024)  # Waiting for task from server/leader rover.
        task = msg.decode('utf-8')
        task = json.loads(task)
        print(task)
        print("N" + str(rover_index) + " ROVER " + str(rover_index) + ": successfully recieved task")
        task_socket.close()
        return task

    except socket.error as err:
        print('Task Socket creation failed with %s ' % (err))
        relink()


async def send_mesg_at_timeout(timeout, func):
    while True:
        await asyncio.sleep(timeout)
        await func()


async def start_stream():
    global gateway_socket
    global infoManager
    rover_info = infoManager.get_rover_info()
    try:
        if bool(rover_info) and status == 3:
            # gateway_socket.sendall(json.dumps(rover_info).encode('utf-8'))

            public_key = security.read_public_key()
            msg = json.dumps(rover_info).encode('utf-8')
            encrypted_msg = security.encrypt_data(msg, public_key)
            gateway_socket.sendall(encrypted_msg)

    except Exception as e:
        print("Exception occurred in start_stream")
        print(e)
        pass

    except socket.timeout as e:
        pass


def connectToGateway(address):
    global gateway_socket, gatewayClosed
    socket_address = address
    if gatewayClosed:
        gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gateway_socket.connect(socket_address)
    else:
        gateway_socket.connect(socket_address)
    gateway_socket.setblocking(False)


# This function is used for receiving the data from gateway and send it to all other rovers.
async def receiveGatewayData(loop):
    global status
    global client_info
    global gateway_socket
    if status == 3:
        while True:
            try:
                msg = await loop.sock_recv(gateway_socket, 4096)
                # data = msg.decode('utf-8')
                # data = json.loads(data)
                # print(data)
                private_key = security.read_private_key()
                decrypted_msg = security.decrypt_data(msg, private_key).decode('utf-8')
                print('====================Data Received from Gateway====================')
                print(decrypted_msg)
                if not msg:
                    break
                else:
                    if client_info:
                        for client in client_info:
                            task = {'type': 'UpdateMessageFromNetwork1'}
                            # print(json.loads(decrypted_msg))
                            # print('Sending data to rover')
                    else:
                        break
            except Exception as e:
                print("Error occurred in receiveGateWay")
                print(e)
                pass


async def handle_client(address, loop, sock):
    # Initial socket setup
    # sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # print("Server Address: ",address)

    sock.bind(address)
    sock.listen(10)
    print('Server listening', address)
    sock.setblocking(False)  # Setting to non blocking sockets
    connectToGateway(gateway_address)
    task1 = loop.create_task(send_mesg_at_timeout(WAIT_TIME_SECONDS, start_stream))
    task2 = loop.create_task(receiveGatewayData(loop))
    while status == 3:
        try:
            client, addr = await loop.sock_accept(sock)  # Accepting connections from clients
            print('Connection from', addr)

            # loop.create_task(handle_client_data(client,loop,addr,task1,task2))
            loop.create_task(handle_client_data(client, loop, addr, sock,task1,task2))

        except socket.error as err:
            print('ERROR:  %s' % (err))


async def handle_client_data(client, loop, addr, sock,task1,task2):
    # async def handle_client_data(client, loop, addr,task1,task2):
    # global infoManager, temperature, flag, status, server_port,server_addr,server_ip,gatewayClosed,gateway_socket
    global infoManager, taskGenerator, temperature, flag, status, server_port, server_addr, server_ip,gatewayClosed,gateway_socket
    server_temp_increasing_speed = 2
    while status == 3:
        try:
            msg = await loop.sock_recv(client, 4096)  # Receiving data from clients
            data = msg

            if not data:  # If no data message is recieved
                break
            else:
                data = data.decode('utf-8')
                data = json.loads(data)
                print('Data recevied from ', addr)
                print(data)
                info_type = data['type']
                if info_type == 'health_report':
                    infoManager.update_rover_info(addr, data)
                    # If rover is overheating, require it to sleep
                    if check_rover_temperature(data['temperature']) == 0:
                        client.send(taskGenerator.generate_simple_task('sleep', server_port))
                    # else if rover is healthy, send move+collect task, exchange task, or redirect task
                    elif check_rover_temperature(data['temperature']) == 1:
                        # if server is healthy, send move & collect task
                        if temperature < 80:
                            temperature = temperature + server_temp_increasing_speed
                            client.send(taskGenerator.generate_move_task(data['location_x'], data[
                                'location_y']))  # Send move+collect task to rover.
                        # else if server is overheating, send exchange and redirect task
                        else:
                            if flag == 0:
                                task1.cancel()
                                task2.cancel()
                                public_key = security.read_public_key()
                                msg = 'Closing'.encode('utf-8')
                                encrypted_msg = security.encrypt_data(msg, public_key)
                                gateway_socket.sendall(encrypted_msg)
                                gateway_socket.close()
                                gatewayClosed = True
                                server_port = infoManager.find_rover_port(data['rover'])
                                server_addr = (server_ip, server_port)
                                flag = 1
                                client.send(taskGenerator.generate_simple_task('exchange', server_port))
                                sleep(2)
                                status = 0
                                infoManager.broadcast(server_port)
                                infoManager.clear_all_info()
                            elif flag == 1:
                                client.send(taskGenerator.generate_simple_task('redirect', server_port))

                elif info_type == 'addr_report':
                    infoManager.update_client_info(client, data['Port'], data['rover'])
                    print("Added rover to client_info")

        except socket.error as err:
            print('ERROR:  %s' % (err))  # Includes accidental disconnect of client
            break

    print('Connection closed', addr)  # Includes no data recieved, parse error and keyboard interrupt as well
    client.close()


if __name__ == '__main__':
    start()
