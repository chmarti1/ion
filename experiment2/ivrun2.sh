#!/bin/bash

ERROR_FILE=ivchar2.err
MONITOR_CMD=./monitor2.bin
IVCHAR_CMD=./ivchar2.bin

# Execute monitor with the error redirected to the error file
$MONITOR_CMD 2> $ERROR_FILE

# Execute IVCHAR
$IVCHAR_CMD 2>> $ERROR_FILE

# Rename the new data file
DATA_FILE=ivchar`date +%Y%m%d%H%M%S`.dat
cp -v ivchar2.dat data/$DATA_FILE
