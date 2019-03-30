import numpy as np
import matplotlib.pyplot as plt
import lconfig
import lplot
import tc
import os

# Compare a steel plate test against a copper test

def smooth(x, N=20):
    xx = np.cumsum(x)/N
    xx = xx - np.roll(xx,N)
    xx[:N] = 0.
    xx[-N:] = 0.
    return xx

def median_filter(x, N=100):
    NN = int(N/2)
    xx = np.zeros_like(x)
    for index in range(NN,len(x)-NN):
        xs = list(x[(index-NN):(index+NN)])
        xs.sort()
        xx[index] = xs[NN]
    return xx


def fsanalysis(fileobj):
    # First, copy the meta parameters using the default function
    out = lconfig.default_afun(fileobj)
    # Create calibrated data
    V = fileobj.data[:,0]
    I = fileobj.data[:,1]*25.242500 - .15605
    ts = 1./fileobj.config[0].samplehz
    t = fileobj.t()
    out['V'] = V
    out['I'] = I
    return out


steelfile = 'data/a3_1.dat'
#steelfile = 'data/b2_3.dat'
steel = lconfig.dfile(steelfile, afun=fsanalysis, afile=None)
C = lconfig.collection(afun = fsanalysis, asave=False)
C.add_dir('../experiment2/data/150_1')
cufile = '../experiment2/data/150_1/ivchar20170412170728.dat'
#cufile = '../experiment2/data/150_1/ivchar20170412175533.dat'
cu1 = lconfig.dfile(cufile, afun=fsanalysis, afile=None)
cufile = '../experiment2/data/150_1/ivchar20170412175136.dat'
#cufile = '../experiment2/data/150_1/ivchar20170412171254.dat'
cu2 = lconfig.dfile(cufile, afun=fsanalysis, afile=None)

plt.close('all')
lplot.set_defaults(screen_dpi=112)

ax0 = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)',figure_size=(6.,4.5))
ax0.plot(steel.analysis['V'][17700:349700], steel.analysis['I'][17700:349700], 'o', mec='gray', mfc='gray', markersize=4, label='Steel')
ax0.plot(cu1.analysis['V'], cu1.analysis['I'], 's', mec='k', mfc='w', markersize=6, label='Cu Series 1')
ax0.plot(cu2.analysis['V'], cu2.analysis['I'], '^', mec='k', mfc='w', markersize=6, label='Cu Series 2')
ax0.set_ylim([-100,250])
ax0.legend(loc=0)

plt.show(block=False)
