### Scalable Computing - Project 3

Communicating between the RPis with socket programming and asynchronous sockets (TCP).

RPi 21 - rasp-021.berry.scss.tcd.ie 10.35.70.21 - server1 + rover 1-1 + rover 2-1

RPi 22 - rasp-022.berry.scss.tcd.ie 10.35.70.22 - server2 + rover 1-2 + rover 2-2

exec.sh - bash script that runs multiple rovers.

Clone the repo in both RPis. 

Run the following (in this order): 

Starting the gateway and the servers: 

RPi 21 : 

`python3 gateway.py`

`python3 server1.py`

RPi 22: 

`python3 server2.py`

Staring the rovers: 

RPi 21: 

`python3 rover1-1.py`

`python3 rover2-1.py`

`python3 rover3-1.py`

`python3 rover4-1.py`

RPi 22: 

`python3 rover1-2.py`

`python3 rover2-2.py`

`python3 rover3-2.py`

`python3 rover4-2.py`


Alternatively, run the bash files: 

RPi 21: 

`chmod +x exec1.sh`

`./exec1.sh`

RPi 22: 

`chmod +x exec2.sh`

`./exec2.sh`
