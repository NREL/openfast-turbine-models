
from weis.glue_code.runWEIS     import run_weis
from wisdem.commonse.mpi_tools  import MPI
import os, time, sys

## File management
run_dir                = os.path.dirname( os.path.realpath(__file__) )
fname_wt_input         = os.path.join(run_dir, 'NREL-2p5-116.yaml')
fname_modeling_options = os.path.join(run_dir, "modeling_options_weis.0.yaml")
fname_analysis_options = os.path.join(run_dir, "analysis_options_weis.servo_opt.yaml")


tt = time.time()
wt_opt, modeling_options, opt_options = run_weis(fname_wt_input, fname_modeling_options, fname_analysis_options)

if MPI:
    rank = MPI.COMM_WORLD.Get_rank()
else:
    rank = 0
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
