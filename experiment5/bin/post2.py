#!/usr/bin/python
"""
post2.py DATADIR
    Second post-processing step.  Read in post1 data files (p1d) wire
    current as a function of angle and disc position, and generate a
    single post2 data file p2d
    
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
from scipy import sparse
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt
import wiretools as wt
import pool

# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
Nx = 11     # How many x-points
Ny = 11     # How many y-points
delta = 25./Ny  # grid size in mm

# Initialize the grid
grid = wt.Grid(Nx,Ny,delta)


# Define a data processing algorithm for parallelization
# This opens the listed p1dfile and returns its contribution to the
# deconvolution matrix
def _p2proc(p1dfile, grid):
    dims = {'x':0., 'y':0., 'r':25.4*5, 'dw':25.4*.01, 'w':0., 'wstd':0.}
    line = 0
    with open(p1dfile,'r') as ff:
        print(p1dfile)
        # Read in the three dimensional parameters
        thisline = ff.readline()
        line += 1
        while thisline:
            if thisline[0] != '#':
                elements = thisline.split()
                # If the first element is no longer a parameter name
                if not elements[0].isalpha():
                    break
                elif len(elements)!=2:
                    raise Exception('Syntax error on line %d in file %s\n'%(line, p1dfile))
                elif elements[0] not in dims:
                    raise Exception('Unrecognized dimensional parameter, %s, on line %d in file: %s'%(elements[0], line, p1dfile))
                
                try:
                    elements[1] = float(elements[1])
                except:
                    raise Exception('Numerical syntax error on line %d in file %s\n'%(line, p1dfile))
                dims[elements[0]] = elements[1]
                
            thisline = ff.readline()
            line += 1

        r = dims['r']
        x = dims['r'] - dims['x']
        dw = dims['dw']

        while thisline:
            elements = thisline.split()
            try:
                theta = float(elements[0])
                i_uA = float(elements[3])
            except:
                raise Exception('Numerical syntax error on line %d in file %s\n'%(line, p1dfile))
            I = i_uA / np.pi / dw
            # Fold in the data
            grid.add_data(r,x,theta,I)

            thisline = ff.readline()
            line += 1

# Identify the data set directory from the command line argument
source_spec = '4713'
#source_spec = sys.argv[1]
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

# Has post1 been run on this data set?
post1_dir = os.path.join(source_dir, 'post1')
if not os.path.isdir(source_dir):
    raise Exception('Post1 does not seem to have been run on data set %s\n'%source_dir)

target_dir = os.path.join(source_dir, 'post2')
contents = os.listdir(post1_dir)

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif raw_input('Post 2 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(target_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(target_dir, thisfile))
else:
    print("Stopping.")
    exit(0)



pp = pool.Pool()

print('Pre-processing p1d files...')

for thisfile in contents:
    thisid = thisfile.split('.')[0]
    fullfile = os.path.join(post1_dir, thisfile)
    if os.path.isfile(fullfile) and thisfile.endswith('.p1d'):
        pp.add(_p2proc, (fullfile,grid))
        #_p2proc(fullfile, grid)
        
pp.start()
pp.stop()

print('Saving matrices...')
grid.save(target_dir)
