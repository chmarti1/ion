#!/usr/bin/python3

import os,sys

workon = ['3412', '4140', '4929', '5357', '5713', '0405', '0814']


datadir = '../data'
logfile = './postbatch.log'

def getdir(tag):
    found = None
    for this in os.listdir(datadir):
        if this.endswith(tag):
            if found:
                raise Exception('Found multiple directories ending with: ' + tag)
            found = os.path.abspath(os.path.join(datadir,this))
    if found:
        return found
    raise Exception('Tag not found.')

with open(logfile,'w') as lf:
    for this in workon:
        try:
            target = getdir(this)
            lf.write(this + '\n')
            if not os.path.isdir(os.path.join(target, 'post1')):
                lf.write('post1\n')
                os.system('./post1.py ' + this)
                
            p6dir = os.path.join(target, 'post6')
            if os.path.isdir(p6dir):
                os.system('rm -rf ' + p6dir)
            lf.write('post6\n')
            os.system('./post6.py ' + this)
        except:
            lf.write(repr(sys.exc_info()) + '\n')

