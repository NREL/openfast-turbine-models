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

# Blade optimization without the stall margin constraint
mpirun -np 94 python blade_aerostruct_opt.0.py
python create_conv_plots.py analysis_options.0.yaml

# Smooth the blade twist distribution and then re-run opt with that fixed
python smooth_geom.py aerostruct.0/NREL-2.8-127.yaml \
                      aerostruct.0/NREL-2.8-127_smooth_twist.yaml
mpirun -np 82 python blade_aerostruct_opt.1.py
python create_conv_plots.py analysis_options.1.yaml

# Blade optimization with the stall margin constraint
mpirun -np 94 python blade_aerostruct_opt.2.py
python create_conv_plots.py analysis_options.2.yaml

# Tower optimization _with frequency constraint_
python tower_struct_opt.py

echo ''
echo "Finished design at `date`"
echo ''

