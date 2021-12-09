#!/bin/sh
python3 leader_rover.py --port 33000 --network_index 2 --rover_index 1&
sleep 1
python3 node_rover.py --port 34000 --network_index 2 --rover_index 2 > network2_rover2.log&
python3 node_rover.py --port 33001 --network_index 2 --rover_index 3 > network2_rover3.log&
python3 node_rover.py --port 33002 --network_index 2 --rover_index 4 > network2_rover4.log&
python3 node_rover.py --port 33003 --network_index 2 --rover_index 5 > network2_rover5.log&