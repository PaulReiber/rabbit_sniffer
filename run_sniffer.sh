#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: run_sniffer.sh [routing_key]"
    exit 1
fi

./rabbit_sniffer.py "$1"
