
from wisdem.glue_code.runWISDEM import run_wisdem
#from weis.glue_code.runWEIS     import run_weis
from wisdem.commonse.mpi_tools  import MPI
import os, time, sys

## File management
run_dir = './'
fname_modeling_options = run_dir + "modeling_options.yaml"

# step 0: sanity check, initial IEA-3.4-130-RWT -- NO OPT
fname_wt_input         = run_dir + "IEA-3.4-130-RWT.yaml"
fname_analysis_options = run_dir + "analysis_options.0.yaml"

# step 1: updated turbine rating, rotor size -- NO OPT
# - scaled x and z values of components.blade.outer_shape_bem.reference_axis,
#   defined as id001, by factor of 116/130
fname_wt_input         = run_dir + "NREL-2_5-116-step0.yaml"
fname_analysis_options = run_dir + "analysis_options.1.yaml"

# step 2: updated turbine height -- NO OPT
# - scaled values components.tower.outer_shape_bem.reference_axis.z,
#   by factor of 80/108
fname_wt_input         = run_dir + "NREL-2_5-116-step1.yaml"
fname_analysis_options = run_dir + "analysis_options.2.yaml"

# step 3: unconstrained twist opt for AEP
# - adjusted min/max twist to be in bounds
# - downgraded openmdao: `conda install -c conda-forge openmdao=3.2.1`
fname_wt_input         = run_dir + "NREL-2_5-116-step2.yaml"
fname_analysis_options = run_dir + "analysis_options.3.yaml"

# step 4: constrained twist+chord opt for AEP
# - increase TSR to 9.0 (for smaller turbine)
# - change rotor speed range to between 5-14 RPM (IEA 3.4: 6.9-12.1)
# - add stall and max-chord constraint
fname_wt_input         = run_dir + "NREL-2_5-116-step3.yaml"
fname_analysis_options = run_dir + "analysis_options.4.yaml"

# step 5: constrained structural opt for blade mass
# - add tip deflection constraint
fname_wt_input         = run_dir + "NREL-2_5-116-step4.yaml"
fname_analysis_options = run_dir + "analysis_options.5.yaml"

# step 6: constrained structural opt for blade mass
# - add tip deflection constraint
fname_wt_input         = run_dir + "NREL-2_5-116-step5.yaml"
fname_analysis_options = run_dir + "analysis_options.6.yaml"


tt = time.time()
wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

if MPI:
    rank = MPI.COMM_WORLD.Get_rank()
else:
    rank = 0
if rank == 0:
    print('Run time: %f'%(time.time()-tt))
    sys.stdout.flush()
