# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
Wenn in der er ersten und letzten Minute des Tages "0.0" (mm) 
steht und alle anderen Minuten leer d.h. ohne Werte sind,
dann hat es an diesem Tag nicht geregnet. Wenn es an dem Tag geregnet hat,
dann stehen die Daten an den entsprechenden Zeitstempeln.
  
  
Wenn in die ersten und letzte Minute des Tages leer ist,
dann ist der ganze Tag "NaN". Im Beispiel unten hätte die 8.
Station NaNs, der Rest hat 0.0mm.

2015-06-30 23:59:00;;;;;;;;;;;;
2015-07-01 00:00:00;0.0;0.0;0.0;0.0;0.0;0.0;0.0;;0.0;0.0;0.0;
2015-07-01 00:01:00;0.0;0.0;0.0;0.0;0.0;0.0;0.0;;0.0;0.0;0.0;
2015-07-01 00:02:00;;;;;;;;;;;;


"""

__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# =============================================================================
import os

import numpy as np
import pandas as pd
import math
from pathlib import Path
#==============================================================================
#
#==============================================================================

main_dir = Path(r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
                r'\dataframe_as_HDF5_Reutlingen_Stations')
os.chdir(main_dir)

# path for rainfall df, all stations
df_rainfall_file = main_dir / 'data_df_26072021_filled_missing_dates.csv'

temp_res = '1Min'
#==============================================================================
#
#==============================================================================
# read ppt df and make a copy

df_ppt = pd.read_csv(df_rainfall_file, sep=';', index_col=0,
                     parse_dates=True, infer_datetime_format=True,
                     engine='c')

df_ppt_new = df_ppt.copy(deep=True)


start_minutes = df_ppt.index[(df_ppt.index.hour == 0)
                             & (df_ppt.index.minute == 0)]
end_minutes = df_ppt.index[(df_ppt.index.hour == 23)
                           & (df_ppt.index.minute == 59)]

# keep cmn days
start_minutes_cmn = pd.DatetimeIndex(
    [strt for strt, endt in zip(start_minutes, end_minutes)
     if strt.day == endt.day])
end_minutes_cmn = pd.DatetimeIndex(
    [endt for endt in end_minutes if endt.day in start_minutes_cmn.day])

assert start_minutes_cmn.size == end_minutes_cmn.size


for ix_end, ix_start in zip(end_minutes_cmn, start_minutes_cmn):
    print(ix_end, ix_start)

    time_range_to_fill = pd.date_range(
        start=ix_start,
        end=ix_end,
        freq=temp_res)
    # get start minute
    day_to_test_start = df_ppt.loc[ix_start, :]
    day_to_test_end = df_ppt.loc[ix_end, :]
#    break

    for stn_id in day_to_test_start.index:
        val_start_day = day_to_test_start[stn_id]
        val_end_day = day_to_test_end[stn_id]
        #  break
        if (math.isnan(val_start_day)) and (math.isnan(val_end_day)):
            #print('adding nans')
            df_ppt_new.loc[
                df_ppt_new.index.intersection(time_range_to_fill), stn_id] = np.nan

        elif (not math.isnan(val_start_day)) | (not math.isnan(val_end_day)):

            cmn_idx = df_ppt_new.index.intersection(time_range_to_fill)

            values_for_that_day = df_ppt_new.loc[cmn_idx, stn_id]

            values_for_that_day_no_blank = values_for_that_day[
                values_for_that_day.values >= 0]

            if np.sum(values_for_that_day_no_blank) == 0:
                df_ppt_new.loc[cmn_idx, stn_id] = 0

            elif np.sum(values_for_that_day_no_blank) > 0:
               # print('adding zeros and vals')
                ix_to_replace = pd.DatetimeIndex(
                    [ixk for ixk in values_for_that_day.index
                        if ixk not in values_for_that_day_no_blank.index])
                df_ppt_new.loc[ix_to_replace, stn_id] = 0


# df_ppt_new
# assert df_ppt_new.sum() == df_ppt.sum()

print('Savving new DF')
# import matplotlib.pyplot as plt
# stn0 = df_ppt_new.loc[:, '1']
# stn1 = df_ppt.loc[:, '1']
# plt.ioff()
# stn0.plot(alpha=0.5)
# stn1.plot(alpha=0.5)
# plt.show()

# save df
df_ppt_new.to_csv((main_dir / 'data_df_with_zero_and_nan_values_26072021_no_missing_vals.csv'),
                  sep=';', float_format='%0.2f')

print('Done with Everything')
