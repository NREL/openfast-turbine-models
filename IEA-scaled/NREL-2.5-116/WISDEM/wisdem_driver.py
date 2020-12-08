
from wisdem.glue_code.runWISDEM import run_wisdem
#from weis.glue_code.runWEIS     import run_weis
from wisdem.commonse.mpi_tools  import MPI
import os, time, sys

## File management
run_dir = './'
fname_modeling_options = run_dir + "modeling_options.yaml"

tt = time.time()

# step 0: sanity check, initial IEA-3.4-130-RWT -- NO OPT
fname_wt_input         = run_dir + "IEA-3p4-130-RWT.yaml"
fname_analysis_options = run_dir + "analysis_options.0.yaml"
print('STEP 0')
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

# step 1: updated turbine rating, rotor size -- NO OPT
# - rated_power: 2500000.0 W
# - rotor_diameter: 116 m
# - hub_height: 80 m
print('STEP 1')
fname_wt_input         = run_dir + "NREL-2_5-116-step0.yaml"
fname_analysis_options = run_dir + "analysis_options.1.yaml"
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

# step 2: unconstrained twist opt for AEP
# - add stall constraint
# - need to use downgraded openmdao: `conda install -c conda-forge openmdao=3.2.1`
print('STEP 2')
fname_wt_input         = run_dir + "NREL-2_5-116-step1.yaml"
fname_analysis_options = run_dir + "analysis_options.2.yaml"
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

# step 3: unconstrained twist opt for AEP
# - increase TSR to 9.0 (for smaller turbine)
# - increased rotor speed range to 8-14 (IEA 3.4: 6.9-12.1)
# - add stall and max-chord constraint
# - peak thrust shaving: 75%
print('STEP 3')
fname_wt_input         = run_dir + "NREL-2_5-116-step2.yaml"
fname_analysis_options = run_dir + "analysis_options.3.yaml"
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

# step 4: constrained structural spar-cap opt for blade mass
# - add tip deflection constraint
print('STEP 4')
fname_wt_input         = run_dir + "NREL-2_5-116-step3.yaml"
fname_analysis_options = run_dir + "analysis_options.4.yaml"
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

# step 5: unconstrained structural wall-thickness opt for tower mass
# - reduced max tower diameter to 4.0 m (land-based transport limitations)
# - scale min tower diameter by 3.87/6 (from NREL 5MW RWT)
# - lienar taper from mid height
print('STEP 5')
fname_wt_input         = run_dir + "NREL-2_5-116-step4.yaml"
fname_analysis_options = run_dir + "analysis_options.5.yaml"
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

if MPI:
    rank = MPI.COMM_WORLD.Get_rank()
else:
    rank = 0
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
