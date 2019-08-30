#!/bin/bash

BASE_DIR=`pwd`; 
STATE="state_"
RNAME="TI_"
DF=(C8OH H7F1 H6F2 H2F6 H1F7 F17O)

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
	    JNAME=${d}"_"$s".sh";
	    cd ${SD};
	    echo "   Submitting jobs for ${JNAME}";
	    qsub ${JNAME};
	    sleep 1;
	    cd ${DN}
	done
    done
done
