#!/usr/bin/python

import os, sys, time

# Quick summary of important variables
#   now         The broken down time for the start of execution
#   datadir     The full path to the directory where data will be contained
#   


# note the time of the start of execution
now = time.localtime()

# create a directory for the results
datadir = os.path.abspath(time.strftime('%Y%m%d%H%M%S', now))
os.mkdir(datadir)

# create a summary file noting the data collection
print("**User input to build a summary file**")
print("  Start of test: %s"%time.asctime(now))


# Create the readme file
readme = os.path.join(datadir, "README.txt")
print("  Readme file: %s"%readme)

with open(readme, 'w') as ff:
    ff.write("""README
    
Test began: """ + time.asctime(now))
