# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
For HOCHWASSER events, fing how was the Radolan data and PPT station data
"""

__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# ===================================================


from datetime import timedelta

import _01_intersect_radar_reutlingen as radolan_reutl

import os
import timeit
import time

import fnmatch
import shapefile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from adjustText import adjust_text

plt.style.use('fast')
plt.rcParams.update({'font.size': 16})
plt.rcParams.update({'axes.labelsize': 14})


#==============================================================================
# Data and directories
#==============================================================================
path_to_ppt_df = (r'X:\hiwi\ElHachem\Jochen'
                  r'\Reutlingen_Radolan'
                  r'\final_df_Reutlingen_.csv')


stn_locations = (r'X:\hiwi\ElHachem\Jochen'
                 r'\Reutlingen_Radolan'
                 r'\tobi_metadata_ser_copy_abbas.csv')

# path_to_radolan_data_dir = (r'X:\hiwi\ElHachem\Jochen'
#                             r'\Reutlingen_Radolan'
#                             r'\raw_data_1_event_12012019_14012019_')

path_to_radolan_data_dir = (r'X:\hiwi\ElHachem\Jochen'
                            r'\Reutlingen_Radolan'
                            r'\raw_data_2_event_23122018_14122018_')

shp_reutlingen = r'x:\exchange\seidel\tracks\RT_bbox.shp'
assert os.path.exists(shp_reutlingen), 'wrong shapefile location'

out_save_dir = (r'X:\hiwi\ElHachem\Jochen'
                r'\Reutlingen_Radolan'
                r'\results_plots')
if not os.path.exists(out_save_dir):
    os.mkdir(out_save_dir)

# counding box Reutlingen
xMin, yMin = 9.02108, 48.3714
xMax, yMax = 9.39639, 48.614

# use this for shifting Ppt data to match Radolan data
labelshift_minutes = timedelta(minutes=50)
#==============================================================================
#
#==============================================================================


def list_all_full_path(ext, file_dir):
    """
    Purpose: To return full path of files in all dirs of a 
            given folder with a
            given extension in ascending order.
    Description of the arguments:
        ext (string) = Extension of the files to list
            e.g. '.txt', '.tif'.
        file_dir (string) = Full path of the folder in which the files
            reside.
    """
    new_list = []
    patt = '*' + ext
    for root, _, files in os.walk(file_dir):
        for elm in files:
            if fnmatch.fnmatch(elm, patt):
                full_path = os.path.join(root, elm)
                new_list.append(full_path)
    return(sorted(new_list))
#==============================================================================
#
#==============================================================================


def resampleDf(data_frame, df_sep_,
               temp_freq,  temp_shift, label_shift,
               out_save_dir=None,
               fillnan=False, df_save_name=None):
    ''' sample DF based on freq and time shift and label shift '''

    df_ = data_frame.copy()
    df_res = df_.resample(temp_freq,
                          label='right',
                          closed='right',
                          loffset=label_shift,
                          base=temp_shift).sum()
    if fillnan:
        df_res.fillna(value=0, inplace=True)

    if df_save_name is not None and out_save_dir is not None:
        df_res.to_csv(os.path.join(out_save_dir, df_save_name),
                      sep=df_sep_)
    return df_res
#==============================================================================
#
#==============================================================================


def get_radolan_reutlingen_lon_lat():
    ''' this function call the first script: extract RADOLAN for Reutlingen'''

    lons, lats = radolan_reutl.tranform_radolan_coords('wgs84')

    (final_lons_idx, final_lats_idx,
     wanted_lons, wanted_lats) = radolan_reutl.extract_wanted_data(xMin,
                                                                   yMin,
                                                                   xMax,
                                                                   yMax,
                                                                   lons,
                                                                   lats)
    return (final_lons_idx, final_lats_idx, wanted_lons, wanted_lats)

#==============================================================================
#
#==============================================================================


def get_radolan_data(path_to_radolan_data, final_lons_idx, final_lats_idx):
    wanted_ppt_data, time_of_pic = radolan_reutl.read_radolanRW(
        path_to_radolan_data, final_lons_idx, final_lats_idx)

    return wanted_ppt_data, time_of_pic
#==============================================================================
#
#==============================================================================


def plot_radolan_ppt_data(wanted_lons, wanted_lats,
                          wanted_ppt_data, time_of_pic,
                          df_ppt_same_time, stn_df,
                          out_dir):
    fig, (ax0, ax1) = plt.subplots(2, 1,
                                   figsize=(20, 12),
                                   dpi=100)

    stn_colrs = ['r', 'b', 'g', 'k', 'c', 'darkgreen',
                 'maroon', 'm', 'k', 'orange', 'brown', 'navy']

    markers = ['o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd', '*']
    sf = shapefile.Reader(shp_reutlingen)

    for shape_ in sf.shapeRecords():
        x0 = np.array([i[0] for i in shape_.shape.points[:][::-1]])
        y0 = np.array([i[1] for i in shape_.shape.points[:][::-1]])
        ax0.plot(x0, y0,
                 color='r', alpha=0.65,
                 marker='+', linewidth=1,
                 label='Reutlingen')

    pm = ax0.scatter(wanted_lons, wanted_lats,
                     c=wanted_ppt_data, marker='o',
                     s=80, cmap=plt.get_cmap('viridis_r'))

    for i in range(len(markers)):
        ax0.scatter(stn_df.lon.values[i], stn_df.lat.values[i],
                    c=stn_colrs[i],
                    marker=markers[i], s=100,
                    label='Ppt stations')

        ax1.scatter(df_ppt_same_time.index[i], df_ppt_same_time.values[i],
                    c=stn_colrs[i],
                    marker=markers[i], s=100,
                    label='Station %s' % df_ppt_same_time.index[i])

    ax1.plot(df_ppt_same_time.index,
             df_ppt_same_time.values,
             c='grey', alpha=0.5)

    texts = []
    for i, txt in enumerate(df_ppt_same_time.index.values):
        texts.append(ax0.text(stn_df.lon.values[i],
                              stn_df.lat.values[i],
                              txt))
    adjust_text(texts, ax=ax0)

    texts = []
    for i, txt in enumerate(df_ppt_same_time.index.values):
        texts.append(ax1.text(df_ppt_same_time.index[i],
                              df_ppt_same_time.values[i],
                              txt))
    adjust_text(texts, ax=ax1)

    ax0.set_title('Radolan data for %s' % str(time_of_pic))

    cb = fig.colorbar(pm, shrink=0.85, ax=ax0)
    cb.set_label('Ppt (mm/h)')

    ax0.set_xlabel("Longitude")
    ax0.set_ylabel("Latitude")

    ax1.set_title('Station data for %s' % str(time_of_pic))
    ax1.set_xticks([i for i in df_ppt_same_time.index.values])
    ax1.set_ylabel("Ppt (mm/h)")

    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07),
               fancybox=True, shadow=True, ncol=5)
    time_for_save = str(time_of_pic).replace(':', '_').replace(' ', '_')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'data_for_%s_.png' % time_for_save),
                frameon=True, papertype='a4',
                bbox_inches='tight', pad_inches=.2)

    return


if __name__ == '__main__':

    print('**** Started on %s ****\n' % time.asctime())
    START = timeit.default_timer()  # get runtime of the program

    dwd_data = list_all_full_path('.gz', path_to_radolan_data_dir)

    (final_lons_idx, final_lats_idx,
        wanted_lons, wanted_lats) = get_radolan_reutlingen_lon_lat()

    in_ppt_df = pd.read_csv(path_to_ppt_df, sep=';',
                            index_col=0, parse_dates=True,
                            engine='c')
    df_hourly = resampleDf(in_ppt_df, ';', 'H', 0, labelshift_minutes)

    stn_df = pd.read_csv(stn_locations, sep=';', index_col=0)
#     stn_df.sort_values('lat', inplace=True)
    for dwd_file in dwd_data:
        wanted_ppt_data, time_of_pic = get_radolan_data(dwd_file,
                                                        final_lons_idx,
                                                        final_lats_idx)
        assert time_of_pic in df_hourly.index
        ppt_data = df_hourly.loc[time_of_pic, :]
        plot_radolan_ppt_data(wanted_lons, wanted_lats, wanted_ppt_data,
                              time_of_pic, ppt_data, stn_df, out_save_dir)
#         break

    STOP = timeit.default_timer()  # Ending time
    print(('\n****Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ***' % (time.asctime(), STOP - START)))
