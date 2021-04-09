#!/bin/bash
#SBATCH --account=awaken
#SBATCH --time=2:00:00
#SBATCH --job-name=wisdemdesign
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user eliot.quon@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL

# load environment
. ~/.bashrc
WEIS

# check environment
echo 'Checking for WISDEM in environment'
python -c 'from wisdem import run_wisdem'
echo 'Checking for WEIS in environment'
python -c 'from weis.glue_code.runWEIS import run_weis'

# perform sequential optimizations
Nsteps=`ls wisdem_driver.?.py | wc -l`
for i in `seq 0 $((Nsteps-1))`; do
    date
    if [ -f "log.step$i" -a -d "outputs.$i" ]; then
        echo "Step $i has already been run"
    else
        driver="wisdem_driver.${i}.py"
        nDV=`grep 'nDV' $driver | awk '{print $NF}'`
        if [ "$nDV" == 0 ]; then
            #ncores=1
            python $driver 2>&1 | tee log.step$i
        else
            ncores=$((2*nDV))
            echo "Launching $driver with $ncores cores"
            mpirun -v -np $ncores python $driver 2>&1 | tee log.step$i
        fi
        if [ -z "`grep 'Run time' log.step$i`" ]; then
            echo "Step $i did not finish?"
            break
        fi
    fi
    if [ "$i" == 0 ]; then
        echo 'Difference reference and current turbine:'
        diff outputs.0/refturb.yaml NREL-*.start.yaml > refturb.diff
    fi
done

echo "Done at `date`"
