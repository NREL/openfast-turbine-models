# WEIS driver

* `weis_driver.dlc1p1_with_wisdem.py` (or `mpi_dlc1p1_with_wisdem.slurm`) will run DLC1.1 for 18
  wind speeds (1 m/s bins) and 6 turbsim seeds to produce a turbulent power curve.
* The OpenFAST model is generated from WISDEM -- note that this does not perform any pitch
  controller optimization and `zeta_pc` and `omega_pc` may need to be adjusted.

