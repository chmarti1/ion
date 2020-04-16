#!/usr/bin/python3

import ion1d
import matplotlib.pyplot as plt
import os, time

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
J1 = []

fig = plt.figure(1)

with open(sumfile, 'w') as sfd:
    firstentry = True
    sfd.write('Created: ' + time.asctime() + '\n')
    sfd.write('Ion1D version: ' + ion1d.__version__ + '\n')
    for source in contents:
        print(source)
        target = os.path.join(datadir,source)
        p = ion1d.PostIon1D(target)
        p.expand_post()
        p.save(target, overwrite=True)

        # Strip the extension off of the source
        source = source.split('.')[0]

        param = p.param

        if firstentry:
            sfd.write('SOURCE MODEL                ' + param.get_header() + '\n')
            firstentry = False
        sfd.write('{:6s} {:20s} '.format(source, p.model.__name__) + param.get_entry() + '\n')

        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p.z, p.eta, 'k', label='$\eta$ (H$_3$O$^+$)')
        ax.plot(p.z, p.nu, 'k--', label='$\\nu$ (e$^-$)')
        ax.set_xlabel('z')
        ax.legend(loc=0)
        ax.grid(True)
        fig.savefig(os.path.join(exportdir,source+'.png'))
        
        ax.set_xlim([.92, 1.])
        ax.set_ylim([0., 0.15])
        
        fig.savefig(os.path.join(exportdir, source+'_wsheath.png'))
        
        ax.set_xlim([0, .05])
        ax.set_ylim([0., 0.25])
        
        fig.savefig(os.path.join(exportdir, source+'_tsheath.png'))
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p.z, p.eta-p.nu, 'k')
        ax.set_xlabel('z')
        ax.set_ylabel('charge')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_charge.png'))
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p.z, p.phi, 'k', label='$\phi$ (V)')
        #ax.plot(p['z'], p['efield'], 'k--', label='-d$\phi$/dz$ (E)')
        ax.set_xlabel('z')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_phi.png'))
        
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p.z, p.eta1, 'k', label='$\eta_1$ (H$_3$O$^+$)')
        ax.plot(p.z, p.nu1, 'k--', label='$\nu_1$ (e$^-$)')
        ax.set_xlabel('z')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_1.png'))
        
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(p.z, p.phi1, 'k', label='$\phi_1$ (V)')
        #ax.plot(p['z'], p['efield'], 'k--', label='-d$\phi$/dz$ (E)')
        ax.set_xlabel('z')
        ax.grid(True)
        fig.savefig(os.path.join(exportdir, source+'_phi1.png'))
        
        phia.append(param.phia)
        J.append(p.J)
        J1.append(p.J1)

fig.clf()
ax = fig.add_subplot(111)
ax.plot(phia,J,'ko')
ax.set_xlabel('$\phi_a$ (nd Voltage)')
ax.set_ylabel('$J$ (nd current)')
ax.grid(True)
fig.savefig(os.path.join(exportdir, 'jphi.png'))

fig.clf()
ax = fig.add_subplot(111)
ax.plot(phia,J1,'ko')
ax.set_xlabel('$\phi_a$ (nd Voltage)')
ax.set_ylabel('$J_1$ (nd conductivity)')
ax.grid(True)
fig.savefig(os.path.join(exportdir, 'j1phi.png'))
