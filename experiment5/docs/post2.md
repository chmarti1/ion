# post2.py

<a name=post2></a>[post2.py](post2.md) constructs a matrix inversion problem to calculate the spatial distribution of current densities that would optimally agree with the individual pedestal signals produced by `post1.py`.  The values of the matrix are stored in `.npz` files, and the solved array of node concentrations is contained in `X.npy`.  Since the solution is a 1D array representing a 2D map of node concentrations, a text file named `grid.conf` contains the shape and resolution of the grid so `X` can be reshaped to the appropriate 2D array.

It is called from the command line with a single argument indicating the data set that should be analyzed.  It's in-line help documentation reads:
```python
"""
post2.py DATADIR
    Second post-processing step.  Read in post1 data files (p1d) wire
    current as a function of angle and disc position, and generate a
    single post2 data file p2d
    
    For ease of use, the DATADIR may be specified merely by its trailing
    characters.  For example, data in a directory named '20191024143210'
    may be specified by the command
        $ post1.py 143210
    If multiple directories are discovered with the trailing characters
    '143210', then an exception is raised.
"""
```

There are several parameters early in the script that are used to configure its behavior.
```python
# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
Nx = 75      # How many x-points
Ny = 101     # How many y-points
delta = 0.25
```

`data_dir`: The scripts are intended to be run with the `bin` directory as the present working directory, so the relative path to the data directory should be given here.

`Nx`, `Ny`: These specify the size of the 2D node array that defines the grid.  The x-axis is taken to be along the direction of wire rotation, and the y-axis is taken to be in the direction of wire insertion into the flame.  x is taken to be zero along the theta=0 line where the wire is exactly parallel to the y-axis.  y is taken to be zero at the wire's tip during the outer-most measurement.

`delta` specifies the grid's spatial resolution in mm.  Since the grid is taken to be uniform, there is only one resolution parameter.

For each disc angle found in each `.p1d` file, at each disc location, the algorithm calculates coefficients representing the contributions that each node should have to the wire in that location.  For any given wire location, the vast majority of the nodes will not contribute to its signal; only nodes adjacent to the wire's path will contribute.  These are aggregated into a matrix using an analysis described in [1] referenced in the root [README.md](../README.md).  

This entire process is implemented in the `wiretools.py` module, which is imported at the top of `post2.py`.  For users wishing to understand `wiretools.py`, it has its own detailed in-line documentation.

This process is expensive, since it involves individually mapping the path of each wire location in each file.  The script uses the `multiprocess` Python module to split off a pool of workers equal to the number of system CPU cores.  Each one works on one data file at a time, and prints a `'.'` character to the screen to establish a kind of progress bar so the user can monitor the algorithm's progress.

The matrix solution is astonishingly quick given the pre-processing time required assemble it.  Saving and reloading the solution is automated by the `wiretools.py` module.  The matrix and vector used to form the matrix inversion problem are stored in `A.npz` and `B.npz`.  The solution vector is stored in `X.npy`.  Since the solution vector is a 1D array of values, it needs to be re-mapped into a 2D array before it can be plotted.  For this reason, the `grid.conf` file is also generated, which only contains three lines:

```python
Nx 75
Ny 101
delta 2.500000e-01
```

This defines the grid shape and resolution (in mm).  Remapping the 1D array into the 2D array is also automated by `wiretools.py`.

The units of the solution in `X.npy` are current density (usually uA/mm^2^ or A/m^2^) - not concentration.  `post2.py` is only responsible for deconvolving the total integrated wire current into a local current density map.  `post3.py` and `post4.py` rescale that into a number density.
