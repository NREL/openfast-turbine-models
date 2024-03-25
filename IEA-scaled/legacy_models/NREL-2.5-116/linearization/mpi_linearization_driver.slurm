#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=0:15:00
#SBATCH --job-name=fast_lin_turb_NREL2p5
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

# load environment
. ~/.bashrc
WEIS

python runLinTurbine.py

