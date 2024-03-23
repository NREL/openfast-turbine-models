#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=1:00:00
#SBATCH --job-name=weis_dlcs
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=100
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=logs/log.opt.%j
#SBATCH --reservation=weto-debug
#SBATCH --qos=standby

nC=80

# load environment
source ~/.bashrc
conda activate weis-env
which python

echo "Started DLCs at `date`"
echo ''

# Note: This approach uses WISDEM to generate the OpenFAST model
mpiexec -n $nC python weis_driver.dlc1p1_with_wisdem.py

echo "Finished DLCs at `date`"
echo ''
