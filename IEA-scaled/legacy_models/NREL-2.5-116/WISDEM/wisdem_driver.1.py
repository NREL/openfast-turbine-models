# nDV: 0
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from wisdem_interface.helpers import load_yaml, save_yaml
import os, time, sys

istep = 1

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, 'NREL-2p5-116.start.yaml')
fname_modeling_options = os.path.join(run_dir, 'modeling_options.wisdem.yaml')
fname_analysis_options = os.path.join(run_dir, f'analysis_options.{istep}.yaml')

if MPI:
    rank = MPI.COMM_WORLD.Get_rank()
else:
    rank = 0

if rank == 0:
    print('STEP',istep)

    ## Update analysis options
    aopt = load_yaml(os.path.join(run_dir,'analysis_options.start.yaml'))
    aopt['general']['folder_output'] = f'outputs.{istep}'
    aopt['general']['fname_output'] = f'NREL-2p5-116-step{istep}'
    save_yaml(fname_analysis_options, aopt)

tt = time.time()

# step 1: manually updated turbine geometry, rated power, rotor speed range -- NO OPT
wt_opt, modeling_options, opt_options = run_wisdem(
    fname_wt_input,
    fname_modeling_options,
    fname_analysis_options
)
 
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
