# Data Files

The raw data files are included in the [data](../data) directory.  Each file was written by the [lconfig](github.com/chmarti1/lconfig) system, which is under continuous development and has its [own detailed documentation](https://github.com/chmarti1/lconfig/blob/master/docs/documentation.md).

Each data file is named with a timestamp that uniquely identifies when the respective test was executed (ivchar_YYYYmmDDHHMMSS.dat).  The contents of each data file are divided into two parts: a **header** and a **body**, with another time stamp separating them.  The header includes meta data that describe the conditions under which the test was conducted and the settings that were used to configure the [LabJack T7](https://labjack.com/products/t7) data acquisition unit.  The body contains the raw voltage data (two channels in this case) collected at the indicated sample rate.

In these experiments, the analog output channel 0 was configured to generate a triangle wave, which was amplified to bias the torch voltage.  Meanwhile, both voltage and current measurements were fed back to analog inputs 0 and 1.  In this way, data from a single test repeatedly scans the a +/- 10V range while monitoring both current and voltage, so that the IV characteristic could be constructed.

## Body

In these experiments, the analog output channel 0 was connected to a custom amplifier circuit that was used to supply a voltage to the torch.  The torch voltage and the current driven were buffered and fed back to analog input channels 0 and 1 respectively.  Channel 0 is the torch voltage relative to work, and requires no calibration.  Nominally the calibration of the current signal on channel 1 was designed to be 4V for every 100uA.  Careful calibration showed that when _ai1_ is the voltage on analog input 1, and _i_ is the current (positive from torch to work),

_i = ai1 * 25.242500(uA/V) - .15605(uA)_

## Header

We leave the meaning of the standard configuration directives to the Lconfig documentation, but in this document, we establish the significance of those parameters that are peculiar to this experiment.


| Meta Parameter | Units | Description |
|:--------------:|:----:|:-----:|
| periods | - | The number of triangle wave periods that were applied in this test.|
| plate_Thigh_C  | deg. C | The upper coupon thermocouple measurement |
| plate_Tlow_C | deg. C | The lower coupon thermocouple measurement |
| plate_Q_kW | kW | The heat flux through the coupon calculated from Tlow and Thigh.
| plate_Tpeak_C | deg. C | The maximum temperature at the plate surface calculated from Tlow and Thigh. |
| cool_Thigh_C | deg. C | The measured air-water coolant mixture exhaust temperature. |
| cool_Tlow_C | deg. C | The measured air-water coolant mixture inlet temperature. |
| air_psig | psi (gauge) | The measured coolant air pressure upstream of a critical orifice; used to calculate the air flow rate into the coolant mixture. |
| water_gph | US Gal. per hour | The measured water flow rate into the coolant mixture (via rotameter).
| cool_Q_kW | kW | The heat flux into the coolant calculated from the rise in enthalpy of the coolant mixture.  This calculation included latent heat of vaporization for the water vapor portion of the exhaust.  In some tests, it was not calculated.
| standoff_in | inches | The shortest distance between the torch tip and the coupon surface.
| oxygen_scfh | std. cu. ft per hour | The molar flow rate of preheat oxygen. |
| fuel_scfh | std. cu. ft per hour | The molar flow rate of methane. |
| flow_scfh | std. cu. ft. per hour | The calculated total flow rate (fuel + oxygen) |
| ratio_fto | - | The calculated fuel-to-oxygen ratio by volume (fuel / oxygen). |


