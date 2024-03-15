#!/usr/bin/env python
import numpy as np
from wisdem_interface import WisdemInterface

# my wisdem-env on NREL Eagle HPC has some quirks...
#import os
#condaroot = os.environ['CONDA_PREFIX']
#mpirun = os.path.join(condaroot,'bin','mpirun')

#TOL = 1e-4  # should be good enough (default)
TOL = 1e-5  # change in twist/chord should be negligible at this point
#TOL = 1e-6  # should not be needed!

wiz = WisdemInterface(
    turbine_prefix='NREL-2.8-127',
    starting_geometry='NREL-2.8-127.start.yaml',
    default_modeling_options='modeling_options.wisdem.yaml',
    default_analysis_options='analysis_options.start.yaml',
    #mpirun=mpirun,
    tol=TOL)

# Baseline model options
wiz.mopt['WISDEM']['RotorSE']['peak_thrust_shaving'] = True
wiz.mopt['WISDEM']['RotorSE']['thrust_shaving_coeff'] = 0.70


#===============================================================================
#
# AERODYNAMIC OPTIMIZATION
# ------------------------
#
# 1. Stall-constrained twist optimization (note: n_opt=8 control pts)
#    Don't change the shape near the root
#
#wiz.aopt['merit_figure'] = 'AEP'
wiz.aopt['merit_figure'] = 'Cp'  # optimize for aerodynamic performance

twistDV = wiz.aopt['design_variables']['blade']['aero_shape']['twist']
twistDV['flag'] = True
twistDV['index_start'] = 2
#twistDV['index_end'] = 7  # excluding the tip seems to hurt convergence
twistDV['index_end'] = 8  # allow tip twist to change

blade_constraint = wiz.aopt['constraints']['blade']
blade_constraint['stall']['flag'] = True
blade_constraint['stall']['margin'] = 0.05235987756  # [rad] == 3 deg

wiz.optimize('Opt twist')


# 2. Add chord optimization with max-chord constraint (note: n_opt=8 control pts)
#    Don't change the shape near the root
#
chordDV = wiz.aopt['design_variables']['blade']['aero_shape']['chord']
chordDV['flag'] = True
chordDV['index_start'] = 2
chordDV['index_end'] = 7  # exclude the tip

blade_constraint['chord']['flag'] = True
blade_constraint['chord']['max'] = 4.5

# penalize outboard loading to get a more realistic chord distribution
blade_constraint['moment_coefficient']['flag'] = True
blade_constraint['moment_coefficient']['max'] = 0.16

wiz.optimize('Opt twist+chord')


#===============================================================================
#
# STRUCTURAL OPTIMIZATION
# -----------------------
#
# 3. Switch to structural optimization, with blade mass as the figure of merit
#
wiz.reset() # Turn off all previous optimizations/constraints
blade_constraint = wiz.aopt['constraints']['blade'] # Need to set this again after reset

wiz.aopt['merit_figure'] = 'blade_mass'

# Turn on spar cap thickness optimization for both the suction and pressure
# sides, constrained by tip deflection
spar_cap_ss = wiz.add_blade_struct_dv('Spar_Cap_SS')
spar_cap_ps = wiz.add_blade_struct_dv('Spar_Cap_PS')

blade_constraint['tip_deflection']['flag'] = True
blade_constraint['tip_deflection']['margin'] = 1/0.7 # cannot exceed 70% (default)

wiz.optimize('Min blade mass')


# #
# # 4. Add additional constraints for 3P separation
# #
# # Note: 3P freq: 0.675 Hz
# blade_constraint['frequency']['first_flap']['flag'] = True
# blade_constraint['frequency']['first_flap']['target'] = 0.6075 # 10% margin
# blade_constraint['frequency']['first_flap']['acceptable_error'] = 0.03375 # 5% of 3P
# blade_constraint['frequency']['first_edge']['flag'] = True
# blade_constraint['frequency']['first_edge']['target'] = 0.7425 # 10% margin
# blade_constraint['frequency']['first_edge']['acceptable_error'] = 0.03375 # 5% of 3P
# blade_constraint['strains_spar_cap_ss']['flag'] = True
# blade_constraint['strains_spar_cap_ps']['flag'] = True
# blade_constraint['strains_te_ss']['flag'] = True
# blade_constraint['strains_te_ps']['flag'] = True
# 
# # ... and degrees of freedom to make that achievable
# max_change = dict(max_decrease=0.2, max_increase=5.0) # default multiplicative factor: 0.5, 1.5
# shell_skin  = wiz.add_blade_struct_dv('Shell_skin',         index_start=3,index_end=8,**max_change)
# LE_reinf    = wiz.add_blade_struct_dv('LE_reinf',           index_start=1,index_end=7,**max_change)
# TE_reinf_ss = wiz.add_blade_struct_dv('TE_reinforcement_SS',index_start=1,index_end=7,**max_change)
# TE_reinf_ps = wiz.add_blade_struct_dv('TE_reinforcement_PS',index_start=1,index_end=7,**max_change)
# spar_cap_ss['index_start'] = 1; spar_cap_ss['index_end'] = 7 # for manufacturability
# spar_cap_ps['index_start'] = 1; spar_cap_ps['index_end'] = 7 # for manufacturability
# 
# wiz.optimize('Min blade mass, target freq')


# write the postprocessing script at this point because comparing with the
# tower-optimization output does not work (because RotorSE is turned off)
wiz.write_postproc_script()


