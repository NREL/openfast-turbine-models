# WEIS driver

Scripts:

* `mpirun_servo_opt.slurm` calls `weis_driver.servo_opt.py`, followed by
  `weis_driver.dlc1p1.py` with the resulting servo-optimized model
* `weis_driver.servo_opt.py` performs a pitch control optimization based on a
  single wind speed in Region III
* `weis_driver.dlc1p1.py` will run DLC1.1 for 10 wind speeds (with 2 m/s bins)
  and six turbsim seeds to produce a turbulent power curve, using an _existing_
  OpenFAST model
* `weis_driver.dlc1p1_with_wisdem.py` (or `mpirun_dlc1p1_with_wisdem.slurm`)
  will run the same DLC1.1 cases as `weis_driver.dlc1p1.py` but using an
  OpenFAST model generated from WISDEM -- note that this does not perform any
  controls optimization and `zeta_pc` and `omega_pc` should be set appropriately

