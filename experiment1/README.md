# Experiment 1

This is the first data collection in a series of experiments studying ion currents in the preheat flame of the oxyfuel cutting torch.  The purpose of this data set is to establish the current-voltage (IV) characteristic between the flame and steel work piece and to establish empirical relationships between the IV characteristic and process parameters.

A detailed description of the work is provided in the [2017 Experimental Thermal and Fluid Science paper](./docs/2017_etfs.pdf) [1] included in the "docs" folder.

This data set was collected over a cooled steel coupon in the preheat configuration so that the steel temperature could be stabilized and controlled independently of the fuel and oxygen flow rates.  This disc-shaped coupon contained cooling channels below a 3/4-inch thick steel disc with embedded thermocouples.

For a detailed description of the contents of the raw data files in the `data` directory, see [docs/data.md](./docs/data.md).

For a description of the post-analysis results tabulated in `TABLE.wsv`, see [docs/results.md](./docs/results.md).

For a description of the plots contained in the `export` directory, see [docs/export.md](./docs/export.md).

There is a number of other files that will not be of interest to most users.  All `*.bin` files are compiled executables that were responsible for the data collection, and their respective `*.conf` files were used to configure the data acquisition.  These are included merely because they were run in this directory to generate the data in the first place.  However, their respective settings were embedded directly in the headers of the data files, so should not need to be consulted.

The `NPTABLE.wsv` summarizes data collected from the `data/noplate` directory.  These were exploritory experiments conducted over a steel slat that were never published.  Similarly, the `data/precision` directory contains exploratory data collected using sine wave excitation instead of triangle waves.  These data were never published, but were the first attempt at the method that is now standard for measuring Regime 2 resistance directly.

The `pictures` directory contains images and one video collected during data acquisition.

## References

[1] C. Martin, C. Leonard, and J. VonFricken, *A study of the electrical characteristics of an oxy-fuel flame,* Experimental Thermal and Fluid Science, vol. 88, pp. 65-72, 2017. http://dx.doi.org/10.1016/j.expthermflusci.2017.05.010.

[2] C. R. Martin, _Mechanized oxyfuel control with ion current sensing,_ Welding Journal, vol. 96, pp. 154-162, May 2017.

[3] C. R. Martin, _Replacing mechanized oxyfuel cutting sensors with ion current sensing,_ in Proceedings of the ASME Manufacturing Science and Engineering Conference, (Los Angeles, CA), 2017. MSEC2017-2789. 