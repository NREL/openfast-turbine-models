#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=1:00:00
#SBATCH --job-name=weis_servo_opt
#SBATCH --nodes=1
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

nDV=4 # Number of design variables (x2 for central difference)
nOF=1 # Number of openfast runs per finite-difference evaluation (n_wind_speed * n_seeds)
nC=$((nDV + nDV * nOF)) # Number of cores needed. Make sure to request an appropriate number of nodes = N / 36

# load environment
. ~/.bashrc
weis-env
echo "Note: The default mpirun is `which mpirun`"
echo ''

echo "Started controls optimization at `date`"
echo ''

mpirun -n $nC --bind-to=core python weis_driver.servo_opt.py &> log.weis.servo_opt

echo "Finished controls optimization at `date`"
echo ''
