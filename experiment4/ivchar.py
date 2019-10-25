#!/usr/bin/python

# Generate a series of snapshots of the IV characteristic durring a cut

import lconfig as lc
import matplotlib.pyplot as plt
import lplot
import numpy as np
import sys, os

lplot.set_defaults(font_size=16, legend_font_size=16)

gray = [0.8, 0.8, 0.8]

DIR = 'ivchar'

styles = [\
	{'marker':'d', 'mec':'k', 'mfc':'w', 'ms':4, 'ls':'none'},
#	{'marker':'d', 'mec':'k', 'mfc':gray, 'ms':4, 'ls':'none'},
	{'marker':'d', 'mec':'k', 'mfc':'k', 'ms':4, 'ls':'none'},
	{'marker':'s', 'mec':'k', 'mfc':'w', 'ms':4, 'ls':'none'},
#	{'marker':'s', 'mec':'k', 'mfc':gray, 'ms':4, 'ls':'none'},
	{'marker':'s', 'mec':'k', 'mfc':'k', 'ms':4, 'ls':'none'},
	{'marker':'v', 'mec':'k', 'mfc':'w', 'ms':4, 'ls':'none'},
#	{'marker':'v', 'mec':'k', 'mfc':gray, 'ms':4, 'ls':'none'},
	{'marker':'v', 'mec':'k', 'mfc':'k', 'ms':4, 'ls':'none'},
	{'marker':'o', 'mec':'k', 'mfc':'w', 'ms':4, 'ls':'none'},
#	{'marker':'o', 'mec':'k', 'mfc':gray, 'ms':4, 'ls':'none'},
	{'marker':'o', 'mec':'k', 'mfc':'k', 'ms':4, 'ls':'none'},
	{'marker':'^', 'mec':'k', 'mfc':'w', 'ms':4, 'ls':'none'},
#	{'marker':'^', 'mec':'k', 'mfc':gray, 'ms':4, 'ls':'none'},
	{'marker':'^', 'mec':'k', 'mfc':'k', 'ms':4, 'ls':'none'},
]


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


# Build a list of times at which to perform the anlaysis
# Were there specific times requested at the command prompt?
t_list = None
if len(sys.argv) > 2:
	t_array = np.array([float(this) for this in sys.argv[2:]])
else:
	# Number of samples between window beginnings
	Nt = D.get_index(t_sample)
	t_array = D.get_time(downsample=Nt)



ax1 = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)')

for ii, t in enumerate(t_array):
	ii = ii%len(styles)
	figname = '%0.3f.png'%t
	print('Generating figure ' + figname)
	ax = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)')
	V = D.get_channel('Voltage', start=t, stop=(t+t_window))
	I = D.get_channel('Current', start=t, stop=(t+t_window))
	ax.plot(V, I, **styles[ii])
	ax1.plot(V,I,label='%0.2fs'%t, **styles[ii])
	ax.set_title('T = %0.1fs'%(t))
	ax.get_figure().savefig(os.path.join(target, figname))
	plt.close(ax.get_figure())

ax1.legend(loc=0)
ax1.get_figure().savefig(os.path.join(target, 'total.png'))
plt.show()
