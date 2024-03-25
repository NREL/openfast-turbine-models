#!/usr/bin/env python
import os
import sys
import openmdao.api as om
import wisdem.inputs as sch
from wisdem.glue_code.gc_RunTools import PlotRecorder


fname_analysis_options = sys.argv[1]
assert os.path.isfile(fname_analysis_options)

analysis_options = sch.load_analysis_yaml(fname_analysis_options)
wt_opt = om.Problem(model=PlotRecorder(opt_options=analysis_options), reports=False)
wt_opt.setup(derivatives=False)
wt_opt.run_model()
