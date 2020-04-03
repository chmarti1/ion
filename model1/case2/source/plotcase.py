#!/usr/bin/python3

import ion1d
import matplotlib.pyplot as plt
import os

datadir = '../data'
exportdir = '../export'
sumfile = '../contents.txt'

datadir = os.path.abspath(datadir)
exportdir = os.path.abspath(exportdir)
sumfile = os.path.abspath(sumfile)

contents = os.listdir(datadir)
contents.sort()

phia = []
J = []

fig = plt.figure(1)

with open(sumfile, 'w') as sfd:
    firstentry = True
    for source in contents:
        print(source)
        p = ion1d.load_post(os.path.join(datadir,source), verbose=False)

        param = p['param']

        if firstentry:
            sfd.write(param.get_header() + '\n')
            firstentry = False
        sfd.write(param.get_entry() + '\n')

        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p['z'], p['eta'], 'k', label='$\eta$ (H$_3$O$^+$)')
        ax.plot(p['z'], p['nu'], 'k--', label='$\\nu$ (e$^-$)')
        ax.set_xlabel('z')
        ax.legend(loc=0)
        ax.grid(True)
        fig.savefig(os.path.join(exportdir,source+'.pdf'))
        
        ax.set_xlim([.92, 1.])
        ax.set_ylim([0., 0.15])
        
        fig.savefig(os.path.join(exportdir, source+'_sheath.pdf'))
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p['z'], p['charge'], 'k')
        ax.set_xlabel('z')
        ax.set_ylabel('charge')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_charge.pdf'))
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p['z'], p['phi'], 'k', label='$\phi$ (V)')
        #ax.plot(p['z'], p['efield'], 'k--', label='-d$\phi$/dz$ (E)')
        ax.set_xlabel('z')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_phi.pdf'))
        
        phia.append(param.phia)
        J.append(p['J'])

fig.clf()
ax = fig.add_subplot(111)
ax.plot(phia,J,'ko')
ax.set_xlabel('$\phi_a$ (nd Voltage)')
ax.set_ylabel('$J$ (nd current)')
ax.grid(True)
fig.savefig(os.path.join(exportdir, 'jphi.pdf'))

