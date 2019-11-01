import threading
import time

class shared:
    _lock = False
    _waitfor = .001
    value = 0.
    
    def __init__(self):
        self._lock=False
        self._waitfor = .001
        self.value = 0.
        
    def acquire_lock(self):
        if self._waitfor < 0 or self._waitfor > 1:
            self._waitfor = .001
        while self._lock:
            time.sleep(self._waitfor)
        self._lock=True
        
        
    def release_lock(self):
        self._lock = False

    def update(self, value):
        self.acquire_lock()
        local = self.value
        time.sleep(0.1)
        self.value = local + value
        self.release_lock()

def tfun(a, sh):
    sh.update(a * a)
    

if __name__=="__main__":
    pool = []
    sh = shared()
    for aa in range(5):
        th = threading.Thread(target=tfun, args=(aa, sh))
        th.start()
        pool.append(th)
    for th in pool:
        th.join()
    
