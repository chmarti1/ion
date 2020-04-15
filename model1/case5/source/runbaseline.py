#!/usr/bin/python3

import ion1d
import os
import numpy as np
import multiprocessing as mp

baseline = '../baseline'

baseline = os.path.abspath(baseline)

M = ion1d.AnchoredFiniteIon1D()
M.init_param(z1=.4, beta=20., R=1000., alpha=1e-3, phia=0., mu=200., tau=1.)
M.init_grid(d=.001, r=(.02, 1, .02))
M.init_mat()
M.init_solution()

for count in range(50):
    M.show_solution()
    if M.test_solution():
        M.init_post().save(baseline, overwrite=True)
        exit(0)
    M.step_solution()

raise Exception('Failed to converge after {} solution steps'.format(count))
