### Scalable Computing - Project 3

Communicating between the RPis with socket programming and asynchronous sockets (TCP).

RPi 21 - rasp-021.berry.scss.tcd.ie 10.35.70.21 - We will be runnning Gateway Node and Rover Network 1

RPi 22 - rasp-022.berry.scss.tcd.ie 10.35.70.22 - We will be running Rover Network 2

Clone the git on RPis. 

Run the following commands on RPi 21 in the following order :

- Start the Gateway Node - 

```
python3 gateway.py
```
  
- Give Permission to Shell script - 

```
chmod +x network1.sh
```

- Start the Rover Network 1 - 

```
./network1.sh
```

Similarly, run following commands on RPi 22 in the following order :

- Give Permission to Shell script - 

```
chmod +x network2.sh
```

- Start the Rover Network 2 - 

```
./network2.sh
```
