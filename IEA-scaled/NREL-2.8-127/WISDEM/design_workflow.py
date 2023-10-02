#!/usr/bin/env python
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
wiz.mopt['WISDEM']['RotorSE']['thrust_shaving_coeff'] = 0.72


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
wiz.aopt['design_variables']['blade']['aero_shape']['twist']['flag'] = True
wiz.aopt['design_variables']['blade']['aero_shape']['twist']['index_start'] = 2
#wiz.aopt['design_variables']['blade']['aero_shape']['twist']['index_end'] = 7  # excluding the tip hurts convergence
wiz.aopt['design_variables']['blade']['aero_shape']['twist']['index_end'] = 8  # allow tip twist to change
wiz.aopt['constraints']['blade']['stall']['flag'] = True
wiz.aopt['constraints']['blade']['stall']['margin'] = 0.05235987756  # [rad] == 3 deg

wiz.optimize('Opt twist')


# 2. Add chord optimization with max-chord constraint (note: n_opt=8 control pts)
#    Don't change the shape near the root
#
wiz.aopt['design_variables']['blade']['aero_shape']['chord']['flag'] = True
wiz.aopt['design_variables']['blade']['aero_shape']['chord']['index_start'] = 2
wiz.aopt['design_variables']['blade']['aero_shape']['chord']['index_end'] = 7  # exclude the tip
wiz.aopt['constraints']['blade']['chord']['flag'] = True
wiz.aopt['constraints']['blade']['chord']['max'] = 4.5

wiz.optimize('Opt twist+chord')


#===============================================================================
#
# STRUCTURAL OPTIMIZATION
# -----------------------
#
# 3. Switch to structural optimization, with blade mass as the figure of merit
#
# Turn off previous optimizations
wiz.aopt['design_variables']['blade']['aero_shape']['twist']['flag'] = False
wiz.aopt['design_variables']['blade']['aero_shape']['chord']['flag'] = False

# Turn on spar cap thickness optimization for both the suction and pressure
# sides, constrained by tip deflection
wiz.aopt['merit_figure'] = 'blade_mass'
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['flag'] = True
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['flag'] = True

# - this does _not_ converge due to tip deflection constraint (blade mass = 12666.5037462894 kg)
#wiz.aopt['constraints']['blade']['tip_deflection']['flag'] = True
#wiz.aopt['constraints']['blade']['tip_deflection']['margin'] = 1/0.7 # cannot exceed 70%
#wiz.optimize('Min blade mass')

# Some tweaks to help with convergence...

# - this converges: blade mass = 13292.1028188629
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['max_decrease'] = 0.75
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['max_decrease'] = 0.75
#wiz.optimize('Min blade mass')

# -this converges: blade mass = 13054.2240454714
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['max_decrease'] = 0.71
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['max_decrease'] = 0.71
wiz.optimize('Min blade mass')

# - optimization fails (tol=1e-5), even though trends appear convergent
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['max_decrease'] = 0.7
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['max_decrease'] = 0.7
#wiz.optimize('Min blade mass')

# - this does _not_ converge
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['max_decrease'] = 0.667
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['max_decrease'] = 0.667
#wiz.optimize('Min blade mass')

# - this converges with a relaxed tip constraint : blade mass = 12798.5043640817
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['max_decrease'] = 0.667
#wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['max_decrease'] = 0.667
#wiz.aopt['constraints']['blade']['tip_deflection']['margin'] = 1/0.75 # max tip deflection cannot exceed 75%
#wiz.optimize('Min blade mass')


# write the postprocessing script at this point because comparing with the
# tower-optimization output does not work (because RotorSE is turned off)
wiz.write_postproc_script()


# 4. Finally, optimize the tower mass
#
# Apply previous RNA loading
wiz.mopt['WISDEM']['Loading'] = wiz.rna_loading # updated after the last optimize call

# Don't need to use the rotor and drivetrain modules now
wiz.mopt['WISDEM']['RotorSE']['flag'] = False
wiz.mopt['WISDEM']['DriveSE']['flag'] = False
wiz.mopt['WISDEM']['TowerSE']['buckling_method'] = 'dnvgl' # Buckling code type [eurocode or dnvgl]
#wiz.mopt['WISDEM']['TowerSE']['buckling_length'] = 30.0 # Buckling length factor in Eurocode safety check

# Turn off previous optimizations
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ss']['flag'] = False
wiz.aopt['design_variables']['blade']['structure']['spar_cap_ps']['flag'] = False

# Turn on tower optimization
wiz.aopt['merit_figure'] = 'tower_mass'
wiz.aopt['design_variables']['tower']['outer_diameter']['flag'] = True
wiz.aopt['design_variables']['tower']['layer_thickness']['flag'] = True

# Add realistic land-based turbine constraints
wiz.aopt['design_variables']['tower']['outer_diameter']['lower_bound'] = 2.0
wiz.aopt['design_variables']['tower']['outer_diameter']['upper_bound'] = 4.0
wiz.aopt['constraints']['tower']['stress']['flag'] = True
wiz.aopt['constraints']['tower']['global_buckling']['flag'] = True
wiz.aopt['constraints']['tower']['shell_buckling']['flag'] = True
wiz.aopt['constraints']['tower']['d_to_t'] = dict(flag=True,
                                                  lower_bound=80.0,
                                                  upper_bound=500.0)
wiz.aopt['constraints']['tower']['taper'] = dict(flag=True,
                                                 lower_bound=0.2)
wiz.aopt['constraints']['tower']['slope']['flag'] = True

# Additional dynamics constraints
#wiz.aopt['constraints']['tower']['frequency_1']['flag'] = True
#wiz.aopt['constraints']['tower']['frequency_1']['lower_bound'] = 0.270 # 10% over 1P cut-out

wiz.optimize('Min tower mass')

