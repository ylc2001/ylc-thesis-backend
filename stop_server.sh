#!/bin/bash

# dirs
CURRENT_DIR=$(dirname $0)
VAR_DIR=$CURRENT_DIR/.var
# FIFO path
FIFO_PATH=$VAR_DIR/.fifo
# PID files of server and log rotation
PID_FILE=$VAR_DIR/server.pid
PID_ROTATE_FILE=$VAR_DIR/rotate.pid

# colors for output
LIGHT_RED='\033[1;31m'
LIGHT_CYAN='\033[1;36m'
NC='\033[0m'

# Read the process ID of server and kill the process
if [ -f "$PID_FILE" ]; then
    BG_PID=$(cat $PID_FILE)
    # kill children processes
    pkill -P $BG_PID
    # kill parent process
    kill $BG_PID
    rm $PID_FILE
    printf "${LIGHT_CYAN}Server (parent PID ${LIGHT_RED}$BG_PID${LIGHT_CYAN}) killed${NC}\n"
else
    echo "Server is not running or $PID_FILE is missing."
fi

# Read the process ID of log rotation and kill the process
if [ -f "$PID_ROTATE_FILE" ]; then
    BG_PID=$(cat $PID_ROTATE_FILE)
    # kill children processes
    pkill -P $BG_PID
    # kill parent process
    kill $BG_PID
    rm $PID_ROTATE_FILE
    printf "${LIGHT_CYAN}Log rotation (parent PID ${LIGHT_RED}$BG_PID${LIGHT_CYAN}) killed${NC}\n"
else
    echo "Log rotation is not running or $PID_ROTATE_FILE is missing."
fi

# remove FIFO
if [ -p "$FIFO_PATH" ]; then
    rm $FIFO_PATH
    echo "FIFO deleted"
fi
