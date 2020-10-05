# post5.py

`post5.py` is a specialized script that was written to visualize data collected while adjusting the probe bias while the wire was fully inserted into the flame.  The dataset that was finally adopted for this test was performed on January 16th, 2020.

The vast majority of data were collected with a wire bias voltage 20V below ground.  However, it was not clear whether this parameter was appropriate.  The 1/16/2020 datasets were performed at a constant height with the wire fully emersed in the flame.  Only the probe bias voltage was adjusted.

`post5.py` uses the same command-line system as `post1.py` and `post2.py` to identify the target data set on which to operate.  Because `post5.py` does not require a complete horizontal scan, there is no need to run `post2.py` on the data; only `post1.py` needs to be run.

There are two plots produced by `post5.py`.  The first is the pedestal signal in uA produced by each of the bias voltages.  In the second plot, the current at two selected disc angles are plotted against bias voltage.  Two candidate models relating wire current to ion concentration are extrapolated from the 20V bias for comparison against experimental results.  This is the method that was used to establish which of the models is appropriate for the present system.

The behavior of `post5.py` can be modified by editing these lines near the top of the script.

```python
# These are options that you might want to change before running this script...
use_long = True        # Use the long or short pulse when finding the angle offset?
data_dir = '../data'    # Where are the data?
theta_start = -0.03       # Exclude data not between theta_start and theta_stop
theta_stop = 0.1
theta1 = .0183
theta2 = .0345
```

`use_long` is a vestage from a prior version of `post5.py` when it also performed the job done by `post1.py`.  It is no longer used, but it was never removed.

`data_dir` gives the relative path to the directory where the datasets reside.

`theta_start` and `theta_stop` indicate the range of angles (in radians) over which to plot the pedestal signal.  Most of the disc angle exhibit no current, so this allows the plot to be appropriately scaled to show the actual data.

`theta1` and `theta2` set the angles (in radians) to be plotted in the current versus voltage plot.