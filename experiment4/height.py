#!/usr/bin/python

import lconfig as lc
import matplotlib.pyplot as plt
import numpy as np
import lplot

lplot.set_defaults()

styles = [{'marker':'^', 'mfc':'k', 'mec':'k', 'ls':'none'},
		{'marker':'o', 'mfc':'k', 'mec':'k', 'ls':'none'},
		{'marker':'d', 'mfc':'w', 'mec':'k', 'ls':'none'},
		{'marker':'o', 'mfc':'w', 'mec':'k', 'ls':'none'},
		{'marker':'s', 'mfc':'w', 'mec':'k', 'ls':'none'}]

# Each source is listed by a file, a group index, and a True/False flag
# The group index indicates how the data point should be plotted
# The True/False flag indicates whether the data point should be 
# included in the analysis.  Points that are excluded have 
# rationalizations in comments

sources = [\
	('190320/test1.dat', 1, False),	# Evidence that the plate moved during test
	('190320/test2.dat', 1, True),
	('190320/test3.dat', 1, False),	# Height was incorrect
	('190320/test4.dat', 1, True),
	('190320/test5.dat', 1, True),
	('190320/test6.dat', 1, True),
	('190320/test7.dat', 1, False),	# Height was incorrect
	('190320/test8.dat', 1, False),	# Height was incorrect
	('190320/test9.dat', 1, True),
	('190320/test10.dat', 1, True),
	('190320/test11.dat', 1, True),
	('190322/test4.dat', 1, True),
	('190322/test5.dat', 1, True),
	('190322/test6.dat', 1, True),
	('190322/test7.dat', 1, True),
	('190322/test8.dat', 4, False),
	('190322/test9.dat', 4, False),
	('190322/test10.dat', 4, False),
	('190322/test11.dat', 4, False),
	('190322/test12.dat', 4, False),
	('190322/test13.dat', 4, False),
	('190322/test14.dat', 1, False),	# Evidence that the plate moved during the test
	('190322/test15.dat', 1, True),
	('190327/test1.dat', 2, False),
	('190327/test2.dat', 2, False),
	('190327/test3.dat', 2, False),
	('190327/test4.dat', 2, False),
	('190327/test5.dat', 2, False),
	('190327/test6.dat', 2, False),
	('190327/test7.dat', 2, False),
	('190327/test8.dat', 3, True),
	('190327/test9.dat', 3, True),
	('190327/test10.dat', 3, True),
	('190327/test11.dat', 3, True),
	('190327/test12.dat', 3, True),
	('190327/test13.dat', 3, True),
	('190327/test14.dat', 3, True),
	('190327/test15.dat', 3, True),
	('190327/test16.dat', 3, True),
	('190327/test17.dat', 3, True),
	('190327/test18.dat', 3, True),
	('190327/test19.dat', 3, True)]
	

# Parameters
excite_hz = 10.
window_sec = 0.5

R_mean = []
R_std = []
SO_mm = []
group = []
incl = []

ax1, _ax1 = lplot.init_xxyy(xlabel='Standoff (mm)', ylabel='Resistance (M$\Omega$)',
		x2label='Standoff (in)')

ax2, _ax2 = lplot.init_xxyy(xlabel='Standoff (mm)', ylabel='Resistance (M$\Omega$)',
		x2label='Standoff (in)')

for thisfile, thisgroup, thisinclude in sources:
	print(thisfile, thisinclude)
	thisdata = lc.LConf(thisfile, data=True, cal=True)
	# Retrieve the test conditions
	meta = thisdata.get(0,'meta')
	# Find the start and stop of the cut
	istart = thisdata.get_index(meta['start_sec'])
	istop = thisdata.get_index(meta['stop_sec'])
	# How many data points are there in the cut set
	Nd = istop - istart

	# Get the voltage and current data
	v_t = thisdata.get_channel('Voltage')[istart:istop]
	i_t = thisdata.get_channel('Current')[istart:istop]
	
	# Grab the sample rate for FFT calculations
	sample_hz = thisdata.get(0,'samplehz')
	# How many samples per window?
	Nt = int(np.round(sample_hz * window_sec))
	# How many unique frequency data points
	Nf = int(np.floor(Nt/2))
	# How many windows are there in the data?
	Nw = int(np.round((istop - istart)/Nt))
	# At which index is the excitation frequency?
	iexcite = int(np.round(excite_hz * Nt / sample_hz))
	
	R = []
	time = []
	
	for index in range(0,Nd,Nt):
		v_f = np.fft.fft(v_t[index:index+Nt])
		i_f = np.fft.fft(i_t[index:index+Nt])
		# Test to be sure this is the correct index
		# Use the False/True literal to disable/enable testing
		if False and \
				(np.abs(i_f[iexcite-1]) > np.abs(i_f[iexcite]) or \
				np.abs(i_f[iexcite+1]) > np.abs(i_f[iexcite])):
			print('file = ' + thisfile)
			print('iexcite = %d'%iexcite)
			print('time = %f'%(index/sample_hz))
			print(i_f)
			raise Exception('The excitation index does not appear to be correct.')
		
		R.append( (v_f[iexcite] / i_f[iexcite]).real )
		time.append(index / sample_hz)
	
	Rmean = np.average(R)
	Rstd = np.std(R)
	
	# Accumulate points for the calibration fit
	R_std.append(Rstd)
	R_mean.append(Rmean)
	SO_mm.append(25.4 * meta['so_in'])
	group.append(thisgroup)
	incl.append(thisinclude)

# Convert to numpy arrays
R_std = np.asarray(R_std)
R_mean = np.asarray(R_mean)
SO_mm = np.asarray(SO_mm)
group = np.asarray(group, dtype=int)
incl = np.asarray(incl, dtype=bool)

# Plot the groups
I = np.logical_and((group==1), incl)
ax1.plot(SO_mm[I], R_mean[I], label='0-25uA sine', **styles[1])
I = np.logical_and((group==3), incl)
ax1.plot(SO_mm[I], R_mean[I], label='5-15uA sine', **styles[3])


#ax2.errorbar(SO_in, R_mean, xerr=np.abs(rise_in), yerr=2*np.array(R_std), fmt='ko', capsize=2, ecolor='k')

# Curve fit R(s)
coef, cov = np.polyfit(SO_mm[incl], R_mean[incl], 1, cov=True)
var_coef = [cov[0,0], 2*cov[1,0], cov[1,1]]

print('With s in mm and R in MOhm')
print('***=====================***')
print('R = %e s + %e'%tuple(coef))
print('With a 95\% confidence interval')
print('slope = %e +/- %e'%(coef[0], 1.9*np.sqrt(cov[0,0])))
print('offset = %e +/- %e'%(coef[1], 1.9*np.sqrt(cov[1,1])))
print('Uncertainty in the fit for R is')
print('var_R = %e s^2 + %e s + %e'%tuple(var_coef))

#ax2.plot(s, R, 'k')
#ax2.plot(s, R + 3*std, 'k--')
#ax2.plot(s, R - 3*std, 'k--')

# Curve fit s(R)
coef, cov = np.polyfit(R_mean[incl], SO_mm[incl], 1, cov=True)
R = np.linspace(0.022, 0.45, 50)
s = np.polyval(coef, R)
var_coef = [cov[0,0], 2*cov[1,0], cov[1,1]]
std = np.sqrt(np.polyval(var_coef, R))

print('***=====================***')
print('s = %f R + %f'%tuple(coef))
print('With a 95\% confidence interval')
print('slope = %f +/- %f'%(coef[0], 1.9*np.sqrt(cov[0,0])))
print('offset = %f +/- %f'%(coef[1], 1.9*np.sqrt(cov[1,1])))
print('Uncertainty in the fit for s is')
print('var_s = %f R^2 + %f R + %f'%tuple(var_coef))
print('***=====================***')
ax1.plot(s, R, 'k')
ax1.plot(s + 1.9*std, R, 'k--')
ax1.plot(s - 1.9*std, R, 'k--')

ax1.set_xlim([0,8.])
ax1.set_ylim([0,0.055])
# Scale the inches scale
lplot.scale_xxyy(ax1, xscale=1./25.4)
ax1.legend(loc=0)
ax1.get_figure().savefig('height.png')


# Scatter plot

I = np.logical_and(group==1, incl)
ax2.plot(SO_mm[I], R_mean[I], label='0-25uA sine', **styles[1])
I = (group==2)
ax2.plot(SO_mm[I], R_mean[I], label='0-10uA sine', **styles[2])
I = np.logical_and(group==3, incl)
ax2.plot(SO_mm[I], R_mean[I], label='5-15uA sine', **styles[3])
I = (group==4)
ax2.plot(SO_mm[I], R_mean[I], label='0.65 f/o', **styles[4])

ax2.legend(loc=0)

plt.show(block=False)
