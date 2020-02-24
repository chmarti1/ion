# Experiment 2

The second ion current experiment was over a cooled copper coupon.  Similar to the steel tests in Experiment 1, the coupon was cooled by a water-air mixture.  Unlike Experiment 1, copper coupons of different diameters were used to assess the impact of work surface area on the ion current measurements.

## Coupon

The coupons were 3/8-inch thick copper discs between 1.05" and 2.25" in diameter.  Each coupon had a 1/4-inch wide 1/8-inch deep circular channel milled into its underside, forming a step onto which a 1/2-inch pipe was pressed.  The assembly formed a male threaded cap with the disc at the pipe end.  A brass tube concentric to the pipe delivered coolant to the back surface of the disc, and the warm mixture was returned in the outer anulus formed between the concentric cylinders.

Temperature measurements were made at the coolant inlet and outlet.  A thermocouple was also cemented to the underside of the copper at the edge of the 1/4-inch channel.  After the severe thermal cycling involved in some of the tests, some of the coupons' press fits failed.  These were either discarded or they were brazed into place.

## Data

Data are organized into directories that indicate the disc diameter coupon over which they were collected.  When tests over a particular diameter were repeated on different days, the new directories were created with an appended hyphenated index to indicate their order.  Each data file includes meta data describing the gas flow rates, the measured temperatures, and the standoff distance.


## Files
The `loadall.py` script is responsible for generating the `TABLE.wsv` file.  This is a tabulated collection of parameters extracted from the raw voltage-current data and the meta data embedded in each data file.  The individual data files are plain text written with the [lconfig](http://github.com/chmarti1/lconfig) laboratory experiment configuration system.  These files include embedded meta data that define the experimental conditions at which the test was run.  Then, the various `post_.py` scripts are responsible for generating the plots found in the export directory.

The `TABLE.wsv` is a whitespace separated variable file with a row for every data set.  In the table are the various physical conditions under which the test was run and parameters that define a piece-wise linear fit of the current-voltage characteristic:


| Header    | Description |
|:---------:|-------------|
|file_name  | The original raw data file name |
|d_in       | Disc diameter (inches) |
|flow_scfh  | Total gas flow rate (scfh) |
|ratio_fto  | Fuel/Oxygen ratio by volume |
|plate_t_c  | Copper surface temperature (degC) |
|tip_t_c    | Torch tip temperature (degC) |
|plate_q_kw | Heat transferred to the plate (kW) |
|standoff_in| Standoff distance from coupon to torch tip (in) |
|b1         | Regime-1 IV characteristic y-intercept (uA) |
|R1         | Regime-1 IV characteristic slope (MOhm) |
|b2         | Regime-2 IV characteristic y-intercept (uA) |
|R2         | Regime-2 IV characteristic slope (MOhm) |
|b3         | Regime-3 IV characteristic y-intercept (uA) |
|R3         | Regime-3 IV characteristic slope (MOhm) |

