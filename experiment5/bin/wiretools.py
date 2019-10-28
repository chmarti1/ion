#
#   Wire deconvolution tools
#

import numpy as np
from scipy import sparse
import scipy.sparse.linalg as linalg
import os, sys


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
"""
    def __init__(self, Nx, Ny, delta):
        self.N = np.array((Nx, Ny), dtype=int)
        self.delta = float(delta)
        self._yoffset = -self.delta * (self.N[1]-1) / 2.
        # Initialize the solution matrices
        size = self.N[0] * self.N[1]
        self.A = sparse.csr_matrix((size, size), dtype=float)
        self.B = sparse.csc_matrix((size,1), dtype=float)
        self.X = None
    
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
        # Initialize an empty lambda vector
        L = sparse.lil_matrix((self.size(),1), dtype=float)

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
            return sparse.csr_matrix(L)
            
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
            n = self.ij_to_n(ii,jj)
            L[n,0] += abs_dp*PHI00
            n = self.ij_to_n(ii+1,jj)
            L[n,0] += abs_dp*PHI10
            n = self.ij_to_n(ii,jj+1)
            L[n,0] += abs_dp*PHI01
            n = self.ij_to_n(ii+1,jj+1)
            L[n,0] += abs_dp*PHI11
            
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
        
        return sparse.csr_matrix(L)


    def add_data(self, R, d, theta, I):
        """Add data into the solution matrices
    add_data(R, d, theta, I)
    
R is the radius from center of rotation to the wire tip in mm
d is the distance from the grid origin to the center of rotation in mm
theta is the wire angle from the x-axis in radians
I is the wire current divided by the wire circumference (i_uA/pi/D_mm)

ADD_DATA() calls LAM() to construct a lambda vector for the point.  Then
contributions to the A matrix and B vector are computed and added so
that
    A * X = B
where X is the solution vector
"""
        L = self.lam(R,d,theta)
        self.B += L*I
        self.A += L*L.T
