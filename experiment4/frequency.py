#!/usr/bin/python

import lconfig
import os
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import lplot

lplot.set_defaults(font_size=16., legend_font_size=16)

# Window
t_window = 0.5
# The excitaiton frequency
f_hz = 10.

filename = sys.argv[1]
tstart = None
tstop = None
if len(sys.argv) > 3:
    tstart = float(sys.argv[2])
    tstop = float(sys.argv[3])


D = lconfig.LConf(filename, data=True)
#D = lconfig.LConf('190222/test1.dat', data=True)
Nw = D.get_index(t_window)

Fs = D.get(0,'samplehz')
Ts = 1./Fs
indf = int(np.round(Nw * f_hz * Ts))

V = D.get_channel('Voltage')
I = D.get_channel('Current')

Nf = Nw/2
Nt = D.ndata()/Nw

T = np.zeros((Nt,))
R = np.zeros((Nt,))
VDC = np.zeros((Nt,))
V0 = np.zeros((Nt,))
V1 = np.zeros((Nt,))
V2 = np.zeros((Nt,))

for index in range(0, Nt):
    ii = I[index*Nw:(index+1)*Nw]
    vv = V[index*Nw:(index+1)*Nw]
    
    v_f = np.fft.fft(vv) / Nw
    i_f = np.fft.fft(ii) / Nw
    
    VDC[index] = np.abs(v_f[0])
    V0[index] = np.abs(v_f[indf])
    V1[index] = np.abs(v_f[indf*2])
    V2[index] = np.abs(v_f[indf*3])
    
    R[index] = (v_f[indf] / i_f[indf]).real
    T[index] = Ts * index * Nw
    

# Strip the / out of the filename
filename = '_'.join(filename.split('/'))
# Drop the .dat
filename = filename.split('.')[0]

if tstart:
    istart = int(tstart / t_window)
    istop = int(tstop / t_window)
else:
    istart = 0
    istop = -1

# Resistance plot
ax = lplot.init_fig('Time (s)', 'Resistance (M$\Omega$)')
ax.plot(T[istart:istop], R[istart:istop], 'k')
ax.set_ylim([0, 2*np.average(R[istart:istop])])
#ax.get_figure().savefig('frequencies/r_' + filename + '.png')

ax = lplot.init_fig('Time (s)', 'FFT Magnitude (V)')
ax.plot(T[istart:istop],VDC[istart:istop], 'g', label='DC')
ax.plot(T[istart:istop],V0[istart:istop], 'k', label='fundamental')
ax.plot(T[istart:istop],V1[istart:istop], 'b', label='first harmonic')
ax.plot(T[istart:istop],V2[istart:istop], 'r', label='second harm.')
ax.set_ylim([0, 2*np.average(V0[istart:istop])])
#ax.set_ylim([0, 10.5])
ax.legend(loc=0)
ax.get_figure().savefig('frequencies/v_' + filename + '.png')

ax = lplot.init_fig('Time (s)', 'FFT Magnitude (V)')
ax.plot(T[istart:istop],VDC[istart:istop], 'k-.', label='DC')
ax.plot(T[istart:istop],V0[istart:istop], 'k', label='fundamental')
ax.plot(T[istart:istop],V1[istart:istop], 'k--', label='first harmonic')
ax.plot(T[istart:istop],V2[istart:istop], 'k:', label='second harm.')
ax.set_ylim([0, 2*np.average(V0[istart:istop])])
#ax.set_ylim([0, 10.5])
ax.legend(loc=0)
ax.get_figure().savefig('frequencies/v_' + filename + '_bw.png')

plt.show()
