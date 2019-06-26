# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
GOAL: Construct one dataframe from all the data available for the
12 stations in Reutlingen.

Dataframe: 
    Index: Time
    Columns: Stations 1 to 12
"""

__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# ===================================================

from pathlib import Path

from _03_compare_ppt_ro_radolan import list_all_full_path

import os
import timeit
import time
import pandas as pd
import numpy as np
path_to_seperate_dfs = (r'X:\hiwi\ElHachem\Jochen'
                        r'\Reutlingen_Radolan\seperate_data')

path_to_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                  r'\Reutlingen_Radolan'
                  r'\df_all_21052014_05042019.csv')

start_date = '15-05-2014 00:00:00'
end_date = '01-04-2019 00:00:00'

date_range = pd.date_range(start=start_date, end=end_date, freq='Min')

data = np.zeros(shape=(date_range.shape[0], 12))
data[data == 0] = np.nan

#  df12 = pd.read_csv(r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\seperate_da
#     ...: ta\0000000012_0102_20170712105304_copy_Abbas.csv", sep=';', parse_dates=[['
#     ...: date1', 'date2']], infer_datetime_format=True)

# df12.rename(columns={'date1_date2': 'Time'}, inplace=True)
# df12.set_index('Time', inplace=True)

final_df_combined = pd.DataFrame(data=data, index=date_range,
                                 columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

if __name__ == '__main__':

    print('**** Started on %s ****\n' % time.asctime())
    START = timeit.default_timer()  # to get the runtime of the program
    all_dfs = list_all_full_path('.csv', path_to_seperate_dfs)
    in_df = pd.read_csv(all_dfs[-1], sep=';', encoding='latin1', engine='c')

    dfs = {i: [] for i in range(1, 13)}

    for stn in dfs.keys():
        for ix in in_df.index:
            try:
                idx = pd.to_datetime(ix, format='%d.%m.%Y')
                dfs[stn].append([idx, in_df.loc[ix, :]])
                break
            except Exception as msg:
                print(msg)
                break
            continue

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
