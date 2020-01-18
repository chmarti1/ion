#!/usr/bin/python3
"""
post5.py
    This is a post-processing code made especially for the 1/15/2020 probe
    bias tests.  It loads the flow rate data and the bias data, and adjusts
    the probe data to be for probe angle.  
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
    
    
target_dir = os.path.join(source_dir, 'post5')
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

ax = lp.init_fig('Wire Angle (rad)', 'Wire Current ($\mu$A)', label_size=16)
ax.grid(True)
ax.set_xlabel('Wire angle (rad)')
ax.set_ylabel('Wire current ($\mu$A)')

styles = ['k', 'k--', 'k-.', 'k:']
style_index = 0

V = []
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
        ax.plot(data[II,0], data[II,2], styles[style_index])
        style_index = (style_index+1)%len(styles)
        
        # Build the I(V) curves
        V.append(float(thisfile[1:3]))
        dtheta = (data[1,0] - data[0,0])/2.
        for index in range(data.shape[0]-1):
            theta_low = data[index,0]-dtheta
            theta_high = data[index,0]+dtheta
            if theta_low <= theta1 and theta_high > theta1:
                I1.append(-data[index,3])
            if theta_low <= theta2 and theta_high > theta2:
                I2.append(-data[index,3])
            

ylim = ax.get_ylim()
ax.vlines([theta1, theta2], ylim[0], ylim[1], color=[.7, .7, .7], ls='--')
ax.get_figure().savefig(os.path.join(target_dir, 'profile.pdf'))

ax = lp.init_fig('Voltage (V)', 'Current ($\mu$A)', label_size=16.)
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True, which='both')

ax.loglog(V, I1, 'ko', mec='k', mfc='w', label='Peak')
ax.loglog(V, I2, 'ks', mec='k', mfc='w', label='Center')

# Make Clements and Smy model projections based on the 20V data
L = .006    # Use wire emersion length of 6mm
U = 75.     # use velocity 75m/s
D = .000254 # wire diameter is .010 inches
# Start with model 1 in dataset 1
n = csprobe.cs1_n(V[1], I1[1]*1e-6/L, U, D)
print('Data set 1, model 1', n)
ax.loglog(V, 1e6*L*csprobe.cs1(V,n,U,D), 'k--', label='Thick Sheath')
# Now use model 2 with dataset 1
n = csprobe.cs2_n(V[1], I1[1]*1e-6/L, U, D)
print('Data set 1, model 2', n)
ax.loglog(V, 1e6*L*csprobe.cs2(V,n,U,D), 'k-', label='Thin Sheath')

# Start with model 1 in dataset 1
n = csprobe.cs1_n(V[1], I2[1]*1e-6/L, U, D)
print('Data set 2, model 1', n)
ax.loglog(V, 1e6*L*csprobe.cs1(V,n,U,D), 'k--')
# Now use model 2 with dataset 1
n = csprobe.cs2_n(V[1], I2[1]*1e-6/L, U, D)
print('Data set 2, model 2', n)
ax.loglog(V, 1e6*L*csprobe.cs2(V,n,U,D), 'k-')

ax.legend(loc=0)

ax.get_figure().savefig(os.path.join(target_dir, 'iv.pdf'))
