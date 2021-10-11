#!/bin/bash
screen -L -S astra -dm ./run_astra.sh
screen -L -S throttle -dm ./throttled_data_node.py
