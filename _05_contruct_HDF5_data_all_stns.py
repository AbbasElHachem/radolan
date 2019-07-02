# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
GOAL: Construct one HDF5 dataset for all stations (1 to 12)

Use Reutlingen rainfall data as dataset constructed in script _04_

Add for every station:
    
    Start date
    End data
    Number of Nans
    Location
    Official Name
    
Save the HDF5 data
"""

__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# =============================================================================
import os

import h5py
import numpy as np

from pathlib import Path

main_dir = Path(r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radoland'
                r'\dataframe_as_HDF5_Reutlingen_Stations')
os.chdir(main_dir)

df_rainfall_file = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radoland'
                    r'final_df_Reutlingen_.csv')
f = h5py.File("mytestfile.hdf5", "a")
