import os
from wisdem import run_wisdem

mydir = os.path.dirname(os.path.realpath(__file__))  # get path to this file
fname_wt_input         = os.path.join(mydir, "aerostruct.0/NREL-2.3-116.yaml")
fname_modeling_options = os.path.join(mydir, "modeling_options.yaml")
fname_analysis_options = os.path.join(mydir, "analysis_options.1.yaml")

wt_opt, modeling_options, analysis_options = run_wisdem(
    fname_wt_input, fname_modeling_options, fname_analysis_options
)

