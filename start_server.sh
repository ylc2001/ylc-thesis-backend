#!/bin/bash

# dirs
CURRENT_DIR=$(dirname $0)
VAR_DIR=$CURRENT_DIR/.var
LOG_DIR=$CURRENT_DIR/server_logs

# create VAR_DIR or LOG_DIR if not exists
if [ ! -d "$VAR_DIR" ]; then
    mkdir -p $VAR_DIR
fi
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p $LOG_DIR
fi

# server log path (will be rotated)
LOG_PATH=$LOG_DIR/server.log
# FIFO path
FIFO_PATH=$VAR_DIR/.fifo
# max log size in MB
MAX_LOG_SIZE=5
# log of log rotation
ROTATE_FILE=$LOG_DIR/rotate.log

# PID files of server and log rotation
# [!IMPORTANT] do not manually change these files
PID_FILE=$VAR_DIR/server.pid
PID_ROTATE_FILE=$VAR_DIR/rotate.pid

# stop server
$CURRENT_DIR/stop_server.sh

# check FIFO
if [ -e $FIFO_PATH ]; then
    if [ ! -p $FIFO_PATH ]; then
        # If it exists but is not a FIFO, remove it
        rm -f $FIFO_PATH
        mkfifo $FIFO_PATH
    fi
else
    mkdir -p $(dirname $FIFO_PATH)
    mkfifo $FIFO_PATH
fi

# start virtual environment
. $CURRENT_DIR/.venv/bin/activate

# colors for output
LIGHT_RED='\033[1;31m'
LIGHT_CYAN='\033[1;36m'
NC='\033[0m'

# start log rotation
nohup python3 -u $CURRENT_DIR/log_rotate.py --fifo-path $FIFO_PATH --log-path $LOG_PATH --max-log-size $MAX_LOG_SIZE >> $ROTATE_FILE 2>&1 &
echo $! > $PID_ROTATE_FILE
printf "${LIGHT_CYAN}Log rotation (parent PID ${LIGHT_RED}$!${LIGHT_CYAN}) running${NC}\n"

# read .env to get HOST and PORT
if [ -f $CURRENT_DIR/.env ]; then
  . $CURRENT_DIR/.env
fi
echo Server addr: $HOST:$PORT

# Run the server in the background using nohup, and save the process ID to a file
nohup gunicorn -k eventlet --chdir $CURRENT_DIR --bind $HOST:$PORT app:app >> $FIFO_PATH 2>&1 &
echo $! > $PID_FILE
printf "${LIGHT_CYAN}Server (parent PID ${LIGHT_RED}$!${LIGHT_CYAN}) running${NC}\n"

# change oom_score to avoid killing the server
sudo echo -1000 > /proc/$!/oom_score_adj
echo oom_score: $(cat /proc/$!/oom_score)

