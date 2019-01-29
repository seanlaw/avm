#!/bin/sh

./kill.sh
nohup ./avm.py &> LOG &
echo $! > PID
