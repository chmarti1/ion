#!/usr/bin/python3

import os,sys

workon = ['5559', '0553', '1532', '2516', '3446', '4433', '0306', '1302', '2716', '3738', '4754', '5742']


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
            if not os.path.isdir(os.path.join(target, 'post2')):
                lf.write('post2\n')
                os.system('./post2.py ' + this)
            if not os.path.isdir(os.path.join(target, 'post3')):
                lf.write('post3\n')
                os.system('./post3.py ' + this)
        except:
            lf.write(repr(sys.exc_info()) + '\n')

