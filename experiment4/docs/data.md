# Data Files

The raw data files are included in directories with a date stamp indicating when the data were collected.  The tests are merely numbered in order they were collected, but each file contains the meta data necessary to understand the test conditions.  Each file was written by the [lconfig](github.com/chmarti1/lconfig) system, which is under continuous development and has its [own detailed documentation](https://github.com/chmarti1/lconfig/blob/master/docs/documentation.md).

The contents of each data file are divided into two parts: a **header** and a **body**, with another time stamp separating them.  The header includes meta data that describe the conditions under which the test was conducted and the settings that were used to configure the [LabJack T7](https://labjack.com/products/t7) data acquisition unit.  The body contains the raw voltage data (two channels in this case) collected at the indicated sample rate.

In these experiments, the analog output channel 0 was configured to generate a triangle wave, which was amplified to bias the torch voltage.  Meanwhile, both voltage and current measurements were fed back to analog inputs 0 and 1.  In this way, data from a single test repeatedly scans the a +/- 10V range while monitoring both current and voltage, so that the IV characteristic could be constructed.

## Body

In these experiments, the analog output channel 0 was connected to a custom amplifier circuit that was used to supply a voltage to the torch.  The torch voltage and the current driven were buffered and fed back to analog input channels 0 and 1 respectively.  Channel 0 is the torch voltage relative to work, and requires no calibration.  Nominally the calibration of the current signal on channel 1 was designed to be 4V for every 100uA.  Careful calibration showed that when _ai1_ is the voltage on analog input 1, and _i_ is the current (positive from torch to work),

_i = ai1 * 25.242500(uA/V) - .15605(uA)_

## Header

We leave the meaning of the standard configuration directives to the Lconfig documentation, but in this document, we establish the significance of those parameters that are peculiar to this experiment.

| Meta Parameter | Units | Description |
|:--------------:|:----:|:-----:|
| type | - | Type of test conducted.  This indicates which of the post-processing algorithms will use the file.  `speed` feed rate was varied; `height` all conditions were held constant; `incline` the work was deliberately inclined so that standoff changed during the cut.  Absence of meta data may indicate that the data were merely exploratory.
| start_sec | sec | The time since the beginning of the test when the cut is well into the plate and analysis may begin |
| stop_sec | sec | The time since the beginning of the test when the cut is nearly finished and analysis should stop |
|so_in | inches | The standoff distance in inches |
| rise_in | inches | The nominal increase in standoff over the course of the cut.  This is usually zero except in inclined tests. |
| feed_ipm | inches per minute | Feed rate |
| o2_scfh | scfh | Preheat oxygen flow rate |
| fg_scfh | scfh | Preheat methane flow rate |

Comments were manually added to most (if not all) of the "speed" tests to indicate how the feedrate was varied throughout the experiment.  That includes the sequence of feed rates in order, and the distance of cut for each.