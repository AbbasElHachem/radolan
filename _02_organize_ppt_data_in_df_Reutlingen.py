# !/usr/bin/env python.
# -*- coding: utf-8 -*-

""" Script to read the observed Precipitation data and Organize it in a DF

Parameters
----------
file_loc : str
    The file location of the precipitaiton sheet


Returns
-------
Data Frame
    a dataframe with columns as stations and data as Precipitaion values
"""

__author__ = "Abbas El Hachem"
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# =============================================================================
from pathlib import Path

import os
import timeit
import time

import pandas as pd

# changes in code

main_dir = Path(os.getcwd())
os.chdir(main_dir)

in_ppt_file = r'Niederschlagsdaten.csv'
assert os.path.exists(in_ppt_file)
# TODO FIX ME
in_df = pd.read_csv(in_ppt_file, sep=';', encoding='latin1')
# skiprows=1, parse_dates=[1, 2])
if __name__ == '__main__':

    print('**** Started on %s ****\n' % time.asctime())
    START = timeit.default_timer()  # to get the runtime of the program

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
