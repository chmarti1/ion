import lconfig
import numpy as np
from scipy import optimize
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
import lplot


scfh_to_lpm = .472
pref = 1.01325  # standard pressure bar
Tref = 273.15   # standard temperature K
Ru = 8314.      # Universal gas constant in J/kg/K
mw_O2 = 32.     # molecular weight O2
mw_CH4 = 16.    # molecular weight CH4

def fsanalysis(fileobj):
    # First, copy the meta parameters using the default function
    out = lconfig.default_afun(fileobj)
    # Create calibrated data
    V = fileobj.data[:,0]
    I = fileobj.data[:,1]*25.242500 - .15605
    out['V'] = V
    out['I'] = I
    
    # Define an interpolation function
    def proto(c):
        # The ordered coefficients are in slopes and offsets
        # I = V*K + b
        # Regime 1 offset
        b1 = c[0]
        # Regime 1 resistance (slope)
        K1 = c[1]
        # Regime 2 offset
        b2 = c[2]
        # Regime 2 resistance (slope)
        K2 = c[3]
        # Regime 3 offset
        b3 = c[4]
        # Regime 3 resistance (slope)
        K3 = c[5]
        # Compute the intersection conditions
        v12 = (b2 - b1)/(K1 - K2)
        v23 = (b3 - b2)/(K2 - K3)
        # Compute the square of the errors
        Ifit = np.empty(I.shape)
        # Evaluate the fit by regimes
        error = 0.
        # The error in each regime is calculated separately.  This allows us
        # to apply different weighting factors to the different regimes.
        index = V<v12
        Ifit = V[index]*K1 + b1
        error += np.sum((I[index] - Ifit)**2)
        index = (V>=v12) * (V<v23)
        Ifit = V[index]*K2 + b2
        error += 10.*np.sum((I[index] - Ifit)**2)
        index = V>=v23
        Ifit = V[index]*K3 + b3
        error += np.sum((I[index] - Ifit)**2)
        return error
    
    # Formulate initial guesses for the optimum
    index = V<-5.
    b1,K1 = polyfit(V[index], I[index], 1)
    index = V>5.
    b3,K3 = polyfit(V[index], I[index], 1)
    index = np.abs(I)<7.
    b2,K2 = polyfit(V[index], I[index], 1)
    fit = optimize.minimize(proto, (b1,K1,b2,K2,b3,K3) ,method='Nelder-Mead')
    out['b1'] = fit.x[0]
    out['R1'] = 1./fit.x[1]
    out['b2'] = fit.x[2]
    out['R2'] = 1./fit.x[3]
    out['b3'] = fit.x[4]
    out['R3'] = 1./fit.x[5]
    Vwindow = 0.2
    out['Vwindow'] = Vwindow
    Vtest = 3.
    out['Vtest1'] = Vtest
    index = (V < (Vtest+Vwindow)) * (V > (Vtest-Vwindow))
    out['Imeas1'] = np.mean(I[index])
    out['Imax1'] = np.max(I[index]) - out['Imeas1']
    out['Imin1'] = -(np.min(I[index]) - out['Imeas1'])
    Vtest = 9.5
    out['Vtest2'] = Vtest
    index = (V < (Vtest+Vwindow)) * (V > (Vtest-Vwindow))
    out['Imeas2'] = np.mean(I[index])
    out['Imax2'] = np.max(I[index]) - out['Imeas2']
    out['Imin2'] = -(np.min(I[index]) - out['Imeas2'])

#    ax = plt.gca()
#    ax.clear()
#    ax.set_title(fileobj.filename)
#    ax.plot(V,I,'k.')
#    ax.plot(V,fit.x[0] + fit.x[1]*V, 'b')
#    ax.plot(V,fit.x[2] + fit.x[3]*V, 'r')
#    ax.plot(V,fit.x[4] + fit.x[5]*V, 'g')
#    plt.gcf().savefig('fit.png')
    return out

if '__loadall__' not in globals():
    C = lconfig.collection(afun=None)
    __loadall__ = True
    
    C105 = lconfig.collection(afun=fsanalysis, asave=False)
    C105.add_dir('data/105')
    for dat in C105.data:
        dat.analysis['d_in'] = 1.05
    C.merge(C105)
    
    C105_1 = lconfig.collection(afun=fsanalysis, asave=False)
    C105_1.add_dir('data/105_1')
    for dat in C105_1.data:
        dat.analysis['d_in'] = 1.05
    C.merge(C105_1)
    
    C125 = lconfig.collection(afun=fsanalysis, asave=False)
    C125.add_dir('data/125')
    for dat in C125.data:
        dat.analysis['d_in'] = 1.25
    C.merge(C125)
    
    C125_1 = lconfig.collection(afun=fsanalysis, asave=False)
    C125_1.add_dir('data/125_1')
    for dat in C125_1.data:
        dat.analysis['d_in'] = 1.25
    C.merge(C125_1)
    
    C125_2 = lconfig.collection(afun=fsanalysis, asave=False)
    C125_2.add_dir('data/125_2')
    for dat in C125_2.data:
        dat.analysis['d_in'] = 1.25
    C.merge(C125_2)
    
    C125_3 = lconfig.collection(afun=fsanalysis, asave=False)
    C125_3.add_dir('data/125_3')
    for dat in C125_3.data:
        dat.analysis['d_in'] = 1.25
    C.merge(C125_3)
    
    C150 = lconfig.collection(afun=fsanalysis, asave=False)
    C150.add_dir('data/150')
    for dat in C150.data:
        dat.analysis['d_in'] = 1.50
    C.merge(C150)
    
    C150_1 = lconfig.collection(afun=fsanalysis, asave=False)
    C150_1.add_dir('data/150_1')
    for dat in C150_1.data:
        dat.analysis['d_in'] = 1.50
    C.merge(C150_1)
    
    C150_2 = lconfig.collection(afun=fsanalysis, asave=False)
    C150_2.add_dir('data/150_2')
    for dat in C150_2.data:
        dat.analysis['d_in'] = 1.50
    C.merge(C150_2)
    
    C150_3 = lconfig.collection(afun=fsanalysis, asave=False)
    C150_3.add_dir('data/150_3')
    for dat in C150_3.data:
        dat.analysis['d_in'] = 1.50
    C.merge(C150_3)
    
    C225 = lconfig.collection(afun=fsanalysis, asave=False)
    C225.add_dir('data/225')
    for dat in C225.data:
        dat.analysis['d_in'] = 2.25
    C.merge(C225)
    
    C225_1 = lconfig.collection(afun=fsanalysis, asave=False)
    C225_1.add_dir('data/225_1')
    for dat in C225_1.data:
        dat.analysis['d_in'] = 2.25
    C.merge(C225_1)
    
    C.table(('d_in','flow_scfh','ratio_fto','plate_t_c','tip_t_c','plate_q_kw','standoff_in','b1','R1','b2','R2','b3','R3'),
            fileout='table.wsv')


# Construct comparison plots
plt.close('all')
lplot.set_defaults()

# Figure 1
# Overplot the IV curves for tests
ax = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)')

for dat in C150_1:
    ax.plot(dat.analysis['V'], dat.analysis['I'],'y.')
    
for dat in C105:
    ax.plot(dat.analysis['V'], dat.analysis['I'], 'b.')
    
for dat in C105_1:
    ax.plot(dat.analysis['V'], dat.analysis['I'], 'r.')
    
ax.legend(loc=0)
ax.set_xlim([-10,10])


# Figure 2
# Show tests with 20scfh
ax = lplot.init_fig('Voltage (V)', 'Current ($\mu$A)', figure_size=(6.,4.5))
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('Current ($\mu$A)')
flow = 20.
CC = C(flow_scfh = (flow-.5, flow+.5), d_in= (2.24,2.26))
CC.merge(C(flow_scfh = (flow-.5, flow+.5), d_in=(1.24,1.26)))
#CC.merge(C(flow_scfh = (flow-.5, flow+.5), d_in=(1.0,1.1)))
for dat in CC:
    leglab = 'F/O: %.2f Dia: %dmm'%(dat.analysis['ratio_fto'], 25.4*dat.analysis['d_in'])
    if dat.analysis['d_in'] > 2.24 and dat.analysis['d_in'] < 2.26:
        mfc = 'k'
    else:
        mfc = 'w'
    if dat.analysis['ratio_fto']<0.575:
        ms = 'o'
    elif dat.analysis['ratio_fto']<.625 and dat.analysis['ratio_fto']>.575:
        ms = '^'
    elif dat.analysis['ratio_fto']<.675 and dat.analysis['ratio_fto']>.625:
        ms = 'd'
    elif dat.analysis['ratio_fto']<.725 and dat.analysis['ratio_fto']>.675:
        ms = 's'
    ax.plot(dat.analysis['V'], dat.analysis['I'], ms, mec='k', mfc=mfc, ms=4.)
ax.set_xlim([-10,10])
lplot.floating_legend(ax.get_figure(), (0.97, 0.16),
    [[{'ls':'none','marker':'o','mec':'k','mfc':'w'}, {'ls':'none','marker':'o','mec':'k','mfc':'k'},'F/O ratio 0.55'],
     [{'ls':'none','marker':'^','mec':'k','mfc':'w'}, {'ls':'none','marker':'^','mec':'k','mfc':'k'},'F/O ratio 0.60'],
     [{'ls':'none','marker':'d','mec':'k','mfc':'k'},'F/O ratio 0.65'],
     [{'ls':'none','marker':'s','mec':'k','mfc':'w'}, {'ls':'none','marker':'s','mec':'k','mfc':'k'},'F/O ratio 0.70'],
     [{'ls':'none','marker':'o','mec':'k','mfc':'w'}, {'ls':'none','marker':'^','mec':'k','mfc':'w'}, {'ls':'none','marker':'s','mec':'k','mfc':'w'},'Dia. 32mm (1.25in)'],
     [{'ls':'none','marker':'o','mec':'k','mfc':'k'}, {'ls':'none','marker':'^','mec':'k','mfc':'k'}, {'ls':'none','marker':'d','mec':'k','mfc':'k'}, {'ls':'none','marker':'s','mec':'k','mfc':'k'},'Dia. 57mm (2.25in)'],],
     loc_edge = 'rb')
ax.get_figure().savefig('f20iv.png')


# Figure 4
# i vs flow

##
# Fit the charge density against flow rate
Cfit = C150_1()
Cfit.merge(C225_1)
Cfit.merge(C150_2)
Cfit.merge(C150_3)
Vdot = np.array(Cfit['flow_scfh'])
I = np.array(Cfit['Imeas2'])
coef = np.polynomial.polynomial.polyfit(Vdot, I/Vdot, 1)
# 

ax,ax1 = lplot.init_xxyy('Flow (L/min)','$I$ ($\mu$A)',x2label='Flow (scfh)',figure_size=(6.,4.5))

x = np.arange(0., 30., 1.)
ax.plot(scfh_to_lpm*x, (coef[1]*x + coef[0])*x, 'k--')
ax.errorbar(scfh_to_lpm*np.array(C150_1['flow_scfh']), C150_1['Imeas2'], fmt='k^',
            yerr=[C150_1['Imin2'], C150_1['Imax2']], 
            mec='k',mfc='w',ms=8,ecolor='k', label='Dia 38mm (1.5in)')
ax.errorbar(scfh_to_lpm*np.array(C150_2['flow_scfh']), C150_2['Imeas2'], fmt='ks',
            yerr=[C150_2['Imin2'], C150_2['Imax2']], 
            mec='k',mfc='w',ms=8,ecolor='k', label='38mm Test 2')
ax.errorbar(scfh_to_lpm*np.array(C150_3['flow_scfh']), C150_3['Imeas2'], fmt='kd',
            yerr=[C150_3['Imin2'], C150_3['Imax2']], 
            mec='k',mfc='w',ms=8,ecolor='k', label='38mm Test 3')
ax.errorbar(scfh_to_lpm*np.array(C225_1['flow_scfh']), C225_1['Imeas2'], fmt='ko',
            yerr=[C225_1['Imin2'], C225_1['Imax2']], 
            mec='k',mfc='w',ms=8,ecolor='k', label='Dia 57mm (2.25in)')
            


flashback_scfh = 6.

ax.axvline(x=scfh_to_lpm * flashback_scfh, color='k', linewidth = 2.)
ax.text(scfh_to_lpm*flashback_scfh, 5., 'FLASHBACK', rotation='vertical', 
        verticalalignment='bottom')

ax.set_xlim((0,12))
lplot.scale_xxyy(ax,xscale=1./.472)
ax.legend(loc=2, numpoints=1, fontsize=12.)
ax.get_figure().savefig('flow.png')



ax,ax1 = lplot.init_xxyy('Flow (L/min)',
                         'Charge fraction ($\\frac{n^+}{n_{cold} } \\times 10^9$)',x2label='Flow (scfh)',figure_size=(6.,4.5))

lpm_to_molps = pref * 1e5 / 8.314 / Tref / 60. / 1000.
columbs_to_moles = 1./96485.33289

x = np.arange(0,30.,1.)
ax.plot(scfh_to_lpm * x, 
        1e3 * columbs_to_moles * (coef[1]*x + coef[0]) / scfh_to_lpm / lpm_to_molps, 
        'k--')

Vdot = scfh_to_lpm * np.array(C150_1['flow_scfh'])
n = 1e3 * columbs_to_moles * np.array(C150_1['Imeas2']) / (lpm_to_molps * Vdot)
ax.plot(Vdot, n, 'k^',
            mec='k',mfc='w',ms=8,label='Dia 38mm (1.5in)')

Vdot = scfh_to_lpm * np.array(C150_2['flow_scfh'])
n = 1e3 * columbs_to_moles * np.array(C150_2['Imeas2']) / (lpm_to_molps * Vdot)
ax.plot(Vdot, n, 'ks',
            mec='k',mfc='w',ms=8,label='Dia 38mm Test 2')

Vdot = scfh_to_lpm * np.array(C150_3['flow_scfh'])
n = 1e3 * columbs_to_moles * np.array(C150_3['Imeas2']) / (lpm_to_molps * Vdot)
ax.plot(Vdot, n, 'kd',
            mec='k',mfc='w',ms=8,label='Dia 38mm Test 3')

Vdot = scfh_to_lpm * np.array(C225_1['flow_scfh'])
n = 1e3 * columbs_to_moles * np.array(C225_1['Imeas2']) / (lpm_to_molps * Vdot)
ax.plot(Vdot, n, 'ko',
            mec='k',mfc='w',ms=8,label='Dia 57mm (2.25in)')


ax.set_xlim([0,12])
ax.set_ylim([0,40])
ax.legend(loc=0)
lplot.scale_xxyy(ax,xscale=1./scfh_to_lpm)


Cheat = C(plate_t_c=(0.,270.))
ax,dummy = lplot.init_xxyy('Flow (L/min)', 'Heating (kW)', x2label='Flow (scfh)', figure_size=(6,4.5))
ax.plot(scfh_to_lpm * np.array(Cheat['flow_scfh']), Cheat['plate_q_kw'], 'ko')
lplot.scale_xxyy(ax,xscale=1./scfh_to_lpm)

# vtest = 4.0
#
#flow = C125_2['flow_scfh']
#R3 = np.array(C125_2['R3'])
#b3 = np.array(C125_2['b3'])
#ax.plot(flow, b3 + vtest/R3, 'bo', label='1.25-2 (%.1fV)'%vtest)
#
#flow = C125_3['flow_scfh']
#R3 = np.array(C125_3['R3'])
#b3 = np.array(C125_3['b3'])
#ax.plot(flow, b3 + vtest/R3, 'co', label='1.25-3 (%.1fV)'%vtest)
#
#flow = C150['flow_scfh']
#R3 = np.array(C150['R3'])
#b3 = np.array(C150['b3'])
#ax.plot(flow, b3 + vtest/R3, 'go', label='1.50 (%.1fV)'%vtest)
#

##### THIS WAS ON #####
#flow = C150_1['flow_scfh']
#R3 = np.array(C150_1['R3'])
#b3 = np.array(C150_1['b3'])
#ax.plot(flow, b3 + vtest/R3, '^', 
#        markeredgecolor='k', markerfacecolor='w',
#        label='1.50-1 (%.1fV)'%vtest)
#
#flow = C150_2['flow_scfh']
#R3 = np.array(C150_2['R3'])
#b3 = np.array(C150_2['b3'])
#ax.plot(flow, b3 + vtest/R3, 'o', 
#        markeredgecolor='k', markerfacecolor='w',
#        label='1.50-2 (%.1fV)'%vtest)
#
#flow = C150_3['flow_scfh']
#R3 = np.array(C150_3['R3'])
#b3 = np.array(C150_3['b3'])
#ax.plot(flow, b3 + vtest/R3, 's', 
#        markeredgecolor='k', markerfacecolor='w',
#        label='1.50-3 (%.1fV)'%vtest)
#############

#flow = C225['flow_scfh']
#R3 = np.array(C225['R3'])
#b3 = np.array(C225['b3'])
#ax.plot(flow, b3 + vtest/R3, 'ro', label='2.25 (%.1fV)'%vtest)

##### THIS WAS ON ########
#flow = C225_1['flow_scfh']
#R3 = np.array(C225_1['R3'])
#b3 = np.array(C225_1['b3'])
#ax.plot(flow, b3 + vtest/R3, 'd', 
#        markeredgecolor='k', markerfacecolor='w',
#        label='2.25-1 (%.1fV)'%vtest)
###################

#vtest = 8.5

#flow = C125_2['flow_scfh']
#R3 = np.array(C125_2['R3'])
#b3 = np.array(C125_2['b3'])
#ax.plot(flow, b3 + vtest/R3, 'b^', label='1.25-2 (%.1fV)'%vtest)
#
#flow = C125_3['flow_scfh']
#R3 = np.array(C125_3['R3'])
#b3 = np.array(C125_3['b3'])
#ax.plot(flow, b3 + vtest/R3, 'c^', label='1.25-3 (%.1fV)'%vtest)
#
#flow = C150['flow_scfh']
#R3 = np.array(C150['R3'])
#b3 = np.array(C150['b3'])
#ax.plot(flow, b3 + vtest/R3, 'g^', label='1.50 (%.1fV)'%vtest)
#


######### THIS WAS ON ###############
#flow = C150_1['flow_scfh']
#R3 = np.array(C150_1['R3'])
#b3 = np.array(C150_1['b3'])
#ax.plot(flow, b3 + vtest/R3, 'm^', label='1.50-1 (%.1fV)'%vtest)
#
#flow = C150_2['flow_scfh']
#R3 = np.array(C150_2['R3'])
#b3 = np.array(C150_2['b3'])
#ax.plot(flow, b3 + vtest/R3, 'y^', label='1.50-2 (%.1fV)'%vtest)
#
#flow = C150_3['flow_scfh']
#R3 = np.array(C150_3['R3'])
#b3 = np.array(C150_3['b3'])
#ax.plot(flow, b3 + vtest/R3, 'k^', label='1.50-3 (%.1fV)'%vtest)
#####################

#flow = C225['flow_scfh']
#R3 = np.array(C225['R3'])
#b3 = np.array(C225['b3'])
#ax.plot(flow, b3 + vtest/R3, 'r^', label='2.25 (%.1fV)'%vtest)

########################
#flow = C225_1['flow_scfh']
#R3 = np.array(C225_1['R3'])
#b3 = np.array(C225_1['b3'])
#ax.plot(flow, b3 + vtest/R3, 'c^', label='2.25-1 (%.1fV)'%vtest)
#######################

