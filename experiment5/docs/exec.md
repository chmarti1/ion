# Executables

The various scripts used for conducting experiment 5 and processing its results are contained in the `bin` directory.  Follow the links below to read more about each:

## Performing an experiment
[wscan.py](wscan.md) prompts the user to enter parameters and then automates a single horizontal slice of the flame.

[vscan.py](vscan.md) prompts the user to enter parameters and then automates a series of horizontal slices of the flame at a series of regular vertical intervals.

Each of these generates a series of data files in the `data` directory - each file containing current data corresponding to a single disc location.

## Post processing

[post1.py](post1.md) processes each of the raw current vs time data files and transpose the signal to current versus disc position using the offsets entered by the user and a photointerrupter signal.  