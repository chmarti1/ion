#!/usr/bin/python3

import os, sys
from os import path
import time
import numpy as np

x = 20.
y_start = 1.
y_stop = 10.
y_step = 1
disc_offset_angle = np.pi + np.arcsin(1.5/4.)
rising_edge_angle = disc_offset_angle
wire_length = 25.4

start = time.localtime()

datadir = path.abspath(time.strftime("../data/%Y%m%d%H%M%S", start))
configfile = 'vscan.conf'

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
    print('  Enter the distances from the torch tip in mm.  The torch tip is y=0,')
    print('  and the work is in the positive direction.  This will be used to')
    print('  position the torch.')
    print('> Enter the starting y-distance.')
    y_start = float(input('(mm):'))
    print('> Enter the final y-distance.')
    y_stop = float(input('(mm):'))
    print('> Enter the y-step size.')
    y_step = float(input('(mm):'))
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

if y_start < 0.5 or y_start > 50 or y_stop < 0.5 or y_stop > 50:
	print('The y-values you entered were y_start=%fmm, y_stop=%fmm'%(y_start,y_stop))
	print('Are you nuts!?')
	exit(-1)
	

os.mkdir(datadir)

# Take a preliminary flow rate data file
thisfile = path.join(datadir, 'flow.pre')
cmd = 'lcburst -n 64 -c flow.conf -d %s'%thisfile
os.system(cmd)

class SkipIter:
	def __init__(self, start, stop, step):
		if (stop - start)*step <= 0:
			raise Exception('Illegal start, stop, step combination!')
		self.start = start
		self.stop = stop
		self.step = step
		self.index = None
		self.nindex = int((stop-start)//step)
		self.nextcall = self._first
		
	def __iter__(self):
		return self
		
	def __next__(self):
		return self.nextcall()

	def _first(self):
		self.index = 0
		self.nextcall = self._incr
		return self.index * self.step + self.start
		
	def _incr(self):
		self.index += 2
		if self.index <= self.nindex:
			return self.index * self.step + self.start
		elif self.nindex // 2:
			self.index -= 3
		else:
			self.index -= 1
		self.nextcall = self._decr
		return self.index * self.step + self.start
		
	def _decr(self):
		self.index -= 2
		if self.index > 0:
			return self.index * self.step + self.start
		raise StopIteration()

# Loop through y locations
# Start with y=y_start, loop outward skipping steps and come backwards filling in the
# skipped steps.
yindex = 0
for y in SkipIter(y_start, y_stop, y_step):
    
    thisfile = path.join(datadir, '%03d.dat'%yindex)
    cmd = 'movexy %f %f'%(x,y)
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    if yindex == 0:
        time.sleep(10.)
    else:
        time.sleep(1.)
    cmd = 'lcburst -c ' + configfile + ' -d ' + thisfile + \
            ' -f x=%f -f y=%f -f theta=%f -f r=%f -s who=\"%s\"'%(x, y, rising_edge_angle, wire_length+4*25.4, initials) + \
            ' -s rot=\"%s\" -f vwire=%f -f standoff=%f'%(['ccw', 'cw'][rotation], wire_voltage, standoff)
    print(cmd)
    if os.system(cmd):
        print('FAILED')
        exit(-1)
    
    yindex += 1
        
cmd = 'movexy %f %f'%(0,y_start)
os.system(cmd)


# Take a post flow rate data file
thisfile = path.join(datadir, 'flow.post')
cmd = 'lcburst -n 64 -c flow.conf -d %s'%thisfile
os.system(cmd)
