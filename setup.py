from setuptools import setup, find_packages

setup(
    name='WISDEMInterface',
    version='0.0.1',
    url='https://github.com/NREL/openfast-turbine-models.git',
    author='Eliot Quon',
    author_email='Eliot.Quon@nrel.gov',
    description='An interface for WISDEM that facilitates running design optimization sequences',
    packages=['wisdem_interface'],
    install_requires=[],
)
