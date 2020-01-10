#!/usr/bin/python3

import os, sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


import os,sys
import wiretools as wt
import lconfig as lc
import lplot as lp

def read_p1d(filename):
    data = {'theta':[], 'count':[], 'mean':[], 'median':[], 'std':[]}
    
    with open(filename, 'r') as ff:
        head = True
        for thisline in ff:
            if head:
                if thisline[0] == '#'
                    head = False
                else:
                    param, value = thisline.split()
                    data[param] = float(value)
            else:
                temp = [float(xx) for xx in thisline.split()]
                data['theta'].append(temp[0])
                data['count'].append(temp[1])
                data['mean'].append(temp[2])
                data['median'].append(temp[3])
                data['std'].append(temp[4])



whichfile = '079'
whichdir = '../data/20191120163922/'
window = [-0.03, 0.07]

source = whichdir+whichfile+'.dat')
dd = lc.LCconf(source,data=True)
source = whichdir+'post1/'+whichfile+'.p1d'
p1d = read_p1d(source)

#fig.colorbar(h, ax=axes)
#fig.savefig(target_png)
#fig.savefig(target_pdf)
fig.savefig(target)
