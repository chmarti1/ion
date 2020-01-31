#!/usr/bin/python3

import os,sys
import wiretools as wt
import lplot as lp
import lconfig as lc
import time


# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
U = 75.
D = .000254
V = None

# Identify the data set directory from the command line argument
#source_spec = '756'
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

# If the bias voltage is not explicitly specified, determine it from the
# raw data files and adjust it for the voltage divider in the isoshunt
if V is None:
    dd = lc.LConf(os.path.join(source_dir,'000.dat'))
    V = 0.9166*dd.get_meta(0,'vwire')


# Has post2 been run on this data set?
post2_dir = os.path.join(source_dir, 'post2')
if not os.path.isdir(source_dir):
    raise Exception('Post2 does not seem to have been run on data set %s\n'%source_dir)

target_dir = os.path.join(source_dir, 'post3')
contents = os.listdir(post2_dir)

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif not input('Post 3 results already exist.  Risk overwriteing? (y/n):') == 'y':
    print("Stopping.")
    exit(0)

tstart = time.time()

print("Loading Post 2 matrix results...")
grid = wt.grid_load(post2_dir)
print("Generating plots...")
target = os.path.join(target_dir, 'pcolor.png')
grid.density(V,U,D)
ax = grid.pseudocolor(savefig=target, vscale=(0,3e18), values=1)
#ax = grid.pseudocolor(savefig=target, vscale=(0,7), values=1)

