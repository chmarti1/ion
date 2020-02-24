# Post analysis and plotting for the flamesense data
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import lconfig
import os
poly = np.polynomial.polynomial

data_dir = 'data/'
export_dir = 'export/'



matplotlib.rc('font',size=9.)
std_size = (4., 3.5)
std_dpi = 300
std_type = '.tif'

def init_fig(xlabel,ylabel):
    """set up a figure with a single axes
    ax = init_fig(xlabel,ylabel)
Returns the axis for plotting    
"""

    f = plt.figure(figsize=std_size, dpi=std_dpi)
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

so_in = []
temp_C = []
o2_scfh = []
fg_scfh = []
flow_scfh = []
fo_ratio = []
r1_mohm = []
r2_mohm = []
r3_mohm = []
v0_volts = []
i1_ua = []
i2_ua = []
filename = []

# Load the whitspace-separated-variable file
with open('TABLE.wsv','r') as ff:
    text=ff.readline()
    for text in ff:
        line = text.split()
        index = 1
        so_in.append(float(line[index])); index+=1
        temp_C.append(float(line[index])); index+=1
        o2_scfh.append(float(line[index])); index+=1
        fg_scfh.append(float(line[index])); index+=1
        flow_scfh.append(float(line[index])); index+=1
        fo_ratio.append(float(line[index])); index+=1
        r1_mohm.append(float(line[index])); index+=1
        r2_mohm.append(float(line[index])); index+=1
        r3_mohm.append(float(line[index])); index+=1
        v0_volts.append(float(line[index])); index+=1
        i1_ua.append(float(line[index])); index+=1
        i2_ua.append(float(line[index])); index+=1
        filename.append(line[index])

so_in = np.array(so_in)
temp_C = np.array(temp_C)
o2_scfh = np.array(o2_scfh)
fg_scfh = np.array(fg_scfh)
flow_scfh = np.array(flow_scfh)
fo_ratio = np.array(fo_ratio)
r1_mohm = np.array(r1_mohm)
r2_mohm = np.array(r2_mohm)
r3_mohm = np.array(r3_mohm)
v0_volts = np.array(v0_volts)
i1_ua = np.array(i1_ua)
i2_ua = np.array(i2_ua)


np_so_in = []
np_temp_C = []
np_o2_scfh = []
np_fg_scfh = []
np_flow_scfh = []
np_fo_ratio = []
np_r1_mohm = []
np_r2_mohm = []
np_r3_mohm = []
np_v0_volts = []
np_i1_ua = []
np_i2_ua = []
np_filename = []
# Load the whitspace-separated-variable file
with open('NPTABLE.wsv','r') as ff:
    text=ff.readline()
    for text in ff:
        line = text.split()
        index = 1
        np_so_in.append(float(line[index])); index+=1
        np_temp_C.append(float(line[index])); index+=1
        np_o2_scfh.append(float(line[index])); index+=1
        np_fg_scfh.append(float(line[index])); index+=1
        np_flow_scfh.append(float(line[index])); index+=1
        np_fo_ratio.append(float(line[index])); index+=1
        np_r1_mohm.append(float(line[index])); index+=1
        np_r2_mohm.append(float(line[index])); index+=1
        np_r3_mohm.append(float(line[index])); index+=1
        np_v0_volts.append(float(line[index])); index+=1
        np_i1_ua.append(float(line[index])); index+=1
        np_i2_ua.append(float(line[index])); index+=1
        np_filename.append(line[index])

np_so_in = np.array(np_so_in)
np_r2_mohm = np.array(np_r2_mohm)


# First, close any open plots
plt.close('all')

#
#   Now, it's time to tell the story
#   These plots are organized by the topic being investigated
#

if True:
    #===============================#
    #   Generic IV characteristics  #
    #===============================#
    
    ax1,ax2 = init_xxyy('Time (seconds)', 'Applied Voltage', y2label='Measured Current ($\mu$A)')
    
    this = lconfig.dfile(data_dir + filename[22])
    T = 1./this.config[0].samplehz
    i = this.data[:,1]*25.242500 - .15605
    v = this.data[:,0]
    t = np.arange(0,len(i)*T, T)
    vline = ax1.plot(t,v,'k-')
    iline = ax2.plot(t,i,'k--')
    ax1.set_xlim([0,max(t)])
    ax2.set_xlim([0,max(t)])
    ax2.set_ylim([-100,100])
    ax1.legend(vline+iline,('Voltage','Current'),loc=1)
    export_file = 'signal'
    plt.savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    ax2 = init_fig('Applied Voltage', 'Measured Current ($\mu$A)')
    this = lconfig.dfile(data_dir + filename[22])
    i = this.data[:,1]*25.242500 - .15605
    v = this.data[:,0]
    ax2.plot(v,i,marker='d',ms=4,mec='k',mew=.5,mfc='w',ls='none',label='.23in, .55')
    this = lconfig.dfile(data_dir + filename[27])
    i = this.data[:,1]*25.242500 - .15605
    v = this.data[:,0]
    ax2.plot(v,i,marker='o',ms=4,mec='k',mew=.5,mfc='w',ls='none', label='.23in, .80')
    this = lconfig.dfile(data_dir + filename[39])
    i = this.data[:,1]*25.242500 - .15605
    v = this.data[:,0]
    ax2.plot(v,i,marker='s',ms=4,mec='k',mew=.5,mfc='w',ls='none', label='.46in, .55')
    ax2.legend(loc=0)
    ax2.set_xlim([-10,10])
    
    export_file = 'ivchar'
    plt.savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)

if False:
    #===================#
    #   STANDOFF        #
    #===================#
    #35-47 constitute a standoff experiment
    #nominal flow was 20scfh
    # mixture was 0.55fto
    use = range(35,48)
    s = so_in[use]
    r2 = r2_mohm[use]
    # Use curve fit
    C = poly.polyfit(s,r2,1)
    
    ax1,ax2 = init_xxyy('Standoff (in)', 'Resistance $R_{OC}$ (k$\Omega$)',\
                        x2label='Standoff (mm)')
    ax1.set_xlim([0,.6])
    ax2.set_xlim([0,.6*25.4])
    
    ax1.errorbar(s,1e3*r2,xerr=.01,marker='d',ecolor='k', mec='k', mfc='w', mew=1., ls='none')
    ax1.plot(np_so_in, 1e3*np_r2_mohm, marker='s',mfc='k',ls='none')
    ss = np.arange(0,0.6,.05)
    RR = poly.polyval(ss,C)
    ax1.plot(ss,1e3*RR,'k--')
    ax1.text(.25,90.,
            "{:.1f}k$\Omega$-in$^{{-1}}$\n{:.2f}k$\Omega$mm$^{{-1}}$"\
            .format(C[1]*1e3, C[1]*1e3/25.4),
            backgroundcolor='w')
            
    export_file = 'so'
    plt.savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    

if False:
    #===================#
    #   MIXTURE         #
    #===================#
    # There are four mixture tests
    # 17-29 are at .228 standoff, 20scfh flow
    # 48-55 are at .456 standoff, 20scfh flow
    # 56-63 are at .684 standoff, 20scfh flow
    
    #ax1 = f1.add_subplot(211)
    #ax2 = f1.add_subplot(212)
    ax1 = init_fig('F/O Ratio', '$R_1$ (M$\Omega$)')
    ax1.set_xlim([0.5,0.8])
    ax1.set_ylim([0,.6])
    ax2 = init_fig('F/O Ratio', '$R_{IC}$ (M$\Omega$)')
    ax2.set_xlim([0.5,0.8])
    ax2.set_ylim([0,.6])
    ax3 = init_fig('F/O Ratio', '$R_{OC}$ (M$\Omega$)')
    ax3.set_xlim([0.5,0.82])
    ax4 = init_fig('$R_{IC} - R_{IC}(.6)$ (M$\Omega$)',
                   '$R_{OC} - R_{OC}(.6)$ (M$\Omega$)')
    ax4.set_xlim([-.1,1.5])
    ax4.set_ylim([-.01,.2])
    ax5 = init_fig('F/O Ratio', 'Region 1 Saturation ($\mu$A)')
    
    
    r_ref = 0.6
    xx = np.array([])
    yy = np.array([])
    
    use = range(17,29)
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    r = fo_ratio[use]
    v0 = v0_volts[use]
    isat = i1_ua[use]
    
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
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    r = fo_ratio[use]
    v0 = v0_volts[use]
    isat = i1_ua[use]
    
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
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    r = fo_ratio[use]
    v0 = v0_volts[use]
    isat = i1_ua[use]
    b = ((R1-R2)*isat - v0)/R1
    temp = isat / (R1-R2)
    err = (temp*R2*.05)**2 + ((b/(R1-R2) - temp)*R1*.05)**2
    err = err ** .5
    
    
    R1adj = R1-R2
    ax1.plot(r,R1,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax2.plot(r,R1-R2,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax3.plot(r,R2,marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    index = np.argmin(np.abs(r-r_ref))
    ax4.plot(R1adj-R1adj[index],R2-R2[index],marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    ax5.errorbar(r,isat,yerr=err,ecolor='k',marker='^',mec='k',mfc='k',ls='none',label='.68 (17.3)')
    xx = np.concatenate((xx,R1adj-R1adj[index]))
    yy = np.concatenate((yy,R2-R2[index]))
    
    # Perform fit.
    use = xx < 0.8
    C = poly.polyfit(xx[use],yy[use],1)
    x = np.arange(-.1,1.)
    ax4.plot(x, poly.polyval(x,C), 'k--')
    ax4.text(.5,.05,'$\Delta R_{{OC}} = ({:.4f})\Delta R_{{IC}}$'.format(C[1]),backgroundcolor='w')
    
    ax1.legend(loc=2)
    ax2.legend(loc=2)
    ax3.legend(loc=2)
    ax4.legend(loc=2)
    ax5.legend(loc=0)
    
    export_file = 'r1r'
    ax1.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'r1pr'
    ax2.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'r2r'
    ax3.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'r2r1p'
    ax4.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'i1r'
    ax5.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)

if False:
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
    
    ax2,ax11 = init_xxyy('Total Flow (scfh)', '$R_{IC}$ (M$\Omega$)', \
                    x2label='Total Flow (Lpm)')
    ax2.set_xlim(xlim)
    ax2.set_ylim([0,.3])
    ax11.set_xlim(xlim*.4719)
    
    ax3,ax11 = init_xxyy('Total Flow (scfh)', '$R_{OC}$ (M$\Omega$)', \
                    x2label='Total Flow (Lpm)')
    ax3.set_xlim(xlim)
    ax3.set_ylim([0,.09])
    ax11.set_xlim(xlim*.4719)
    
    ax6,ax11 = init_xxyy('Total Flow (scfh)', 'I_1 ($\mu$A)', x2label='Total Flow (Lpm)')
    ax6.set_xlim(xlim)
    ax11.set_xlim(xlim*.4719)
    
    
    use = [14,15] + range(29,34)
    flow = flow_scfh[use]
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    R3 = r3_mohm[use]
    i1 = i1_ua[use]
    ax1.plot(flow,R3-R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .50')
    ax2.plot(flow,R1-R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .50')
    ax3.plot(flow,R2,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .50')
    ax6.plot(flow,i1,marker='d',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .50')
    
    use = range(64,74)
    flow = flow_scfh[use]
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    R3 = r3_mohm[use]
    i1 = i1_ua[use]
    ax1.plot(flow,R3-R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .70')
    ax2.plot(flow,R1-R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .70')
    ax3.plot(flow,R2,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .70')
    ax6.plot(flow,i1,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='.23in, .70')
    
    use = range(87,98)
    flow = flow_scfh[use]
    R1 = r1_mohm[use]
    R2 = r2_mohm[use]
    R3 = r3_mohm[use]
    i1 = i1_ua[use]
    ax1.plot(flow,R3-R2,marker='s',mec='k',mfc='k',mew=1.,ls='none',label='.29in, .70')
    ax2.plot(flow,R1-R2,marker='s',mec='k',mfc='k',mew=1.,ls='none',label='.29in, .70')
    ax3.plot(flow,R2,marker='s',mec='k',mfc='k',mew=1.,ls='none',label='.29in, .70')
    ax6.plot(flow,i1,marker='s',mec='k',mfc='k',mew=1.,ls='none',label='.29in, .70')
    
    ax1.legend(loc=0)
    ax2.legend(loc=0)
    ax3.legend(loc=4)
    ax6.legend(loc=0)
    
    export_file = 'r3pf'
    ax1.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'r1pf'
    ax2.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'r2f'
    ax3.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    
    export_file = 'i1f'
    ax6.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)
    

if True:
    #===========#
    #   Temperature    #
    #===========#
    ax1,ax2 = init_xxyy('Plate Temperature ($^\circ$C)', '$I_2$ ($\mu$A)',\
                        x2label='Plate Temperature ($^\circ$F)')
    ax3,ax4 = init_xxyy('Plate Temperature ($^\circ$C)', '$I_2$ ($\mu$A)',\
                        x2label='Plate Temperature ($^\circ$F)')            
    

    use = range(35,48)
    T = temp_C[use]
    isat = i2_ua[use]
    ax1.plot(T,isat,marker='d',mfc='w',mec='k',ls='none',label='Series 1')
    
    use = range(74,78)
    T = temp_C[use]
    isat = i2_ua[use]
    ax1.plot(T,isat,marker='o',mfc='w',mec='k',ls='none',label='Series 2')
    
    use = range(78,80)
    T = temp_C[use]
    isat = i2_ua[use]
    ax1.plot(T,isat,marker='s',mfc='w',mec='k',ls='none',label='Series 3')
    
    use = range(80,87)
    T = temp_C[use]
    isat = i2_ua[use]
    ax1.plot(T,isat,marker='^',mfc='w',mec='k',ls='none',label='Series 4')
    
    xlim = ax1.get_xlim()
    xlim = [a*1.8+32 for a in xlim]
    ax2.set_xlim(xlim)

    ax1.legend(loc=0)    
    
    export_file = 'i2T'
    ax1.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)    
    
    
    
    xlim = ax3.get_xlim()
    xlim = [a*1.8+32 for a in xlim]
    ax4.set_xlim(xlim)
    

    useSO = (so_in == .228) * (np.arange(len(so_in))>8)
    useFLOW = (flow_scfh < 22.) * (flow_scfh > 18.)
    useFLOW = useFLOW * useSO
    useSO *= ~useFLOW

    T = temp_C[useFLOW]
    isat = i2_ua[useFLOW]
    ax3.plot(T,isat,marker='o',mec='k',mfc='w',mew=1.,ls='none',label='20scfh')
    T = temp_C[useSO]
    isat = i2_ua[useSO]
    ax3.plot(T,isat,marker='d',mec='k',mfc='k',mew=1.,ls='none',label='other')

    xlim = ax3.get_xlim()
    xlim = [a*1.8+32 for a in xlim]
    ax4.set_xlim(xlim)

    ax1.legend(loc=0)   

    export_file = 'i2T_'
    ax3.get_figure().savefig(os.path.join(export_dir,export_file + std_type), dpi=std_dpi)

