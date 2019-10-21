#!/usr/bin/python

import os, sys
from os import path
import time
import numpy as np

x_start = 0.0
x_stop = 25.0
x_steps = 100
y = 0.
disc_offset_angle = np.pi + np.arcsin(1.5/4.)
rising_edge_angle = disc_offset_angle
wire_length = 25.4

start = time.localtime()

datadir = path.abspath(time.strftime("%Y%m%d%H%M%S", start))
configfile = 'wscan.conf'

while True:
    print('Enter the disc angle observed under the front edge of the platform\n' +
        'at the rising edge of the photointerrupter')
    rising_edge_angle = -(np.pi/180.) * input('(deg):') + disc_offset_angle
    print('Using offset angle %f deg'%(disc_offset_angle * 180. / np.pi))
    print('Rising edge angle is %f deg from center'%(rising_edge_angle * 180. / np.pi))
    print('Enter the wire length extending radially beyond the disc edge')
    wire_length = input('(mm):')
    print('Who is entering these data?')
    initials = raw_input('(initials):')
    print('')
    if raw_input('Is this correct? (y/n)') == 'y':
        break

os.mkdir(datadir)

for xindex,x in enumerate(np.linspace(x_start, x_stop, x_steps)):
    
    thisfile = path.join(datadir, '%03d.dat'%xindex)
    cmd = 'movexy %f %f'%(x,y)
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    time.sleep(1.)
    cmd = 'lcburst -c ' + configfile + ' -d ' + thisfile + \
            ' -f x=%f -f y=%f -f theta=%f -f wire_length=%f -s initials=%s'%(x, y, rising_edge_angle, wire_length, initials)
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    
cmd = 'movexy %f %f'%(x_start, y)
os.system(cmd)
