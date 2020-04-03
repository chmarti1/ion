#!/usr/bin/python3

import ion1d
import os
import numpy as np
import multiprocessing as mp

datadir = '../data'
baseline = '../baseline'

phimin = -50.
phimax = 40.
phistep = 2.

datadir = os.path.abspath(datadir)
baseline = os.path.abspath(baseline)

if not os.path.isdir(datadir):
    os.mkdir(datadir)
print('Using data directory: ' + datadir)

def worker(worker_ipm):
    firstrun = True
    
    for ii,param in worker_ipm.items():
        # Construct a unique file name
        saveas = os.path.join(datadir, '%03d'%(ii))
        print(saveas)
        # If this is the first model run pull from the baseline
        if firstrun:
            firstrun = False
            eta = np.load(os.path.join(baseline,'eta.npy'))
            nu = np.load(os.path.join(baseline,'nu.npy'))
            phi = np.load(os.path.join(baseline,'phi.npy'))
            z = np.load(os.path.join(baseline, 'z.npy'))
                
        # Otherwise, use the last model run to initialize the next.
        else:
            eta = M.eta
            nu = M.nu
            phi = M.phi
            # Do not alter z
        
        M = ion1d.AnchoredFiniteIon1D()
        M.init_param(param)
        M.init_grid(z)
        M.init_mat()
        M.init_solution(eta=eta, nu=nu, phi=phi)
        
        # Solve!
        converge = False
        for count in range(50):
            #M.show_solution()
            if M.test_solution():
                converge = True
                break
            M.step_solution()

        if not converge:
            print('*** CONVERGENCE FAILURE: ' + saveas)
        M.init_post()
        M.save_post(saveas)



if __name__ == '__main__':
    print('Starting the calculations')
    
    # Steal parameters from baseline
    blp = ion1d.load_post(baseline, loadnpy=False)
    # Modify phia to be an array of applied voltages
    p = blp['param'].asdict().copy()
    p['phia'] = np.arange(phimin, phimax, phistep)
    # Generate a parameter manager for these cases
    ipm = ion1d.IonParamManager(p)
    
    # Set up the parallel processing
    NPROC = 8
    pool = mp.Pool(processes = NPROC)
    # For debugging
    #worker(ipm)
    #exit(0)
    # Spawn new processes for parallel processing
    for this_ipm in ipm.split(NPROC):
        pool.apply_async(worker, args=(this_ipm,))
    
    pool.close()
    pool.join()
else:
    print('__name__ was not __main__')
