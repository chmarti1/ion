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
theta1 = .0183
theta2 = .0345

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
    
    
target_dir = os.path.join(source_dir, 'post6')
source_dir = os.path.join(source_dir, 'post1')
contents = os.listdir(source_dir)

# Check for post 1 results
if not os.path.isdir(source_dir):
    raise Exception('Post 1 results do not seem to exist for this data set.')

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif input('Post 5 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(target_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(target_dir, thisfile))
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

ax2 = lp.init_fig('z (mm)', 'I ($\mu$A)', label_size=16, 
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.grid(True, which='both')

styles = ['k', 'k--', 'k-.', 'k:']
style_index = 0

Z = []
I1 = []
I2 = []

contents = os.listdir(source_dir)
contents.sort()
for thisfile in contents:
    if thisfile.endswith('.p1d'):
        data = []
        with open(os.path.join(source_dir, thisfile), 'r') as ff:
            # Throw away the header
            thisline = ff.readline()
            while thisline[0]!='#':
                thisline = ff.readline()
            thisline = ff.readline()
            while thisline:
                data.append([float(xx) for xx in thisline.split()])
                thisline = ff.readline()
        data = np.asarray(data)
        II = np.logical_and( data[:,0] > theta_start,\
                data[:,0] < theta_stop)
        ax1.plot(data[II,0], data[II,2], styles[style_index])
        style_index = (style_index+1)%len(styles)
        
        # Build the I(Z) curves
        Z.append(dims['y'])
        dtheta = (data[1,0] - data[0,0])/2.
        for index in range(data.shape[0]-1):
            theta_low = data[index,0]-dtheta
            theta_high = data[index,0]+dtheta
            if theta_low <= theta1 and theta_high > theta1:
                I1.append(-data[index,3])
            if theta_low <= theta2 and theta_high > theta2:
                I2.append(-data[index,3])

ylim = ax.get_ylim()
ax1.vlines([theta1, theta2], ylim[0], ylim[1], color=[.7, .7, .7], ls='--')
ax1.get_figure().savefig(os.path.join(target_dir, 'profile.pdf'))

ax2.loglog(Z, I1, 'ko', mec='k', mfc='w', label='Peak')
ax2.loglog(Z, I2, 'ks', mec='k', mfc='w', label='Center')
ax2.get_figure().savefig(os.path.join(target_dir, 'iz.pdf')
