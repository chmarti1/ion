#!/usr/bin/python

import lconfig as lc
import matplotlib.pyplot as plt
import numpy as np
import lplot

lplot.set_defaults(font_size=16, legend_font_size=16)

sources = [\
#    '190315/test4.dat',
    '190301/test6.dat',
    '190301/test7.dat',
    '190322/test3.dat']
    
styles = [\
#    {'ls':'none', 'marker':'s', 'mfc':'w', 'mec':'k', 'ms':4},
    {'ls':'none', 'marker':'o', 'mfc':'w', 'mec':'k', 'ms':4},
    {'ls':'none', 'marker':'^', 'mfc':'w', 'mec':'k', 'ms':4},
    {'ls':'none', 'marker':'d', 'mfc':'k', 'mec':'k', 'ms':4}]
    
# Parameters
excite_hz = 10.
window_sec = 0.5

R_mean = []
R_std = []
SO_in = []

ax1, _ax1 = lplot.init_xxyy('Standoff (mm)', 'Resistance (M$\Omega$)', x2label='Standoff (in)')
ax2 = lplot.init_fig('Time (s)', 'Resistance (M$\Omega$)')

for thisfile,thisstyle in zip(sources, styles):
    
    thisdata = lc.LConf(thisfile, data=True, cal=True)
    # Retrieve the test conditions
    meta = thisdata.get(0,'meta')
    # Find the start and stop of the cut
    istart = thisdata.get_index(meta['start_sec'])
    istop = thisdata.get_index(meta['stop_sec'])
    # Find the standoff and rise
    so_init = 25.4*meta['so_in']
    so_rise = 25.4*meta['rise_in']
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
    # How many data points are available?
    Nn = int(istop - istart)
    # How many windows are there in the data?
    Nw = int(np.round(Nn/Nt))
    # At which index is the excitation frequency?
    iexcite = int(np.round(excite_hz * Nt / sample_hz))
    
    so = []    
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
        so.append(so_init + so_rise * float(index) / Nn)
    ax1.plot(so, R, label=thisfile, **thisstyle)
    ax2.plot(time, R, label=thisfile, **thisstyle)
    
#ax1.legend(loc=0)
ax1.set_ylim([0, 0.05])
ax1.set_xlim([2.5, 6.5])
lplot.scale_xxyy(ax1, xscale=1./25.4)
ax1.get_figure().savefig('incline.png')

ax2.set_ylim([0, .05])
ax2.get_figure().savefig('incline_time.png')
plt.show()
