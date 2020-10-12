
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt


# In[10]:


df_exsisting = pd.read_csv(
    r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan"
    r"\dataframe_as_HDF5_Reutlingen_Stations\data_df_23062020.csv",
    sep=';', index_col=0, engine='c', infer_datetime_format=True, parse_dates=True)


# In[18]:


start_time_ix = df_exsisting.index[0]
end_time_ix = '2020-09-18 00:00:00'

date_range = pd.date_range(start=start_time_ix, end=end_time_ix, freq='Min')

data = np.zeros(shape=(date_range.shape[0], 12))
data[data == 0] = np.nan

final_df_combined = pd.DataFrame(data=data, index=date_range,
                                 columns=[1, 2, 3, 4, 5, 6,
                                          7, 8, 9, 10, 11, 12])


# In[19]:


# append existing data to new dataframe
final_df_combined.loc[df_exsisting.index, :] = df_exsisting.values


# In[16]:
# X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\RT_Pluviodaten\f_until_230620

# get all new data from directory
all_files = glob.glob(
    r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
    r'\RT_Pluviodaten\g_until_180920_Copy\*')
assert len(all_files) > 0, 'directory seems empty'
# all_files[0]


# In[20]:


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
            time_ix_time_obj.strftime(date_format='%d-%m-%Y %H:%M:%S'))
        # get ppt data
        ppt_data_arr = [np.float(ppt.replace(',', '.')) if (
            type(ppt) == str and str(ppt) != '---') else np.nan
            for ppt in df[2]]

        assert len(ppt_data_arr) == len(time_ix_time_obj)

        # create df
        df_ppt = pd.DataFrame(index=time_ix_range, data=ppt_data_arr)
        # df_ppt.plot()
        final_df_combined.loc[df_ppt.index, stn_id] = df_ppt.values.ravel()

        # save df
        # df_ppt.to_csv()
    except Exception as msg:
        print(msg, stn_id, 'ESE')
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

            final_df_combined.loc[df_ppt.index, stn_id] = df_ppt.values.ravel()
        except Exception as msg:
            print(msg, stn_id, df_file)
            continue


# In[22]:


final_df_combined.to_csv(
    r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan"
    r"\dataframe_as_HDF5_Reutlingen_Stations"
    r"\data_df_18092020.csv",
    sep=';', float_format='%0.2f')
