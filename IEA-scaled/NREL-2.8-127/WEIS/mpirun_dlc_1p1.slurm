#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=1:00:00
#SBATCH --job-name=weis_sweep
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

nwspds=10  # == modeling_options['DLC_driver']['n_cases'] == number of wind speeds
nC=$((nwspds+1))

# load environment
. ~/.bashrc
weis-env
echo "Note: The default mpirun is `which mpirun`"
echo ''

echo "Started design at `date`"
echo ''

echo "Performing controller tuning with nC=${nC}..."
mpirun -n $nC --bind-to=core python weis_driver.py &> log.weis.dlc1p1

echo "Finished design at `date`"
echo ''
