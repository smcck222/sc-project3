#!/usr/bin/bash
mkdir -p output
python3 leader_rover.py --port 33000 --network_index 2 --rover_index 1&
sleep 2
python3 node_rover.py --port 34000 --network_index 2 --rover_index 2 > ./output/network2_rover2.log&
python3 node_rover.py --port 33001 --network_index 2 --rover_index 3 > ./output/network2_rover3.log&
python3 node_rover.py --port 33002 --network_index 2 --rover_index 4 > ./output/network2_rover4.log&
python3 node_rover.py --port 33003 --network_index 2 --rover_index 5 > ./output/network2_rover5.log&