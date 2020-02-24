# Use FFT to examine the precision excitations

import loadall
import matplotlib.pyplot as plt
import sys
import os


def init_fig(xlabel,ylabel):
    """set up a figure with a single axes
    ax = init_fig(xlabel,ylabel)
Returns the axis for plotting    
"""
    std_size = (4., 3.5)
    f = plt.figure()
    f.set_size_inches(std_size)
    ax = f.add_axes([.17,.15,.78,.80],label='primary')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid('on')
    return ax


index = 0
precision = loadall.loadall('data/precision')
v = loadall.Xfromindex(precision, 'V', index)
i = loadall.Xfromindex(precision, 'I', index)
T = .001

V = np.fft.fft(v)
I = np.fft.fft(i)
F = np.fft.fftfreq(len(v),d=T)

use = F>=0
V = np.abs(V[use])
I = np.abs(I[use])
F = F[use]

plt.close('all')

ax = init_fig('Frequency (Hz)', 'Magnitude (dB)')
ax.set_xlim([0,200])
ax.set_ylim([0,100])

ax.plot(F,20*np.log10(V),'k--',label='V')
ax.plot(F,20*np.log10(I),'k',label='I')

# Find the peaks
use = (F>4.) * (F<6.)
excite = np.argmax(V[use]) + use.argmax()
use = (F>150.) * (F<200.)
resonance = np.argmax(I[use]) + use.argmax()
ax.text(F[excite], 20*log10(I[excite]), 'Excitation\n{:4.2f}Hz'.format(F[excite]))
ax.text(F[resonance], 20*log10(I[resonance]), 
        'Resonance\n{:5.1f}Hz'.format(F[resonance]),
        horizontalalignment='right')

ax.legend(loc=9)