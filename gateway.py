import socket
import threading
import asyncio
import json
# Time interval
WAIT_TIME_SECONDS = 10
# List of leder rovers in each network
clients = []
# mutex to control access to shared list
clients_lock = threading.Lock()


# This will intialize the gateway and start receiving client request
async def start_server(loop):
    global clients
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print('HOST IP: ',ip)
    #port = 9999
    #socket_address = ('10.35.70.21',33333)
    socket_address = ('127.0.0.1', 9999)
    server_socket.bind(socket_address)
    server_socket.listen()
    server_socket.setblocking(False)
    print('Listening at ',socket_address)
    # Uncomment following line of code if you want to send certain event/messages after time interval.
    #task = loop.create_task(send_mesg_at_timeout(WAIT_TIME_SECONDS, start_stream))
    while True:
        client_socket ,addr = await loop.sock_accept(server_socket)
        print('Client connected',addr)
        with clients_lock:
            clients.append(client_socket)
        loop.create_task(handle_client_data(client_socket,loop,addr))


# Timer function which will send the messages at regular interval
# This method can be resued accorss rover leaders.
async def send_mesg_at_timeout(timeout, func):
    while True:
        await asyncio.sleep(timeout)
        await func()


# Method to receive a data from one network and broadcast to all other networks
async def handle_client_data(client, loop, addr):
    global clients
    while True: 
        try:
            msg = await loop.sock_recv(client,4096)
            #data = msg.decode('utf-8')
            #data = json.loads(data)
            #print(data) # Receiving data from clients
            print(msg)
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
             print('ERROR:  %s'%(err))                   # Includes accidental disconnect of client 
             break 

# This method can be used to send any data currently its sending just a string
# TO DO - Add paramter in this method representing a data object which can be broadcasted
async def start_stream():
    global numbers
    global clients
    # print("accepted connection from client",addr)
    try:
        if clients:
            for client in clients:
                data = "Hi client"
                client.sendall(data.encode('utf-8'))  
    except Exception as e:
        print(e)
        pass
       

if __name__ == '__main__':
    # asyncio.run(start_server())
    loop=asyncio.get_event_loop()
    loop.run_until_complete(start_server(loop))
    loop.close()
