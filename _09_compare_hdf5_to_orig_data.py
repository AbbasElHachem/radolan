'''
Created on Jul 17, 2020

@author: hachem
'''

from _00_read_HDF5 import HDF5

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

HDF52 = HDF5(
    infile=(r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan"
            r"\dataframe_as_HDF5_Reutlingen_Stations"
            r"\Reutlingen_12pluvios_215052014_23062020.h5"))
all_ids = HDF52.get_all_names()

data = HDF52.get_pandas_dataframe('12')


all_files = glob.glob(
    r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
    r'\RT_Pluviodaten'
    r'\c_until_072017\*')  # f_until_230620
assert len(all_files) > 0, 'directory seems empty'


for i, df_file in enumerate(all_files):
    stn_id = i + 1
    print(stn_id)

    try:
        df = pd.read_csv(df_file, sep=';', encoding='latin-1',
                         skiprows=1, header=None)

        # create date time index
        time_ix_str = [ix0.replace('.', '-') + ' ' + ix1
                       for ix0, ix1 in zip(df[0], df[1])]

        time_ix_time_obj = pd.DatetimeIndex(time_ix_str)
        time_ix_range = pd.DatetimeIndex(
            time_ix_time_obj.strftime(
                date_format='%d-%m-%Y %H:%M:%S'))
        # get ppt data
#         for ix, ppt in enumerate(df[2]):
#             print(ix, '/', len(df[2].values))
#             if (type(ppt) == str and str(ppt) != '---'):
#                 #np.float(ppt.replace(',', '.'))
#                 pass
#             else:
#                 print(type(ppt))
#                 print(ppt)

        ppt_data_arr = [np.float(ppt.replace(',', '.')) if (
            type(ppt) == str and str(ppt) != '---') else np.nan
            for ppt in df[2]]

        # create df
        df_ppt = pd.DataFrame(index=time_ix_range, data=ppt_data_arr)

        data = HDF52.get_pandas_dataframe(str(stn_id))

        df_cmn = data.loc[df_ppt.index, :]
        df_cmn.sum()
        df_ppt.sum()

        plt.scatter(df_cmn.values, df_ppt.values)
        pass
        # save df
        # df_ppt.to_csv()
    except Exception as msg:
        try:
            df = pd.read_csv(df_file, sep=';', encoding='latin-1',
                             skiprows=2, header=None)
            # create date time index
            time_ix_str = [ix0.replace('.', '-') + ' ' + ix1
                           for ix0, ix1 in zip(df[0], df[1])]

            time_ix_time_obj = pd.DatetimeIndex(time_ix_str)
            time_ix_range = pd.DatetimeIndex(
                time_ix_time_obj.strftime(date_format='%d-%m-%Y %H:%M:%S'))
            # get ppt data
            ppt_data_arr = [np.float(ppt.replace(',', '.')) if (
                type(ppt) == str and str(ppt) != '---') else np.nan
                for ppt in df[2]]

            assert len(ppt_data_arr) == len(time_ix_time_obj)

            # create df
            df_ppt = pd.DataFrame(index=time_ix_range, data=ppt_data_arr)

        except Exception as msg:
            print(msg, stn_id, df_file)
            continue
