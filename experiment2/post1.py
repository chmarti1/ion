import lconfig
import matplotlib.pyplot as plt
import numpy as np
import tc

def smooth(x, N=20):
    xx = np.cumsum(x)/N
    xx = xx - np.roll(xx,N)
    xx[:N] = 0.
    xx[-N:] = 0.
    return xx

def fsanalysis(fileobj):
    # First, copy the meta parameters using the default function
    out = lconfig.default_afun(fileobj)
    # Create calibrated data
    V = fileobj.data[:,0]
    I = fileobj.data[:,1]*25.242500 - .15605
    Vtc1 = smooth(fileobj.data[:,2],200)
    Vtc2 = smooth(fileobj.data[:,3],200)
    Vcj = tc.KmV(21.)
    ts = 1./fileobj.config[0].samplehz
    t = np.arange(0,len(I)*ts,ts)
    out['V'] = V
    out['I'] = I
    out['T1'] = tc.K(Vtc1*1000.+Vcj)
    out['T2'] = tc.K(Vtc2*1000.+Vcj)
    out['t'] = t
    return out
    
dfile = lconfig.dfile('data/drun2055_2.dat', afun=fsanalysis)


f = plt.figure(1)
f.clf()
ax1 = f.add_subplot(211)
ax2 = f.add_subplot(212)

f = plt.figure(2)
f.clf()
ax3 = f.add_subplot(111)

vtest = 0.0
vtol = .02
index = (dfile.analysis['V']<(vtest+vtol)) * (dfile.analysis['V']>(vtest-vtol))
V = dfile.analysis['V'][index]
I = dfile.analysis['I'][index]
t = dfile.analysis['t'][index]
T2 = dfile.analysis['T2'][index]
ax1.plot(t,I,'k.',label='%.1fV'%vtest)
ax2.plot(t,T2,'k.',label='%.1fV'%vtest)

vtest = 4.0
vtol = .02
index = (dfile.analysis['V']<(vtest+vtol)) * (dfile.analysis['V']>(vtest-vtol))
V = dfile.analysis['V'][index]
I = dfile.analysis['I'][index]
t = dfile.analysis['t'][index]
T2 = dfile.analysis['T2'][index]
ax1.plot(t,I,'b.',label='%.1fV'%vtest)
ax2.plot(t,T2,'b.',label='%.1fV'%vtest)
ax3.plot(T2,I,'b.')

vtest = 8.0
vtol = .02
index = (dfile.analysis['V']<(vtest+vtol)) * (dfile.analysis['V']>(vtest-vtol))
V = dfile.analysis['V'][index]
I = dfile.analysis['I'][index]
t = dfile.analysis['t'][index]
T2 = dfile.analysis['T2'][index]

ax1.plot(t,I,'g.',label='%.1fV'%vtest)
ax2.plot(t,T2,'g.',label='%.1fV'%vtest)
ax3.plot(T2,I,'g.')

ax1.legend(loc=0)