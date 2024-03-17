import os
from wisdem import run_wisdem
from wisdem_interface.helpers import generate_tower_modeling_yaml

mydir = os.path.dirname(os.path.realpath(__file__))  # get path to this file
fname_wt_input         = os.path.join(mydir, "aerostruct.2/NREL-2.8-127.yaml")
fname_modeling_options = os.path.join(mydir, "modeling_options.tower.yaml")
fname_analysis_options = os.path.join(mydir, "analysis_options.tower.yaml")

# extract loading from blade optimization
generate_tower_modeling_yaml('aerostruct.2/NREL-2.pkl', fname_modeling_options)

# scaled from the IEA-3.4 RWT
scaled_tower_diam = [
        4.0,
        3.9599332220367276,
        3.9599332220367276,
        3.9599332220367276,
        3.9599332220367276,
        3.9599332220367276,
        3.9065108514190316,
        3.4190317195325544,
        2.911519198664441,
        2.410684474123539,
        2.0033388981636056]
model_changes = {'towerse.tower_outer_diameter_in': scaled_tower_diam}

wt_opt, modeling_options, analysis_options = run_wisdem(
    fname_wt_input, fname_modeling_options, fname_analysis_options,
    overridden_values=model_changes
)

