import numpy as np
import pandas as pd
import os, platform
import pyFAST.linearization.linearization as lin
# import pyFAST.linearization.LinearModel as lin_mod
import pyFAST.case_generation.case_gen as case_gen
import pyFAST.input_output.fast_output_file as fo
import sys
import pyFAST.case_generation.runner as runner
# from pCrunch.Analysis import Loads_Analysis
import yaml
import scipy as sp


on_login_node = platform.node() in ['el'+str(m) for m in range(10)]
on_dav_node = platform.node() in ['ed'+str(m) for m in range(10)]
parallel_flag = (os.cpu_count() >= 16) and (not on_login_node) and (not on_dav_node)


def run_linearization():
    """ Example to run a set of OpenFAST simulations (linearizations)

    This script uses a reference directory (`ref_dir`) which contains a reference input file (.fst)
    1) The reference directory is copied to a working directory (`out_dir`).
    2) All the fast input files are generated in this directory based on a list of dictionaries (`PARAMS`).
    For each dictionary in this list:
       - The keys are "path" to a input parameter, e.g. `EDFile|RotSpeed`  or `FAST|TMax`.
         These should correspond to the variables used in the FAST inputs files.
       - The values are the values corresponding to this parameter
    For instance:
         PARAMS[0]['DT']                    = 0.01
         PARAMS[0]['EDFile|RotSpeed']       = 5
         PARAMS[0]['InflowFile|HWindSpeed'] = 10

    3) The simulations are run, successively distributed on `nCores` CPUs.
    4) The output files are read, and averaged based on a method (e.g. average over a set of periods,
        see averagePostPro in postpro for the different averaging methods).
       A pandas DataFrame is returned

    """
    # --- Parameters for this script
    of_dir           = '/home/equon/WEIS/local'
    this_dir         = os.path.dirname(__file__)
    ref_dir          = '../OpenFAST'   # Folder where the fast input files are located (will be copied)
    out_dir          = os.path.join(this_dir,'outputs')     # Output folder (will be created)
    main_file        = 'NREL-2p3-107.fst'  # Main file in ref_dir, used as a template
    FAST_EXE         = os.path.join(of_dir,'bin/openfast') # Location of a FAST exe (and dll)

    # --- Read outputs from OF power curve to get operating points (EWQ)
    #op = pd.read_csv('../NREL-2.5-116_openfast.csv').set_index('Wind1VelX_[m/s]')
    op = pd.read_csv('../NREL-2.3-107_openfast.csv').set_index('rotor speed [RPM]')
    op = op.loc[op['Wind1VelX_[m/s]'] <= 11]
    GenTorque = op['generator torque [kN-m]'] * 1000.
    minRotSpeed = op.index[0]

    # --- Defining the parametric study  (list of dictionnaries with keys as FAST parameters)
    LinStart = 600.0
    BaseDict = {'TMax': 660.0}
    BaseDict = case_gen.paramsLinearTrim(BaseDict)   # Run linear trim case
    print(BaseDict)

    RotSpeeds = np.arange(0,16)

    PARAMS=[]
    for i,rpm in enumerate(RotSpeeds): 
        p=BaseDict.copy()

        GenTq = np.interp(rpm, GenTorque.index, GenTorque, left=1e-9)

        # Turn off aero
        p['CompAero']   = 0
        p['CompInflow'] = 0
        
        # Turn on all pertinent structural DOFs
        p['EDFile|FlapDOF1'] = 'True'
        p['EDFile|FlapDOF2'] = 'True'
        p['EDFile|EdgeDOF'] = 'True'
        p['EDFile|DrTrDOF'] = 'True'
        p['EDFile|GenDOF'] = 'False' #'True'
        p['EDFile|TwFADOF1'] = 'True'
        p['EDFile|TwFADOF2'] = 'True'
        p['EDFile|TwSSDOF1'] = 'True'
        p['EDFile|TwSSDOF2'] = 'True'

        # rated generator speed, torque, control params
        #p['ServoFile|VS_RtGnSp'] = 1429.36707 * .9 # Rated generator speed [RPM]
        #p['ServoFile|VS_RtTq'] = 12389.06909 # Rated torque, from DISCON.IN [Nm]
        #p['ServoFile|VS_Rgn2K'] = 0.006851918024 # Generator torque const, from DISCON.IN [Nm/RPM^2]
        #p['ServoFile|VS_SlPc']   = 10.

        # const generator torque
        # https://github.com/OpenFAST/openfast/issues/478#issuecomment-649819664
        #p['ServoFile|VS_RtTq'] = np.interp(rpm, GenTorque.index, GenTorque, left=1e-9)
        p['ServoFile|VS_RtTq'] = GenTq
        p['ServoFile|VS_RtGnSp'] = 1e-9
        p['ServoFile|VS_Rgn2K'] = 1e-9
        p['ServoFile|VS_SlPc'] = 1e-9

        # Operating conditions
        p['EDFile|RotSpeed'] = rpm
        p['EDFile|BlPitch(1)'] = 0.0
        p['EDFile|BlPitch(2)'] = 0.0
        p['EDFile|BlPitch(3)'] = 0.0

        # Set number of linearizations
        #p['TrimCase'] = 2
        p['CalcSteady'] = 'False'
        #p['OutFmt'] = 'E20.12'
        if rpm > 0:
            p['NLinTimes'] = 36
            LinTimes = np.linspace(LinStart, LinStart+60./rpm, num=p['NLinTimes'], endpoint=False)
            p['LinTimes'] = np.array_str(LinTimes, max_line_width=9000, precision=3)[1:-1]
        else:
            p['NLinTimes'] = 1
            p['LinTimes'] = f'{LinStart:.3f}'
            p['TMax'] = LinStart

        # Set case name
        p['__name__'] = f'{i:03d}_{rpm:.1f}rpm'
        PARAMS.append(p)

    # --- Generating all files in a output directory
    fastfiles=case_gen.templateReplace(PARAMS,ref_dir,outputDir=out_dir,removeRefSubFiles=True,main_file=main_file, oneSimPerDir=False)
    print(fastfiles)

    # --- Creating a batch script just in case
    #runner.writeBatch(os.path.join(out_dir,'_RUN_ALL.bat'),fastfiles,fastExe=FAST_EXE)

    # --- Running the simulations
    if parallel_flag:
        nCores = min(len(RotSpeeds), os.cpu_count())
        runner.run_fastfiles(fastfiles,fastExe=FAST_EXE,parallel=True,showOutputs=True,nCores=nCores)
    else:
        #runner.run_fastfiles(fastfiles,fastExe=FAST_EXE,parallel=False,showOutputs=True) # causes error when calling wait()
        runner.run_fastfiles(fastfiles,fastExe=FAST_EXE,parallel=True,showOutputs=True,nCores=1)

    # --- Simple Postprocessing
    # (averaging each signal over the last period for each simulation)
    outFiles = [os.path.splitext(f)[0]+'.outb' for f in fastfiles]
    # avg_results = postpro.averagePostPro(outFiles, avgMethod='periods', avgParam=1, ColMap = {'WS_[m/s]':'Wind1VelX_[m/s]'},ColSort='WS_[m/s]')
    # avg_results.drop('Time_[s]',axis=1, inplace=True)

    return outFiles



if __name__ == '__main__':
    print('on eagle login node:',on_login_node)
    print('on eagle DAV node:',on_dav_node)
    print('is parallel run:',parallel_flag)

    # 1. Run linearizations
    outfiles = run_linearization()

    # 2. Do MBC
    MBC = lin.run_pyMBC(outfiles)

    # Check natural frequencies against matlab
    all_nat_freq = []
    for mbc in MBC:
        eigs = sp.linalg.eig(mbc['AvgA'])[0]
        nat_freq_hz = (np.abs(eigs)/2/np.pi)
        nat_freq_hz.sort()
        all_nat_freq.append(nat_freq_hz)
        print('Natural Freqs. (hz): {}'.format(nat_freq_hz))

    np.savetxt('MBC_natural_frequencies.csv', np.array(all_nat_freq), delimiter=',')
