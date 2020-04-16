#!/usr/bin/python3

import ion1d
import os
import numpy as np
import multiprocessing as mp

baseline = '../baseline'

baseline = os.path.abspath(baseline)

if os.path.isdir(baseline):
    print('Found existing baseline directory: ' + baseline)
    print('Removing.')
    os.system('rm -rf ' + baseline)

M = ion1d.FiniteIon1D()
M.init_param(z1=.01, z2=.21, beta=20., R=1000., alpha=1e-4, phia=0., mu=200., tau=1.)
M.init_grid(d=(.0001,.001,.001), r=(.2, .5, 1, .02))
M.init_mat()
M.init_solution()

for count in range(50):
    M.show_solution()
    if M.test_solution():
        M.init_post().save(baseline)
        exit(0)
    M.step_solution()

raise Exception('Failed to converge after {} solution steps'.format(count))
