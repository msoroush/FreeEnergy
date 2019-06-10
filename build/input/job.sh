#PBS -q mwsuq
#PBS -l select=1:ncpus=NCPU:mem=4gb:cpu_type=Intel
#PBS -j oe
#PBS -m abe
#PBS -M fj2314@wayne.edu

echo Running on host `hostname`
echo Time is `date`

module swap gnu7/7.3.0 intel/2019


cd RUN_DIR
echo Directory is `pwd`

# Run job
echo "RUNING NVT EQ"
cd EQ/NVT/.
./GOMC_CPU_NVT +pNCPU NVT.conf > out.log
echo "RUNING NPT EQ"
cd ../NPT/.
./GOMC_CPU_NPT +pNCPU NPT.conf > out.log
echo "RUNING PRODUCTION"
cd RUN_DIR
./GOMC_CPU_NVT +pNCPU prod.conf > out_pr.log
