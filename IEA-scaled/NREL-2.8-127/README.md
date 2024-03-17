# NREL-2.8-127
2.8 MW turbine with 127 m diameter rotor, default hub height is 89 m

WISDEM model redesigned with new WisdemInterface and current software stack:

* [IEA Task 37: 3.4 MW RWT](https://github.com/IEAWindTask37/IEA-3.4-130-RWT) (c036f783b160604b133a2e4b7317320fde055743) - includes more comprehensive model data for the reference wind turbine (RWT)
* [WISDEM](https://github.com/WISDEM/WISDEM) v3.13.x (228fb93b0e1c67db23efb705c55512898ebfee6d)
* [WEIS](https://github.com/WISDEM/WEIS) v1.2.x (5076e9d94691b8cc7236440db4a55b8e00569446)

The starting RWT geometry is based on the example provided in the WEIS repository, last modified 2022-07-27 (commit 2c30dff082f6cc9a091da8db8eb2ed2c2bb9728f)

To get started, modifications to the baseline turbine geometry can be shown with
`diff ../IEA-3p4-130-RWT.yaml NREL-2.8-127.start.yaml` inside the "WISDEM" directories.

Differences between the legacy and current OpenFAST models are listed in
[this README](legacy_model_comparison/prev_model_updated_for_OpenFASTv3.5/README.diff).
