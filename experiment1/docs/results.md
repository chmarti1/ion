# Analysis Results

The [analysis.py](../analysis.py) script is responsible for loading each raw data file, applying the appropriate calibration, and performing piecewise linear fits to the IV-characteristic represented by each.  

The results of this analysis are tabulated in [TABLE.wsv](../TABLE.wsv).  This whitespace separated variable file includes a row for every data set and a column for every parameter of interest in the analysis.  In the table are the various physical conditions under which the test was run and parameters that define a piece-wise linear fit of the current-voltage characteristic:


| Header | Description |
|:------:|-------------|
|tst     | Test number |
|S.O.    | Standoff distance between torch tip and steel coupon surface (inches) |
|O2      | Oxygen flow rate (scfh) |
|FG      | Fuel gas (CH4) flow rate (scfh) |
|Flow    | Total flow rate (scfh) |
|F/O     | Fuel / oxygen ratio by volume |
|R1      | Regime 1 resistance - dV/dI slope (MOhm) |
|R2      | Regime 2 resistance - dV/dI slope (MOhm) |
|R3      | Regime 3 resistance - dV/dI slope (MOhm) |
|v0      | Floating potential - V at I=0 (Volts) |
|i1      | Regime 1-2 transition current (uA) |
|i2      | Regime 2-3 transition current (uA) |
|File    | The original raw data file name |

The various `postX.py` scripts are merely responsible for loading this table and plotting different selections of the data.