import glob
import ruamel_yaml as ry
import pickle

#
# Case setup
#

def load_yaml(fpath):
    with open(fpath, 'r') as f:
        yaml = ry.YAML().load(f)
    return yaml

def save_yaml(fpath, inputs):
    with open(fpath, 'w') as f:
        yaml = ry.YAML()
        yaml.default_flow_style = None
        yaml.width = float('inf')
        yaml.boolean_representation = ['False', 'True']
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(inputs, f)

def load_pickle(fpath):
    with open(fpath, 'rb') as f:
        p = pickle.load(f)
    return {keyval[0]: keyval[1] for keyval in p}


#
# Analysis
#
def check_blade_freqs(steps,verbose=True):
    """Verify that blade frequencies are higher than rotor frequency
    and that the edgewise frequency is higher than the flapwise
    """
    for istep in steps:
        fpath = glob.glob(f'outputs.{istep}/*.pkl')[0]
        if verbose: print(f'Step {istep}: {fpath}')
        turb = load_pickle(fpath)
        try:
            flapfreqs = turb['wt.rs.frame.flap_mode_freqs']['value']
            edgefreqs = turb['wt.rs.frame.edge_mode_freqs']['value']
        except KeyError:
            if verbose: print('No RotorSE\n')
            continue
        Omg = turb['wt.rp.powercurve.compute_power_curve.rated_Omega']['value'][0]/60.
        if verbose:
            print('  flap mode freqs [Hz]:',flapfreqs)
            print('  edge mode freqs [Hz]:',edgefreqs)
            print('  3P, 6P freqs [Hz]:',3*Omg,6*Omg)
            print('')
            
        # check 1st natural frequencies
        assert (flapfreqs[0] > 1.1*3*Omg), f'WARNING: 1st flap freq too low in step {istep}'
        assert (edgefreqs[0] > flapfreqs[0]), f'WARNING: 1st edge freq less than 1st flap freq in step {istep}'

        # check 2nd natural frequencies
        assert (flapfreqs[1] > 1.1*6*Omg), f'WARNING: 2nd flap freq too low in step {istep}'
        assert (edgefreqs[1] > flapfreqs[1]), f'WARNING: 2nd edge freq less than 2nd flap freq in step {istep}'
        
def check_tower_freqs(steps,verbose=True):
    """Warn if tower is soft-stiff by design"""
    Omg = None
    for istep in steps:
        fpath = glob.glob(f'outputs.{istep}/*.pkl')[0]
        if verbose: print(f'Step {istep}: {fpath}')
        turb = load_pickle(fpath)
        try:
            Omg = turb['wt.rp.powercurve.compute_power_curve.rated_Omega']['value'][0]/60.
        except KeyError:
            if verbose: print('  No RotorSE')
        else:
            if verbose: print('  1P, 3P freqs [Hz]:',1*Omg,3*Omg)
        towerFAfreqs = turb['wt.towerse.post.x_mode_freqs']['value']
        towerSSfreqs = turb['wt.towerse.post.y_mode_freqs']['value']
        if verbose:
            print('  tower fore-aft mode freqs [Hz]:',towerFAfreqs)
            print('  tower side-side mode freqs [Hz]:',towerSSfreqs)
        #assert (towerFAfreqs[0] > Omg), 'WARNING: 1st FA freq too low'
        #assert (towerSSfreqs[0] > Omg), 'WARNING: 1st SS freq too low'
        #assert (towerFAfreqs[0] < 2*Omg), 'WARNING: 1st FA freq too high'
        #assert (towerSSfreqs[0] < 2*Omg), 'WARNING: 1st SS freq too high'
        if (towerFAfreqs[0] < 1.1*Omg):
            print(f'WARNING: 1st FA freq too low in step {istep}')
        if (towerSSfreqs[0] < 1.1*Omg):
            print(f'WARNING: 1st SS freq too low in step {istep}')
        if (towerFAfreqs[0] > 3*Omg):
            print(f'WARNING: 1st FA freq too high in step {istep}')
        if (towerSSfreqs[0] > 3*Omg):
            print(f'WARNING: 1st SS freq too high in step {istep}')
        print('')
