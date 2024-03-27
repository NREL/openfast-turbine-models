* `NREL-2.8-127.start.yaml` is the RWT geometry modified tgo have the target turbine specifications

* `mpi_aerostruct_opt.slurm` is the HPC job submission script that runs the following optimizations:

  1. `blade_aerostruct_opt.0.py` -- perform combined aerodynamics and structural optimization for
    LCOE (without a stall constraint)
  2. `blade_aerostruct_opt.1.py`, which starts from the previous converged design and introduces a
    stall constraint
  3. `tower_struct_opt.py`, which then extracts the aerodynamic loading from the rotor-nacelle
    assembly and performs a tower mass minimization (without RotorSE)

* `NREL-2.8-127.yaml` is the final WISDEM turbine geometry after optimizations have been performed

* `OpenFAST` is the resulting turbine model from running WEIS with the final WISDEM geometry.
  Inputs to WEIS are found in `../WEIS`. After an initial WEIS run, the peak thrust shaving was
  further tuned with the `modeling_options.dlc1p1.yaml` found here.
