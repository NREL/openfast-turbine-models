#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=24:00:00
#SBATCH --job-name=weis_servo_opt
#SBATCH --nodes=1
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

nDV=4 # Number of design variables (x2 for central difference)
nOF=6 # Number of openfast runs per finite-difference evaluation (n_wind_speed * n_seeds)
nwspds=10  # == modeling_options['DLC_driver']['n_cases'] == number of wind speeds
nC=$((nDV + nDV * nOF)) # Number of cores needed. Make sure to request an appropriate number of nodes = N / 36

# load environment
. ~/.bashrc
weis-env
echo "Note: The default mpirun is `which mpirun`"
echo ''


echo "Started controls optimization at `date` with $nC cores"

mpirun -n $nC --bind-to=core python weis_driver.servo_opt.py &> log.weis.servo_opt

echo "Finished controls optimization at `date`"
grep -e '^Pitch PI gain input' -e '^rotor_overspeed' log.weis.servo_opt | tail -n 2


nC=$((nwspds+1))
echo ''
echo "Started DLC 1.1 at `date` with $nC cores"

mpirun -n $nC --bind-to=core python weis_driver.dlc_1p1.py &> log.weis.dlc_1p1

echo "Finished DLC 1.1 at `date`"
