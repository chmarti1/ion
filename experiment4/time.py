#!/usr/bin/python

# Generate a time series plot comparing signals from different tests

import lplot
import lconfig as lc
import matplotlib.pyplot as plt

t_window = 0.2

sources = [\
    ('190322/test2.dat', 95., 'k', '0-25uA'),
    ('190327/test2.dat', 62., 'k-.', '0-10uA'),
    ('190327/test9.dat', 62., 'k--', '5-15uA')]

lplot.set_defaults()
axI = lplot.init_fig('Time (s)', 'Current ($\mu$A)')
axV = lplot.init_fig('Time (s)', 'Voltage(V)')
    
for thisfile, tstart, thisstyle, thislabel in sources:
    D = lc.LConf(thisfile, data=True)
    t = D.get_time(start=tstart, stop=tstart+t_window)
    t-=t[0]
    V = D.get_channel('Voltage', start=tstart, stop=tstart+t_window)
    I = D.get_channel('Current', start=tstart, stop=tstart+t_window)
    axV.plot(t, V, thisstyle, label=thislabel)
    axI.plot(t, I, thisstyle, label=thislabel)
    
axV.legend(loc=0)
axI.legend(loc=0)
axV.get_figure().savefig('voltage.png')
axI.get_figure().savefig('current.png')
plt.show()
