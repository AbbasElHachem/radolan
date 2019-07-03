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

# import os
# import timeit
# import time
import pandas as pd
import numpy as np

from pathlib import Path
# from datetime import datetime

path_to_seperate_dfs = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
                        r'\seperate_data\\df_every_stn_seperate')

path_to_one_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                      r'\Reutlingen_Radolan\seperate_data'
                      r'\Niederschlagsdaten_until102015_copy_Abbas.csv')


path_to_second_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                         r'\Reutlingen_Radolan\seperate_data'
                         r'\Rohdaten_Januar2015_Niederschlag pro Minute_SER fürInfraConsult_copy_Abbas.csv')

path_to_third_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                        r'\Reutlingen_Radolan\seperate_data'
                        r'\Rohdaten_NiederschlagRT21.05.2014-15.06.2015_copy_Abbas.csv')

path_to_fourth_ppt_df = r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\final_df_Reutlingen_.csv'


def get_all_files_in_directory(directory, extension):
    all_files = []
    for filepath in Path(directory).glob('**/*.%s' % extension):
        all_files.append(filepath.absolute())
    return all_files


all_dfs = get_all_files_in_directory(path_to_seperate_dfs, 'csv')

start_date = '2014-05-21 00:00:00'
end_date = '2019-04-05 00:00:00'

date_range = pd.date_range(start=start_date, end=end_date, freq='Min')

data = np.zeros(shape=(date_range.shape[0], 12))
data[data == 0] = np.nan

final_df_combined = pd.DataFrame(data=data, index=date_range,
                                 columns=[1, 2, 3, 4, 5, 6,
                                          7, 8, 9, 10, 11, 12])
#==============================================================================
#
#==============================================================================
for df_file in all_dfs:
    df_name = str(df_file)[-26:-22]
    stn_nbr = int(df_name[2:])

    in_df = pd.read_csv(df_file, sep=';', index_col=0,
                        parse_dates=True,
                        infer_datetime_format=True)
    final_df_combined.loc[in_df.index, stn_nbr] = in_df.values.ravel()

#=====================================================================
#
#=====================================================================

df1 = pd.read_csv(path_to_one_ppt_df, sep=';',
                  parse_dates=[['date1', 'date2']],
                  infer_datetime_format=True)

df1.rename(columns={'date1_date2': 'Time'}, inplace=True)
df1.set_index('Time', inplace=True)
#
#
for ix, stn in zip(df1.index, df1.stn.values):
    print(ix, stn)
#     stn_str = str(stn)
    final_df_combined.loc[ix, stn] = df1[df1.stn == stn].loc[ix, 'ppt']


#=====================================================================
#
#=====================================================================
df2 = pd.read_csv(path_to_second_ppt_df, sep=';',
                  parse_dates=[['date1', 'date2']],
                  infer_datetime_format=True)

df2.rename(columns={'date1_date2': 'Time'}, inplace=True)
df2.set_index('Time', inplace=True)


# df2.index = df2.index.strftime('%Y-%m-%d %H:%M:%S')
# df2.index = pd.datetime(df2.index, format='%Y-%m-%d %H:%M:%S')

for ix, stn in zip(df2.index, df2.stn.values):

    #     stn_str = str(stn)
    #     ix_timefmt = datetime.datetime.strptime(ix, '%d.%m.%Y %H:%M:%S')
    #     ix_timefmt = datetime.datetime.strftime(ix_timefmt, '%Y-%m-%d %H:%M:%S')
    print(ix, stn)
    final_df_combined.loc[ix,
                          stn] = df2[df2.stn == stn].loc[ix, 'ppt']

#=====================================================================
#
#=====================================================================
# #
df3 = pd.read_csv(path_to_third_ppt_df, sep=';',
                  parse_dates=[['date1', 'date2']],
                  infer_datetime_format=True)

df3.rename(columns={'date1_date2': 'Time'}, inplace=True)
df3.set_index('Time', inplace=True)
# df3.index = df3.index.strftime('%Y-%m-%d %H:%M:%S')

for ix, stn in zip(df3.index, df3.stn.values):
    print(ix, stn)
#     stn_str = str(stn)
    final_df_combined.loc[ix, stn] = df3[df3.stn == stn].loc[ix, 'ppt']

#==============================================================================
#
#==============================================================================
df4 = pd.read_csv(path_to_fourth_ppt_df, sep=';',
                  parse_dates=True, index_col=0,
                  infer_datetime_format=True)


for stn in df4.columns:
    print(stn)
    final_df_combined.loc[df4.loc[:, stn].index,
                          int(stn)] = df4.loc[:, stn].values


#==============================================================================
#
#==============================================================================
final_df_combined.to_csv(r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\seperate_data\data_df.csv',
                         sep=';')
# if __name__ == '__main__':
#
#     print('**** Started on %s ****\n' % time.asctime())
#     START = timeit.default_timer()  # to get the runtime of the program
# #     all_dfs = list_all_full_path('.csv', path_to_seperate_dfs)
# #     in_df = pd.read_csv(all_dfs[-1], sep=';', encoding='latin1', engine='c')
# #
# #     dfs = {i: [] for i in range(1, 13)}
# #
# #     for stn in dfs.keys():
# #         for ix in in_df.index:
# #             try:
# #                 idx = pd.to_datetime(ix, format='%d.%m.%Y')
# #                 dfs[stn].append([idx, in_df.loc[ix, :]])
# #                 break
# #             except Exception as msg:
# #                 print(msg)
# #                 break
# #             continue
#
#     STOP = timeit.default_timer()  # Ending time
#     print(('\n****Done with everything on %s.\nTotal run time was'
#            ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
