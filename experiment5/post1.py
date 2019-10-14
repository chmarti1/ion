#!/usr/bin/python
"""
POST1
	First post-processing step.  Read in raw current-time data and
	re-map the data to current-angle files while throwing away nonsense
	data.
"""


import os, sys
from os import path
import lconfig as lc
