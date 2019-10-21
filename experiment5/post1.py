#!/usr/bin/python
"""
POST1
    First post-processing step.  Read in raw current-time data and
    re-map the data to current-angle files while throwing away nonsense
    data.
"""


import os, sys
from os import path
import numpy as np
import matplotlib.pyplot as plt
import lconfig as lc

source_dir = '20191016084713'   # which data set?
use_long = False                 # Use the long or short pulse?

show_start = -0.5
show_stop = 0.5

source_dir = os.path.abspath(source_dir)
target_dir = os.path.join(source_dir, 'post1')
contents = os.listdir(source_dir)

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif raw_input('Post 1 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(target_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(target_dir, thisfile))
else:
    print("Stopping.")
    exit(0)



for thisfile in contents:
    fullfile = os.path.join(source_dir, thisfile)
    #thisfile = os.path.join(target_dir, '084.dat')
    if os.path.isfile(fullfile) and thisfile.endswith('.dat'):
        print(thisfile)
        thisid = thisfile.split('.')[0]
        d = lc.LConf(fullfile, data=True, cal=True, dibits=True)
        #theta_edge = (d.get_meta(0,'theta') % 360.) - 360.
        theta_edge = -188. * np.pi / 180
        
        i_rising = d.get_dievents(0, edge='rising')
        i_falling = d.get_dievents(0, edge='falling')
        # Trim the falling and rising arrays
        while i_falling[0] < i_rising[0]:
            del i_falling[0]
        while len(i_rising) > len(i_falling):
            del i_rising[-1]
        # Downselect the rising edges
        if (i_falling[0]-i_rising[0] > i_falling[1]-i_rising[1]) is use_long:
            i_start = 0
        else:
            i_start = 1
        i_rising = i_rising[i_start::2]
        
        # Produce an angle signal
        theta = np.ndarray((d.ndata(),), dtype=float)
        
        # Extrapolate to establish the first samples
        dt = 2*np.pi / (i_rising[1] - i_rising[0])
        i_start = (i_rising[1] - 2*i_rising[0])
        i_stop = (i_rising[1] - i_rising[0])
        theta[:i_rising[0]] = theta_edge + dt*np.arange(i_start,i_stop)
        # Loop through all full disc rotations
        for ii in range(len(i_rising)-1):
            dt = 2*np.pi / (i_rising[ii+1] - i_rising[ii])
            theta[i_rising[ii]:i_rising[ii+1]] = theta_edge + dt* np.arange(i_rising[ii+1]-i_rising[ii])
        # Extrapolate to establish the final samples
        dt = 2*np.pi / (i_rising[-1] - i_rising[-2])
        i_stop = d.ndata()-i_rising[-1]
        theta[i_rising[-1]:] = theta_edge + dt*np.arange(0,i_stop)
        
        # Write the data
        outfile = os.path.join(target_dir, thisid+'.p1d')
        with open(outfile,'w') as ff:
            ff.write('x %f\n'%d.get_meta(0,'x'))
            #ff.write('y %f\n'%d.get_meta(0,'y'))
            #ff.write('wire_length %f\n'%d.get_meta(0,'wire_length'))
            for tt, ii in zip(theta, d.get_channel(0)):
                ff.write('%.6f\t%.6f\n'%(tt,ii))
        
        I = np.logical_and(theta > show_start, theta < show_stop)
        f = plt.figure(1)
        f.clf()
        f.set_size_inches(8,4)
        ax = f.add_subplot(111)
        ax.plot(theta[I], d.get_channel(0)[I], '.')
        ax.set_xlabel('Angle (radians)')
        ax.set_ylabel('Signal ($\mu$A)')
        f.savefig(os.path.join(target_dir, thisid+'.png'))
