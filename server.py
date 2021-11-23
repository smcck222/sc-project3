# SERVER SIDE SCRIPT TO HANDLE MULTIPLE CLIENTS.

import asyncio
import socket
import struct
import numpy as np
import pandas as pd

satellites_info = pd.DataFrame()

def update_location(data,addr):
    
    global satellites_info
    
    columns = ['satellite_x','satellite_y','planet_x','planet_y']
                
    if satellites_info.shape[0] == 0:
        temp = {'IP':addr[0],'satellite_x':data[0],'satellite_y':data[1],'planet_x':data[2],'planet_y':data[3]}
        satellites_info = satellites_info.append(temp,ignore_index=True)
    else:
        flag = 1
        for i in range(0,satellites_info.shape[0]):
            if satellites_info.loc[i,'IP'] == addr[0]:
                flag = 0
                counter = 0
                for str in columns:
                    satellites_info.loc[i,str] = data[counter]
                    counter = counter + 1
                #satellites_info.loc[i,'satellite_x'] = data[0]
                #satellites_info.loc[i,'satellite_y'] = data[1]
                #satellites_info.loc[i,'planet_x'] = data[2]
                #satellites_info.loc[i,'planet_y'] = data[3]
                break
                
        if flag == 1:
            temp = {'IP':addr[0],'satellite_x':data[0],'satellite_y':data[1],'planet_x':data[2],'planet_y':data[3]}
            satellites_info = satellites_info.append(temp,ignore_index=True)

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
            
            data = struct.unpack('<4f',msg)
            
            if not data:				                 # If no data message is recieved
                break
            else: 
                print('Data recevied from ', addr)
                update_location(data,addr)
                print(satellites_info)
        except socket.error as err:
             print('ERROR:  %s'%(err))                   # Includes accidental disconnect of client 
             break      
        
    print('Connection closed',addr)                      # Includes no data recieved, parse error and keyboard interrupt as well
    client.close() 
    

if __name__ == '__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(handle_client(('127.0.1',33000),loop))
    loop.close()








    




















