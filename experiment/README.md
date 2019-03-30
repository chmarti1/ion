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