#!/bin/bash

BASE_DIR=`pwd`; 
DIRNAME="F";
DF=(F3O F5O F7O F9O F11O F13O F15O F17O)

for d in ${DF[@]}; 
do 
    DN=${BASE_DIR}/$d/EQ;
    cd $DN; 
    echo "Submiting job in `pwd`"
    qsub *.sh;
    sleep 1;
done
