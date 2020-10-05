# Experiment 5

Experiment 5 is the demonstration of a technique for taking spatially resolved ion density measurements in a high-temperature flame using the Langmuir probe method.  A disc spins in the horizontal plane with a fine (0.01") wire protruding radially.  Vertical and horizontal translation stages move the disc so that the path of the wire through the flame can be controlled.

Langmuir probes determine the local ion density from the electrical current to a metal surface in the plasma.  The difficulty of establishing spatially resolved measurements in the oxyfuel flame is twofold: a wire emersed in the flame will receive current that is an amalgamation of all the ion densities along its length; and the fine wire probes necessary for spatial resolution cannot survive in the flame.  The solution to both problems is to monitor the wire current is it follows numerous rapid transits through the flame, and to calculate an ion density that is simultaneously consistent with all of them.

The principle is described in detail in the [2020 Combustion Science and Technology paper](./docs/2020_cst.pdf) [1].

The post-processing in experiment 5 is more sophisticated than any of the others in this collection, so there is decidedly more rigor in organization and documentation.  All executables and scripts used to conduct and analyze the experimental results reside in the `bin` directory.  Raw data and post processing results all reside in the `data` directory.  Exported final results reside in the `export` directory.  Compilation dependencies reside in the `source` directory.

For an overview of the executables and their function, see [docs/exec.md](./docs/exec.md).

For detailed descriptions of each, see their individual

For a detailed description of the raw data files, see [docs/data.md](./docs/data.md).

## References

[1] C. Martin, A. Untaroiu, K. Xu, “Spatially resolved ion density measurements in an oxyfuel cutting flame.”  Combustion Science and Technology, 2020, doi:10.1080/00102202.2020.1792458 [IN PRESS]

[2] C. Martin, et al... “Semiconductor aspects of the oxyfuel cutting torch preheat flame Part II: The flame’s internal electrical structure,” ASME Manufacturing Science and Engineering Conference, Cincinnati, OH, 2020. 