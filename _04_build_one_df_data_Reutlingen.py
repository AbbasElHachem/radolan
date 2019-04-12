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
path_to_seperate_dfs = (r'X:\hiwi\ElHachem\Jochen'
                        r'\Reutlingen_Radolan\seperate_data')

path_to_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                  r'\Reutlingen_Radolan'
                  r'\final_df_Reutlingen_.csv')


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
                dfs[stn].append(idx, in_df.loc[ix, :])
            except Exception:
                break
            continue

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
