Workflow for generating a scaled turbine model in WISDEM from existing files such as NREL-1.7-103.
Includes list of required WISDEM and driver script updates as of July 2022. Turbines scaled from 1.715 or 1.79 files will not need these changes.

1. Copy existing turbine directory and all subdirectories.
2. Rename new directory.
3. Remove .csv files from previous turbine. These will be regenerated.
4. Find reference turbine data.
5. Remove previous reference turbine from WISDEM subdirectory.
6. Update <turbine_name>.start.yaml:
    - Change name.
    - Update assembly parameters.
    - Update control.supervisory parameters.
7. Update all WISDEM/wisdem_driver files:
    - WISDEM/wisdem_driver.0.py:
        - Update fname_wt_input.
    - WISDEM/wisdem_driver.1.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
    - WISDEM/wisdem_driver.2.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
    - WISDEM/wisdem_driver.3.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
    - WISDEM/wisdem_driver.4.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
        - Update mopt <turbine_name>
    - WISDEM/wisdem_driver.5.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
        - Update mopt <turbine_name>
    - WISDEM/wisdem_driver.6.py:
        - Update fname_wt_input.
        - Update aopt[‘general’][‘fname_output’]
        - Update mopt <turbine_name>.
        - Update pklfile <turbine_name>.
        - Remove ‘.geom’ on lines 62 and 64.
        - Change all ‘value’ to ‘val’.
        - Moment of inertia to ‘towerse.turb.rna_I’.
        - Change ‘pre’ to ‘tower’ on lines 77 and 80.
        - Fix missing towerse.pre.mIxx etc. variables.
8. Run wisdem_driver.sh or mpi_wisdem_driver.slurm
    - Change nDV in wisdem_driver scripts.
        - 8 -> 6
        - 16 -> 11
9. Move <turbine_name> from WISDEM/outputs.6 to /WISDEM directory and rename.
