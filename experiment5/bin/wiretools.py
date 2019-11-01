#
#   Wire deconvolution tools
#

import numpy as np
from scipy import sparse
import scipy.sparse.linalg as linalg
import os, sys
import time


def _csr_empty_row(A):
    """While preserving all data in a matrix, shift all empty rows to the bottom
    
The matrix must be a scipy sparse CSR (compact sparse row) object.
Alternately, if this algorithm is used on a CSC matrix, it acts like
_CSR_EMPTY_COL(A).
    
    [[ 1 2 0 3 ]
     [ 2 0 0 0 ]
     [ 0 0 0 0 ]
     [ 3 0 0 1 ]]
     
Is transformed to

    [[ 1 2 0 3 ]
     [ 2 0 0 0 ]
     [ 3 0 0 1 ]
     [ 0 0 0 0 ]]
"""
    last_unique = 0
    for index in range(1,len(A.indptr)):
        if A.indptr[index] != A.indptr[last_unique]:
            last_unique += 1
            if last_unique < index:
                A.indptr[last_unique] = A.indptr[index]
    for index in range(last_unique+1,len(A.indptr)):
        A.indptr[index] = A.indptr[last_unique]

def _csr_empty_col(A):
    """While preserving all data in a matrix, shift all empty columns to the right
    
The algorithm identifes empty columns by looking for indices that are
not represented in the INDEX member of A.  

The matrix must be a scipy sparse CSR (compact sparse row) object.
Alternately, if this algorithm is used on a CSC matrix, it acts like
_CSR_EMPTY_ROW(A).
    
    [[ 1 2 0 3 ]
     [ 2 0 0 0 ]
     [ 0 0 0 0 ]
     [ 3 0 0 1 ]]
     
Is transformed to

    [[ 1 2 3 0 ]
     [ 2 0 0 0 ]
     [ 0 0 0 0 ]
     [ 3 0 1 0 ]]
"""
    # Loop through all columns.
    col_to_move = 0
    cols_to_test = A.shape[1]
    while col_to_move < cols_to_test:
        if col_to_move in A.indices:
            col_to_move += 1
        else:
            cols_to_test -= 1
            # Moving a column requires that every index in the indices list
            # Greater than this column be reduced by one.
            for ii in range(len(A.indices)):
                if A.indices[ii] > col_to_move:
                    A.indices[ii] -= 1

def _csc_empty_row(A):
    """While preserving all data in a matrix, shift all empty rows to the bottom
    
The algorithm identifes empty columns by looking for indices that are
not represented in the INDEX member of A.  

The matrix must be a scipy sparse CSR (compact sparse row) object.
Alternately, if this algorithm is used on a CSC matrix, it acts like
_CSR_EMPTY_ROW(A).
    
    [[ 1 2 0 3 ]
     [ 2 0 0 0 ]
     [ 0 0 0 0 ]
     [ 3 0 0 1 ]]
     
Is transformed to

    [[ 1 2 3 0 ]
     [ 2 0 0 0 ]
     [ 0 0 0 0 ]
     [ 3 0 1 0 ]]
"""
    # Loop through all columns.
    col_to_move = 0
    cols_to_test = A.shape[0]
    while col_to_move < cols_to_test:
        if col_to_move in A.indices:
            col_to_move += 1
        else:
            cols_to_test -= 1
            # Moving a column requires that every index in the indices list
            # Greater than this column be reduced by one.
            for ii in range(len(A.indices)):
                if A.indices[ii] > col_to_move:
                    A.indices[ii] -= 1
                    
_csc_empty_col = _csr_empty_row


#=======================#
# The LineSegment class #
#=======================#

class LineSegment:
    """A 2D parametric formulation of a line based on an x,y coordinate, p0, on 
the line and a length vector dx,dy = dp.  The segment is defined by

    v(s) = p0 + dp*s
    
when p0 = (x,y), dp = (dx,dy), and s is a dimensionless location parameter
between 0  and 1.  The LineSegment is initialized by

    ls0 = LineSegment(p0=(x0,y0), dp=(dx,dy))

"""
    def __init__(self, p0, dp):
        self.p0 = np.asarray(p0)
        self.dp = np.asarray(dp)
        if self.p0.size != 2 or self.dp.size != 2:
            raise Exception('LineSegment: Expected v0 or dv to be two elements wide.')

    def __call__(self, s):
        return self.p0 + s * self.dp
        
    def intersect(self, B, test=True, s=False):
        """Calculate the intersection between self and a second line.
    test = A.intersect(B)
        OR
    test, sA, sB = A.intersect(B, s=True)
        OR
    sA, sB = A.intersect(B, test=False, )

test is a bool indicating whether the segments intersect in space.

Parameters sA and sB are position indicators such that
    A(sA) == B(sB)

The test and s keywords are boolean flags indicating whether to return
the test and sA,sB pair.

If 0<=sA<=1 and 0<=sB<=1, then the segments intersect.  If the two line 
segments are parallel, then sA and sB are returned as None.
"""
        a = np.zeros((2,2))
        a[:,0] = self.dp[:]
        a[:,1] = -B.dp[:]
        
        b = B.p0 - self.p0
        try:
            sA,sB = np.linalg.solve(a,b)
        except:
            sA,sB = None,None
        
        result = []
        if test:
            result.append(0<=sA and sA <=1 and 0<=sB and sB<=1)
        if s:
            result += [sA, sB]
        return tuple(result)
        
    
#================================#
# LineSegment Creation Functions #
#================================#
def LSrtheta(p0, R, theta):
    """Define a line segment from a starting point, a length, and an angle
    LS = LSrtheta(p0, R, theta)
    
The angle, theta, is defined relative to the x-axis in radians.
    dx = R cos(theta)
    dy = R sin(theta)
"""
    return LineSegment(p0, (R*np.cos(theta), R*np.sin(theta)))
    
def LSstop(p0, p1):
    """Define a line segment from starting and stop points.
"""
    p0 = np.asarray(p0)
    p1 = np.asarray(p1)
    return LineSegment(p0, p1 - p0)

#=================#
# Grid definition #
#=================#

class Grid:
    """GRID CLASS
The GRID class is responsible for defining a uniform two-dimensional
grid of nodes and elements for performing the wire current deconvolution
operation.  In a uniform 2D grid, the elements are squares with four
member nodes comprising the vertices of the element.

:: Definitions ::

NODE: A node is a point in space at which the wire current density, J 
    will be approximated explicitly.  The values at all points sur-
    rounding the node will be approximated by interpolation between the 
    surrounding nodes.  See ELEMENT.
    
    Nodes may be indexed by their sequential order from left-to-right 
    then bottom-to-top such or by their column, row coordinates.

ELEMENT: An element is a region of space wherein the values of current 
    density, J, at points in the region can be approximated by interpo-
    lation between the element's member nodes.  In a uniform grid, the
    elements are squares with four member nodes forming the corners of
    the element.  

:: Defining a Grid ::

A grid is defined by its number of nodes in the x- and y-axes and their 
spacing, delta.  The Grid length scale unit system is determined entire-
ly by the choice of units for delta.  If delta is specified in inches, 
then all length scales should be regarded in inches, all areas should be
interpreted as in^2, and all current densities should be interpreted as
Amperes per in^2.  

>>> G = Grid(Nx, Ny, delta)

The properties of the grid and its spacing may be retrieved and modified
by directly referencing the N and delta members.  N is a two-element 
integer numpy array that is equivalent to (Nx,Ny).  The following 
examples generate a grid with 200 horizontal nodes and 150 vertical 
nodes with 0.05 unit length spacing.

>>> G = Grid(200, 150, .05)

:: Node Coordinate System ::

Nodes are indexed either sequentially with a single index, n, or by 
column-and-row pair, (i,j).  The node at the smallest x,y coordinate
(usually regarded as bottom,left) is n=0 or i,j=(0,0).  Sequential ind-
exing proceeds along the x-axis first (row) and resumes at the next row.
A 3x3 grid would have an index table:
i   j   n
---------
0   0   0
1   0   1
2   0   2
0   1   3
1   1   4
2   1   5
... and so on ...

The grid is arranged so that nodes with i=0 are on the y-axis (at x=0) 
and symmetrically about the x-axis, so that j=0 are at negative y-coord-
inates.  A node's x,y coordinates can be calculated from the i,j indices
    x = i*delta
    y = (j - (Ny-1)/2.0)*delta
    
The following member methods are utilities for interacting with the
coordinate system
    size        Calculate the number of nodes N[0] * N[1]
    ij_to_n     Convert from (i,j) to n indexing
    n_to_ij     Convert from n to (i,j) indexing
    node        Returns the x,y coordintes of a node

:: Element Coordinate System ::

Elements are indexed identically to nodes, except that they have one
fewer row and one fewer column.  To make the sequential node indexing
more intuitive, we will ignore the last column and the last column of 
elements.  In this way, each element shares the same indexing scheme
with one of its nodes (the bottom-left node).

The following member methods interact with the grid elements
    esize   Calculate the number of elements (N[0]-1)*(N[1]-1)
    eN      Returns the element dimensions
    element Returns the x,y coordinates of the four element nodes
    
:: Physical Size ::

The dimensions of the grid's domain are delta*(Nx-1), delta*(Ny-1).
This is returned by the dims() funciton.

:: Attriutes ::

A grid object has the following public attributes that are intended to
be read-only.  They are constructed through the methods discussed here.

N   
The grid shape.  This is a two-element tuple, (Nx, Ny), counting the 
number of nodes along the x- and y-axes.
    
delta
The grid spacing.  The is the distance between grid nodes in x and y
in the length units used in the measurement data (usually mm).

A, B, X, and index_map
These solution matrices/vectors set up the deconvolution problem.
    B = A * X
X contains the node values in an n-indexed vector (see above).  A and B
are constructed by the ADD_DATA() method.  Each call to the method 
accumulates new values in A and B.  For efficiency, they are sparse 
matrices, so caution should be used when attempting to manipulate them.

When all the data have been accumulated into A and B, the SOLVE() method
trims rows and columns of zeros from A and B to reduce the problem.  
This happens when the raw data do not pass through some elements of the
solution space, so the corresponding nodes are not represented in the 
matrix problem.  To make the problem linearly independent, we strip 
these nodes out of the problem and assert that they are zero.

The index_map member is an array of indices that map the elements of the
reduced (linearly independent) solution set back to the full solution
set.
"""
    N=(0,0)
    delta=0.
    A=None
    B=None
    index_map=None
    X=None
    _yoffset = 0
    _lock = False

    def __init__(self, Nx, Ny, delta):
        self.N = np.array((Nx, Ny), dtype=int)
        self.delta = float(delta)
        self._yoffset = -self.delta * (self.N[1]-1) / 2.
        # Initialize the solution matrices
        size = self.N[0] * self.N[1]
        self.A = None 
        self.B = None
        self.index_map = None
        self.X = None
        self._lock = False
        
    def save(self, destination=None):
        """Saves the grid settings and (if defined) the solution matrix and node values
    G.save()
        OR
    G.save(destination)

The destination should be a string path to a directory where files defining the
grid will be created.  If no destination is given, the current directory is used
The following files will be created

grid.conf
Plain text file including the grid dimensions (N) and spacing (delta).

A.npy
If the A solution matrix has been set up, A.npy contains it.

B.npy
If the B solution matrix has been set up, B.npy contains it.

X.npy
If the node values have been solved for, their values are stored in X.npy

index_map.npy
The index map is an ordered array of the nodes represented in the matrices A
and B.  
"""
        if destination is None:
            destination = '.'
        destination = os.path.abspath(destination)
        if not os.path.isdir(destination):
            raise Exception('Save: The destination directory does not exist: %s'%destination)
        # Write the grid configuration
        target = os.path.join(destination, 'grid.conf')
        with open(target, 'w') as ff:
            ff.write('Nx %d\nNy %d\ndelta %e'%(self.N[0], self.N[1], self.delta))
        # Write the matrix values
        if self.A:
            target = os.path.join(destination, 'A.npy')
            np.save(self.A,target)
        if self.B:
            target = os.path.join(destination, 'B.npy')
            np.save(self.B,target)
        if self.X:
            target = os.path.join(destination, 'X.npy')
            np.save(self.X,target)
        if self.index_map:
            target = os.path.join(destination, 'index_map.npy')
            np.save(self.index_map, target)
        
        
    def ij_to_n(self, i,j):
        """Calculates the node index from the xy indices
    n = G.ij_to_n(i,j)
"""
        return self.N[0] * j + i
        
    def n_to_ij(self, n):
        """Calculates the x,y indices from the node index
    i,j = G.n_to_ij(n)
"""
        n = int(n)
        j = np.floor(n / self.N[1])
        i = n - self.N[0]*j
        return np.array((i,j), dtype=int)
        
    def size(self):
        """Returns the number of nodes
    Nn = G.size()

Nn is the number of nodes in the grid.
"""
        return self.N[0] * self.N[1]
        
    def esize(self):
        """Returns the number of elements
    Ne = G.esize()

Ne is the number of elements in the grid.
"""
        return (self.N[0]-1)*(self.N[1]-1)
        
    def Ne(self):
        """Returns the element dimensions
    Nex, Ney = G.Ne()
    
Nex and Nex are the number of elements along the x- and y-axes.
"""
        return self.N - 1
        
    def node(self, *key):
        """Calculate an x,y coordinate, p, of a node.
    p = G.node(n)
        OR
    p = G.node(i,j)
    
p is a 2-element numpy array p = (x,y)

Indexing may be performed either by column-row (i,j) or by sequential, n
indexing.  There is no error-checking to be certain that i,j and n are
in-bounds for the grid, so strange results are possible if the calling
application is careless.
"""
        # Force i,j indexing
        if len(key)==2:
            i,j = key
        elif len(key)==1:
            i,j = self.n_to_ij(key[0])
        else:
            raise Exception('Grid nodes must be a single integer or a pair of integers')

        return np.array(
                (i * self.delta,
                j * self.delta + self._yoffset), dtype=float)

    def element(self, *key):
        """Calculate an x,y coordinate, p, of a node.
    p00,p10,p01,p11 = G.element(n)
        OR
    p00,p10,p01,p11 = G.element(i,j)
    
Each point, p, is a 2-element numpy array p = (x,y).  The point indices
indicate their location relative to the element. 

            p01         p11
                +------+             y
                |      |            ^
                |      |            |
                +------+            +---> x
            p00         p10

Indexing may be performed either by column-row (i,j) or by sequential, n
indexing.  There is no error-checking to be certain that i,j and n are
in-bounds for the grid, so strange results are possible if the calling
application is careless.
"""
        p00 = self.node(*key)
        p10 = p00 + [self.delta, 0]
        p01 = p00 + [0, self.delta]
        p11 = p00 + [self.delta, self.delta]
        return p00, p10, p01, p11
        
    def dims(self):
        """Calculate the physical dimensions of the grid domain
    width,height = G.dims()
"""
        return self.delta * (self.N-1.)

    def lam(self, R, d, theta):
        """Calculate the lambda vector from the wire location
    L = G.lam(self, R, d, theta)
    
L is the lambda vector for the wire location
R is the wire radius from the center of rotation
d is the distance between the center of rotation and the left-most node
theta is the wire angle from positive x in radians
"""
        # Initialize an empty lambda vector and index array
        L = []
        Lindex = []

        # Search for the point where the wire first crosses the grid
        # gridLS is a line segment representing the grid's length along
        # the y-axis.
        width,height = self.dims()
        gridLS = LineSegment(self.node(0,0), (0,height))
        # wireLS is the wire's path from center of rotation to the tip
        wireLS = LSrtheta((-d,0), R, theta)
        
        # Where does the wire first intersect the grid?
        test, sw, sg = wireLS.intersect(gridLS, s=True)
        # If the segments do not intersect, just return zeros
        if not test:
            return sparse.csr_matrix((self.size(),1), dtype=float)
            
        # The wire DOES intersect the grid.  At which j index?
        ii = 0
        jj = int(np.floor(sg*height/self.delta))
        
        # Calculate the intersection point
        # pstart is the point where the wire enters the element
        # pstop will be either the wire tip or the point where the wire
        # leaves the element
        pstart = gridLS(sg)
        # Note on which face the wire entered the element
        # Use a numbering system that starts with 0 on the bottom face
        # and progresses clockwise:
        # 0: bottom
        # 1: left
        # 2: top
        # 3: right
        # 4: NONE - the wire's endpoint is in the element
        # The first start face is always left
        fstart = 1
        
        # Keep looping until the wire path through the grid is finished
        while True:
            
            p00, p10, p01, p11 = self.element(ii,jj)
            
            # Search for the stop face.
            for fstop in range(5):
                # Skip this face if it is the start face
                if fstop != fstart:
                    # bottom
                    if fstop == 0:
                        edgeLS = LSstop(p00,p10)
                    # left
                    elif fstop == 1:
                        edgeLS = LSstop(p00,p01)
                    # top
                    elif fstop == 2:
                        edgeLS = LSstop(p01,p11)
                    # right
                    elif fstop == 3:
                        edgeLS = LSstop(p10,p11)
                    # NONE
                    else:
                        fstop = 4
                        pstop = wireLS(1)   # Use wire end-point
                        break
                    test,sw,se = wireLS.intersect(edgeLS, s=True)
                    if test:
                        pstop = edgeLS(se)
                        break

            # We now know the start and stop point of a wire segment in the
            # current element: pstart and pstop

            # Calculate some information about the segment in the element
            dp = pstop - pstart
            abs_dp = np.sqrt(np.sum(dp*dp))
            p0 = (pstart - p00)/self.delta
            dp /= self.delta
            # calculate the dimensionless integrals
            PHI00 = dp[0]*dp[1]/3. - dp[0]*(1.-p0[1])/2. - dp[1]*(1.-p0[0])/2. + (1.-p0[0])*(1.-p0[1])
            PHI10 = -dp[0]*dp[1]/3. + dp[0]*(1.-p0[1])/2. - dp[1]*p0[0]/2. + p0[0]*(1.-p0[1])
            PHI01 = -dp[0]*dp[1]/3. - dp[0]*p0[1]/2. + dp[1]*(1.-p0[0])/2. + (1.-p0[0])*p0[1]
            PHI11 = dp[0]*dp[1]/3. + dp[0]*p0[1]/2. + dp[1]*p0[0]/2. + p0[0]*p0[1]
            
            # modify the lambda vector
            #n = self.ij_to_n(ii,jj)
            #L[n,0] += abs_dp*PHI00
            Lindex.append(self.ij_to_n(ii,jj))
            L.append(abs_dp*PHI00)
            #n = self.ij_to_n(ii+1,jj)
            #L[n,0] += abs_dp*PHI10
            Lindex.append(self.ij_to_n(ii+1,jj))
            L.append(abs_dp*PHI10)
            #n = self.ij_to_n(ii,jj+1)
            #L[n,0] += abs_dp*PHI01
            Lindex.append(self.ij_to_n(ii,jj+1))
            L.append(abs_dp*PHI01)
            #n = self.ij_to_n(ii+1,jj+1)
            #L[n,0] += abs_dp*PHI11
            Lindex.append(self.ij_to_n(ii+1,jj+1))
            L.append(abs_dp*PHI11)
            
            # Move on to the next element
            # The stop point is now the start point
            pstart = pstop
            # Increment the element index based on the stop face
            if fstop==0:
                jj-=1
                fstart = 2
            elif fstop==1:
                ii-=1
                fstart = 3
            elif fstop==2:
                jj+=1
                fstart=0
            elif fstop==3:
                ii+=1
                fstart=1
            elif fstop==4:
                # Exit condition
                break
            # Detect the end of grid
            if ii<0 or ii>(self.N[0]-2) or jj<0 or jj>(self.N[1]-2):
                break
        return sparse.csr_matrix((L, (Lindex,np.zeros_like(Lindex))), shape=(self.size(),1), dtype=float)


    def add_data(self, R, d, theta, I):
        """Add data into the solution matrices
    G.add_data(R, d, theta, I)

R, d, theta, and I represent a single data point in the 

R   is the wire tip radius from the center of rotation in length units (usually
    mm).  This should be half the disc diameter plus the wire protrusion length.
d   is the disc center of rotation distance from the edge of the data set in 
    length units (usually mm)
theta is the wire angle relative to the x-axis in radians
I   is the wire current in uA divided by the wire circumference (i_uA/pi/D_mm)

ADD_DATA() calls LAM() to construct a lambda vector for the point.  Then
contributions to the A matrix and B vector are computed and added so
that
    G.A * G.X = G.B
where X is the solution vector.  The intent is that ADD_DATA be called 
repeatedly to fold in many individual measurements before the SOLVE() member
is finally called to calculate G.X.

For large grids and for large data sets, the matrix construction process 
performed by ADD_DATA can be quite time consuming, so it is designed to be used
in threads.  However, since ADD_DATA modifies the A and B members, race 
conditions become possible.  To make ADD_DATA thread-safe, a very simple 
internal locking mechanism is used, so that parallel executions of ADD_DATA will
wait their turns while A and B are being accessed.

"""
        if self.A is None:
            A = sparse.csr_matrix((size, size), dtype=float)
        if self.B is None:
            B = sparse.csc_matrix((size,1), dtype = float)
        # Calculate lambda
        L = self.lam(R,d,theta)
        # While updating the solution matrices, lock out the grid to prevent
        # a race conditions in multi-threading applications.
        self.acquire_lock()
        self.B += L*I
        self.A += L*L.T
        self.release_lock()


    def solve(self):
        """Execute the deconvolution operation
    solve()
    
Stores the result in self.X
"""
        # First, trim away nodes that do not impact the data represented
        # in A and B.  Start by listing the non-zero entries of
        # B.  This will constitute an ordered list of all the node 
        # indicies (sequential) that are represented in the data set.
        # Nodes not listed can be eliminated from the inversion problem
        # and this serves as a map from the reduced problem to the full
        # problem.
        self.index_map = np.unique(self.A.indices)
        nn = len(self.index_map)
        
        _csr_empty_col(self.A)
        _csr_empty_row(self.A)
        self.A.resize((nn,nn))
        _csc_empty_row(self.B)
        self.B.resize((nn,1))
        
        self.X = np.zeros((self.N[0]*self.N[1]), dtype=float)
        self.X[self.index_map] = linalg.spsolve(self.A, self.B)

    def acquire_lock(self):
        """Block execution of the process until the lock is released
    G.acquire_lock()
    ... do something dangerous to G ...
    G.release_lock()
"""
        # Now, we wait until the lock is released.  Check about once every 
        # millisecond.
        while self._lock:
            time.sleep(.001)
        # Then, we take it back
        self._lock = True

    def release_lock(self):
        """Release an execution lock after having run ACQUIRE_LOCK
    G.acquire_lock()
    ... do something dangerous to G ...
    G.release_lock()
"""
        self._lock = False



def grid_load(source=None):
    """Loads the files generated by the Grid.save() method
G = grid_load()
    OR
G = grid_load(source)

If source is omitted, then the current directory will be used.  Otherwise,
source must be a directory containing the files described by the SAVE() 
method.
"""
    if source is None:
        source = '.'
    source = os.path.abspath(source)
    if not os.path.isdir(source):
        raise Exception('Load: The source directory does not exist: %s\n'%source)
    
    # Load the grid configuration parameters
    target = os.path.join(source, 'grid.conf'):
    gridconf = {'Nx':-1, 'Ny':-1, 'delta':-1.}
    with open(target,'r') as ff:
        for thisline in ff:
            if thisline and thisline[0]!='#':
                param,value = thisline.split()
                if param in gridconf:
                    gridconf[param] = gridconf[param].__type__(value)
                else:
                    raise Exception('Load: grid.conf unrecognized parameter: %s'%param)
    
    G = Grid(gridconf['Nx'], gridconf['Ny'], gridconf['delta'])
    
    # Load the matrices
    target = os.path.join(source, 'A.npy')
    if os.path.isfile(target):
        G.A = np.load(target, allow_pickle=True)
    target = os.path.join(source, 'B.npy')
    if os.path.isfile(target):
        G.B = np.load(target, allow_pickle=True)
    target = os.path.join(source, 'X.npy')
    if os.path.isfile(target):
        G.X = np.load(target, allow_pickle=True)
    target = os.path.join(source, 'index_map.npy')
    if os.path.isfile(target):
        G.index_map = np.load(target, allow_pickle=True)

    return G
