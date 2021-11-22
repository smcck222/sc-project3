# SERVER SIDE SCRIPT TO HANDLE MULTIPLE CLIENTS.

import asyncio
import socket 

async def handle_client(address, loop):
    # Initial socket setup
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                                                                             
    sock.bind(address) 
    sock.listen()           
    print('Server listening')
    sock.setblocking(False)                              # Setting to non blocking sockets 

    while True:                                                                     
        try:
            client,addr = await loop.sock_accept(sock)   # Accepting connections from clients
            print('Connection from',addr)
            
            loop.create_task(handle_client_data(client,loop,addr))
        except socket.error as err:
             print('ERROR:  %s'%(err))

async def handle_client_data(client, loop, addr):
    while True: 
        try:
            
            msg = await loop.sock_recv(client,4096)      # Receiving data from clients
            
            data = msg

            if not data:				                 # If no data message is recieved
                break
            else: 
                print('Data recevied from ', addr) 
                print(data) 

        except socket.error as err:
             print('ERROR:  %s'%(err))                   # Includes accidental disconnect of client 
             break      
        
    print('Connection closed',addr)                      # Includes no data recieved, parse error and keyboard interrupt as well
    client.close() 
    

if __name__ == '__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(handle_client(('',33000),loop))
    loop.close()








    




















