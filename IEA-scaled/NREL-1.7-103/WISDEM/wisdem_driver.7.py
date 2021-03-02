import numpy as np
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from helpers import load_yaml, save_yaml, load_pickle
import os, time, sys

istep = 7

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-1p7-103-step{istep-1}.yaml')
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
    aopt['general']['fname_output'] = f'NREL-1p7-103-step{istep}'

    # - constrained structural opt for tower mass
    #   ADD frequency constraint
    aopt['driver']['optimization']['flag'] = True
   #aopt['driver']['optimization']['tol'] = 1e-10
   #aopt['driver']['optimization']['max_iter'] = 100
    aopt['design_variables']['tower']['layer_thickness']['flag'] = True
    aopt['design_variables']['tower']['outer_diameter']['flag'] = True
    aopt['design_variables']['tower']['outer_diameter']['upper_bound'] = 4.0
   #aopt['constraints']['tower']['stress']['flag'] = True
   #aopt['constraints']['tower']['global_buckling']['flag'] = True
   #aopt['constraints']['tower']['shell_buckling']['flag'] = True
    aopt['constraints']['tower']['frequency_1']['flag'] = True
    aopt['constraints']['tower']['frequency_1']['lower_bound'] = 0.271
    aopt['merit_figure'] = 'tower_mass'
    save_yaml(fname_analysis_options, aopt)

    ## Get last modeling options
    mopt = load_yaml(os.path.join(run_dir,
                                  f'outputs.{istep-1}',
                                  f'NREL-1p7-103-step{istep-1}-modeling.yaml'))
    save_yaml(fname_modeling_options, mopt)

# - calculate new tower profile
#   reduced max tower diameter to 4.0 m (land-based transport limitations)
#   assume linear taper from mid-height (original design started from 60%H)
lastmodel = load_yaml(fname_wt_input)
outerD = lastmodel['components']['tower']['outer_shape_bem']['outer_diameter']
Dgrid = np.array(outerD['grid'])
Dvals = np.array(outerD['values'])
print('tower grid:',Dgrid)
print('tower diam:',Dvals)
newouterD = 4.0 * Dvals / Dvals[0]
kmid = int(len(Dgrid) / 2) # assume evenly spaced grid
newouterD[kmid:] = newouterD[kmid] \
        + (Dvals[-1]-newouterD[kmid])/(Dgrid[-1]-Dgrid[kmid])*(Dgrid[kmid:]-Dgrid[kmid])
print('tower diam:',newouterD,'(NEW)')
model_changes = {
    'towerse.tower_outer_diameter_in': list(newouterD),
    # Note: omega range does not get written out
    'control.minOmega': 0.0, # [rad/s] ~= 5 RPM, don't pitch in Region 1.5
    'control.maxOmega': 1.6504854369, # [rad/s] == 15.8 RPM ==> Vtip = 85 m/s
}

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
