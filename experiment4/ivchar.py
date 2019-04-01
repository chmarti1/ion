#!/usr/bin/python

# Generate a series of snapshots of the IV characteristic durring a cut

import lconfig as lc
import matplotlib.pyplot as plt
import lplot
import numpy as np
import sys, os

DIR = 'ivchar'

lplot.set_defaults()

# Window
t_window = 0.5
# Window spacing
t_sample = 5.

filename = sys.argv[1]
D = lc.LConf(filename, data=True)
#D = lc.LConf('190222/test1.dat', data=True)

# In the ivchar directory, we will 
# Strip the / out of the filename
filename = '_'.join(filename.split('/'))
# Remove the .dat
filename = filename.split('.')[0]
# Name the target directory
target = os.path.join(DIR,filename)

# Check to see if the directory exists
# If this data file has been run before, then remove the results; we're
# starting from scratch.
if os.path.isdir(target):
	print('Found previous results for ' + filename)
	contents = os.listdir(target)
	for this in contents:
		print('Removing ' + this)
		os.remove(os.path.join(target,this))
else:
	os.mkdir(target)


Fs = D.get(0,'samplehz')
Ts = 1./Fs

V = D.get_channel('Voltage')
I = D.get_channel('Current')


# Number of samples in a window
Nwindow = D.get_index(t_window)
# Number of samples between window beginnings
Nt = D.get_index(t_sample)
# Number of plots/samples
Ns = int(D.ndata() / Nt)

for ii in range(0, D.ndata(), Nt):
	print('Generating figure ' + repr(ii) + '.png')
	ax = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)')
	ax.plot(V[ii:ii+Nwindow], I[ii:ii+Nwindow], ls='none', marker='d', ms=4, mec='k', mfc='w')
	ax.set_title('T = %0.1fs'%(ii*Ts))
	ax.get_figure().savefig(os.path.join(target, repr(ii)+'.png'))
	plt.close(ax.get_figure())

plt.show()
