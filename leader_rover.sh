#!/bin/sh
python3 leader_rover.py --port 33000 --network_index 1 --rover_index 1&
python3 leader_rover.py --port 33000 --network_index 2 --rover_index 1&