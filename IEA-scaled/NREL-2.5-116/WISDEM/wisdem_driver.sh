#!/bin/bash
set -e

# check environment
echo 'Checking for WISDEM in environment'
python -c 'from wisdem import run_wisdem'
echo 'Checking for WEIS in environment'
python -c 'from weis.glue_code.runWEIS import run_weis'

# perform sequential optimizations
Nsteps=`ls wisdem_driver.?.py | wc -l`
for i in `seq 0 $((Nsteps-1))`; do
    if [ -f "log.step$i" -a -d "outputs.$i" ]; then
        echo "Step $i has already been run"
    else
        python wisdem_driver.${i}.py 2>&1 | tee log.step$i
    fi
    if [ "$i" == 0 ]; then
        echo 'Difference reference and current turbine:'
        diff outputs.0/refturb.yaml NREL-*.start.yaml || true
    fi
done

echo 'Done.'
