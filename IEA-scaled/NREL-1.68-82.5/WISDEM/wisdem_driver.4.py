# nDV: 11
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from helpers import load_yaml, save_yaml
import os, time, sys

istep = 4

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-1p68-82p5-step{istep-1}.yaml')
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
    aopt['general']['fname_output'] = f'NREL-1p68-82p5-step{istep}'

    # - stall- and max-chord-constrained twist & chord opt for AEP
    aopt['driver']['optimization']['flag'] = True
    aopt['driver']['optimization']['tol'] = 1e-4
    aopt['design_variables']['blade']['aero_shape']['twist']['flag'] = True
    aopt['design_variables']['blade']['aero_shape']['twist']['max_increase'] = 0.02
    aopt['design_variables']['blade']['aero_shape']['twist']['max_decrease'] = 0.02
    aopt['design_variables']['blade']['aero_shape']['chord']['flag'] = True
    aopt['design_variables']['blade']['aero_shape']['chord']['max_increase'] = 1.1
    aopt['design_variables']['blade']['aero_shape']['chord']['max_decrease'] = 0.9
    aopt['constraints']['blade']['stall']['flag'] = True
    aopt['constraints']['blade']['chord']['flag'] = True
    save_yaml(fname_analysis_options, aopt)

    ## Update modeling options
    mopt = load_yaml(os.path.join(run_dir,
                                  f'outputs.{istep-1}',
                                  f'NREL-1p68-82p5-step{istep-1}-modeling.yaml'))
    # - apply 70% peak thrust shaving
    mopt['WISDEM']['RotorSE']['peak_thrust_shaving'] = True
    mopt['WISDEM']['RotorSE']['thrust_shaving_coeff'] = 0.7
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
