import numpy as np
import matplotlib.pyplot as plt

mu = 1.08e-3
ee = 1.60e-19
ep = 8.85e-12
U = 75.
D = .000254


def _cs1(I, n, U=U, D=D):
    """Clements and Smy model 1
    V = _cs1(I, n, U, D)
    
Thick sheath 1969 paper

I   Current per unit length of the wire
n   ion density in the far field
U   bulk velocity
D   wire diameter
"""
    I = np.asarray(I)
    n = np.asarray(n)
    U = np.asarray(U)
    D = np.asarray(D)
    return I ** 1.5 * np.log(I/(U*n*ee*D)) / np.sqrt(2*np.pi*mu*ep) / (2*n*ee*U)
    
    
def cs1(V, n, U=U, D=D):
    """Clements and Smy model 1
    I = cs1(V, n, U, D)
    
Thick sheath 1969 paper

I   Current per unit length of the wire
n   ion density in the far field
U   bulk velocity
D   wire diameter
"""
    if hasattr(V, '__iter__') or hasattr(n, '__iter__') or \
            hasattr(U, '__iter__') or hasattr(D, '__iter__'):
        return np.asarray([cs1(vv,nn,uu,dd) for vv,nn,uu,dd in np.broadcast(V,n,U,D)])
        
    I = U*n*ee*D
    Vtest = _cs1(I, n, U, D)
    count = 0
    while abs(Vtest - V) > 1e-3 and count<100:
        #print(I, Vtest)
        dI = I * .01
        dV = _cs1(I+dI, n, U, D) - Vtest
        I -= (Vtest-V) * dI/dV
        Vtest = _cs1(I, n, U, D)
        count += 1
    return I

def cs1_n(V, I, U=U, D=D):
    """Clements and Smy model 1
    n = cs1_n(V, I, U, D)
    
Thick sheath 1969 paper

n   Ion density in the far field
I   Current per unit length of the wire
V   probe bias voltage
U   bulk velocity
D   wire diameter
"""
    if hasattr(V, '__iter__') or hasattr(I, '__iter__') or \
            hasattr(U, '__iter__') or hasattr(D, '__iter__'):
        return np.asarray([cs1_n(vv,ii,uu,dd) for vv,ii,uu,dd in np.broadcast(V,I,U,D)])
    
    count = 0
    n = I / (ee * U * D)
    Vtest = _cs1(I, n, U, D)
    while abs(Vtest - V) > 1e-3 and count<100:
        #print(I, Vtest)
        dn = n * .01
        dV = _cs1(I, n+dn, U, D) - Vtest
        n -= (Vtest-V) * dn/dV
        Vtest = _cs1(I, n, U, D)
        count += 1
    return n

def cs2(V, n, U=U, D=D):
    """Clements and Smy model 2
    I = cs2(V, n, U, D)
    
Thin sheath 1970 paper

I   Probe current per unit length
V   Probe bias voltage
n   ion density in the far field
U   bulk velocity
D   wire diameter
"""
    V = np.asarray(V)
    n = np.asarray(n)
    U = np.asarray(U)
    D = np.asarray(D)
    return 5.3 * (ep*mu*D/2)**.25 * (ee*U*n)**.75 * np.sqrt(V)
    
def cs2_n(V, I, U=U, D=D):
    """Clements and Smy model 2
    n = cs2_n(V, I, U, D)
    
Thin sheath 1970 paper

n   ion density in the far field
V   Probe bias voltage
I   Probe current per unit length
U   bulk velocity
D   wire diameter
"""
    V = np.asarray(V)
    I = np.asarray(I)
    U = np.asarray(U)
    D = np.asarray(D)
    return (I / 5.3) ** (4./3) / (ep * mu * 0.5 * D)**(1./3) / (ee * U) / V**(2./3)
