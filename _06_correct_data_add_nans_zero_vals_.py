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
df_rainfall_file = main_dir / 'data_df.csv'

temp_res = '1Min'
#==============================================================================
#
#==============================================================================
# read ppt df and make a copy

df_ppt = pd.read_csv(df_rainfall_file, sep=';', index_col=0,
                     parse_dates=True, infer_datetime_format=True,
                     engine='c')

df_ppt_new = df_ppt.copy(deep=True)


imp_days = df_ppt.index[(df_ppt.index.hour == 0) &
                        ((df_ppt.index.minute == 0) |
                            (df_ppt.index.minute == 1))]

df_with_start_end_days = df_ppt.loc[df_ppt.index.intersection(
    imp_days), :]


for ix_end, ix_start in zip(df_with_start_end_days.index[::2],
                            df_with_start_end_days.index[1::2]):
    print(ix_end, ix_start)
    # get start minute
    day_to_test_start = df_with_start_end_days.loc[ix_start, :]
    day_to_test_end = df_with_start_end_days.loc[ix_end, :]

    # make sure it is same day
    assert ((day_to_test_start.name.year == day_to_test_end.name.year)
            and (day_to_test_start.name.month == day_to_test_end.name.month)
            and (day_to_test_start.name.day == day_to_test_end.name.day)
            and (day_to_test_start.name.hour == day_to_test_end.name.hour)
            and (day_to_test_start.name.minute == 1)
            and (day_to_test_end.name.minute == 0))

    for stn_id in day_to_test_start.index:
        val_start_day = day_to_test_start[stn_id]
        val_end_day = day_to_test_end[stn_id]

        if (val_start_day == 0) and (val_end_day == 0):

            time_range_zeros = pd.date_range(
                start=day_to_test_end.name,
                end=day_to_test_end.name + pd.Timedelta(minutes=1439),
                freq=temp_res)

            cmn_idx = df_ppt_new.index.intersection(time_range_zeros)

            values_for_that_day = df_ppt_new.loc[cmn_idx, stn_id]

            values_for_that_day_no_blank = values_for_that_day[
                values_for_that_day.values >= 0]

            if np.sum(values_for_that_day_no_blank) == 0:
                df_ppt_new.loc[cmn_idx, stn_id] = 0

            elif np.sum(values_for_that_day_no_blank) > 0:
                ix_to_replace = pd.DatetimeIndex(
                    [ixk for ixk in values_for_that_day.index
                        if ixk not in values_for_that_day_no_blank.index])
                df_ppt_new.loc[ix_to_replace, stn_id] = 0

        if (math.isnan(val_start_day)) and (math.isnan(val_end_day)):
            time_range_nans = pd.date_range(
                start=day_to_test_end.name,
                end=day_to_test_end.name + pd.Timedelta(minutes=1439),
                freq=temp_res)
            df_ppt_new.loc[
                df_ppt_new.index.intersection(time_range_nans), stn_id] = np.nan
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
df_ppt_new.to_csv((main_dir / 'data_df_with_zero_and_nan_values.csv'),
                  sep=';')

print('Done with Everything')
