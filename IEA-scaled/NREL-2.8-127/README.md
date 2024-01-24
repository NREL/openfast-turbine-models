# NREL-2.8-127
2.8 MW turbine with 127 m diameter rotor

WISDEM model redesigned with new WisdemInterface and current software stack:

* [IEA Task 37: 3.4 MW RWT](https://github.com/IEAWindTask37/IEA-3.4-130-RWT) (c036f783b160604b133a2e4b7317320fde055743) - includes more comprehensive model data for the reference wind turbine (RWT)
* [WISDEM](https://github.com/WISDEM/WISDEM) v3.10.0 (64f5ff971d4b9d2191416dae4a854c6e5cb77038)
* [WEIS](https://github.com/WISDEM/WEIS) develop (6f9de4509c159c1e3c517e0d6a4ab8ac59a4909a)

The starting RWT geometry is based on the example provided in the WEIS repository, last modified 2022-07-27 (commit 2c30dff082f6cc9a091da8db8eb2ed2c2bb9728f)

To get started, modifications to the baseline turbine geometry can be shown with
`diff IEA-3.4-130-RWT.yaml NREL-2.8-127.start.yaml` inside the "WISDEM" directory.

Differences between the legacy and current OpenFAST models are listed in
[this README](legacy_model_comparison/prev_model_updated_for_OpenFASTv3.5/README.diff).
