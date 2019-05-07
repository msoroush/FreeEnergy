#!/bin/bash

BASE_DIR=`pwd`; 
DIRNAME="F";
STATE="state_"

for d in $( seq 3 2 17 ); 
do 
    DN=${BASE_DIR}/${DIRNAME}$d"*"/TI;
    cd $DN;
    echo "Working on `pwd`: ";
    NS=$(( `ls -d ${STATE}* | wc -l` - 1));
    echo "Found states 0-${NS}:"
    for s in $( seq 0 ${NS} );
    do
	SD=${STATE}$s;
	cd ${SD};
	echo "   Submitting jobs for ${SD}";
	qsub *.sh;
	sleep 1;
	cd ${DN}
    done
done
