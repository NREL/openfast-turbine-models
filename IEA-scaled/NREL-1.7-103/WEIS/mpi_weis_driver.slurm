#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=0:30:00
#SBATCH --job-name=weispc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

N_pc_pts=23

# load environment
. ~/.bashrc
WEIS

# check environment
echo 'Checking for WEIS in environment'
python -c 'from weis.glue_code.runWEIS import run_weis'

# Analysis level 2: Run power curve sweep
mpirun -np $((N_pc_pts+1)) python weis_driver.2.py

