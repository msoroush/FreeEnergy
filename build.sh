#!/bin/bash

BASE_DIR=`pwd`;
BUILD_DIR="build"
CPU=4
#system info
SOLVENT="octanol.pdb"
TOT_SOLUTE=(pfmethanol.pdb pfethanol.pdb pfpropanol.pdb pfbutanol.pdb pfpentanol.pdb pfhexanol.pdb pfheptanol.pdb pfoctanol.pdb) 
TOT_SOLUTE_RESNAME=(F3O F5O F7O F9O F11O F13O F15O F17O)
#packing info
N_SOLVENT=200
BOX_SIZE=37.6
#simulation info
T=298
P=1.01325
RCUT=14
RCUTLOW=0.01
FE_MC=50000000 #steps for free energy simulation
EQ_MC=2000000   #steps for eq simulation
NPT_MC=10000000 #steps for NPT simulation
FE_FREQ=5000    #free energy calc frequency
STATES=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27)
VDW=(0.0 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00)
COUL=(0.0 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.20 0.40 0.60 0.70 0.80 0.90 1.00)



if [ ${#COUL[@]} != ${#VDW[@]} ]; then 
    echo "Warning: Number of Lambda states for VDW and COUL does not match!"
    exit 1
elif [ ${#STATES[@]} != ${#VDW[@]} ]; then
    echo "Warning: Number of Lambda states for VDW and COUL does not match!"
    exit 1
fi
if [ ${#SOLUTE[@]} != ${#SOLUTE_RESNAME[@]} ]; then 
    echo "Warning: Number of solute and residue name are not same!"
    exit 1
fi

for s in "${!TOT_SOLUTE[@]}"
do
    SOLUTE=${TOT_SOLUTE[s]}
    SOLUTE_RESNAME=${TOT_SOLUTE_RESNAME[s]}
    echo "Working on ${SOLUTE_RESNAME}"
    WD=${BASE_DIR}/${SOLUTE_RESNAME}
    mkdir $WD
    cp -rf ${BASE_DIR}/${BUILD_DIR} $WD/.
    cd $WD

    echo "Packing the system for ${SOLUTE_RESNAME}"
    cd ${BUILD_DIR}/pack/.
    PACK_SIZE=$( echo "${BOX_SIZE} - 1.5" | bc )
    sed -i 's#SOLVENT#'${SOLVENT}'#g' Pack.inp;
    sed -i 's#SOLV_NUM#'${N_SOLVENT}'#g' Pack.inp;
    sed -i 's#SOLUTE#'${SOLUTE}'#g' Pack.inp;
    sed -i 's#BOXSIZE#'${PACK_SIZE}'#g' Pack.inp;
    ./packmol < Pack.inp >& PACK.log
    vmd -dispdev text < build.tcl >& PACK.log

    if [ ! -f "START.psf" ]; then
	echo "Packing failed! Look at the ${WD}/${BUILD_DIR}/pack/PACK.log file."
    fi

    #set the common variable in config file
    cd ${WD}/${BUILD_DIR}/input/.
    sed -i 's#NCPU#'${CPU}'#g' *.sh
    sed -i 's#TTT#'${T}'#g' *.conf
    sed -i 's#PPPP#'${P}'#g' *.conf
    sed -i 's#BOXSIZE#'${BOX_SIZE}'#g' *.conf
    sed -i 's#RCUT#'${RCUT}'#g' *.conf
    sed -i 's#RLOW#'${RCUTLOW}'#g' *.conf
    sed -i 's#SOLUTE#'${SOLUTE_RESNAME}'#g' *.conf
    sed -i s/"STATES"/"${STATES[*]}"/g *.conf
    sed -i s/"LAMBDA_VDW"/"${VDW[*]}"/g *.conf
    sed -i s/"LAMBDA_COULOMB"/"${COUL[*]}"/g *.conf


    cd $WD
    mkdir EQ
    echo "Working on Equilibration files"
    EQD=${WD}/EQ
    cd ${EQD}
    IND=${WD}/${BUILD_DIR}/input/
    mkdir NVT NPT
    EQ_JOB=${SOLUTE_RESNAME}"_eq.sh"
    cp ${IND}/eq.sh ${EQ_JOB}
    cp ${IND}/NVT.conf ./NVT/.
    cp ${IND}/NPT.conf ./NPT/.
    cp ${IND}/GOMC_CPU_NVT ./NVT/.
    cp ${IND}/GOMC_CPU_NPT ./NPT/.
    sed -i 's#RUN_DIR#'`pwd`'#g' ${EQ_JOB}
    sed -i 's#MCSTEPS#'${EQ_MC}'#g' NVT/*.conf
    sed -i 's#MCSTEPS#'${NPT_MC}'#g' NPT/*.conf
    #qsub  ${EQ_JOB}

    cd $WD
    mkdir TI
    echo "Working on Free Energy files: "
    TID=${WD}/TI
    cd ${TID}
    N=$((${#VDW[@]}-1))
    for d in $( seq 0 $N ); 
    do 
	DN="state_"$d
	echo "    Building ${DN}"
	PR_JOB=${SOLUTE_RESNAME}"_"$d".sh"
	mkdir $DN
	cd $DN
	cp ${IND}/job.sh ${PR_JOB}
	cp ${IND}/GOMC_CPU_NVT .
	cp ${IND}/eq.conf .
	cp ${IND}/prod.conf .
	sed -i 's#MCSTEPS#'${EQ_MC}'#g' eq.conf
	sed -i 's#MCSTEPS#'${FE_MC}'#g' prod.conf
	sed -i 's#FREE_EN_FREQ#'${FE_FREQ}'#g' prod.conf
	sed -i 's#RUN_DIR#'`pwd`'#g' ${PR_JOB}
	sed -i 's#STATENUM#'${d}'#g' *.conf;
	sed -i 's#INIT_STATE#'${d}'#g' *.conf
	#qsub  ${PR_JOB}
	cd ${TID}
    done
done
