#PBS -q wsuq
#PBS -l select=1:ncpus=NCPU:mem=8gb
#PBS -j oe
#PBS -m abe
#PBS -M fj2314@wayne.edu

echo Running on host `hostname`
echo Time is `date`

module swap gnu7/7.3.0 intel/2019


cd RUN_DIR
echo Directory is `pwd`

# Run job
cd NVT/.
./GOMC_CPU_NVT +pNCPU NVT.conf > out.log
cd ../NPT/.
./GOMC_CPU_NPT +pNCPU NPT.conf > out.log
