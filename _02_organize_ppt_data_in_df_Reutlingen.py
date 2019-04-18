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
import numpy as np

main_dir = Path(os.getcwd())
os.chdir(main_dir)

# path to ppt data Reutlingen
in_ppt_file = r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\Niederschlagsdaten_Copy.csv'
assert os.path.exists(in_ppt_file)


def makeDF(ppt_file_path, start_date, end_date):
    ''' 
    function used to read an csv file and output a dataframe 

    The Dataframe has the stations number as a Columns

    And a datetime Object as index with a 1 Minute frequency
    Start 01.07.2017 till 04.05.2019 (defined outside function)

    param: ppt_file_path (path to csv file)

    Note: the csv file has been modified than the original file,
         this is done to make working with it easier 

    # What was changed: 
        1. remove all information regarding the station keep only stn number
        2. remove the ',' as seperator for Ppt data and replace it with '.'
        3. add column headers (station; date1; date2; ppt)

    Return: saved organized Dataframe
    '''

    # read dataframe
    in_df = pd.read_csv(ppt_file_path, sep=';', encoding='latin1', engine='c')

    # make datetime index, combined the two columns
    # (date.month.year + hour.minutes.seconds)
    in_df['Time'] = in_df.date1 + ' ' + in_df.date2
    in_df.drop(['date1', 'date2'], axis=1, inplace=True)
    in_df.set_index('Time', drop=True, inplace=True)
    in_df.index = pd.to_datetime(in_df.index, format='%d.%m.%Y %H:%M:%S')

    # make ppt values as float
    vals = np.empty(shape=in_df.ppt.values.shape[0])
    for i, str_val in enumerate(in_df.ppt.values):
        try:
            vals[i] = float(str_val.replace(',', '.'))
        except:
            vals[i] = -9999
    in_df['ppt'] = vals

    # create datetime index for final DF
    date_range = pd.date_range(start=start_date, end=end_date, freq='Min')

    # get stations number to be used as column headers
    station_nbrs = np.unique(in_df.station.values)
    # create new df, index: Time, columns: stations
    new_df = pd.DataFrame(index=date_range, columns=station_nbrs)

    # interate for every station number, intersect Time and append to new_df
    for stn_nbr in station_nbrs:
        df_stn = in_df[in_df.station == stn_nbr]['ppt']
        idx_intersct = new_df.index.intersection(df_stn.index)
        new_df.loc[idx_intersct, stn_nbr] = df_stn.values
    new_df = new_df[new_df >= 0]
    # save final df and return it
    new_df.to_csv(r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\final_df_Reutlingen_.csv',
                  sep=';', float_format='%0.3f')
    return new_df

# =============================================================================
# CALL FUNCTION HERE
# =============================================================================


if __name__ == '__main__':

    print('**** Started on %s ****\n' % time.asctime())
    START = timeit.default_timer()  # to get the runtime of the program

    start_date = '2017-07-01 00:01:00'
    end_date = '2019-04-05 00:00:00'

    makeDF(in_ppt_file, start_date, end_date)  # call function here

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
