import socket
import threading
import asyncio
import json
import security
from config import network_config

# Time interval
WAIT_TIME_SECONDS = network_config['WAIT_TIME_SECONDS']
# List of leder rovers in each network
clients = []
# mutex to control access to shared list
clients_lock = threading.Lock()


# This will intialize the gateway and start receiving client request
async def start_server(loop):
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print('HOST IP: ', ip)
    port = 9999
    socket_address = (network_config['gateway_ip'],network_config['gateway_port'])
    server_socket.bind(socket_address)
    server_socket.listen()
    server_socket.setblocking(False)
    print('Listening at ', socket_address)
    while True:
        client_socket, addr = await loop.sock_accept(server_socket)
        print('Client connected', addr)
        with clients_lock:
            clients.append(client_socket)
        loop.create_task(handle_client_data(client_socket, loop, addr))


# Timer function which will send the messages at regular interval
# This method can be resued accorss rover leaders.
async def send_mesg_at_timeout(timeout, func):
    while True:
        await asyncio.sleep(timeout)
        await func()


# Method to receive a data from one network and broadcast to all other networks
async def handle_client_data(client, loop, addr):
    global clients, clients_lock
    while True:
        try:
            msg = await loop.sock_recv(client, 4096)
            if len(msg) > 0:
                print('Received data from leader rover > ', addr)
                private_key = security.read_private_key()
                decrypted_msg = security.decrypt_data(msg, private_key).decode('utf-8')
                data = json.loads(decrypted_msg)
            # data = msg.decode('utf-8')
            # data = json.loads(data)
            # print(data) # Receiving data from clients
            if not msg:
                break
            else:
                if clients:
                    for c in clients:
                        if client != c:
                            print('sending data to clients')
                            c.sendall(msg)
                else:
                    break
        except socket.error as err:
            print('ERROR:  %s' % (err))  # Includes accidental disconnect of client
            break
        except ValueError as e:
            is_string = isinstance(decrypted_msg, str)
            if is_string and decrypted_msg == 'Closing':
                print('Leader rover ', addr, ' is sleeping')
                with clients_lock:
                    print('Updating the rover leader list')
                    clients.remove(client)


if __name__ == '__main__':
    # asyncio.run(start_server())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server(loop))
    loop.close()
