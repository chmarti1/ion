#!/usr/bin/python

import lconfig
import os
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import lplot

lplot.set_defaults()

# Window
t_window = 0.5

D = lconfig.LConf(sys.argv[1], data=True)
#D = lconfig.LConf('190222/test1.dat', data=True)
i_window = D.get_index(t_window)

Fs = D.get(0,'samplehz')
Ts = 1./Fs


V = D.get_channel('Voltage')
I = D.get_channel('Current')

Nw = i_window/2
Nt = D.ndata()/i_window

V_F = np.zeros((Nt,Nw))
I_F = np.zeros((Nt,Nw))
T = np.zeros_like(V_F)
W = np.zeros_like(V_F)

for index in range(0, Nt):
    F = np.fft.fft(V[index*i_window:(index+1)*i_window])/i_window
    V_F[index, :] = np.log10(np.abs(F[:Nw]))
    F = np.fft.fft(I[index*i_window:(index+1)*i_window])/i_window
    I_F[index, :] = np.log10(np.abs(F[:Nw]))
    T[index, :] = index * i_window * Ts
    W[index, :] = np.arange(0, Fs/2, Fs/2/Nw)
    
ax = lplot.init_fig('Time (s)', 'Frequency (Hz)')
ax.pcolor(T, W, V_F, vmax=-0.5, vmin=-3.5)
ax.get_figure().savefig('voltage_v.png')

ax = lplot.init_fig('Time (s)', 'Frequency (Hz)')
ax.pcolor(T, W, I_F, vmax=1.11, vmin=-3.0)
ax.get_figure().savefig('waterfall_i.png')
plt.show()
