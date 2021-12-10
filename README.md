### Scalable Computing - Project 3

Communicating between the RPis with socket programming and asynchronous sockets (TCP).

RPi 21 - rasp-021.berry.scss.tcd.ie 10.35.70.21 - We will be runnning Gateway Node and Rover Network 1

RPi 22 - rasp-022.berry.scss.tcd.ie 10.35.70.22 - We will be Rover Network 2

Clone the git repo in both RPis. 

Run the following commands on RPi 21 in the following order :
<ol>
  <li>Start the Gateway Node - <b> `python3 gateway.py` </b></li>
  <li>Give Permission to Shell script- <b> `chmod +x network1.sh` </b></li>
  <li>Start the Rover Network 1 - <b> `./network1.sh` </b></li>
</ol>

Similarly, run following commands on RPi 22 in the following order :
<ol>
  <li>Give Permission to Shell script- <b> `chmod +x network2.sh` </b></li>
  <li>Start the Rover Network 2 - <b> `./network2.sh` </b></li>
</ol>
