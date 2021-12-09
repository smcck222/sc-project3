#!/bin/sh
python3 node_rover.py --port 34000 --network_index 1 --rover_index 2&
python3 node_rover.py --port 33001 --network_index 1 --rover_index 3&
python3 node_rover.py --port 33002 --network_index 1 --rover_index 4&
python3 node_rover.py --port 33003 --network_index 1 --rover_index 5&
python3 node_rover.py --port 34000 --network_index 2 --rover_index 2&
python3 node_rover.py --port 33001 --network_index 2 --rover_index 3&
python3 node_rover.py --port 33002 --network_index 2 --rover_index 4&
python3 node_rover.py --port 33003 --network_index 2 --rover_index 5&