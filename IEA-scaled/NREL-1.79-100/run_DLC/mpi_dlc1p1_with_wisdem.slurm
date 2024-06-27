#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=1:00:00
#SBATCH --job-name=weis_dlcs
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=104
#SBATCH --mail-user ryan.scott@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=logs/log.opt.%j

nC=80

# load environment
module purge
module load conda
module load intel/2023.2.0
conda activate weis-env

echo "Started DLCs at `date`"
echo ''

# Note: This approach uses WISDEM to generate the OpenFAST model
mpiexec -n $nC python weis_driver.dlc1p1_with_wisdem.py

echo "Finished DLCs at `date`"
echo ''