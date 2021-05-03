#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=4:00:00
#SBATCH --job-name=weis_2p5-116
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

N_pc_pts=23

nDV=4 # Number of design variables (x2 for central difference)
nOF=12  # Number of openfast runs per finite-difference evaluation
nC=$((nDV + nDV * nOF)) # Number of cores needed. Make sure to request an appropriate number of nodes = N / 36

# load environment
. ~/.bash_profile
WEIS

# check environment
echo 'Checking for WEIS in environment'
python -c 'from weis.glue_code.runWEIS import run_weis'


echo 'Performing controller tuning...'
#mpirun -np $nC python weis_driver.0.py
mpiexec -n $nC --bind-to core python weis_driver.0.py

outfile=`ls outputs/*.pkl`
fname=${outfile##*/}
prefix="${fname%.pkl}"
cp -v outputs/${prefix}.yaml ${prefix}.servo_opt.yaml

# Note: manually tune torque controller for now


echo 'Generating OpenFAST model'
python weis_driver.1.py


echo 'Run power curve sweep with steady inflow'
mpirun -np $((N_pc_pts+1)) python weis_driver.2.py


echo 'Run DLC 1.1'
mpirun -np $((N_pc_pts+1)) python weis_driver.3.py

