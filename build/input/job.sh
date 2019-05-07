#PBS -q wsuq
#PBS -l select=1:ncpus=NCPU:mem=8gb:cpu_type=Intel
#PBS -j oe
#PBS -m abe
#PBS -M fj2314@wayne.edu

echo Running on host `hostname`
echo Time is `date`

module swap gnu7/7.3.0 intel/2019


cd RUN_DIR
echo Directory is `pwd`

# Run job
./GOMC_CPU_NVT +pNCPU eq.conf > out_eq.log
./GOMC_CPU_NVT +pNCPU prod.conf > out_pr.log
