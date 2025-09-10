#!/usr/bin/env bash

# Logverzeichnis sicherstellen
mkdir -p log
echo "start.sh started at $(date)" >> log/start.log

# Endlosschleife
while true; do
    ../venv/bin/python3 main.py >> log/$(date +"%Y-%m-%d_%H-%M-%S").log 2>&1 || venv/bin/python3 main.py >> log/$(date +"%Y-%m-%d_%H-%M-%S").log 2>&1 
    sleep 60
done
