# nDV: 16
import numpy as np
from wisdem import run_wisdem
from wisdem.commonse.mpi_tools  import MPI
from helpers import load_yaml, save_yaml, load_pickle
import os, time, sys

istep = 6

## File management
run_dir = './'
fname_wt_input = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-2p5-116-step{istep-1}.yaml')
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
    aopt['general']['fname_output'] = f'NREL-2p5-116-step{istep}'

    # - constrained structural opt for tower mass
    aopt['driver']['optimization']['flag'] = True
   #aopt['driver']['optimization']['tol'] = 1e-6
   #aopt['driver']['optimization']['max_iter'] = 50
    aopt['design_variables']['tower']['layer_thickness']['flag'] = True
    aopt['design_variables']['tower']['outer_diameter']['flag'] = True
    aopt['design_variables']['tower']['outer_diameter']['upper_bound'] = 4.0
    aopt['constraints']['tower']['stress']['flag'] = True
    aopt['constraints']['tower']['global_buckling']['flag'] = True
    aopt['constraints']['tower']['shell_buckling']['flag'] = True
   #aopt['constraints']['tower']['frequency_1']['flag'] = True
   #aopt['constraints']['tower']['frequency_1']['lower_bound'] = 0.270 # 10% over 1P cut-out
    aopt['merit_figure'] = 'tower_mass'
    save_yaml(fname_analysis_options, aopt)

    ## Update modeling options
    mopt = load_yaml(os.path.join(run_dir,
                                  f'outputs.{istep-1}',
                                  f'NREL-2p5-116-step{istep-1}-modeling.yaml'))
    mopt['WISDEM']['RotorSE']['flag'] = False
    mopt['WISDEM']['DriveSE']['flag'] = False
    mopt['WISDEM']['TowerSE']['nLC'] = 1

    # - apply loading so we can skip RotorSE
    pklfile = os.path.join(run_dir, f'outputs.{istep-1}', f'NREL-2p5-116-step{istep-1}.pkl')
    lastoutput = load_pickle(pklfile)
    pklprefix = 'comp.wt.'
    loading = {
        # need to explicitly cast to float, as workaround to what appears to be this issue:
        # https://github.com/SimplyKnownAsG/yamlize/issues/3
        'mass': float(lastoutput[pklprefix+'towerse.geom.turb.rna_mass']['value'][0]),
        'center_of_mass': [
            float(val) for val in lastoutput[pklprefix+'towerse.geom.turb.rna_cg']['value']
        ],
        'moment_of_inertia': [
            float(lastoutput[pklprefix+'towerse.pre.mIxx']['value'][0]),
            float(lastoutput[pklprefix+'towerse.pre.mIyy']['value'][0]),
            float(lastoutput[pklprefix+'towerse.pre.mIzz']['value'][0]),
            float(lastoutput[pklprefix+'towerse.pre.mIxy']['value'][0]),
            float(lastoutput[pklprefix+'towerse.pre.mIxz']['value'][0]),
            float(lastoutput[pklprefix+'towerse.pre.mIyz']['value'][0]),
        ],
        'loads': [
            {
                'force': [
                    float(val) for val in lastoutput[pklprefix+'towerse.pre.rna_F']['value']
                ],
                'moment': [
                    float(val) for val in lastoutput[pklprefix+'towerse.pre.rna_M']['value']
                ],
                'velocity': float(lastoutput[pklprefix+'rotorse.rp.powercurve.compute_power_curve.rated_V']['value'][0]),
            },
        ],
    }
    mopt['WISDEM']['Loading'] = loading
    save_yaml(fname_modeling_options, mopt)

if MPI:
    MPI.COMM_WORLD.Barrier()

# - calculate new tower profile
#   reduced max tower diameter to 4.0 m (land-based transport limitations)
#   assume linear taper from mid-height (original design started from 60%H)
lastmodel = load_yaml(fname_wt_input)
outerD = lastmodel['components']['tower']['outer_shape_bem']['outer_diameter']
Dgrid = np.array(outerD['grid'])
Dvals = np.array(outerD['values'])
newouterD = 4.0 * Dvals / Dvals[0]
kmid = int(len(Dgrid) / 2) # assume evenly spaced grid
newouterD[kmid:] = newouterD[kmid] \
        + (Dvals[-1]-newouterD[kmid])/(Dgrid[-1]-Dgrid[kmid])*(Dgrid[kmid:]-Dgrid[kmid])
if rank == 0:
    print('tower grid:',Dgrid)
    print('tower diam:',Dvals)
    print('tower diam:',newouterD,'(NEW)')

model_changes = {
    'towerse.tower_outer_diameter_in': list(newouterD),
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
