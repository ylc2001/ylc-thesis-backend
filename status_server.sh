#!/bin/bash

# dirs
CURRENT_DIR=$(dirname $0)
VAR_DIR=$CURRENT_DIR/.var

# PID files of server and log rotation
PID_FILE=$VAR_DIR/server.pid
PID_ROTATE_FILE=$VAR_DIR/rotate.pid

# colors for output
LIGHT_RED='\033[1;31m'
LIGHT_CYAN='\033[1;36m'
NC='\033[0m'

# check if server is running
PID=$(cat $PID_FILE 2>/dev/null)
if [ -z $PID ]; then
  printf "${LIGHT_RED}Server is not running${NC}\n"
else
  printf "${LIGHT_CYAN}Server is running with PID ${LIGHT_RED}$PID${NC}\n"
  ps -ef | grep $PID | grep -v grep
fi

# check if log rotation is running
ROTATE_PID=$(cat $PID_ROTATE_FILE 2>/dev/null)
if [ -z $ROTATE_PID ]; then
  printf "${LIGHT_RED}Log rotation is not running${NC}\n"
else
  printf "${LIGHT_CYAN}Log rotation is running with PID ${LIGHT_RED}$ROTATE_PID${NC}\n"
  ps -ef | grep $ROTATE_PID | grep -v grep
fi

