# Experiment 3

The third ion current experiment was over half-inch thick steel plates.  These tests were performed with one of two excitations: (1) a sawtooth wave permitting a scan of the entire IV characteristic, and (2) a constant +10V allowing constant monitoring of the regime-3 saturation current levels.  These tests were run over long durations to monitor for changes as the plates heated.

## Samples

The plate samples were two 0.5-inch-thick steel plates 12in x 12in square.  Each was marked to divide it into four 6-inch square quadrants; at the center of which was a test location.  On the underside beneath each test location, a 1/8-inch hole was drilled to 1/8-inch of the plate surface.  A type-K thermocouple was cemented in each.  A thermal model was used to construct the temperature of the plate surface from the thermocouple value and the known heat load from the torch.

One of the samples was in good condition, was cleaned with a wire brush to remove rust and particulates, and was further wiped with a dry cloth prior to test.  The second was soaked in bleach and vinegar solution and left in direct sunlight to cause deliberate severe corrosion.  The bleach and vinegar produced salt crystals, which grew on the plate as the water evaporated.  Half of the plate was washed of the salt crystals they were allowed to remain on the other half.

## Data

Data are labeled by a letter and a number (e.g. a1.dat).  The letter identifies which plate was under test (a = corroded plate, b = clean plate).  The number identifies which quadrant was under test.  Which type of excitation was used may be determined by inspecting the analog output configuration in the data header.

## Files

Because there are not many data files, the analysis codes for this data set are not especially carefully organized or documented.  The `analysis_.py` scripts are responsible for loading the raw data and producing plots from them.  They also contain hard-coded references to which files are IV scans and which are constant excitations.

