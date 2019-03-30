#!/usr/bin/python

import lconfig
import os
import matplotlib.pyplot as plt
import numpy as np
import sys, os

# Window
t_window = 0.5
# The excitaiton frequency
f_hz = 10.

D = lconfig.LConf(sys.argv[1], data=True)
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
V0 = np.zeros((Nt,), dtype=complex)
V1 = np.zeros((Nt,), dtype=complex)
V2 = np.zeros((Nt,), dtype=complex)

for index in range(0, Nt):
    ii = I[index*Nw:(index+1)*Nw]
    vv = V[index*Nw:(index+1)*Nw]
    
    FF = np.fft.fft(vv)
    
    V0[index] = FF[indf]
    V1[index] = FF[indf*2]
    V2[index] = FF[indf*3]
    
    R[index] = (V0[index] / np.fft.fft(ii)[indf]).real
    T[index] = Ts * index * Nw
    
    
plt.figure(1)
plt.clf()
plt.plot(T, R)
plt.grid(True)

f = plt.figure(2)
f.clf()
ax = f.subplots(1,1)
ax.plot(T,np.abs(V0), 'k', label='fundamental')
ax.plot(T,np.abs(V1), 'b', label='first harmonic')
ax.plot(T,np.abs(V2), 'r', label='second harm.')
ax.legend(loc=0)
ax.grid(True)

plt.show()
