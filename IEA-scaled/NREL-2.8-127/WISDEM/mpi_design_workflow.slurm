#!/bin/bash
#SBATCH --account=car
#SBATCH --time=1:00:00
#SBATCH --job-name=wisdem_design
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

# load environment
. ~/.bashrc
wisdem-env
echo "Note: The default mpirun is `which mpirun`"
echo ''

echo "Started design at `date`"
echo ''

python design_workflow.py

echo "Finished design at `date`"
echo ''

sh compare_NREL-2.8-127_designs.sh
