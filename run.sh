#!/bin/sh

./kill.sh
./avm.py &> LOG &
echo $! > PID
