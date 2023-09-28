# nDV: 8
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from wisdem_interface.helpers import load_yaml, save_yaml
import os, time, sys

istep = 2

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-2p8-127-step{istep-1}.yaml')
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
    aopt['general']['fname_output'] = f'NREL-2p8-127-step{istep}'

    # - stall-constrained twist opt for AEP
    aopt['driver']['optimization']['flag'] = True
    aopt['design_variables']['blade']['aero_shape']['twist']['flag'] = True
    aopt['constraints']['blade']['stall']['flag'] = True
    save_yaml(fname_analysis_options, aopt)

if MPI:
    MPI.COMM_WORLD.Barrier()

tt = time.time()

wt_opt, modeling_options, opt_options = run_wisdem(
    fname_wt_input,
    fname_modeling_options,
    fname_analysis_options
)
 
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
