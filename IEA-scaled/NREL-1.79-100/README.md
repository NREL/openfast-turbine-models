# NREL-1.79-100
_1.79 MW turbine with 100 m diameter rotor, default hub height is 80 m_

**AWAKEN modelers should use the OpenFAST model**

The WISDEM model was designed with the following software stack:

* [WISDEM](https://github.com/WISDEM/WISDEM) v3.13.x (0b6469c2ab9a453762cd98057a2cc5383a0b0a25, ran on NREL Kestrel HPC)
* [WEIS](https://github.com/WISDEM/WEIS) v1.2.x (965de6abfdb6ab1d45779c5a6eafbd23a7a23b98, ran on NREL Kestrel HPC)
* [OpenFAST](https://github.com/OpenFAST/openfast) v3.5.2 (6a7a543790f3cad4a65b87242a619ac5b34b4c0f ran on NREL Kestrel HPC)
* [ROSCO](https://github.com/NREL/ROSCOA) v2.9.0 (e95511cbc2f4401df8a8fc2112c7c70de69fe5e8)

The starting RWT geometry is based on the NREL-2.3-116 model

To get started, modifications to the baseline turbine geometry can be shown with
`diff ../NREL-2.3-116.yaml NREL-1.79-100.start.yaml` inside the design directories.

The final geometry was designed in two steps:

1. Complete aerostructural optimization, but without stall margin constraint
2. Repeat with stall margin constrained to >= 3 deg

Details are provided in Quon et al., 2024, _Design of Wind Turbine Models for the American WAKE ExperimeNt (AWAKEN)_ -- manuscript in preparation.