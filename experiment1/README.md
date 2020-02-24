# Experiment 1

The first ion current experiments were conducted over a cooled steel coupon.  This disc-shaped coupon contained cooling channels below a 3/4-inch thick steel disc with embedded thermocouples.

## Cooling
The data files include meta data describing the flow rates of air and water to the coupon, the inlet and outlet temperature of the collant mixture.  This provides enough information to calculate the heat removed by the collant.

## Coupon Temperature
Using a thermal model for the disc-shaped coupon, the peak surface temperature was extrapolated from two embedded thermocouples.  In addition to providing a surface temperature, this method also provides an estimate for the heat conducted through the coupon to the coolant below.  This estimate was compared against the cooling heat measurement as a verification of the coupon thermal model.

## IVCHAR
The Current-Voltage Characteristics were measured by applying a +/- 10V triangle wave between the torch and coupon.  Both current and voltage were monitored by the amplifier circuit's internal measurements and acquired by the LabJack T7.

## Results
A table summarizing anaysis results is given in the "TABLE.wsv" file.  Test conditions are described by the coupon surface temperature, the standoff distance, the fuel gas, and the oxygen flow rates.  The results are the slopes in regimes 1, 2, and 3 (R1, R2, R3), and the saturations currents i1, and i2, obtained by a piecewise-linear fit of the IVCHAR data.

Tests conducted without the coupon over an uncooled piece of low carbon steel are summaried in NPTABLE.wsv.

Precision data (in data/precision) were collected by applying a low-amplitude sine wave as a means to more precisely measure the regime-2 slope (R2).

## Files
The `loadall.py` script is responsible for generating the `TABLE.wsv` file.  This is a tabulated collection of parameters extracted from the raw voltage-current data and the meta data embedded in each data file.  The individual data files are plain text written with the [lconfig](http://github.com/chmarti1/lconfig) laboratory experiment configuration system.  These files include embedded meta data that define the experimental conditions at which the test was run.  Then, the various `post_.py` scripts are responsible for generating the plots found in the export directory.

The `TABLE.wsv` is a whitespace separated variable file with a row for every data set.  In the table are the various physical conditions under which the test was run and parameters that define a piece-wise linear fit of the current-voltage characteristic:


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

