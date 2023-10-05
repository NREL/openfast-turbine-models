# OpenFAST Turbine Models

This repository contains turbine aeroservoelastic models developed for research activities at the National Renewable Energy Laboratory (NREL). 

NREL researchers should refer to the internal repository at https://github.nrel.gov/NWTC/openfast-turbine-models.

## Overview of Design Process
The design process involves rescaling an existing reference wind turbine (RWT) to have specified turbine characteristics and then optimizing the resulting geometry.

### Software Stack

* [WISDEM](https://wisdem.readthedocs.io) -- uses OpenMDAO to optimize a turbine geometry for realistic aeroelastic performance subject to appropriate system constraints; includes numerous submodels, e.g., CCBlade for blade-element momentum theory aerodynamic analysis and pyFrame3DD for structural analysis
* [WEIS](https://weis.readthedocs.io) -- performs multi-fidelity co-design with a time-domain aeroservo[hydro]elastic solver, OpenFAST, in the loop
* [OpenFAST](https://openfast.readthedocs.io) -- individual turbine or wind-farm model (FAST.Farm); can simulate steady or turbulent inflow; structural analysis may be performed by ElastoDyn (Euler-Bernoulli beam theory) or BeamDyn (geometrically exact beam theory)
* [ROSCO](https://rosco.readthedocs.io/) -- reference open-source controller that may be used in OpenFAST (specified as a "Bladed-style DLL" controller in ServoDyn); when compiled, produces a libdiscon.so controller that uses a specified DISCON.IN file

### Input/Outputs

* Inputs to WISDEM include a universal geometry file (described [here](https://windio.readthedocs.io)) in YAML format, analysis options file (described [here](https://wisdem.readthedocs.io/en/master/inputs/analysis_schema.html#), and a modeling options file (described [here](https://wisdem.readthedocs.io/en/master/inputs/modeling_schema.html#)).

	* Every time WISDEM is run, a new geometry YAML file is produced.
	* WISDEM may be run without any optimizations turned on in order to access all the derived quantities of interest (a full list of outputs is found [here](https://wisdem.readthedocs.io/en/master/outputs.html)).

* Inputs to WEIS are similar to WISDEM, including geometry, analysis options, and modeling options YAML files. Outputs include OpenFAST time-domain simulation data and necessarily include a functional OpenFAST model (that may be independently run, outside of WEIS).

## Getting Started

The design process depends on the tools in the [WISDEM Interface](https://github.com/ewquon/WisdemInterface) package. Users should start by installing [WISDEM](https://github.com/WISDEM/WISDEM) and [WEIS (develop)](https://github.com/wisdem/weis/tree/develop) in separate clean Python environments. While WEIS depends on WISDEM, the current develop branch tracks an older version of WISDEM and using the latest stable version of WISDEM is not a bad idea. In addition, WiSDEM and WEIS have different dependencies, so the package will be easier to install if conda/mamba does not need to resolve all dependencies simultaneously. The use of [mamba](https://github.com/conda-forge/miniforge#mambaforge) is recommended as it is both more robust (at solving for package dependencies) and is computationally much more efficient. 

The WISDEM workflow is generally as follows:

1. Identify an appropriate starting turbine geometry (e.g., an IEA RWT)
2. Update turbine geometry file with known properties (e.g., rated power, hub height, rotor speed range, ...)
3. Run `design_workflow.py` or submit `mpi_design_workflow.slurm` (appropriately modified for your high-performance computing environment) to your job scheduler
4. Run the resulting `compare_TURBINENAME_designs.py`, verify convergence of optimization steps and sanity check the resulting optimized turbine properties.
5. Adjust optimization parameters in `design_workflow.py` and re-run if needed.

Using the resulting optimized turbine geometry from WISDEM, the WEIS workflow is generally as follows *-- workflow under development*:

1. Run a power-curve sweep, verify that WISDEM performance can be replicated
2. Optimize the ROSCO pitch controller
3. Run additional design load cases for additional sanity checks

As a final step, designers may wish to linearize the openfast model determine eigenvalues for a detailed structural dynamics analysis.
