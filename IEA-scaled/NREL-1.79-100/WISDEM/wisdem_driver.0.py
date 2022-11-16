# nDV: 0
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
import os, time, sys

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, 'NREL-1p715-103.yaml')
fname_modeling_options = os.path.join(run_dir, 'modeling_options.wisdem.yaml')
fname_analysis_options = os.path.join(run_dir, 'analysis_options.start.yaml')

if MPI:
    rank = MPI.COMM_WORLD.Get_rank()
else:
    rank = 0

if rank == 0:
    print('STEP 0')

tt = time.time()

# step 0: sanity check, initial NREL-1p7-103 -- NO OPT
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
