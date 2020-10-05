# post3.py

`post3.py` loads local current densities calculated by `post2.py` and outputs a properly scaled pseudocolor image of ion density.

This job is not especially computationally expensive, so it may seem strange to split it off as a separate post-processing step.  As discussed in [1], the model that should be used to calculate calibrated ion density from current density is not entirely obvious.  `post3.py` is isolated as a separate step so that different current density models could be explored without repeating the expensive current density calculation.

`post3.py` uses the same commandline argument structure as [post1](post1.md) and [post2](post2.md).  See their documentation for how to call `post3.py`.  

The output of `post3.py` is a pair of pseudocolor plots stored in a `post3` directory in the source data directory.  `pcolor_i.png` is a verbatim representation of the current density calculated by `post2.py`, while `pcolor.png` is in calibrated number density units.

The behavior of `post3.py` can be modified by editing several lines near the top of the script.

```python
# These are options that you might want to change before running this script...
data_dir = '../data'    # Where are the data?
U = 75.
D = .000254
V = None
```

`data_dir` is a prefix used to construct the relative path to the data directory identified at the command line.

`U` is the approximate fluid velocity in m/s to be used in the ion density model.

`D` is the wire density in m to be used in the ion density model.  Technically, this is redundant with the `dw` parameter supplied in the source data files.  While this invites a new opportunity for error in the data, it saves the script from needing to dig through the data to identify the wire diameter, and it allows users to experiment with the sensitivity of the parameter on the rescaled data.

`V` is the bias voltage applied to the wire in volts below ground.  If it is set to `None`, `post3.py` will extract it from the header of `000.dat`, and it is automatically scaled down by a factor of 91.66% to account for the small voltage drop in the shunt circuit used to measure the current.  Allowing users to explicitly specify voltage makes it possible to experiment with the sensitivity of the parameter on the rescaling model.

The rescaing is done using Clements and Smy's 1970 thin sheath paper (full citation included in [1]).  The model is applied by the `wiretools.Grid.density()` method.  To do this, the `density()` function relies on the `csprobe.py` module's `cs2()` and `cs2_n()` functions, which actually implement the model.
