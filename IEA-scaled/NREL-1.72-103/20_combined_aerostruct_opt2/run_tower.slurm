#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=1:00:00
#SBATCH --job-name=wisdem_design
#SBATCH --nodes=1
#SBATCH --mail-user ryan.scott@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

# load environment
module purge
module load conda
module load intel/2023.2.0
conda activate weis-env

echo "Started design at `date`"
echo ''

# Tower optimization _with frequency constraint_
python tower_struct_opt.py

echo ''
echo "Finished design at `date`"
echo ''