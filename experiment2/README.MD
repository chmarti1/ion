# Experiment 2

The second ion current experiment was over a cooled copper coupon.  Similar to the steel tests in Experiment 1, the coupon was cooled by a water-air mixture.  Unlike Experiment 1, copper coupons of different diameters were used to assess the impact of work surface area on the ion current measurements.

A detailed description of the experiment and its results is given as a part of this 2018 Experimental Thermal and Fluid Science paper [/docs/2018_etfs.pdf](docs/2018_etfs.pdf) [1].

## Coupon

The coupons were 3/8-inch thick copper discs between 1.05" and 2.25" in diameter.  Each coupon had a 1/4-inch wide 1/8-inch deep circular channel milled into its underside, forming a step onto which a 1/2-inch pipe was pressed.  The assembly formed a male threaded cap with the disc at the pipe end.  A brass tube concentric to the pipe delivered coolant to the back surface of the disc, and the warm mixture was returned in the outer anulus formed between the concentric cylinders.

Temperature measurements were made at the coolant inlet and outlet.  A thermocouple was also cemented to the underside of the copper at the edge of the 1/4-inch channel.  After the severe thermal cycling involved in some of the tests, some of the coupons' press fits failed.  These were either discarded or they were brazed into place.

## Data and Results

Data are organized into directories that indicate the disc diameter coupon over which they were collected.  When tests over a particular diameter were repeated on different days, the new directories were created with an appended hyphenated index to indicate their order.  Each data file includes meta data describing the gas flow rates, the measured temperatures, and the standoff distance.

For a detailed description of the contents of the raw data files, see [docs/data.md](./docs/data.md).

For a detailed description of analysis results tabulated in `table.wsv`, see [docs/results.md](./docs/results.md).

For a description of each of the plots produced by the `postX.py` scripts, see [docs/export.md](./docs/export.md).

## References

[1] C. Martin, “A study of ion currents in an oxyfuel flame due to work surface chemical action,” Experimental Thermal and Fluid Sciences, vol. 98, pp. 239-250, 2018. https://doi.org/10.1016/j.expthermflusci.2018.06.003.

[2] C. R. Martin, J. Kinney, A. Matzik, and J. Molina, “Electrical signatures for chemical action at the work surface in an oxyfuel flame,” in Proceedings of the ASME 13th Manufacturing Science and Engineering Conference, vol. 3, (College Station, TX), 2018. doi:10.1115/MSEC2018-6354.