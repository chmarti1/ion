#!/usr/bin/python3
"""
post6.py
    This is a post-processing code for vertical full-emersion scans of the flame.
    In these tests, the wire is emersed fully in the flame and moved vertically
    rather than horizontally.  These tests make no attempt to fully resolve the
    flame cross-seciton, but permit quick and precise measurements of cross-
    secitonal mean ion density.
"""


import os, sys
from os import path
import numpy as np
import matplotlib.pyplot as plt
import lconfig as lc
import lplot as lp
import multiprocessing as mp
import time
import csprobe

lp.set_defaults(font_size=16, legend_font_size=16.)

# These are options that you might want to change before running this script...
use_long = True        # Use the long or short pulse when finding the angle offset?
data_dir = '../data'    # Where are the data?
theta_start = -0.03       # Exclude data not between theta_start and theta_stop
theta_stop = 0.1
theta1 = .025
theta2 = .038
z_start = 6.        # Perform the slope fit starting at z=?

# Identify the data set directory from the command line argument
source_spec = sys.argv[1]
# List all available data directories
contents = os.listdir(data_dir)
source_dir = None
# Any data set that ends with (or is identical to) the character set
# provided by the user is a candidate.  If there are multiple candidates
# then the source_spec is ambiguous, and we need to raise an error
for this in contents:
    if this.endswith(source_spec):
        if source_dir:
            raise Exception('There were muliple data sets consistent with the source specifier: %s'%source_spec)
        source_dir = os.path.abspath(os.path.join(data_dir, this))
        
if source_dir is None:
    raise Exception('Did not file a data set ending in %s'%source_spec)
    
    
post6_dir = os.path.join(source_dir, 'post6')
post1_dir = os.path.join(source_dir, 'post1')
contents = os.listdir(source_dir)

# Check for post 1 results
if not os.path.isdir(source_dir):
    raise Exception('Post 1 results do not seem to exist for this data set.')

# Create the target directory if it doesn't exist
if not os.path.isdir(post6_dir):
    os.mkdir(post6_dir)
elif input('Post 5 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(post6_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(post6_dir, thisfile))
else:
    print("Stopping.")
    exit(0)


def _load_post1(filename):
    dims = {'x':0., 'y':0., 'r':25.4*5, 'dw':25.4*.01, 'w':0., 'wstd':0.}
    data = []
    line = 0
    with open(filename,'r') as ff:
        p1d = ff.readlines()
    # Read in the header until a numerical value is found in place of a parameter
    # name
    header = True
    for line,thisline in enumerate(p1d):
        elements = thisline.split()
        if header:
            if len(thisline)==0 or thisline[0] == '#':
                pass
            # If the first element is no longer a parameter name
            elif not elements[0].isalpha():
                header = False
            elif len(elements)!=2:
                raise Exception('Syntax error on line %d in file %s\n'%(line, p1dfile))
            elif elements[0] not in dims:
                raise Exception('Unrecognized dimensional parameter, %s, on line %d in file: %s'%(elements[0], line, p1dfile))
            else:
                try:
                    elements[1] = float(elements[1])
                except:
                    raise Exception('Numerical syntax error on line %d in file %s\n'%(line, p1dfile))
                dims[elements[0]] = elements[1]
        # Not using an if/else scheme allows allows the algorithm to continue
        # on the first line where the header is found to end.
        if not header:
            if thisline[0] != '#':
                try:
                    data.append([float(this) for this in elements])
                except:
                    raise Exception('Data format error on line %d in file %s\n  %s\n'%(line, filename, thisline))
    return dims, data

ax1 = lp.init_fig('Wire Angle (rad)', 'Wire Current ($\mu$A)', label_size=16)
ax1.grid(True)

ax2 = lp.init_fig('z (mm)', '$I^{-4/3}$ ($\mu$A$^{-4/3}$)', label_size=16)
ax2.grid(True, which='both')

styles = ['k', 'k--', 'k-.', 'k:']
style_index = 0

Z = []
I1 = []
I2 = []

contents = os.listdir(post1_dir)
contents.sort()
for thisfile in contents:
    if thisfile.endswith('.p1d'):
        dims, data = _load_post1(os.path.join(post1_dir, thisfile))
        data = np.asarray(data)
        II = np.logical_and( data[:,0] > theta_start,\
                data[:,0] < theta_stop)
        ax1.plot(data[II,0], data[II,2], styles[style_index])
        style_index = (style_index+1)%len(styles)
        
        # Build the I(Z) curves
        Z.append(dims['y'])
        # Calculate where the theta indices may be found
        dtheta = (data[1,0] - data[0,0])
        index = int((theta1 - data[0,0] - 0.5*dtheta)//dtheta)
        I1.append(-data[index,3])
        index = int((theta2 - data[0,0] - 0.5*dtheta)//dtheta)
        I2.append(-data[index,3])
        
Z = np.asarray(Z, dtype=float)
I1 = np.asarray(I1, dtype=float)
I2 = np.asarray(I2, dtype=float)

index = Z >= z_start
C = np.polyfit(Z[index],I1[index]**(-1.3333),1)
c0 = C[1]
c1 = C[0]

# Check flow rates
data = lc.LConf(os.path.join(source_dir,'flow.pre'), data=True, cal=True)
fg_pre = np.mean(data.get_channel(0))
o2_pre = np.mean(data.get_channel(1))

data = lc.LConf(os.path.join(source_dir,'flow.post'), data=True, cal=True)
fg_post = np.mean(data.get_channel(0))
o2_post = np.mean(data.get_channel(1))

# Generate output files
# Profile plots
ylim = ax1.get_ylim()
ax1.vlines([theta1, theta2], ylim[0], ylim[1], color=[.7, .7, .7], ls='--')
ax1.get_figure().savefig(os.path.join(post6_dir, 'profile.pdf'))
# I vs Z plots
ax2.plot(Z[index], c0 + Z[index] * c1, 'k-')
ax2.plot(Z, I1**(-1.3333), 'ko', mec='k', mfc='w', label='Peak')
ax2.plot(Z, I2**(-1.3333), 'ks', mec='k', mfc='w', label='Center')
ax2.legend(loc=0)
ax2.get_figure().savefig(os.path.join(post6_dir, 'iz.pdf'))
# Analysis plot
with open(os.path.join(post6_dir, 'post6.dat'),'w') as df:
    df.write('fg_pre_scfh %.4f\n'%fg_pre)
    df.write('o2_pre_scfh %.4f\n'%o2_pre)
    df.write('fg_post_scfh %.4f\n'%fg_post)
    df.write('o2_post_scfh %.4f\n'%o2_post)
    df.write('total_scfh %.4f\n'%(fg_pre + o2_pre))
    df.write('ratio_fo %.6f\n'%(fg_pre / o2_pre))
    df.write('c0 %.8e\n'%c0)
    df.write('c1 %.8e\n'%c1)
    df.write('Uc1 %.8e\n'%(c1 * (fg_pre + o2_pre)))
