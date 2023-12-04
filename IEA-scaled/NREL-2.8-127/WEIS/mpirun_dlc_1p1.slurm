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

echo "Started DLCs at `date`"
echo ''

mpirun -n $nC --bind-to=core python weis_driver.dlc_1p1.py &> log.weis.dlc_1p1

echo "Finished DLCs at `date`"
echo ''
