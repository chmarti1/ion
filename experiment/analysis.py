#
#   Run analysis on the flamesense data
#

# Grab the module for loading these data
import loadall
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
poly = np.polynomial.polynomial

# Where to find the data files
master_dir = 'data'
precision_dir = master_dir + '/precision'
noplate_dir = master_dir + '/noplate'
# resize the default font to 8
matplotlib.rc('font',size=9.)

def init_fig(xlabel,ylabel):
    """set up a figure with a single axes
    ax = init_fig(xlabel,ylabel)
Returns the axis for plotting    
"""
    std_size = (4., 3.5)
    f = plt.figure()
    f.set_size_inches(std_size)
    ax = f.add_axes([.17,.15,.78,.80],label='primary')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid('on')
    return ax

def init_xxyy(xlabel,ylabel,x2label=None,y2label=None):
    """set up a figure with two axes overlayed
    ax1,ax2 = init_xxyy(xlabel,ylabel,x2label=None,y2label=None)

Used for making dual x or y axis plots, ax1 contains all data and the primary
x and y axes.  ax2 is used solely to create top (right) x (y) ticks with a 
different scale.

If x2label and/or y2label are specified, then the 
"""
    ax1 = init_fig(xlabel,ylabel)
    f = ax1.get_figure()
    p = ax1.get_position()
    ax2 = f.add_axes(p,label='secondary')
    ax2.set_axis_bgcolor('none')
    axis = ax2.get_xaxis()
    axis.set_ticks_position('top')
    axis.set_label_position('top')
    if x2label==None:
        ax2.set_xticks([])
    else:
        p.y1 = .85
        ax2.set_xlabel(x2label)
    axis = ax2.get_yaxis()
    axis.set_ticks_position('right')
    axis.set_label_position('right')
    if y2label==None:
        ax2.set_yticks([])
    else:
        p.x1 = .83
        ax2.set_ylabel(y2label)
    ax1.set_position(p)
    ax2.set_position(p)
    return ax1,ax2


#===============#
#   LOAD DATA   #
#===============#
if False:
    print "Loading files...",
    record = loadall.loadall(master_dir)
    noplate = loadall.loadall(noplate_dir)
    precision = loadall.loadall(precision_dir)
    print "done."
    
#=======================#
#    RENEW CURVE FITS   #
#=======================#

if False:
    print "Renewing master curve fits",
    loadall.fitindex(record,range(9,87))
    print "Curve fits complete."


# These indices correspond to precision measurements in the negative saturation
# and ohmic regions
precision_nsat = []
for ii in range(0,40,4):
    precision_nsat += [ii, ii+3]
precision_ohmic =range(40,61)

if False:
    print "Renewing precision measurements..",
    for thisindex in precision_nsat:
        v = precision['V'][thisindex]
        i = precision['I'][thisindex]
        N = v.size
        fexcite = precision['data'][thisindex].config[0].aoch[0].frequency
        fsample = precision['data'][thisindex].config[0].samplehz
        V = np.fft.fft(v)
        I = np.fft.fft(i)
        f0 = fsample/N  # the frequency resolution
        findex = int(np.round(fexcite / f0)) # the index nearest the excitation
        # Find the slope and offset
        a1 = (I[findex]/V[findex]).real
        b1 = (I[0].real - a1*V[0].real)/N
        c = [0]*6
        c[0] = a1
        c[4] = b1
        precision['analysis'][thisindex]['c'] = c
        
    for thisindex in precision_ohmic:
        v = precision['V'][thisindex]
        i = precision['I'][thisindex]
        N = v.size
        fexcite = precision['data'][thisindex].config[0].aoch[0].frequency
        fsample = precision['data'][thisindex].config[0].samplehz
        V = np.fft.fft(v)
        I = np.fft.fft(i)
        f0 = fsample/N  # the frequency resolution
        findex = int(np.round(fexcite / f0)) # the index nearest the excitation
        # Find the slope and offset
        a2 = (I[findex]/V[findex]).real
        v0 = (V[0].real - I[0].real/a2)/N
        c = [0]*6
        c[1] = a2
        c[3] = v0
        precision['analysis'][thisindex]['c'] = c
    print "done."
    



#========================#
#    SAVE TABULAR DATA   #
#========================#
if True:
    # test standoff peakT oxygen fuel flow f/o R1 R2 R3 v0 i1 i2
    head = '{:3s} {:5s} {:4s} {:5s} {:5s} {:5s} {:5s} {:8s} {:8s} {:8s} {:8s} {:8s} {:8s} {:s}\n'
    fmt = '{:3d} {:5.3f} {:4d} {:5.2f} {:5.2f} {:5.2f} {:5.3f} {:8.6f} {:8.6f} {:8.6f} {:8.6f} {:8.6f} {:8.6f} {:s}\n'
    filename = 'TABLE.wsv'
    with open(filename,'w+') as ff:
        # write the header
        ff.write(head.format('tst','S.O.','Temp','O2','FG','Flow','F/O','R1','R2','R3','v0','i1','i2','File'))
        
        Nrec = len(record['filename'])
        for index in range(Nrec):
            s = record['standoff_in'][index]
            tpeak = int(record['plate_tpeak_c'][index])
            o2 = record['oxygen_scfh'][index]
            fg = record['fuel_scfh'][index]
            flow = record['flow_scfh'][index]
            r = record['ratio_fto'][index]
            if record['analysis'][index]:
                R1 = 1./record['analysis'][index]['c'][0]
                R2 = 1./record['analysis'][index]['c'][1]
                R3 = 1./record['analysis'][index]['c'][2]
                v0 = record['analysis'][index]['c'][3]
                i1 = record['analysis'][index]['c'][4]
                i2 = record['analysis'][index]['c'][5]
            else:
                R1=R2=R3=v0=i1=i2=0.
            thisfile = record['filename'][index]
            ff.write(fmt.format(index,s,tpeak,o2,fg,flow,r,R1,R2,R3,v0,i1,i2,thisfile))
            
    

if False:
    # First, close any open plots
    plt.close('all')
    
    #
    #   Now, it's time to tell the story
    #   These plots are organized by the topic being investigated
    #
    
    #===============================#
    #   Generic IV characteristics  #
    #===============================#
    ax1 = init_fig('Voltage (V)','Current ($\mu$A)')
    i = record['I'][22]
    v = record['V'][22]
    ax1.plot(v,i,marker='d',mec='k',mew=.5,mfc='w',ls='none',label='.23in, .55')
    i = record['I'][27]
    v = record['V'][27]
    ax1.plot(v,i,marker='o',mec='k',mew=.5,mfc='w',ls='none', label='.23in, .80')
    i = record['I'][39]
    v = record['V'][39]
    ax1.plot(v,i,marker='s',mec='k',mew=.5,mfc='k',ls='none', label='.46in, .55')
    ax1.legend(loc=0)
    ax1.set_xlim([-10,10])
    
    
    #===================#
    #   STANDOFF        #
    #===================#
    #35-47 constitute a standoff experiment
    #nominal flow was 20scfh
    # mixture was 0.55fto
    use = range(35,48)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    s = loadall.Xfromindex(record,'standoff_in',use)
    # Use curve fit
    C = poly.polyfit(s,R2,1)
    
    ax1,ax2 = init_xxyy('Standoff (in)', 'Resistance $R_1$ (k$\Omega$)',\
                        x2label='Standoff (mm)')
    ax1.set_xlim([0,.6])
    ax2.set_xlim([0,.6*25.4])
    
    ax1.errorbar(s,1e3*R2,xerr=.01,marker='d',ecolor='k', mec='k', mfc='w', mew=1., ls='none')
    ss = np.arange(0,0.6,.05)
    RR = poly.polyval(ss,C)
    ax1.plot(ss,1e3*RR,'k--')
    ax1.text(.11,65.,
            "{:.1f}k$\Omega$-in$^{{-1}}$\n{:.2f}k$\Omega$mm$^{{-1}}$"\
            .format(C[1]*1e3, C[1]*1e3/25.4),
            backgroundcolor='w')
    
    
    
    #===================#
    #   MIXTURE         #
    #===================#
    # There are four mixture tests
    # 17-29 are at .228 standoff, 20scfh flow
    # 48-55 are at .456 standoff, 20scfh flow
    # 56-63 are at .684 standoff, 20scfh flow
    
    #ax1 = f1.add_subplot(211)
    #ax2 = f1.add_subplot(212)
    ax1 = init_fig('F/O Ratio', 'Effective $R_1$ (M$\Omega$)')
    ax1.set_xlim([0.5,0.8])
    ax1.set_ylim([0,.6])
    ax2 = init_fig('F/O Ratio', 'Effective $R_1^\prime$ (M$\Omega$)')
    ax2.set_xlim([0.5,0.8])
    ax2.set_ylim([0,.6])
    ax3 = init_fig('F/O Ratio', '$R_2$ (M$\Omega$)')
    ax3.set_xlim([0.5,0.82])
    ax4 = init_fig('$R_1^\prime - R_1^\prime(.6)$ (M$\Omega$)',
                   '$R_2 - R_2(.6)$ (M$\Omega$)')
    ax4.set_xlim([-.1,1.5])
    ax4.set_ylim([-.01,.2])
    ax5 = init_fig('F/O Ratio', 'Region 1 Saturation ($\mu$A)')
    
    
    r_ref = 0.6
    xx = np.array([])
    yy = np.array([])
    
    use = range(17,29)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    v0 = loadall.Rfromindex(record,4,use)
    isat = loadall.Rfromindex(record,5,use)
    #b1 = loadall.Rfromindex(record,5,use)
    # (isat-b1)*R1 == isat*R2 + v0
    #isat = (v0 + b1*R1)/(R1-R2)
    r = loadall.Xfromindex(record,'ratio_fto',use)
    R1adj = R1-R2
    ax1.plot(r,R1,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')
    ax2.plot(r,R1adj,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')
    ax3.plot(r,R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')
    index = np.argmin(np.abs(r-r_ref))
    ax4.plot(R1adj-R1adj[index],R2-R2[index],marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')
    ax5.plot(r,isat,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in (5.8mm)')
    xx = np.concatenate((xx,R1adj-R1adj[index]))
    yy = np.concatenate((yy,R2-R2[index]))
    
    use = range(48,55)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    v0 = loadall.Rfromindex(record,4,use)
    isat = loadall.Rfromindex(record,5,use)
    #b1 = loadall.Rfromindex(record,5,use)
    # i1 = v/R1 + b1
    # i2 = (v-v0)/R2
    # (isat-b1)*R1 == isat*R2 + v0
    #isat = (v0 + b1*R1)/(R1-R2)
    r = loadall.Xfromindex(record,'ratio_fto',use)
    R1adj = R1-R2
    ax1.plot(r,R1,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')
    ax2.plot(r,R1adj,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')
    ax3.plot(r,R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')
    index = np.argmin(np.abs(r-r_ref))
    ax4.plot(R1adj-R1adj[index],R2-R2[index],marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')
    ax5.plot(r,isat,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.46 (11.7)')
    xx = np.concatenate((xx,R1adj-R1adj[index]))
    yy = np.concatenate((yy,R2-R2[index]))
    
    use = range(56,64)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    v0 = loadall.Rfromindex(record,4,use)
    isat = loadall.Rfromindex(record,5,use)
    #b1 = loadall.Rfromindex(record,5,use)
    # (isat-b1)*R1 == isat*R2 + v0
    #isat = (v0 + b1*R1)/(R1-R2)
    r = loadall.Xfromindex(record,'ratio_fto',use)
    R1adj = R1-R2
    ax1.plot(r,R1,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax2.plot(r,R1-R2,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax3.plot(r,R2,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    index = np.argmin(np.abs(r-r_ref))
    ax4.plot(R1adj-R1adj[index],R2-R2[index],marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax5.plot(r,isat,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    xx = np.concatenate((xx,R1adj-R1adj[index]))
    yy = np.concatenate((yy,R2-R2[index]))
    
    # Perform fit.
    use = xx < 0.8
    C = poly.polyfit(xx[use],yy[use],1)
    x = np.arange(-.1,1.)
    ax4.plot(x, poly.polyval(x,C), 'k--')
    ax4.text(.5,.05,'$\Delta R_2 = ({:.4f})\Delta R_1^\prime$'.format(C[1]),backgroundcolor='w')
    
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax3.legend(loc=2)
    ax4.legend(loc=2)
    ax5.legend(loc=0)
    
    #===========#
    #   FLOW    #
    #===========#
    # There are three flow tests
    # 14,15 are at standoff .228in, various fto
    # 29-34 are at standoff .228in, .50fto
    # 64-73 are at standoff .228in, .70fto
    ax1,ax11 = init_xxyy('Total Flow (scfh)', '$R_3^\prime$ (M$\Omega$)', \
                    x2label='Total Flow (Lpm)')
    xlim = np.array([20,32])
    ax1.set_xlim(xlim)
    ax11.set_xlim(xlim*.4719)
    
    ax2,ax11 = init_xxyy('Total Flow (scfh)', '$R_1^\prime$ (M$\Omega$)', \
                    x2label='Total Flow (Lpm)')
    ax2.set_xlim(xlim)
    ax2.set_ylim([0,.3])
    ax11.set_xlim(xlim*.4719)
    
    ax3,ax11 = init_xxyy('Total Flow (scfh)', '$R_2$ (M$\Omega$)', \
                    x2label='Total Flow (Lpm)')
    ax3.set_xlim(xlim)
    ax3.set_ylim([0,.08])
    ax11.set_xlim(xlim*.4719)
    
    
    use = [14,15] + range(29,34)
    flow = loadall.Xfromindex(record,'flow_scfh',use)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    ax1.plot(flow,R3-R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.50')
    ax2.plot(flow,R1-R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.50')
    ax3.plot(flow,R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.50')
    
    use = range(64,74)
    flow = loadall.Xfromindex(record,'flow_scfh',use)
    R1 = loadall.Rfromindex(record,1,use)
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    ax1.plot(flow,R3-R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.70')
    ax2.plot(flow,R1-R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.70')
    ax3.plot(flow,R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.70')
    
    ax1.legend(loc=0)
    ax2.legend(loc=0)
    ax3.legend(loc=4)
    
    
    #===========#
    #   Temperature    #
    #===========#
    ax1,ax2 = init_xxyy('Plate Temperature ($^\circ$C)', '$R_3^\prime$ (M$\Omega$)',\
                        x2label='Plate Temperature ($^\circ$F)')
    ax3,ax4 = init_xxyy('Plate Temperature ($^\circ$C)', '$R_3^\prime$ (M$\Omega$)',\
                        x2label='Plate Temperature ($^\circ$F)')
    
    use = [22, 35, 45]
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    T = loadall.Xfromindex(record,'plate_tpeak_c',use)
    ax1.errorbar(T,R3-R2,xerr=100.,ecolor='k',marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.55')
    
    use = range(78,80)
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    T = loadall.Xfromindex(record,'plate_tpeak_c',use)
    ax1.errorbar(T,R3-R2,xerr=100.,ecolor='k',marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.70')
    
    use = range(74,78) + range(80,87)
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    T = loadall.Xfromindex(record,'plate_tpeak_c',use)
    #ax1.errorbar(T,R3-R2,xerr=100.,ecolor='k',marker='s',mec='k',mfc='k',mew=1.,ls='none',label='.55')
    ax1.plot(T,R3-R2,marker='s',mec='k',mfc='w',mew=1.,ls='none',label='.55')
    
    xlim = ax1.get_xlim()
    xlim = [a*1.8+32 for a in xlim]
    ax2.set_xlim(xlim)
    
    ax1.legend(loc=0)
    
    use = range(9,87)
    R2 = loadall.Rfromindex(record,2,use)
    R3 = loadall.Rfromindex(record,3,use)
    T = loadall.Xfromindex(record,'plate_tpeak_c',use)
    ax3.plot(T,R3-R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.70')
    
