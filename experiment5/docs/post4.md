# post4.py

`post4.py` loads the results of many `post2.py` solutions and plots them side-by-side in an array.  This is particularly useful for visualizing results of `vscan.py`.  Because this script is run on multiple datasets simultaneously, its output is left in the `experiment5` root directory instead of the dataset directory.

Unlike `post1.py` through `post3.py`, `post4.py` can accept many data directories as arguments.  Each may still be specified using the same abbreviated format like in `post1.py`.  The scaled ion density pseudocolor images are arranged in an array of images in a single plot, and each is labeled with that dataset's z-axis height.  The individual plots will be arranged in the same order they are specified at the command line starting from left to right and then proceeding down.  The plots will fill in a maximum of three per row and new rows will be added as needed to show all of the plots specified.

`post4.py` requires that `post1.py` and `post2.py` be run in advance on each of the datasets to be included in the plot.

The behavior of `post4.py` can be adjusted by editing these lines near the top of the script:
```python
# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
vscale = (0., 3e18)
window = [7., -2. ,17., 8.]
```

`data_dir` specifies the relative path to the directory where the raw data collections can be found.

`vscale` specifies the pseudocolor density scale to use.  In the example above the minimum is zero and the maximum is 3 x 10^18^ m^-3^.

`window` specifies a rectangular window in the format [xmin, ymin, xmax, ymax] in units of mm.  This is a subset of the total image to show in the image array.  In most datasets, the region of interest is only a small subset of the total image, so this allows the user to crop out the black background.

The design intent is that users will collect many horizontal slices (e.g. using `vscan.py`) of a flame under stable operating conditions.  Then, using `list.py`, the user will isolate the datasets that were part of that scan and type them in the order to be displayed when evoking `post4.py` from the command prompt.

`post3.py` was originally used to validate the Clements and Smy model used to calculate ion density from `post2.py`'s output.  `post4.py` presumes that work has already been done, and relies on the default wire diameter, flame velocity, and probe bias voltage parameters coded into the `csprobe.py` module.  _This is a dangerous design, since it may not be appropriate to future data sets, but it was a convenient and effective way to produce aesthetic plots for the preliminary data set._