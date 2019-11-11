#!/usr/bin/python3

import os, sys
from os import path
import time
import numpy as np

x_start = 0.0
x_stop = 20.0
x_step = .125
y = 0.
disc_offset_angle = np.pi + np.arcsin(1.5/4.)
rising_edge_angle = disc_offset_angle
wire_length = 25.4

start = time.localtime()

datadir = path.abspath(time.strftime("../data/%Y%m%d%H%M%S", start))
configfile = 'wscan.conf'

while True:
    print('> Enter the disc angle observed under the front edge of the platform')
    print('  at the rising edge of the photointerrupter.')
    rising_edge_angle = -(np.pi/180.) * float(input('(deg):')) + disc_offset_angle
    print('  Using offset angle %f deg'%(disc_offset_angle * 180. / np.pi))
    print('  Rising edge angle is %f deg from center'%(rising_edge_angle * 180. / np.pi))
    print('> Enter the wire length extending radially beyond the disc edge')
    wire_length = float(input('(mm):'))
    print('> Enter the disc direction of rotation.')
    print('  The usual direciton is counter-clock-wise.')
    rotation = int(input('(0=ccw, 1=cw):'))
    print('> Enter the power supply voltage.')
    wire_voltage = float(input('(V):'))
    print('> Enter the torch standoff from the work')
    standoff = float(input('(mm):'))
    print('> Enter the distance from the torch tip in mm.  The torch tip is y=0,')
    print('  and the work is in the positive direction.  This will be used to')
    print('  position the torch.')
    y = float(input('(mm):'))
    print('Who is entering these data?')
    initials = input('(initials):')
    print('')
    if input('Is this correct? (y/n):') == 'y':
        break

# Check the inputs for sanity
if rising_edge_angle > np.pi or rising_edge_angle < -np.pi:
    print('The calculated wire angle at the encoder rising edge is %f degrees.'%rising_edge_angle * 180 / np.pi)
    print('It looks like you are using the wrong encoder edge.  Try again')
    exit(-1)
    
if rotation<0 or rotation>1:
    print('Rotation should have been 0 (ccw) or 1 (cw).  You entered %d'%rotation)
    exit(-1)
elif rotation == 1:
    print('Disc rotation is usually counter-clock-wise (0).  Are you sure it is clock-wise in this test?')
    if input('(y/n):') == 'y':
        print('OK.  Sorry; just checking.')
    else:
        print('Stopping.')
        exit(-1)
    
if len(initials) > 4 or len(initials) < 2:
    print('This does not look like a user''s initials: ' + initials)
    print('What are you trying to pull, anyway?')
    exit(-1)

if y < 0.5 or y > 50.:
	print('The y-value you entered was %fmm'%y)
	print('Are you nuts!?')
	exit(-1)

os.mkdir(datadir)

# Take a preliminary flow rate data file
thisfile = path.join(datadir, 'flow.pre')
cmd = 'lcburst -n 64 -c flow.conf -d %s'%thisfile
os.system(cmd)

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
            ' -f x=%f -f y=%f -f theta=%f -f r=%f -s who=\"%s\"'%(x, y, rising_edge_angle, wire_length+4*25.4, initials) + \
            ' -s rot=\"%s\" -f vwire=%f -f standoff=%f'%(['ccw', 'cw'][rotation], wire_voltage, standoff)
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


# Take a post flow rate data file
thisfile = path.join(datadir, 'flow.post')
cmd = 'lcburst -n 64 -c flow.conf -d %s'%thisfile
os.system(cmd)
