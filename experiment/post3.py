# Post analysis and plotting for the flamesense data
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib
import matplotlib.pyplot as plt
import sys
import lconfig
import os
poly = np.polynomial.polynomial

data_dir = 'data/'



matplotlib.rc('font',size=9.)

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

def init_xxyy(xlabel,ylabel,x2label=None,y2label=None):
    """set up a figure with two axes overlayed
    ax1,ax2 = init_xxyy(xlabel,ylabel,x2label=None,y2label=None)

Used for making dual x or y axis plots, ax1 contains all data and the primary
x and y axes.  ax2 is used solely to create top (right) x (y) ticks with a 
different scale.

If x2label and/or y2label are specified, then the 
"""
    ax1 = init_fig(xlabel,ylabel)
    f = ax1.get_figure()
    p = ax1.get_position()
    ax2 = f.add_axes(p,label='secondary')
    ax2.set_axis_bgcolor('none')
    axis = ax2.get_xaxis()
    axis.set_ticks_position('top')
    axis.set_label_position('top')
    if x2label==None:
        ax2.set_xticks([])
    else:
        p.y1 = .85
        ax2.set_xlabel(x2label)
    axis = ax2.get_yaxis()
    axis.set_ticks_position('right')
    axis.set_label_position('right')
    if y2label==None:
        ax2.set_yticks([])
    else:
        p.x1 = .83
        ax2.set_ylabel(y2label)
    ax1.set_position(p)
    ax2.set_position(p)
    return ax1,ax2

so_in = []
temp_C = []
o2_scfh = []
fg_scfh = []
flow_scfh = []
fo_ratio = []
r1_mohm = []
r2_mohm = []
r3_mohm = []
v0_volts = []
i1_ua = []
i2_ua = []
filename = []

# Load the whitspace-separated-variable file
with open('TABLE.wsv','r') as ff:
    text=ff.readline()
    for text in ff:
        line = text.split()
        index = 1
        so_in.append(float(line[index])); index+=1
        temp_C.append(float(line[index])); index+=1
        o2_scfh.append(float(line[index])); index+=1
        fg_scfh.append(float(line[index])); index+=1
        flow_scfh.append(float(line[index])); index+=1
        fo_ratio.append(float(line[index])); index+=1
        r1_mohm.append(float(line[index])); index+=1
        r2_mohm.append(float(line[index])); index+=1
        r3_mohm.append(float(line[index])); index+=1
        v0_volts.append(float(line[index])); index+=1
        i1_ua.append(float(line[index])); index+=1
        i2_ua.append(float(line[index])); index+=1
        filename.append(line[index])

so_in = np.array(so_in)
temp_C = np.array(temp_C)
o2_scfh = np.array(o2_scfh)
fg_scfh = np.array(fg_scfh)
flow_scfh = np.array(flow_scfh)
fo_ratio = np.array(fo_ratio)
r1_mohm = np.array(r1_mohm)
r2_mohm = np.array(r2_mohm)
r3_mohm = np.array(r3_mohm)
v0_volts = np.array(v0_volts)
i1_ua = np.array(i1_ua)
i2_ua = np.array(i2_ua)


# First, close any open plots
plt.close('all')

# Fit for I1 vs FO ratio
ax = init_fig('$r$, F/O Ratio','$I_1$, Negative Sat. Current ($\mu$A)')
ax2 = init_fig('$(r-r0)^2$', 'log I')

use = range(17,29)
i1 = i1_ua[use]
r = fo_ratio[use]
ax.plot(r,i1,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')

y = -i1
x = (r-.5)**2
C = poly.polyfit(x, np.log(y), 1, w=y)
r1 = 1./np.sqrt(-C[1])
i0 = -np.exp(C[0])
ax2.plot(x,y,'ks')
rr = np.arange(.5,.9,.01)
ii = -i0 * np.exp( -((rr-0.5)/r1)**2 )
ax2.plot((rr-.5)**2,ii,'k')
ax2.set_yscale('log')

use = range(48,55)
i1 = i1_ua[use]
r = fo_ratio[use]
ax.plot(r,i1,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')

use = range(56,64)
i1 = i1_ua[use]
r = fo_ratio[use]
ax.plot(r,i1,marker='^',mec='k',mfc='k',mew=1.,ls='none',label='.68 (17.3)')

rr = np.arange(.5,.9,.01)
ii = i0 * np.exp( -((rr-0.5)/r1)**2 )
ax.plot(rr,ii,'k')
ax.text(.60,-40.,
r'$I_1 = {0:.1f} \mu\mathrm{{A}}\,\exp \left( \frac{{-(r-.50)^2}}{{{1:.3f}^2}} \right) $'.format(i0,r1),
fontsize=12,backgroundcolor='w')

ax.legend(loc=7)