#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=8:00:00
#SBATCH --job-name=wisdem_design
#SBATCH --nodes=3
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

# load environment
. ~/.bashrc
wisdem-env
echo "Note: The default mpirun is `which mpirun`"

echo "Started design at `date`"
echo ''

mpirun -np 94 python blade_aerostruct_opt.0.py
python create_conv_plots.py analysis_options.0.yaml

python tower_struct_opt.py

echo ''
echo "Finished design at `date`"
echo ''

