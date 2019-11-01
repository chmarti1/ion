"""POOL

A miniature module for a quick-and-dirty thread pool manager.  Python 2 doesn't 
appear to have support for thread pool management (only process management).  
This is my re-inventing of the wheel both to tinker intellectually with the 
thread management and also to keep from having to transition to Python 3.  I 
know I need to, but that doesn't mean I can't put it off.  Don't judge me.

This is designed to run in a POSIX environment.
"""


import threading as thrd
import time
import os

def nproc():
    try:
        return os.sysconf('SC_NPROCESSORS_ONLN')
    except:
        raise Exception('This does not appear to be a POSIX system')


class Pool:
    """The Pool class manages the scheduled jobs to complete and the pool of working threads.

import pool
p = pool.Pool()
... add jobs ...
p.add(my_funciton, (my, arguments))
... 
p.start()
... keep adding jobs ...
p.add(other_function, (other, arguments))
...
p.stop()
"""
    _workers = []
    _worker_active = []
    _max_workers = 0
    _sched = []
    _go = False
    _sleep_for = .001
    
    def __init__(self, max_workers=None, sleep_for=None):
        # If the user did not specify the number of workers, automatically 
        # detect the number of cores
        if max_workers is None:
            self._max_workers = nproc()
        elif max_workers > 0:
            self._max_workers = int(max_workers)
        else:
            raise Exception('max_workers must be a positive integer.')
        
        if sleep_for is None:
            self._sleep_for = .001
        elif sleep_for > 0 and sleep_for < 1:
            self._sleep_for = sleep_for
        else:
            raise Exception('sleep_for must be positive and less than 1 second')
            
        self._sched = []
        self._workers = []
        self._worker_active = []
        self._go = False
        
    def _worker(self, wid):
        """The worker member funciton
    _worker(wid)

The pool of _WORKERS is a list of threads each executing the _WORKER() method.  
If the _SCHED list still contains funcitons and arguments to execute, then each
worker will pop them from the list and execute them until the _SCHED is 
depleted.  If a worker function sees that no job is scheduled, then it will 
sleep for _SLEEP_FOR seconds to allow the parent process a chance to either
halt the pool or add more jobs to the schedule.
"""
        # Keep running if the _go flag is set or if there are still jobs to do
        while self._go or self._sched:
            if self._sched:
                self._worker_active[wid] = True
                target,args = self._sched.pop(0)
                try:
                    target(*args)
                except:
                    print('Worker %d encountered an exception'%wid)
                    print(os.sys.exc_info()[1])
            else:
                self._worker_active[wid] = False
                time.sleep(self._sleep_for)
            
                
    def add(self, target, args):
        """Adds a job to the pool's schedule.
    pool.add(my_function, (my, arguments, go, here, ... ))
    
Adds a job to the schedule
    my_function(my,arguments,go,here,...)
"""
        self._sched.append((target,args))

    def start(self):
        """Start the pool threads.  The worker threads will continue running even if
the schedule/queue is depleted.  The parent applicaiton may continue to add jobs
until the JOIN() or CLOSE() method is called."""
        self._go = True
        
        if self._workers:
            raise Exception('The pool already appears to be running!')
        elif self._max_workers <= 0:
            raise Exception('The _max_workers member seems to have been tampered with. Naughty Naughty.')
            
        for wid in range(self._max_workers):
            self._worker_active.append(False)
            self._workers.append(thrd.Thread(target=self._worker, args=(wid,)))
            self._workers[-1].start()
        
    def stop(self):
        """Wait for the threads to complete and clean up after."""
        # Clear the _go flag so the workers will exit when the jobs are complete
        self._go = False
        # Wait for all the workers to exit
        for wid,worker in enumerate(self._workers):
            worker.join()
        # Clean up and get ready for 
        self._workers = []
        self._worker_active = []

    def get_active(self):
        """Returns a list of boolean values indicating which of the workers are busy"""
        return list(self._worker_active)
