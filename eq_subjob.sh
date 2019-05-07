#!/bin/bash

BASE_DIR=`pwd`; 
DIRNAME="F";

for d in $( seq 3 2 17 ); 
do 
    DN=${BASE_DIR}/${DIRNAME}$d"*"/EQ;
    cd $DN; 
    echo "Submiting job in `pwd`"
    qsub *.sh;
    sleep 1;
done
