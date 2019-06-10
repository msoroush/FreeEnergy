#!/bin/bash

DF=(C8OH H7F1 H6F2 H2F6 H1F7 F17O)
NREP=1


BASE_DIR=`pwd`; 
RNAME="TI_"

for d in ${DF[@]}; 
do
    cd ${BASE_DIR}/$d
    for r in $( seq 1 ${NREP} )
    do
	DN=${BASE_DIR}/$d/${RNAME}$r;
	cd $DN;
	echo "Working on `pwd`: ";
	NS=$(( `ls -d state_* | wc -l` - 1));
	echo "Found states 0-${NS}:"
	for s in $( seq 0 ${NS} );
	do
	    SD="state_"$s;
	    JNAME=${d}"_"$s".sh";
	    cd ${SD};
	    echo "   Submitting jobs for ${JNAME}";
	    qsub ${JNAME};
	    sleep 1;
	    cd ${DN}
	done
    done
done
