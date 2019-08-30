# FreeEnergy
This repository is a bash script to prepare the simulation files for absolute FreeEnergy calculation using TI and FEP methods in GOMC.
GOMC currently bias LJ and Coulombic interaction with lambda, using soft-core or hard-core scheme, as implemented in GROMACS. For more details regarding the biasing scheme, please refer to GROMACS [Documentation](http://manual.gromacs.org/documentation/2019/reference-manual/functions/free-energy-interactions.html). 

## Software dependency:
1. [packmol](http://leandro.iqm.unicamp.br/packmol/versionhistory/) for packing molecule in box. 
    - Update the packmol executable file in `build/pack/.` directory.
2. [vmd](https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD) for generating PSF file.
    - vmd executable must be added to the path.
3. [GOMC](https://github.com/GOMC-WSU/GOMC/tree/FreeEnergy) Monte Carlo code to run simulation in NVT and NPT ensemble.
    - Update the GOMC executable files (GOMC_CPU_NVT, and GOMC_CPU_NPT) in `build/input/.` directory.
4. [alchemlyb](https://github.com/alchemistry/alchemlyb) for analysis the results using TI and FEP methods.

## What does it do?
The `build.sh` will pack the box with defined number of solvent and a solute, generate PDB and PSF file for solvent and solute. It creates directory for each solvent. Inside each solvent directory, it creates `EQ` direcotry for NVT and NPT equilibration simulation. Then it creates `TI_` direcotry for each replica and inside that create separate `state_0, state_1, ...` directory.

There are two python scripts available to calculate the free energy using BAR, MBAR, and TI estimators in alchemlyb python library.
1. `freeEn_correlated_data.py`: Calculate the free energy difference using correlated samples.
2. `freeEn_uncorrelated_data.py`: Calculate the free energy difference using uncorrelated samples.

```
Solvent
|___________ build
|            |______ input files (config files, GOMC executables, job scripts)
|            |______ pdb files (single PDB files for solvent and solute)
|            |______ model (parameter and topology files for solvent and solute)
|            |______ pack (initial PDB and PSF files for equilibration)
|
|___________ EQ
|            |_______ NVT (running NVT simulation prior NPT, using PDB and PSF files in build/pack)
|            |_______ NPT (running NPT simulation from equilibrated NVT simulation, using PDB and PSF files in EQ/NVT)
|
|____________ TI_1
             |_______ state_0 (equilibrte the system with NVT simulation with lambda state 0, using PDB and PSF files in EQ/NPT) 
             |                (production run in NVT simulation with lambda state 0, using equilibrated system)
             |_______ state_1 (running NVT simulation with lambda state 1, using PDB and PSF files in EQ/NPT)
             |                (production run in NVT simulation with lambda state 0, using equilibrated system)
             |_______  ...
  ```
  
## How to modify the configuration file
To modify the configuration file, modify the `NVT.conf`(for NVT equilibratio), `NPT.conf` (for NPT equilibration), `eq.conf` (NVT equilibration with lambda i), and `prod.conf` (production run in NVT) in `build/input/` directory.

## How to add another solvent or solute
To add another molecule, you need to:
1.  Generate the PDB file for single molecule in `build/pdb/` directory. (using gaussview or VMD [molfacture](https://www.ks.uiuc.edu/Research/vmd/plugins/molefacture/) tools)
2.  Update the Topology.top file in `build/model/`
3.  Update the parameter.par file in `build/model/`

## How to modify the system parameter?
### Free energy systems:
We can define a range of solute name in `build.sh` to calculate the free energy.
```bash
#system info
NREP=5                                                      # number of TI replica
SOLVENT="octanol.pdb"                                       # pdb name of solvent
TOT_SOLUTE=(pfmethanol.pdb pfethanol.pdb pfpropanol.pdb)    # pdb names of solute 
TOT_SOLUTE_RESNAME=(F3O F5O F7O)                            # residue name of solute 
```

### Config file:
There are some options in config files that can be controls by `build.sh`:
```bash
#simulation info
T=298                                            # temperature (K)
P=1.01325                                        # pressure (bar)
RCUT=14                                          # cutoff distance (A)
RCUTLOW=0.00                                     # hard cutoff (A) to avoid overlap
FE_MC=50000000                                   # steps for free energy simulation
EQ_MC=2000000                                    # steps for equilibration simulation (both NVT.conf and eq.conf)
NPT_MC=10000000                                  # steps for NPT equilibration simulation
FE_FREQ=5000                                     # free energy calc frequency
STATES=(0    1    2    3    4    5    6    7)    # state id (for user only) 
VDW=(0.00  0.20 0.40 0.60 0.80 1.00 1.00 1.00)   # lambda vector for VDW
COUL=(0.00 0.00 0.00 0.20 0.40 0.60 0.80 1.00)   # lambda vector for Coulomb
```

### Packing parameters:
We can set the number of solvent and box size to be packed in `build.sh`:
```bash
#packing info 
N_SOLVENT=200                                    # number of solvent
BOX_SIZE=37.6                                    # length of cubic box (A)
```

### Parallelization:
Modify the job script `job.sh` in `build/input/`
We can set the number threads for openmp parallelization in `build.sh`:
```bash
#packing info 
CPU=4                                            # number of CPU threads
```
