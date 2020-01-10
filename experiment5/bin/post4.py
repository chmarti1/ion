#!/usr/bin/python3

import os, sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


import os,sys
import wiretools as wt
import lconfig as lc
import lplot as lp
import time


# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
vscale = (0., 7.)
window = [7., -2. ,17., 8.]

# List all available data directories
contents = os.listdir(data_dir)
# Any data set that ends with (or is identical to) the character set
# provided by the user is a candidate.  If there are multiple candidates
# then the source_spec is ambiguous, and we need to raise an error
# Loop through the sources specified at the command line; translate each into
# a full path
source_list = []
for source_spec in sys.argv[1:]:
    for this in contents:
        if this.endswith(source_spec):
            source_dir = None
            if source_dir:
                raise Exception('There were muliple data sets consistent with the source specifier: %s'%source_spec)
            source_dir = os.path.abspath(os.path.join(data_dir, this))
    if source_dir is None:
        raise Exception('Did not file a data set ending in %s'%source_spec)
    source_list.append(source_dir)

    # Has post2 been run on this data set?
    post2_dir = os.path.join(source_dir, 'post2')
    if not os.path.isdir(source_dir):
        raise Exception('Post2 does not seem to have been run on data set %s\n'%source_dir)


# Now that we've checked the source directories, let's start building the plots
tstart = time.localtime()
# What are the output files?
target = os.path.abspath('../post4.pdf')
target_summary = os.path.abspath('../post4.txt')

fig = plt.figure()
nplots = len(source_list)
nhorizontal = min(nplots,3)
nvertical = nplots // nhorizontal + 1

fig.set_size_inches([4.*nhorizontal, 4.*nvertical])
axes = []
with open(target_summary, 'w') as sumff:
    for index, source_dir in enumerate(source_list):
        # Get the z-height from one of the data files
        dat = os.path.join(source_dir, '000.dat')
        dd = lc.LConf(dat, data=False)
        z = dd.get_meta(0,'y')
        
        post2_dir = os.path.join(source_dir, 'post2')
        sumff.write(source_dir + '\n')
        print(source_dir)
        print("Loading Post 2 matrix results...")
        grid = wt.grid_load(post2_dir)
        
        ax = fig.add_subplot(nvertical,nhorizontal,index+1)
        axes.append(ax)
        #h =grid.pseudocolor(ax=ax, vscale=vscale, colorbar=False)
        pscargs = {'ax':ax, 'vscale':vscale, 'window':window, 'colorbar':False, 'xlabel':None, 'ylabel':None, 'title':'z=%.1fmm'%z}
        # If this is the first plot in the row
        if index % nhorizontal == 0:
            pscargs['ylabel'] = 'y (mm)'
        # If this is the last plot in the column
        if (index // nhorizontal) + 1 == nvertical:
            pscargs['xlabel'] = 'x (mm)'
        # If this is the last plot in the first row
        if index+1 == nhorizontal:
            pscargs['colorbar'] = True
        grid.pseudocolor(**pscargs)
        ax.set_aspect('equal')

#fig.colorbar(h, ax=axes)
#fig.savefig(target_png)
#fig.savefig(target_pdf)
fig.savefig(target)
