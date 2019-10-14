#!/usr/bin/python

import os, sys
from os import path
import time
import numpy as np

x_start = 0.0
x_stop = 25.0
x_steps = 100
y = 0.

start = time.localtime()

datadir = path.abspath(time.strftime("%Y%m%d%H%M%S", start))
configfile = 'wscan.conf'

os.mkdir(datadir)

for xindex,x in enumerate(np.linspace(x_start, x_stop, x_steps)):
	
	thisfile = path.join(datadir, '%03d.dat'%xindex)
	cmd = 'movexy %f %f'%(x,y)
	print(cmd)
	os.system(cmd)
	time.sleep(2.)
	cmd = 'lcburst -c ' + configfile + ' -d ' + thisfile + ' -f x=%f'%x
	print(cmd)
	os.system(cmd)
	
