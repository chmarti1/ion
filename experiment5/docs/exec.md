# Executables

The various scripts used for conducting experiment 5 and processing its results are contained in the `bin` directory.  Follow the links below to read more about each:

The sections in this document are
[Performing an experiment](#exp)
- [wscan](#wscan)
- [vscan](#vscan)
[Post processing](#post)
- [list](#list)
- [post1](#post1)
- [post2](#post2)
- [post3](#post3)
- [post4](#post4)
- [post5](#post5)
- [post6](#post6)

The list below is comprised of direct links to the detailed documentation for each file.  These links are also provided in the text below.

[wscan.md](wscan.md)
[vscan.md](vscan.md)
[list.md](list.md)
[post1.md](post1.md)
[post2.md](post2.md)
[post3.md](post3.md)
[post4.md](post4.md)
[post5.md](post5.md)
[post6.md](post6.md)

---


## <a name=exp></a> Performing an experiment
[wscan.py](wscan.md) automates a single horizontal scan of the flame.  The script prompts the user to enter parameters and then alternates between data collection and small incremental motion of the horizontal translation stage.  The results of a single horizontal scan are gathered into a single directory in `data`, so that all files in a directory represent data collected at different disc locations, but all at the same vertical location.

[vscan.py](vscan.md) prompts the user to enter parameters and then collects data at a series of uniformly spaced vertical intervals.  `vscan.py` behaves identically to `wscan.py`, but the disc moves vertically instead of horizontally.  Since these scans only provide a single pedestal signal per vertical location, they do not provide enough information to reconstruct spatial resolution.  Instead, these kinds of scans are excellent ways of capturing high resolution information on the veritcal decay of ions in the outer cone.

Each of these generates a series of data files in a subdirectory of the `data` directory - each file containing current data corresponding to a single disc location.  Each subdirectory represents a "scan" of the flame, so that the flame's ion concentration can be reconstructed from an aggregation of all of the individual data files.

## Post processing

The raw [data](data.md) files are merely a series of samples of the wire's current and a photointerrupter state in time.  Each sample indicates the current measured from the wire at a unique moment in time, and there may be dozens of files representing different disc locations in a single scan.  Distilling this into a single spatially resolved measurement is an inherently multi-step process.

When analyzing a dataset, each `postX.py` script creates its own `postX` directory in the target dataset's directory.  It deposits its results there, and its existance is a record for all the algorithms that follow that the prior analysis steps have been run and are available.  If a `postX.py` script finds that its results already exist, it will usually prompt the user for what to do.

<a name=list></a>Because the data set is so large, it is necessary to have tools to quickly visualize their contents.  The [list.py](list.md) script prints a table listing each horizontal scan dataset with the date and time it was collected, its `z` (height), the number of files in the dataset, and a list of the post-processing steps that are found.

<a name=post1></a>[post1.py](post1.md) processes each raw data file into a .p1d (post-1-data) file containing a white space delimited table of calibrated wire current mean, median, and standard deviations at a series of disc angles.  These files are stored alongside a plot of the pedestal signals that may be manually inspected to ensure that the data are clean and that the algorithm is working properly.

<a name=post2></a>[post2.py](post2.md) constructs a matrix inversion problem to calculate the spatial distribution of current densities that would optimally agree with the individual pedestal signals produced by `post1.py`.  The values of the matrix are stored in `.npz` files, and the solved array of node concentrations is contained in `X.npy`.  Since the solution is a 1D array representing a 2D map of node concentrations, a text file named `grid.conf` contains the shape and resolution of the grid so `X` can be reshaped to the appropriate 2D array.

<a name=post3></a>[post3.py](post3.md) loads local current densities calculated by `post2.py` and outputs a properly scaled pseudocolor image.

<a name=post4></a>[post4.py](post4.md) loads the results of many `post2.py` solutions and plots them side-by-side in an array.  This is particularly useful for visualizing results of `vscan.py`.  Because this script is run on multiple datasets simultaneously, its output is left in the `experiment5` root directory instead of the dataset directory.

<a name=post5></a>[post5.py](most5.md) is a specialized script that was written to visualize data collected while adjusting the probe bias while the wire was fully inserted into the flame.  These tests were done January 15th and 16th.  Before then, a 20V bias had been used, and it wasn't clear whether that was optimal.

<a name=post6></a>[post6.py](post6.md) is a specialized script for visualizing the vertical scans collected by the `vscan.py` script, where full spatial resoution is not desired.  Instead, the wire is inserted fully and only the `z` height is varied.  This is a useful means of quickly scanning for relative vertical changes in mean ion concentration without the complexity of a fully resolved scan.

There are several other minor scripts that are not explicitly documented, but that were useful.  For example, the `postbatch.py` script was edited as needed to automate the process of calling the various post-processing steps in sequence for large data sets.  The analysis process usually took less than an hour, but longer than one would typically want to supervise.

There are also modules that are imported by the scripts and do not need to be evoked by the user: `lconfig.py` is responsible for loading and calibrating raw data; `lplot.py` is responsible for formatting plots; `csprobe.py` is responsible for applying the Clements and Smy candidate Langmuir probe current models; and `pool.py` was originally used to experiment with parallel threading in Python2 before abandoning it (By deliberate design, Python cannot execute simultaneous parallel threads).  Instead, multi-threading was abandoned for forking multiple processes using the `multiprocess` module.