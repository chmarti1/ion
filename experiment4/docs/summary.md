# Summary of data
There are three types of tests conducted here: incline tests where a plate set at a deliberate angle is cut, speed tests where a level plate is cut with varying speed, and height tests where a level plate is cut under constant conditions.

## 190114 (1/14/2019)
These were the first attempts to collect data while cutting.  The ground wire was disconnected, so no valid data were collected.

## 190128 (1/28/2019)
Tests 1 and 2 were not valid because the ground and torch leads were reversed.  Test 3 was the only data collected.  The standoff was not noted!

## 190130 (1/30/2019)
Three triangle wave tests on a sloped plate ranging in height from 0.1 to 0.4 inches.  Each test used a different speed, but identical preheat and cutting O2 settings.

## 190211 (2/11/2019)
Three triangle wave tests on a sloped plate ranging in height from 0.1 to 0.43 inches.  These supposedly replicate the tests conducted in 190130.

## 190222 (2/22/2019)
These are the first tests conducted with a sine excitation.  The fuel/oxygen ratios were also more realistic, and the tests were conducted with a constant standoff.  However, the height and level controls on the plates were not yet adequate.

These are also the first tests where the test condition details are embedded in the data files as meta data.

## 190301 (3/1/2019)
Attempted to use shims to control level; took eight constant standoff measurements.

## 190315 (3/15/2019)
Three variable speed tests and one incline test.  Experimental control for height was not adequate.

## 190320 (3/20/2019)
First tests using the three-point plate leveling system.  Eleven tests at constant standoff.

## 190322 (3/22/2019)
Two speed tests, one incline test, and twelve constant standoff tests using the plate leveling method.  Five of the tests were at f/o ratio 0.65 instead of 0.78.

## 190325 (3/25/2019)
Two speed tests and two pierce tests.

## 190327 (3/27/2019)
Identified super-harmonics in the sine measurements; experimented with different excitations to ensure linearity.  Seven tests with 0-10uA excitations, and twelve tests were with 5-15uA excitation.

## Selected tabulated tests and their descriptions

| Date      | Test  | Type  | speed | S.O.  | Flow  | FG/O2 | Notes |
|           |       |       | (ipm) | (in)  | (scfh)| ratio |       |
|:---------:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|-------|
|3/22/19    |1      |speed  | -     | .10   | 25.3  | .78   | 10, 14, 16, 12, 8, 6, 10ipm in 2" lengths. SO after cut was .084 |
|           |2      |speed  | -     | .25   | 25.3  | .78   | same speeds, SO after cut was .23 |
|           |3      |incline| 12    | -     | 25.3  | .78   | .10" to .25" standoff over 12" ramp; after cut measured SO .081@start .239@stop |
|           |4      |const. | 12    | .15   | 25.3  | .78   | .147" SO after cut |
|           |5      |const. | 12    | .25   | 25.3  | .78   | .233" SO after cut, start failed |
|           |6      |const. | 12    | .15   | 25.3  | .78   | .139" SO after cut |
|           |7      |const. | 12    | .25   | 25.2  | .78   | .228" SO after cut |
|           |8      |const. | 12    | .10   | 25.2  | .65   | Short length of plate 5-3/4"LG, SO unchanged |
|           |9      |const. | 12    | .20   | 25.2  | .65   | SO unchanged |
|           |10     |const. | 12    | .30   | 25.2  | .65   | |
|           |11     |const. | 12    | .10   | 25.3  | .65   | |
|           |12     |const. | 12    | .20   | 25.4  | .65   | |
|           |13     |const. | 12    | .30   | 25.5  | .65   | Cutting O2 50psig, maybe as high as 55psig |
|           |14     |const. | 12    | .15   | 25.2  | .79   | Fresh plate, Cutting O2 70psig |
|           |15     |const. | 12    | .15   | 25.3  | .78   | |
|3/25/19    |1      |speed  | -     | .10   | 25.3  | .78   | 10,14,16,12,8,6,10ipm in 2" lengths. |
|           |2      |speed  | -     | .25   | 25.3  | .78   | same speeds |
|           |3      |pierce | -     | .25   | 25.3  | .78   | Failed pierce |
|           |4      |pierce | -     | .15   | 25.3  | .78   | Successful pierce |
|3/27/19    |1      |const. | 12    | .10   | 25.3  | .78   | 6" long cuts, height stable, 0-10uA excite |
|           |2      |const. | 12    | .15   | 25.3  | .78   | SO reduced about .01 (not measured) |
|           |3      |const. | 12    | .20   | 25.3  | .78   | SO reduced about .015 (not measured), cleaned obstructed PH channel |
|           |4      |const. | 12    | .40   | 25.3  | .78   | Tiny SO red. .005-.01" |
|           |5      |const. | 12    | .30   | 25.3  | .78   | |
|           |6      |const. | 12    | .15   | 25.3  | .78   | |
|           |7      |const. | 12    | .25   | 25.4  | .79   | |
|           |8      |const. | 12    | .15   | 25.3  | .78   | 5-15uA excite |
|           |9      |const. | 12    | .25   | 25.3  | .78   | narrow cut-off piece |
|           |10     |const. | 12    | .10   | 25.3  | .79   | |
|           |11     |const. | 12    | .15   | 25.3  | .78   | |
|           |12     |const. | 12    | .20   | 25.4  | .78   | |
|           |13     |const. | 12    | .25   | 25.3  | .78   | |
|           |14     |const. | 12    | .30   | 25.3  | .78   | |
|           |15     |const. | 12    | .30   | 25.3  | .78   | |
|           |16     |const. | 12    | .15   | 25.3  | .78   | |
|           |17     |const. | 12    | .25   | 25.3  | .78   | |
|           |18     |const. | 12    | .10   | 25.3  | .78   | |
|           |19     |const. | 12    | .20   | 25.3  | .78   | |

