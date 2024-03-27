* `NREL-2.8-127.start.yaml` is the RWT geometry modified tgo have the target turbine specifications

* `mpi_aerostruct_opt.slurm` is the HPC job submission script that runs the following optimizations:

  1. `blade_aerostruct_opt.0.py` -- perform combined aerodynamics and structural optimization for
    LCOE (without a stall constraint)
  2. `blade_aerostruct_opt.1.py`, which starts from the previous converged design and introduces a
    stall constraint
  3. `tower_struct_opt.py`, which then extracts the aerodynamic loading from the rotor-nacelle
    assembly and performs a tower mass minimization (without RotorSE)

* Note that the design workflow in `with_smoothing` includes an additional step to smooth the blade
  twist distribution after the initial aerostructural optimization to make it monotonic; a
  subsequent optimization is performed with twist optimization turned off to converge the design
  with the adjusted twist profile.

* `NREL-2.8-127.yaml` is the final WISDEM turbine geometry after optimizations have been performed
  (without smoothing the blade twist distribution)

* `OpenFAST` is the resulting turbine model from running WEIS with the final WISDEM geometry.
  Inputs to WEIS are found in `../WEIS`. After an initial WEIS run, the peak thrust shaving was
  further tuned with the `modeling_options.dlc1p1.yaml` found here.
