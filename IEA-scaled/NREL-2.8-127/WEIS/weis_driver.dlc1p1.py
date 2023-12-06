
from weis.glue_code.runWEIS     import run_weis
from wisdem.commonse.mpi_tools  import MPI
import os, time, sys

from weis.aeroelasticse.FileTools import load_yaml, save_yaml

rank = MPI.COMM_WORLD.Get_rank() if MPI else 0

## File management
run_dir                = os.path.dirname( os.path.realpath(__file__) )
fname_wt_input         = os.path.join(run_dir, 'NREL-2.8-127.yaml')
fname_modeling_options = os.path.join(run_dir, "modeling_options.dlc_1p1.yaml")
fname_analysis_options = os.path.join(run_dir, "analysis_options.yaml")
tuning_yaml            = os.path.join(run_dir, "NREL2p8_tuning.yaml") # from ROSCO 2.8

## Generate modeling options from template
if rank == 0:
    modopt = load_yaml('modeling_options.template.yaml')
    # make sure servo opt ran
    fstname = modopt['General']['openfast_configuration']['OF_run_fst'] + '_0.fst'
    fstpath = os.path.join('outputs','servo_opt','rank_0',fstname)
    assert os.path.isfile(fstpath)
    # scrape log file for optimal values
    omega_pc = None
    zeta_pc = None
    with open('log.weis.servo_opt','r') as f:
        for line in f:
            if line.startswith('Pitch PI gain inputs'):
                line = line.split()
                assert line[4] == 'omega_pc[0]'
                omega_pc = float(line[6].rstrip(','))
                assert line[7] == 'zeta_pc[0]'
                zeta_pc = float(line[9])
    assert omega_pc and zeta_pc
    print(f'optimal pitch PI gain inputs: omega={omega_pc:g}, zeta={zeta_pc:g}')
    # update values
    modopt['Level3']['openfast_file'] = fstname
    modopt['Level3']['openfast_dir'] = os.path.join(run_dir,'outputs','servo_opt','rank_0')
    modopt['ROSCO']['tuning_yaml'] = tuning_yaml
    modopt['ROSCO']['zeta_pc'] = [zeta_pc]
    modopt['ROSCO']['omega_pc'] = [omega_pc]
    # write input file
    save_yaml(run_dir, os.path.split(fname_modeling_options)[1], modopt)

tt = time.time()
wt_opt, modeling_options, opt_options = run_weis(fname_wt_input, fname_modeling_options, fname_analysis_options)

if rank == 0:
    print('Run time: %f'%(time.time()-tt))
