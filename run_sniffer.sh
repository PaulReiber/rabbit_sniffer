#!/bin/bash

if [[ $@ -ne 2 ]]; then
    echo "Usage: run_sniffer.sh [routing_key]"
    exit 1
fi

sudo rabbitmqctl trace_on
./rabbit_sniffer.py $1
sudo rabbitmqctl trace_off
