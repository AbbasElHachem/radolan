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
import pandas as pd

#==============================================================================
#
#==============================================================================

main_dir = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
            r'\dataframe_as_HDF5_Reutlingen_Stations')
os.chdir(main_dir)

# path for rainfall df, all stations
df_rainfall_file = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
                    r'\dataframe_as_HDF5_Reutlingen_Stations'
                    r'\data_df_with_zero_and_nan_values_23062020.csv')
# path to coordinates df
ppt_coords = (r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\RT_Pluviodaten"
              r"\tobi_metadata_ser.csv")

#==============================================================================
#
#==============================================================================
# read ppt df and define time frequency as 1min
df_ppt = pd.read_csv(df_rainfall_file, sep=';', index_col=0,
                     parse_dates=True, infer_datetime_format=True,
                     engine='c')
df_ppt = df_ppt.asfreq(freq='1Min')

# get all ppt data as array
ppt_data = np.array(df_ppt.values)

# read coordinates df
df_coords = pd.read_csv(ppt_coords, sep=';', index_col=0)
lons_float = [np.float(_v.replace(',', '.')) for _v in df_coords['lon'].values]
lats_float = [np.float(_v.replace(',', '.')) for _v in df_coords['lat'].values]
z_float = [np.float(_v) for _v in df_coords['z'].values]

# define hdf5 object
hf = h5py.File("Reutlingen_12_ppt_stns_21052014_23062020.h5", "w")

# assign ppt data as dataset
hf.create_dataset('data', data=ppt_data, dtype='f8')

# create a group for coordinates, assign lon, lat and elevation
g2 = hf.create_group('coords')
g2.create_dataset('lon', data=lons_float, dtype='f8')
g2.create_dataset('lat', data=lats_float, dtype='f8')
g2.create_dataset('z', data=z_float, dtype='f8')

# create a dataset for station name
hf.create_dataset('name', data=np.string_(df_coords['name']))

# create new group for timestamps, add start, end dates and nbr of minutes
# ix_str = [np.string_(ix) for ix in df_ppt.index.to_list()]

# dt = h5py.string_dtype(encoding='utf-8')

g3 = hf.create_group('Timestamps')
g3.create_dataset('Start_Date', data=np.string_(df_ppt.index[0]))
g3.create_dataset('End_Date', data=np.string_(df_ppt.index[-1]))
g3.create_dataset('Index_1Min_Freq',
                  data=np.string_(df_ppt.index))
# np.arange(0, len(df_ppt.index), 1)
# close file, save is automatic
hf.close()
