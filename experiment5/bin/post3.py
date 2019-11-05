#!/usr/bin/python3

import os,sys
import wiretools as wt
import lplot as lp
import time


# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?


# Identify the data set directory from the command line argument
source_spec = '756'
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

# Has post2 been run on this data set?
post2_dir = os.path.join(source_dir, 'post2')
if not os.path.isdir(source_dir):
    raise Exception('Post2 does not seem to have been run on data set %s\n'%source_dir)

target_dir = os.path.join(source_dir, 'post3')
contents = os.listdir(post2_dir)

# Create the target directory if it doesn't exist
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
elif input('Post 3 results already exist.  Overwrite? (y/n):') == 'y':
    for thisfile in os.listdir(target_dir):
        print('Removing ' + thisfile)
        os.remove(os.path.join(target_dir, thisfile))
else:
    print("Stopping.")
    exit(0)

tstart = time.time()

print("Loading Post 2 matrix results...")
grid = wt.grid_load(post2_dir)
print("Solving...")
grid.solve()
print("Generating plots...")

