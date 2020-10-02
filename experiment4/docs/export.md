# Export

Experiment 4 uses six python scripts to aggregate analysis results across all of the cut tests.  Each is named for the type of analysis it is intended to perform.

`frequency.py` isolates the DC, fundamental excitation frequency, and the first and second harmonics of the voltage signal to construct the regime 2 resistance signal throughout an entire test.  This script can be called from the command line with a data file as an argument to produce this analysis, and the results are stored in the `frequency` directory.  Each execution of `frequency.py` creates two files: one named `r_[testname].png` showing the resistance signal, and one named `v_[testname].png` showing each of the frequency components.

`height.py` aggregates all of the cuts that were performed under constant conditions to produce `height.png`, a plot of the regime 2 resistance against the standoff.  Like `incline.py` and `speed.py`, there is a hard-coded menu of available data written into the beginning of `height.py`, and its behavior is configurable by changing the states of T/F flags next to each of the file names in the scripts.  This is explained in more detail by comments in each script.  `height.py` is responsible for generating `height.png` and `rms.png`. The results are tabulated in detail in `height_results.txt`, which serves as a record for how the fits in `height.png` were produced.

`incline.py` aggregates the tests conducted while cutting on an incline to produce `incline.png` and `incline_time.png`.  Like `height.py` and `speed.py`, the list of available inclined tests is hard-coded into the top of the script.

`ivchar.py` produces a series of "snapshot" IV characteristic plots for individual tests.  Like `frequency.py`, it can be called from the command line with the source data and times at which snapshots should be taken as arguments.  The results are stored in the `ivchar/[testname]` directory as a sequence of plots named for the time in the test when the snapshot was taken.

`speed.py` aggregates tests conducted with varying speeds to produce `speed.png`.  Like `height.py` and `incline.py`, there is a hard-coded list of available data at the top of the script that defines its behavior.

`waterfall.py` generates a waterfall diagram of both current and voltage throughout a test.  Like `ivchar.py` and `frequency.py`, it can be called from the command line with a data set as an argument, and it places output in the `waterfalls` directory.  `waterfall.py` creates files named `i_[testname].png` and `v_[testname].png` that show the waterfall diagram for the current and voltage signals respectively.  These diagrams are used to diagnose noise and nonlinearity in the system.