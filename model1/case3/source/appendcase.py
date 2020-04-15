#!/usr/bin/python3

import ion1d
import os
import numpy as np
import multiprocessing as mp

datadir = '../data'
baseline = '../baseline'

phimin = -9
phimax = 13.
phistep = 2.

datadir = os.path.abspath(datadir)
baseline = os.path.abspath(baseline)

# Determine the largest prior index
datafiles = os.listdir(datadir)
datafiles.sort()
startindex = int(datafiles[-1].split('.')[0])+1
print('Starting at index: %d'%startindex)
    

def worker(worker_ipm):
    firstrun = True
    
    for ii,param in worker_ipm.items():
        # Construct a unique file name
        saveas = os.path.join(datadir, '%03d'%(ii+startindex))
        print(saveas)
        # If this is the first model run pull from the baseline
        if firstrun:
            firstrun = False
            P = ion1d.PostIon1D(baseline)
            eta = P.eta
            nu = P.nu
            phi = P.phi
            z = P.z
                
        # Otherwise, use the last model run to initialize the next.
        else:
            eta = M.eta
            nu = M.nu
            phi = M.phi
            # Do not alter z
        
        M = ion1d.FiniteIon1D()
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
        M.init_post().save(saveas)



if __name__ == '__main__':
    print('Starting the calculations')
    
    # Steal parameters from baseline
    P = ion1d.PostIon1D(baseline)
    # Modify phia to be an array of applied voltages
    p = P.param.asdict()
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
