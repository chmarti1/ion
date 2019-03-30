#!/usr/bin/python

import lconfig as lc
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

sources = [\
	'190315/test2.dat',
	'190315/test3.dat',
	'190322/test1.dat',
	'190322/test2.dat',
	'190325/test1.dat',
	'190325/test2.dat']

length_in = 2.
speeds_ipm = [10., 14., 16., 12., 8., 6.]
styles = [\
	{'ls':'none', 'marker':'o', 'ms':4, 'mec':'k', 'mfc':'w'},
	{'ls':'none', 'marker':'^', 'ms':4, 'mec':'k', 'mfc':'w'},
	{'ls':'none', 'marker':'s', 'ms':4, 'mec':'k', 'mfc':'w'},
	{'ls':'none', 'marker':'d', 'ms':4, 'mec':'k', 'mfc':'w'},
	{'ls':'none', 'marker':'o', 'ms':4, 'mec':'k', 'mfc':'k'},
	{'ls':'none', 'marker':'^', 'ms':4, 'mec':'k', 'mfc':'k'}
]
patch_styles = [\
	{'color':'b'},
	{'color':'r'},
	{'color':'g'},
	{'color':'c'},
	{'color':'m'},
	{'color':'y'}
]
	
# Parameters
excite_hz = 10.
window_sec = 0.5

f = plt.figure(1)
f.clf()
ax1 = f.add_subplot(111)

tstart = 0.
for speed,pstyle in zip(speeds_ipm,patch_styles):
	tduration = length_in * 60. / speed
	ax1.add_patch(\
		Rectangle( (tstart, 0.), tduration, .05, alpha=0.2, **pstyle))
		
	ax1.text(tstart + 0.5*tduration, 0.0, '%.1f\nipm'%speed, ha='center')
	tstart += tduration

for thisfile,thisstyle in zip(sources,styles):
	thisdata = lc.LConf(thisfile, data=True, cal=True)
	# Retrieve the test conditions
	meta = thisdata.get(0,'meta')
	# Find the start and stop of the cut
	istart = thisdata.get_index(meta['start_sec'])
	istop = thisdata.get_index(meta['stop_sec'])
	# How many data points are there in the cut set
	Nd = istop - istart

	# Get the voltage and current data
	v_t = thisdata.get_channel('Voltage')[istart:istop]
	i_t = thisdata.get_channel('Current')[istart:istop]
	
	# Grab the sample rate for FFT calculations
	sample_hz = thisdata.get(0,'samplehz')
	# How many samples per window?
	Nt = int(np.round(sample_hz * window_sec))
	# How many unique frequency data points
	Nf = int(np.floor(Nt/2))
	# How many windows are there in the data?
	Nw = int(np.round((istop - istart)/Nt))
	# At which index is the excitation frequency?
	iexcite = int(np.round(excite_hz * Nt / sample_hz))
	
	R = []
	time = []
	
	for index in range(0,Nd,Nt):
		v_f = np.fft.fft(v_t[index:index+Nt])
		i_f = np.fft.fft(i_t[index:index+Nt])
		# Test to be sure this is the correct index
		if np.abs(i_f[iexcite-1]) > np.abs(i_f[iexcite]) or \
				np.abs(i_f[iexcite+1]) > np.abs(i_f[iexcite]):
			raise Exception('The excitation index does not appear to be correct.')
		
		R.append( (v_f[iexcite] / i_f[iexcite]).real )
		time.append(index / sample_hz)
	ax1.plot(time, R,label=thisfile,**thisstyle)
	

ax1.legend(loc=0)
ax1.grid(True)
ax1.set_xlabel('Time (sec)')
ax1.set_ylabel('Resistance (M$\Omega$)')
plt.show()
