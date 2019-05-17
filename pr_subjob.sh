#!/bin/bash

BASE_DIR=`pwd`; 
STATE="state_"
RNAME="TI_"
DF=(F3O F5O F7O F9O F11O F13O F15O F17O)

for d in ${DF[@]}; 
do
    cd ${BASE_DIR}/$d
    NR=$(( `ls -d ${RNAME}* | wc -l` ));
    for r in $( seq 1 ${NR} )
    do
	DN=${BASE_DIR}/$d/${RNAME}$r;
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
done
