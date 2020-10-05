# post6.md

`post6.py` is a specialized script for visualizing the vertical scans collected by the `vscan.py` script, where full spatial resoution is not desired.  Instead, the wire is inserted fully and only the `z` height is varied.  This is a useful means of quickly scanning for relative vertical changes in mean ion concentration without the complexity of a fully resolved scan.

Like `post5.py`, `post6.py` only requires the pedestal signals produced by `post1.py`.

The `post6.py` script outputs a single plot with all of the pedestal signals overplotted, called `profile.png`.  From that profile, the currents at two angles are sampled from each height and scaled to calibrated ion density.  The inverse of ion density is then plotted versus height in `iz.png`.  The line formed far downstream is predicted by the recombination model.  Finally, a `post6.dat` file is generated that summarizes the results of the analysis.

The behavior of `post6.py` can be changed by editing several lines early in the script.
```python
# These are options that you might want to change before running this script...
use_long = True        # Use the long or short pulse when finding the angle offset?
data_dir = '../data'    # Where are the data?
theta_start = -0.03       # Exclude data not between theta_start and theta_stop
theta_stop = 0.1
theta1 = .025       # First wire position
L1 = 6.             # First wire length
theta2 = .038       # Second wire position
L2 = 5.5             # Second wire length
z_start = 6.        # Perform the slope fit starting at z=?
```

`use_long` was originally added so that `post6.py` could perform its analysis without needing to run `post1.py`, but that approach was abandoned, and `use_long` is no longer used.

`data_dir` specifies the relative path to the directory where the data directories can be found.

`theta_start` and `theta_stop` indicate the range of disc angles (in radians) over which to plot in the pedestal signals.

`theta1` and `theta2` indicate the two disc angles at which the pedestals should be sampled to produce the i-z plot.

`L1` and `L2` are estimates for the length of wire emersed in the flame at each angle.  These are used to crudely estimate the current density to the wire.  Later modifications to the code ignore the `L2` setting provided, and instead choose it such that the mean current densities close to the torch are identical.

In other words, if `I(theta)` were the pedestal signal,
```python
L2 = L1 * I(theta2) / I(theta1)
```

`z_start` indicates the height below which a linear fit will be performed on the 1/n data.

It is important to note that `post6.py` makes aggressive assumptions about the wire diameter, velocity, and applied voltage.  Lines 162 - 168 have hard-coded assumptions that the bias voltage is 20V, and the wire diameter is .254mm.  The mean fluid velocity is estimated by assuming that it is about 75m/s when the total flow is 21scfh, so when `total_scfh` is the preheat flow rate in scfh,
```python
U = (75.) * (total_scfh / 21.)
```

It will be essential that `post6.py` be adjusted to be more flexible if it is re-used in future experiments.

The contents of a `post6.dat` output file might appear as below.
```python
# Example post6.dat file
fg_pre_scfh 10.1879
o2_pre_scfh 15.0244
fg_post_scfh 10.0753
o2_post_scfh 15.0261
total_scfh 25.2124
ratio_fo 0.678090
c0 -1.60159452e-18
c1 2.26976989e-18
Uc1 2.04379438e-16
```

`fg_pre_scfh` is the calibrated methane preheat flow rate measured prior to the scan in scfh.

`o2_pre_scfh` is the calibrated oxygen preheat flow rate measured prior to the scan in scfh.

`fg_post_scfh` is the calibrated methane preheat flow rate measured after the scan in scfh.

`o2_post_scfh` is the calibrated oxygen preheat flow rate measured after the scan in scfh.

In horizontal scans, drift in flow rate while the test is under way would have an obvious impact on the data, but that may not be true for a vertical scan.  These pre- and post-flow data provide a record so tests may be discarded if significant drift has corrupted them.

`total_scfh` is an effective total flow rate calculated from the pre- measurements (fuel+oxygen).

`ratio_fo` is the fuel-to-oxygen ratio calculated from the pre- measurements (fuel/oxygen).

`c0` and `c1` are the linear regression coefficients that form the line shown in the i-z plot.  They form a fit of the form

n<sup>-1</sup> = c<sub>0</sub> + c<sub>1</sub> z

where `c0` has units m^3^, and `c1` has units m^3^mm^-1^.

The quantity, `Uc1` is the estimated velocity times the `c1` regression coefficient.  This quantity should be proportional to the ion-electron recombination coefficient in the outer cone of the flame.  It is calculated explicitly to see how severly it changes from test to test.