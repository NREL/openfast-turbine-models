# nDV: 8
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from helpers import load_yaml, save_yaml
import os, time, sys

istep = 5

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-2p3-116-step{istep-1}.yaml')
fname_modeling_options = os.path.join(run_dir, f'modeling_options.{istep}.yaml')
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
    aopt['general']['fname_output'] = f'NREL-2p3-116-step{istep}'

    # - blade-mass opt constrained by tip deflection
    aopt['driver']['optimization']['flag'] = True
    aopt['design_variables']['blade']['structure']['spar_cap_ss']['flag'] = True
    aopt['design_variables']['blade']['structure']['spar_cap_ps']['flag'] = True
    aopt['constraints']['blade']['tip_deflection']['flag'] = True
    aopt['merit_figure'] = 'blade_mass'
    save_yaml(fname_analysis_options, aopt)

    ## Update modeling options
    mopt = load_yaml(os.path.join(run_dir,
                                  f'outputs.{istep-1}',
                                  f'NREL-2p3-116-step{istep-1}-modeling.yaml'))
    save_yaml(fname_modeling_options, mopt)

if MPI:
    MPI.COMM_WORLD.Barrier()

model_changes = {}

tt = time.time()

wt_opt, modeling_options, opt_options = run_wisdem(
    fname_wt_input,
    fname_modeling_options,
    fname_analysis_options,
    overridden_values=model_changes,
)
 
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
