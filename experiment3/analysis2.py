import numpy as np
import matplotlib.pyplot as plt
import lplot
import lconfig
import tc



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
            if I[index]<0. and I[index+1]>=0.:
                Vsample.append(\
                    V[index] - (V[index+1] - V[index])/(I[index+1] - I[index]) * I[index])
                Is = I[index:index+100].tolist()
                Is.sort(reverse=True)
                tsample.append(t[index+50])
                Isample.append(Is[4]) # Reject the 4 largest points
                Tsample.append(np.mean(out['T'][index:index+100]))
                index+=120
            else:
                index += 1

    out['Tsample'] = Tsample
    out['Isample'] = Isample
    out['tsample'] = tsample
    out['Vsample'] = Vsample
    return out
    

datafile = 'data/b2_1.dat'
#datafile = 'data/b1_1.dat'
data = lconfig.dfile(datafile, afun=fsanalysis, afile=None)

plt.close('all')
lplot.set_defaults(screen_dpi=112)

ax0 = lplot.init_fig('time (s)', 'Current ($\mu$A)',figure_size=(6.,4.5))
I = median_filter(data.analysis['I'],20)
ax0.plot(data.t(), data.analysis['I'],color=[.45,.45,.45])
ax0.plot(data.t(), I,'k')
ax0.set_ylim([0,120])
zax = lplot.zoom_ax(ax0, [.27, .65, .4, .27], xlim=[64.2, 65.6], ylim=[20., 65.], box=False)
zax.set_xticks([64.5, 65., 65.5])
zax.set_yticks([20,40,60])
ax0.get_figure().savefig('ivst.png')
ax0.get_figure().savefig('ivst.')
ax0.get_figure().savefig('ivst.png')

index = data.analysis['T'] > 100.
ax1,ax2 = lplot.init_xxyy('Surface Temperature (C)', 'Current ($\mu$A)', x2label='Surface Temperature (F)', figure_size=(6.,4.5))
ax1.plot(data.analysis['T'][index]+300.,I[index],'k')
lplot.scale_xxyy(ax1,xscale = 1.8, xoffset=32.)
ax1.get_figure().savefig('ivsT.png')