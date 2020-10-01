# Analysis Results

The `loadall.py` script is responsible for loading each raw data file, applying the appropriate calibration, and performing piecewise linear fits to the IV-characteristic represented by each.  

The results of this analysis are tabulated in [table.wsv](../table.wsv).  This whitespace separated variable file includes a row for every data set and a column for every parameter of interest in the analysis.  In the table are the various physical conditions under which the test was run and parameters that define a piece-wise linear fit of the current-voltage characteristic:


| Header | Description |
|:------:|-------------|
|file_name     | The name of the raw data file from which the results were calculated |
|d_in | Disc diameter in inches |
|flow_scfh | Total flow (fuel + oxygen) in scfh |
| ratio_fto | Fuel/oxygen ratio (fuel / oxygen) |
|plate_t_c | Plate temperature in deg. C measured by thermocouple. |
|tip_t_c | Torch tip temperature measured in deg. C |
|plate_q_kw | Plate heat flux in kW, calculated from calculated enthalpy increase of the coolant |
|standoff_in | Standoff distance between the torch and work piece in inches |
|b1 | Regime 1 offset (uA) |
|R1 | Regime 1 slope (MOhms) |
|b2 | Regime 2 offset (uA) |
|R2 | Regime 2 slope (MOhms) |
|b3 | Regime 3 offset (uA) |
|R3 | Regime 3 slope (MOhms) |

The various `postX.py` scripts are merely responsible for loading this table and plotting different selections of the data.