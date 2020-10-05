# post1.py

[post1.py](post1.md) processes each raw data file into a .p1d (post-1-data) file containing a white space delimited table of calibrated wire current mean, median, and standard deviations at a series of disc angles.  These files are stored alongside a plot of the pedestal signals that may be manually inspected to ensure that the data are clean and that the algorithm is working properly.

It is called from the command line with a single argument indicating the data set that should be analyzed.  It's in-line help documentation reads:
```python
"""
post1.py DATADIR
    First post-processing step.  Read in raw current-time data and
    re-map the data to current-angle files while throwing away nonsense
    data.  The results are discovered in ../data/DATADIR/ and the results
    are stored in ../DATADIR/post1/.  Results are plain text post1 data
    files (*.p1d) and png plots of the data.
    
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
use_long = True        # Use the long or short pulse when finding the angle offset?
data_dir = '../data'    # Where are the data?
theta_start = -0.3       # Exclude data not between theta_start and theta_stop
theta_step = .0007        # Organize the data into bins theta_step wide
theta_stop = 0.3
```

`use_long`:  Because the photointerrupter generates two pulses per rotation, it is necessary to ignore one of them.  Because the shaft features that generate the pulse are not entirely symmetrical, one of the pulses is longer than the other.  Setting the `use_long` parameter determines which of the two pulses' rising edges should be used as the reference point for 0-degrees disc angle.

`data_dir`: The scripts are intended to be run with the `bin` directory as the present working directory, so the relative path to the data directory should be given here.

`theta_start`, `theta_stop`: These specify the range of disc angles (in radians) to be included in the analysis output.  Everything outside of these values is ignored since the wire will be nowhere near the flame.

`theta_step`: This specifies the increments between disc angles in the output.  The range between `theta_start` and `theta_stop` will be divided into equal bins of this size (in radians), and every sample will be added to one of these bins for analysis.  Once the bins are assembled, each is analyzed for number of points, mean, median, and standard deviation.

The [raw data](data.md) documentation describes the methods for establishing the wire's calibrated current from the raw voltage samples and methods for calculating the wire position when each sample was taken.

This entire process is expensive, since it involves individually sorting and analyzing millions of samples across a single scan.  The script uses the `multiprocess` Python module to split off a pool of workers equal to the number of system CPU cores.  Each one works on one data file at a time, and prints the name of the file under analysis to allow the user to monitor progress.

The outputs of `post1.py` are tabulated `.p1d` files; one for every `.dat` file in the data directory.  Each `.p1d` file also has an accompanying plot visualizing the analysis results.  Bad data can be caught quickly by a brief inspection of the pedestal signals in these plots.

The `.p1d` files include a header that defines the conditions (including disc location) at which the data were collected.  The first lines of one of these files might appear as shown below.


```python
# An example .p1d file
x 2.750000
y 2.000000
r 127.000000
dw .254
w 32.740613
wstd 0.006687
# theta(rad)	count	mean(uA)	median(uA)	std dev(uA)
-0.300000	10	-0.005951	-0.011636	0.049964
-0.299300	10	-0.004609	0.000201	0.054786
-0.298600	10	-0.005871	0.005729	0.064447
-0.297900	10	-0.002399	-0.004928	0.053599
-0.297200	10	-0.017238	-0.021501	0.044058
-0.296500	10	-0.002715	0.004544	0.055240
-0.295800	10	0.001705	0.004544	0.059039
-0.295100	19	-0.009556	-0.015583	0.052601
-0.294400	11	-0.000511	0.022301	0.067127
-0.293700	10	-0.005004	-0.004137	0.051556
-0.293000	10	-0.001136	-0.011241	0.053812
-0.292300	10	-0.013448	-0.007294	0.051291
-0.291600	10	-0.003188	-0.004533	0.056653
...
```

`x` and `y` specify the location of the disc center of rotation in mm.  There is some potential confusion because the x,y coordinates in this file are transposed from the coordinate system used in the final visualization.  These are translation stage coordinates, where x is horizontal with positive in the direction of the flame (y-axis in flame coordinates), and y is the vertical location with down (away from the torch) being positive (z-axis in flame coordinates.

`r` is the radius from the center of disc rotation to the wire tip in mm.

`dw` is the wire diameter in mm.

`w` is intended to be read as "omega", and is the disc rotational speed in radians per second.

`wstd` is the standard deviation of the disc's rotational speed in radians per second.

`theta` is the disc's angle with 0 being parallel to the y-axis (x-axis in translation stage coordinates).

`count` is the number of current samples that were found to be included in this angle's bin for aggregation of statistics.

`mean`, `median`, and `std dev` are the respective staticistcs for the current samples found at that angle in microamps.
