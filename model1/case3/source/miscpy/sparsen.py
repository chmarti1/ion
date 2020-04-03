# SparseN
#   A module for providing the SparseN N-dimensional sparse tensor class
#

# To Do items:
#   Create overloaded basic operations (multiply, add, subtract, negate)
# that allow the application to demand in-place or thin operations.  All
# binary math operators are currently thick; they result in the creation
# of a new tensor (except for the in-place operations).

import time
import multiprocessing as mp
import numpy as np




class SparseN:
    """SparseN  an N-dimensional sparse tensor class
    s = SparseN( (N0, N1, ...) )
        OR
    s = SparseN( s )
        OR
    s = SparseN( d )
    
An empty SparseN matrix can be created by defining its size (N0, N1, ...) or
as a copy of an existing SparseN matrix, S, or from a dense array, D.

Once created, indices can be summoned or set as normal
    S[ii, jj, ...] = value
    value = S[ii, jj, ...]

Meta data on the tensor shape are available in numpy-compatible member data
    A.ndim      # Number of dimensions
    A.shape     # tensor shape tuple (len(shape) == ndim)

SparseN tensors support basic mathematical operaitons
Unary operations with sparse tensors:
    -S1
    S1.transpose(..)
    
Binary operations with two sparse tensors:
    S1 + S2
    S1 += S2
    S1 - S2
    S1 -= S2
    S1 * S2         # Inner dot product
    S1.dot(.. S2)   # Multiplicaiton along one or more simultaneous dimensions

Binary operations with dense tensors:
    S+D, D+S    # Returns a dense array
    S += D      # Modifies existing sparse in place
    S-D, D-S    # Returns a dense array
    S -= D
    S*D, D*S    # Inner dot product
    
Binary operations with scalars:
    S+a, a+S
    S += a
    S-a, a-S
    S -= a
    S*a, a*S
"""

    def __init__(self, S):
        if issubclass(type(S), SparseN):
            SparseN.__init__(self, S.shape)
            self.index = S.index.copy()
            self.value = S.value.copy()
        elif isinstance(S, np.ndarray):
            SparseN.__init__(self, S.shape)
            for index,value in zip(np.ndindex(S.shape),np.nditer(S)):
                if value != 0:
                    self.index.append(index)
                    self.value.append(np.asscalar(value))
        else:
            self.shape = tuple(S)
            self.size = np.product(self.shape)
            self.ndim = len(self.shape)
            for dd in self.shape:
                if dd<=0:
                    raise Exception('Tensor dimensions must be positive.')
            self.index = []
            self.value = []
    
    def __setitem__(self, index, value):
        self._inrange(index)
        found, ii = self._find_index(index)
        if not found:
            self.index.insert(ii,index)
            self.value.insert(ii,value)
        else:
            self.value[ii] = value
    
    def __delitem__(self, index):
        self._inrange(index)
        found, ii = self._find_index(index)
        if found:
            del self.index[ii]
            del self.value[ii]
    
    def __getitem__(self, index):
        self._inrange(index)
        found, ii = self._find_index(index)
        if not found:
            return 0.
        return self.value[ii]
        
    def __bool__(self):
        return bool(self.value)
        
    def __len__(self):
        return self.size
        
    def __add__(self, b):
        # If b is dense, use dense arithmatic
        if isinstance(b, np.ndarray):
            c = self.todense()
            np.add(c,b,out=c)
            return c
        c = self.copy()
        c.__iadd__(b)
        return c
        
    def __radd__(self,b):
        return self.__add__(self,b)

    def __iadd__(self, b):
        # Sparse
        if issubclass(type(b), SparseN):
            if b.shape != self.shape:
                raise Exception('Addition and subtraction of tensors requires identical shapes.')
            for bi, bvalue in zip(b.index, b.value):
                self.increment(bi,bvalue)
        # Dense
        elif isinstance(b, np.ndarray):
            if b.shape != self.shape:
                raise Exception('Addition and subtraction of tensors requires identical shapes.')
            for bi in np.nditer(b):
                self.increment(bi,b[bi])
        # Scalar
        else:
            for ii in range(len(self.value)):
                self.value[ii] += b
        
    def __repr__(self):
        out = '<'
        for ii in self.shape[:-1]:
            out += str(ii) + 'x'
        out += str(self.shape[-1]) + ' SparseN tensor with ' + str(self.nnz()) + ' stored elements>'
        return out
        
    def __neg__(self):
        b = SparseN(self.shape)
        b.index = self.index.copy()
        b.value = [-vv for vv in self.value]
        # Note to my future self...
        # If you change neg to work with a ThinSparseN, you need to change
        # __rsub__, which relies on __neg__ to generate a copy for in-place
        # subtraction.
        return b
        
    def __sub__(self, b):
        if isinstance(b, np.ndarray):
            c = self.todense()
            np.subtract(c,b,out=c)
            return c
        c = self.copy()
        c.__isub__(b)
        return c
        
    def __rsub__(self, b):
        if isinstance(b, np.ndarray):
            c = self.todense()
            np.subtract(b,c,out=c)
            return c
        c = self.__neg__()
        c.__iadd__(b)
        return c
        
    def __isub__(self, b):
        # Sparse
        if issubclass(type(b), SparseN):
            if b.shape != self.shape:
                raise Exception('Addition and subtraction of tensors requires identical shapes.')
            for bi, bvalue in zip(b.index, b.value):
                self.increment(bi,-bvalue)
        # Dense
        elif isinstance(b, np.ndarray):
            if b.shape != self.shape:
                raise Exception('Addition and subtraction of tensors requires identical shapes.')
            for bi in np.nditer(b):
                self.increment(bi,-b[bi])
        # Scalar
        else:
            for ii in range(len(self.value)):
                self.value[ii] -= b
        
    def __mul__(self, b):
        # Vector/matrix/tensor products
        if issubclass(type(b), SparseN) or isinstance(b, np.ndarray):
            return self.dot(self.ndim-1, 0, b)
        else:
            c = SparseN(self.shape)
            c.index = self.index.copy()
            c.value = [b*vv for vv in self.value]
            return c
        
    def __rmul__(self, b):
        if issubclass(type(b), SparseN) or isinstance(b, np.ndarray):
            return self.dot(0, b.ndim-1, b)
        else:
            c = SparseN(self.shape)
            c.index = self.index.copy()
            c.value = [b*vv for vv in self.value]
            return c
        
    def _inrange(self, index):
        """Tests the index tuple for the correct dimension and range"""
        if len(index) != self.ndim:
            raise Exception('SparseN tensor has %d dimensions, and requires the same number of indices.'%self.ndim)
        for ii, ss in zip(index,self.shape):
            if ii < 0 or ii >= ss:
                raise Exception('Index is out of range: %d'%index)
    
    def _find_index(self, index, iimin=None, iimax=None):
        """Perform a bisection search on the index array
    found, ii = s._find_index( index )
    
index is a tuple of N indices
ii is the integer index in the s.index array where the specified index was 
    found OR where it would be inserted were it to be added.
found is a boolean indicating whether the specified index was located.

To specify a smaller subset of the index list to search, the optional iimin
and iimax parameters may be set.

For speed, very little error checking is done.  _find_index is intended to be
a back-end method, so be careful when using iimin or iimax!  Don't specify 
iimin larger than iimax, and make sure you ACTUALLY include a portion of the
list where the target resides.
"""
        if iimin is None:
            aa = 0
        else:
            aa = iimin

        if iimax is not None:
            bb = iimax
        else:
            bb = len(self.index)-1
            
        # Check to see if the index is even in the range
        if bb < aa:
            return (False, aa)
        elif index <= self.index[aa]:
            return (index == self.index[aa], aa)
        elif index == self.index[bb]:
            return (True, bb)
        elif index > self.index[bb]:
            return (False, bb+1)
            
        # the value definitely lies inside the list, and it is neither aa
        # nor bb.
        while bb-aa>1:
            ii = (aa+bb)//2
            # Eventually, we'll hit the value
            if index == self.index[ii]:
                return (True, ii) 
            elif index < self.index[ii]:
                bb = ii
            else:
                aa = ii
        # Unless the value isn't in the list.
        return (False, bb)

    def nnz(self):
        """Number of non-zero elements"""
        return len(self.value)
        
    def copy(self):
        """another_s = s.copy()
    Makes a new object with copies of the data in the original object.
"""
        return SparseN(self)
        
    def increment(self, index, value):
        """s.increment(index, value)
    
Increments an element of the matrix.  This is equivalent to
    s[index] += value
but it only searches for the index once instead of twice through a call
to __getitem__ and to __setitem__
"""
        self._inrange(index)
        if value==0:
            return
        found,ii = self._find_index(index)
        if found:
            self.value[ii] += value
            if self.value[ii] == 0:
                del self.index[ii]
                del self.value[ii]
        else:
            self.index.insert(ii, index)
            self.value.insert(ii, value)
            
    def todense(self):
        """Return a dense copy of the tensor
    D = S.todense()
    
Be careful; large multi-dimensional tensors can require large amounts
of memory in dense realizations."""
        d = np.zeros(self.shape)
        for index,value in zip(self.index, self.value):
            d[index] = value
        return d
        
    def dot(self, adim, bdim, b, asdense=False):
        """Multiply two sparse tensors along the specified dimensions
    C = A.dot(adim, bdim, B)
    
When A is an NA dimensional sparse tensor, and B is an NB dimensional sparse 
tensor or dense array, and there are NN dimensions specified in adims and bdims,
C will be an (NA + NB - 2) dimensional tensor.

For example, if A and B are 3-dimensional, then 
    C = A.dot(2, 0, B)
is equivalent to
    C[i,j,l,m] = sum_k A[i,j,k] * B[k,l,m]
    
The dims may be specified as integers or, to specify simultaneous 
multiplication across multiple indices, as lists or tuples of integers.
So, for the same tensors in the last example,
    C = A.multiply(adims=(1,2), bdims=(0,1), B)
is equivalent to
    C[i,l] = sum_j sum_k A[i,j,k] * B[j,k,l]

The order of the dimensions is also important.
    C = A.multiply(adims=(1,2), bdims=(1,0), B)
is equivalent to
    C[i,l] = sum_j sum_k A[i,j,k] * B[k,j,l]
    
To force C to be a dense array, use the optional ASDENSE keywrod

    C = A.dot(adim, bdim, B, asdense=True)
"""
        if hasattr(adim,'__iter__') and hasattr(bdim,'__iter__'):
            adim = tuple(adim)
            bdim = tuple(bdim)
            if len(adim) != len(bdim):
                raise Exception('adim and bdim must specify the same number of dimensions.')
        else:
            adim = int(adim)
            bdim = int(bdim)
            
        # There are four different execution cases:
        #   If the input is sparse
        #       --> and there are multiple specified dimensions
        #       --> and there is a single dimension
        #   If the input is dense
        #       --> and there are multiple specified dimensions
        #       --> and there is a single dimension

        # If B is sparse ...            
        if issubclass(type(b), SparseN):
            # Case out whether adim and bdim are scalars or array-like
            # Generate a set of constants and helper functions that will handle 
            # the multiplication
            # _match(aindex, bindex)  Determine whether two indices should be multiplied
            # _cindex(aindex, bindex) Generate a result index from the two product indices
            # cshape                  The shape of the result tensor

            if isinstance(adim, tuple):
                # Do some error checking on the dimensions
                for ai in adim:
                    if ai < 0 or ai >= self.ndim:
                        raise Exception('adim index must be non-negative and within the dimension of A')
                for bi in bdim:
                    if bi < 0 or bi >= b.ndim:
                        raise Exception('bdim index must be non-negative and within the dimension of B')
                    
                cdima = []  # list of dimensions from a and b that will be used
                cdimb = []  # to build the cindex.
                cshape = []
                for ai in range(self.ndim):
                    if ai not in adim:
                        cdima.append(ai)
                        cshape.append(self.shape[ai])
                for bi in range(b.ndim):
                    if bi not in bdim:
                        cdimb.append(bi)
                        cshape.append(b.shape[bi])
                        
                def _cindex(aindex, bindex):
                    cindex = ()
                    for ai in cdima:
                        cindex += (aindex[ai],)
                    for bi in cdimb:
                        cindex += (bindex[bi],)
                    return cindex
                    
                def _match(aindex, bindex):
                    for ai,bi in zip(adim,bdim):
                        if aindex[ai] != bindex[bi]:
                            return False
                    return True
            else:
                # Do some error checking on the dimensions
                if adim < 0 or adim >= self.ndim:
                    raise Exception('adim index must be non-negative and within the dimension of A')
                if bdim < 0 or bdim >= b.ndim:
                    raise Exception('bdim index must be non-negative and within the dimension of B')
                    
                def _match(aindex,bindex):
                    return aindex[adim] == bindex[bdim]
                def _cindex(aindex,bindex):
                    return aindex[:adim] + aindex[adim+1:] + bindex[:bdim] + bindex[bdim+1:]
                cshape = self.shape[:adim] + self.shape[adim+1:] + b.shape[:bdim] + b.shape[bdim+1:]
            
            # Initialize the result
            if asdense:
                c = np.zeros(cshape)
            else:
                c = SparseN(cshape)
            # perform the multiplication
            for aindex, avalue in zip(self.index, self.value):
                for bindex, bvalue in zip(b.index, b.value):
                    # Test for index agreement
                    if _match(aindex, bindex):
                        if asdense:
                            c[cindex(aindex,bindex)] += avalue*bvalue
                        else:
                            c.increment(_cindex(aindex, bindex), avalue*bvalue)
            
        # If B is dense...
        else:
            # Force the input to be a numpy array
            b = np.asarray(b)

            # When B is dense, we will actually loop over the entire array
            # _cindex()  Generate the cindex from aindex and bindex
            # _nextb() Generates the next bindex from the one prior
            if isinstance(adim,tuple):
                # Do some error checking on the dimensions
                for ai in adim:
                    if ai < 0 or ai >= self.ndim:
                        raise Exception('adim index must be non-negative and within the dimension of A')
                for bi in bdim:
                    if bi < 0 or bi >= b.ndim:
                        raise Exception('bdim index must be non-negative and within the dimension of B')
                        
                cshape = [] # Solution tensor shape
                cdima = []  # dimensions of a that contribute to cindex
                cdimb = []  # dimensions of b that contribute to bindex
                for ai in range(self.ndim):
                    if ai not in adim:
                        cshape.append(self.shape[ai])
                        cdima.append(ai)
                for bi in range(b.ndim):
                    if bi not in bdim:
                        cshape.append(b.shape[bi])
                        cdimb.append(bi)
                
                def _initb(aindex):
                    bindex = [0]*b.ndim
                    for ai,bi in zip(adim,bdim):
                        bindex[bi] = aindex[ai]
                    return bindex
                
                def _nextb(bindex):
                    for ii,bi in enumerate(cdimb):
                        bindex[bi] += 1
                        if bindex[bi] < b.shape[bi]:
                            return bindex
                        bindex[bi] = 0
                    return None
                
                def _cindex(aindex,bindex):
                    cindex = ()
                    for ai in cdima:
                        cindex += (aindex[ai],)
                    for bi in cdimb:
                        cindex += (bindex[bi],)
                    return cindex
            else:
                # Do some error checking
                if adim < 0 or adim >= self.ndim:
                    raise Exception('adim index must be non-negative and within the dimension of A')
                if bdim < 0 or bdim >= b.ndim:
                    raise Exception('bdim index must be non-negative and within the dimension of B')
                    
                cshape = []
                cdimb = []
                for ai in range(self.ndim):
                    if ai != adim:
                        cshape.append(self.shape[ai])
                for bi in range(b.ndim):
                    if bi != bdim:
                        cshape.append(b.shape[bi])
                        cdimb.append(bi)
                
                def _initb(aindex):
                    bindex = [0]*b.ndim
                    bindex[bdim] = aindex[adim]
                    return bindex
                
                def _nextb(bindex):
                    for ii,bi in enumerate(cdimb):
                        bindex[bi] += 1
                        if bindex[bi] < b.shape[bi]:
                            return bindex
                        bindex[bi] = 0
                    return None
                
                def _cindex(aindex,bindex):
                    return aindex[:adim] + aindex[adim+1:] + tuple(bindex[:bdim] + bindex[bdim+1:])
            
            if asdense:
                c = np.zeros(cshape)
            else:
                c = SparseN(cshape)
            
            # Iterate over all nonzero values of self
            for aindex, avalue in zip(self.index, self.value):
                # Iterate over all corresponding indices of B
                bindex = _initb(aindex)
                while bindex is not None:
                    # only operate on the value if the B value is non-zero
                    bvalue = b[tuple(bindex)]
                    if bvalue!=0:
                        if asdense:
                            c[_cindex(aindex,bindex)] += avalue*bvalue
                        else:
                            c.increment(_cindex(aindex,bindex), avalue * bvalue)
                    bindex = _nextb(bindex)

        # All done
        return c


    def transpose(self, adim, bdim):
        """Transpose two dimensions in place.
    S.transpose(a,b)
    
a and b are dimensions to transpose so that
    S = SparseN((3,3,3))
    ... code assigning values to S ...
    S2 = SparseN(S)     # Copy S
    S2.transpose(1,2)   # Switch the second and third dimensions
    S[i,j,k] == S2[i,k,j]   # True for all i,j,k
"""
     
        def imap(index):
            return index[:imap.adim] + (index[imap.bdim],) + \
                index[imap.adim+1:imap.bdim] + (index[imap.adim],) + \
                index[imap.bdim+1:]
                
        imap.adim = min(adim,bdim)
        imap.bdim = max(bdim,adim)
        
        # Check legality
        if imap.adim < 0 or imap.bdim >= self.ndim:
            raise Exception('adim and/or bdim are/is out of range.')
        elif adim == bdim:
            return self
   
        return ThinSparseN(self, shape=imap(self.shape), imap=imap)
            

class VMap:
    """This is a wrapper class for the SparseN index and value lists.  
It allows index and values to be re-mapped on the fly without requiring 
data to be copied.  This is useful for resizing, reshaping, or 
transposing sparse matricies efficiently.

    VM = VMap(imap, imapi, target)
    
    
VMAP
    This is a callable index map function.  It maps indicies passed to a
    ThinSparseN object into the original indicies.  
    It must be of the form: 
        target_index_tuple = imap(index_tuple)

VMAPI
    This is a callable index map inverse function.  It maps indicies 
    passed to the original SparseN object into the new indices passed to
    the ThinSparseN object.  It must be of the form: 
        index_tuple = imapi(target_index_tuple)

TARGET
    This is the source list of tuples.  Each tuple is an N-dimensional 
    sparse matrix index.
"""
    def __init__(self, vmap, vmapi, target):
        self.vmap = vmap
        self.vmapi = vmapi
        self.target = target
        
    def __getitem__(self, index):
        return self.vmapi(self.target.__getitem__(index))
        
    def __setitem__(self, index, value):
        self.target.__setitem__(index, self.vmap(value))
        
    def __delitem__(self, index):
        self.target.__delitem__(index)
        
    def __iter__(self):
        return map(self.vmapi, self.target)
        
    def insert(self, index, value):
        self.target.insert(index, self.vmap(value))
        
    def copy(self):
        return [ii for ii in self]
    

class ThinSparseN(SparseN):
    """A ThinSparseN contains no data, but forms a wrapper around a SparseN.
The intent is that a ThinSparseN will map indices to a parent SparseN
tensor with identical data, but in different arrangements.  This allows
a SparseN to be efficiently resized, transposed, or reshaped.  Write
operations to the child will affect the parent and vice versa.

    TS = ThinSparseN(parent, shape, imap, imapi, vmap, vmapi)

The parent SparseN is required, but the three optional keyword arguments
define the mapping.

SHAPE is a tuple defining the shape of the new tensor.  If it is not 
explicitly specified, it will be inherited from the parent SparseN.  If there is
and imap/imapi defined, then shape = imapi(S.shape) will be used.

IMAP, IMAPI are funcitons defining an index maping and inverse mapping.
    TS[ index ] == S[ imap(index) ]
    TS[ imapi(index) ] == S[ index ]
If IMAP is set, but IMAPI is not, then IMAP will be used for both.  This is 
useful in transpose operations, but it will not usually lead to a funcitonal
object.  User beware!

Just like IMAP and IMAPI are funcitons mapping indices for the thin sparse, the
VMAP and VMAPI funcitons are used to map values.
    TS[index] == vmap( S[index] )
    vmapi( TS[index] ) == S[index]
If VMAP is set and VMAPI is not, then VMAP will be used for both.  This is useful
for negation or inverse operations, but it will not usually result in a 
funcitonal object.  User beware!
"""
    def __init__(self, S, shape=None, imap=None, imapi=None, vmap=None, vmapi=None):
        if isinstance(S, ThinSparseN):
            raise exception('Layered ThinSparseN are not currently allowed. ThinSparseN must be built from SparseN tensors.')
        elif not isinstance(S, SparseN):
            raise Exception('The ThinSparseN must be initialized from a SparseN')
        
        # Who is the parent?
        self.parent = S
        # If the index map is defined, then set up the index re-mapping
        if imap and imapi is None:
             imapi = imap
        elif imap is None and imapi:
            raise Exception('If IMAPI is defined, then IMAP must be defined.')

        if vmap and vmapi is None:
            vmapi = vmap
        elif vmap is None and vmapi:
            raise Exception('If VMAPI is defined, then VMAP must be defined.')

        # Remember the index maps
        self.imap = imap
        self.imapi = imapi
        self.vmap = vmap
        self.vmapi = vmapi
        
        # If shape is explicitly defined, use that.  Otherwise, inherit shape from the parent.
        # Calling the SparseN initializer will define ndim, size, and
        # other useful constants.
        if shape:
            SparseN.__init__(self, shape)
        elif imapi is None:
            SparseN.__init__(self, S.shape)
        else:
            SparseN.__init__(self, imapi(S.shape))
        
        # This MUST come last because it overwrites value and index
        if imap:
            self.index = VMap(imap, imapi, S.index)
            self._find_index = self._find_index_wrapper
        else:
            self.index = S.index
            
        if vmap:
            # Note that the mapping is reversed from the indices
            self.value = VMap(vmapi, vmap, S.value)
        else:
            self.value = S.value

    def _find_index_wrapper(self, index, iimin=None, iimax=None):
        return self.parent._find_index(self.imap(index), iimin=iimin, iimax=iimax)
    

    
