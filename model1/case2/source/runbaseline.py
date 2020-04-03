#!/usr/bin/python3

import ion1d
import os
import numpy as np
import multiprocessing as mp

baseline = '../baseline'

baseline = os.path.abspath(baseline)

M = ion1d.FiniteIon1D()
M.init_param(z1=.01, z2=.21, beta=20., R=2500., alpha=1e-3, phia=0., mu=200., tau=1.)
M.init_grid(d=(.00002,.001,.001), r=(1, .1, .5, .02))
M.init_mat()
M.init_solution()

for count in range(50):
    M.show_solution()
    if M.test_solution():
        M.init_post()
        M.save_post(baseline)
        exit(0)
    M.step_solution()

raise Exception('Failed to converge after {} solution steps'.format(count))
