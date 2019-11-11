#!/usr/bin/python3
"""
post1.py DATADIR
    First post-processing step.  Read in raw current-time data and
    re-map the data to current-angle files while throwing away nonsense
    data.  The results are discovered in ../data/DATADIR/ and the results
    are stored in ../DATADIR/post1/.  Results are plain text post1 data
    files (*.p1d) and png plots of the data.
    
    For ease of use, the DATADIR may be specified merely by its trailing
    characters.  For example, data in a directory named '20191024143210'
    may be specified by the command
        $ post1.py 143210
    If multiple directories are discovered with the trailing characters
    '143210', then an exception is raise.
"""


import os, sys
from os import path
import numpy as np
import matplotlib.pyplot as plt
import lconfig as lc
import multiprocessing as mp
import time

# These are options that you might want to change before running this script...
use_long = False        # Use the long or short pulse when finding the angle offset?
data_dir = '../data'    # Where are the data?
theta_start = -0.3       # Exclude data not between theta_start and theta_stop
theta_step = .001        # Organize the data into bins theta_step wide
theta_stop = 0.3

def _p1proc(fullfile):
    thisfile = os.path.split(fullfile)[1]
    thisid = thisfile.split('.')[0]
    
    print(thisfile)
    
    d = lc.LConf(fullfile, data=True, cal=True, dibits=True)
    theta_edge = -d.get_meta(0,'theta')
    #theta_edge = -188. * np.pi / 180
    
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
    
    # Initialize a list of angular velocity measurements
    w_rads = []
    # grab the current data
    current_uA = d.get_channel(0)
    # Make a theta array
    theta = np.arange(theta_start, theta_stop, theta_step)
    current_bins = [list() for th in theta]
    
    for ii in range(len(i_rising)-1):
        dth = 2*np.pi / (i_rising[ii+1] - i_rising[ii])
        w_rads.append(d.get(0,'samplehz')*dth)
        for th, thisbin in zip(theta, current_bins):
            i_start_off = int(np.ceil((th - theta_edge - 0.5*theta_step)/ dth))
            i_stop_off = int(np.ceil((th - theta_edge + 0.5*theta_step)/ dth))
            thisbin += list(current_uA[i_rising[ii]+i_start_off:i_rising[ii]+i_stop_off])
        
    # Write the data
    f = plt.figure(1)
    f.clf()
    f.set_size_inches(8,4)
    ax = f.add_subplot(111)
    outfile = os.path.join(target_dir, thisid+'.p1d')
    with open(outfile,'w') as ff:
        ff.write('x %f\n'%d.get_meta(0,'x'))
        ff.write('y %f\n'%d.get_meta(0,'y'))
        ff.write('r %f\n'%d.get_meta(0,'r'))
        #ff.write('dw %f\n'%d.get_meta(0,'wire_diameter'))
        ff.write('dw .254\n')
        ff.write('w %f\n'%np.mean(w_rads))
        ff.write('wstd %f\n'%np.std(w_rads))
        ff.write('# theta(rad)\tcount\tmean(uA)\tmedian(uA)\tstd dev(uA)\n')
        for th, thisbin in zip(theta,current_bins):
            count = len(thisbin)
            if count:
                mean = np.mean(thisbin)
                median = np.median(thisbin)
                std = np.std(thisbin)
            else:
                mean = 0.
                median = 0.
                std = 0.
            ff.write('%f\t%d\t%f\t%f\t%f\n'%(th, count, mean, median, std))
            ax.plot(np.full((len(thisbin),), th), thisbin, 'b.')
            ax.plot(th, mean, 'g.')
            ax.plot(th, median, 'r.')
        


    ax.grid(True)
    ax.set_xlabel('Angle (radians)')
    ax.set_ylabel('Signal ($\mu$A)')
    f.savefig(os.path.join(target_dir, thisid+'.png'))



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
    
#source_dir = '../data/20191016084713'   # which data set?

target_dir = os.path.join(source_dir, 'post1')
contents = os.listdir(source_dir)

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif input('Post 1 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(target_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(target_dir, thisfile))
else:
    print("Stopping.")
    exit(0)

tstart = time.time()

pool = mp.Pool(mp.cpu_count())

for thisfile in contents:
    fullfile = os.path.join(source_dir, thisfile)
    #thisfile = os.path.join(target_dir, '084.dat')
    if os.path.isfile(fullfile) and thisfile.endswith('.dat'):
        pool.apply_async(_p1proc, args=(fullfile,))
        #_p1proc(fullfile)
    
pool.close()
pool.join()

tstop = time.time()
print('Done.')
print('The process took %f seconds.'%(tstop-tstart))
