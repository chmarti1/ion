import numpy as np
import matplotlib.pyplot as plt
import lconfig
import lplot
import tc
import os


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
    Vtc1 = smooth(fileobj.data[:,2],200)
    ts = 1./fileobj.config[0].samplehz
    t = fileobj.t()
    out['V'] = V
    out['I'] = I
    out['T'] = tc.K.T(Vtc1*1000., Tcj=20.)
    out['scan'] = V.mean() < 5.
    tsample = []
    Tsample = []
    Isample = []
    Vsample = []
    # Extract a sample from each 10V peak for sawtooth scans
    if out['scan']:
        # Perform a test for a rising-edge trigger
        index = 0
        while index < (len(V)-120):
            # look for the positive 0 crossing in voltage
            if V[index]<0. and V[index+1]>=0.:
                Is = I[index:index+100].tolist()
                Is.sort(reverse=True)
                tsample.append(t[index+50])
                Isample.append(Is[4]) # Reject the 4 largest points
                Tsample.append(np.mean(out['T'][index:index+100]))
                index+=120
            else:
                index += 1
                
        index = 0
        while index < (len(V)-120):
            if I[index]<0. and I[index+1]>=0.:
                Vsample.append(\
                    V[index] - (V[index+1] - V[index])/(I[index+1] - I[index]) * I[index])
                index+=120
            else:
                index+=1

    else:
        # Downsample rate
        N = 200
        index = 0
        while index<len(V)-N:
            Is = I[index:index+N].tolist()
            Is.sort()
            Isample.append(Is[int(N/2)])
            tsample.append(fileobj.t()[index+int(N/2)])
            Tsample.append(np.mean(out['T'][index:index+N]))
            index+=N
            
    out['Tsample'] = Tsample
    out['Isample'] = Isample
    out['tsample'] = tsample
    out['Vsample'] = Vsample
    return out
    
if '__analysis__' not in globals():
    __analysis__ = ''
    C = lconfig.collection(afun=fsanalysis, asave=False)
    C.add_dir('data',verbose=True)

use = {'b1_2.dat':'ko-', 'b2_1.dat':'ks-', 'a2_1.dat':'k^-', 'a1_1.dat':'kD-'}
use2 = {'a3_1.dat':'ks-', 'a4_1.dat':'ko-'}


plt.close('all')
lplot.set_defaults(screen_dpi=112.)
#I = data.analysis['I']
ax,dummy = lplot.init_xxyy('Surface Temperature (C)', 'Current ($\mu$A)', x2label='Temperature (F)',
                       figure_size=(6.,4.5))
ax2 = lplot.init_fig('Time (s)', 'Current ($\mu$A)', figure_size=(6.,4.5))

for this in C:
    filename = os.path.basename(this.filename)
    if filename in use:
        if filename[0]=='b':
            label = 'Clean Plate'
        else:
            label = 'Corroded Plate'
        T = np.array(this.analysis['Tsample'])+300.
        I = np.array(this.analysis['Isample'])
        ax.plot(T[:-10], I[:-10], use[filename], markevery=100,
                mec='k', mfc='w', label=label)
                
    elif filename in use2:
        ax2.plot(this.analysis['tsample'], this.analysis['Isample'], use2[filename], markevery=100,
                mec='k', mfc='w', label='%.1f L/min'%(this.analysis['flow_scfh']*.472))
                
ax.set_ylim([20,60])
ax.set_xlim([400,1200])
ax.legend(loc=0)
lplot.scale_xxyy(ax, xscale=1.8, xoffset=32.)
ax.get_figure().savefig('ivsTall.png')
ax.get_figure().savefig('ivsTall.eps')
ax.get_figure().savefig('ivsTall.pdf')


ax2.set_xlim([0,600])
ax2.legend(loc=0)
ax2.get_figure().savefig('ivstsalt.png')
ax2.get_figure().savefig('ivstsalt.eps')
ax2.get_figure().savefig('ivstsalt.pdf')

