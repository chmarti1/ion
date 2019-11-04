#!/usr/bin/python

import os, sys
from os import path
import time
import numpy as np

x_start = 0.0
x_stop = 25.0
x_step = .125
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
    print('Enter the disc direction of rotation.  The usual direciton is counter-clock-wise.')
    rotation = input('(0=ccw, 1=cw):')
    print('Who is entering these data?')
    initials = raw_input('(initials):')
    print('')
    if raw_input('Is this correct? (y/n):') == 'y':
        break

# Check the inputs for sanity
if rising_edge_angle > 180 or rising_edge_angle < -180:
    print('The calculated wire angle at the encoder rising edge is %f degrees.'%rising_edge_angle)
    print('It looks like you are using the wrong encoder edge.  Try again')
    exit(-1)
    
if rotation<0 or rotation>1:
    print('Rotation should have been 0 (ccw) or 1 (cw).  You entered %d'%rotation)
    exit(-1)
elif rotation == 1:
    print('Disc rotation is usually counter-clock-wise (0).  Are you sure it is clock-wise in this test?')
    if raw_input('(y/n):') == 'y':
        print('OK.  Sorry; just checking.')
    else:
        print('Stopping.')
        exit(-1)
    
if len(initials) > 4 or len(initials) < 2:
    print('This does not look like initials: ' + initials)
    print('What are you trying to pull, anyway?')
    exit(-1)


os.mkdir(datadir)

# Loop through x locations
# Start with x=0, loop outward skipping steps and come backwards filling in the
# skipped steps.
x = 0.
x_incr = 2*x_step
xindex = 0
while x>=0.:
    
    thisfile = path.join(datadir, '%03d.dat'%xindex)
    cmd = 'movexy %f %f'%(x,y)
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    time.sleep(1.)
    cmd = 'lcburst -c ' + configfile + ' -d ' + thisfile + \
            ' -f x=%f -f y=%f -f theta=%f -f wire_length=%f -s who=\"%s\"'%(x, y, rising_edge_angle, wire_length, initials) + \
            ' -s rot=\"%s\"'%(['ccw', 'cw'][rotation])
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    
    # Increment x
    # If we're beyond the stop point, turn it around
    xindex += 1
    x += x_incr
    if x > x_stop:
        x -= x_step
        x_incr = -x_incr
        
cmd = 'movexy %f %f'%(x_start, y)
os.system(cmd)
