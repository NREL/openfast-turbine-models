#!/usr/bin/env python
import numpy as np
from scipy.interpolate import make_smoothing_spline

def smooth_geom_twist(s,twist):
    """This is probably pretty ad hoc"""
    # Geom looks good at root and tip, but is wiggly towards the
    # middle, so have the weights at midblade --> 0
    s = np.array(s)
    twist = np.array(twist)
    w = 0.5*(1 + np.cos(2*np.pi*s))
    spl = make_smoothing_spline(s, twist, w=w, lam=0.00005)
    smoo = spl(s)
    return smoo

if __name__ == "__main__":
    import os, sys
    from wisdem_interface.helpers import load_yaml, write_yaml
    import matplotlib.pyplot as plt
    geomfile = sys.argv[1]
    geom = load_yaml(geomfile)
    twist = geom['components']['blade']['outer_shape_bem']['twist']
    s = twist['grid']
    twist0 = twist['values'].copy()
    twist1 = smooth_geom_twist(s,twist0)
    print('smoothed twist:',twist1)
    print('diff:',np.diff(twist1))

    try:
        newgeomfile = sys.argv[2]
    except IndexError:
        pass
    else:
        #twist['values'] = twist1
        # workaround for ruamel.yaml.representer.RepresenterError: cannot represent an object
        for i in range(len(twist1)):
            twist['values'][i] = float(twist1[i])
        write_yaml(geom, newgeomfile)

    plt.plot(s,twist0,label='orig')
    plt.plot(s,twist1,label='smoothed')
    plt.legend(loc='best')
    dpath = os.path.split(geomfile)[0]
    if dpath == '':
        dpath = '.'
    plt.savefig(dpath+'/smoothed_twist.png',bbox_inches='tight')
