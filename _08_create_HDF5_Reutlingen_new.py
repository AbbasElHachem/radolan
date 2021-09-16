# !/usr/bin/env python.
# -*- coding: utf-8 -*-

"""
Name:    create_hdf5.py
Purpose: 
Created on: 02.03.2020
Abbas EL Hachem 
IWS UNI STUTTGART
"""


# ==============================================================================
# import
# ==============================================================================
import os
import numpy as np
import pandas as pd
#import glob
import tables
#import fiona
#import shapely.geometry as sh_geo
import pyproj
import matplotlib.pyplot as plt
#from _00_functions import convert_coords_fr_wgs84_to_utm32_

#os.environ["PYTHONIOENCODING"] = "latin-1"
# ==============================================================================
# settings
# ==============================================================================
# folder, where all the station data is saved in

main_dir = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
            r'\dataframe_as_HDF5_Reutlingen_Stations')
os.chdir(main_dir)

# path for rainfall df, all stations
df_rainfall_file = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
                    r'\dataframe_as_HDF5_Reutlingen_Stations'
                    r'\data_df_with_zero_and_nan_values_26072021.csv')
# path to coordinates df
ppt_coords = (r"X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\RT_Pluviodaten"
              r"\tobi_metadata_ser.csv")

# select time period and temporal resolution
start_dt = '2014-05-01 00:00'
end_dt = '2021-07-26 00:00'

freq = '1min'
# TODO: add resample frequency as a parameter

df_ppt = pd.read_csv(df_rainfall_file, sep=';', index_col=0,
                     engine='c')
df_ppt.index = pd.to_datetime(df_ppt.index, format='%Y-%m-%d %H:%M')
df_ppt = df_ppt.asfreq(freq='1Min')
# select region or state, else region = False


# ==============================================================================


def convert_coords_fr_wgs84_to_utm32_(epgs_initial_str, epsg_final_str,
                                      first_coord, second_coord):
    """
    Purpose: Convert points from one reference system to a second
    --------
        In our case the function is used to transform WGS84 to UTM32
        (or vice versa), for transforming the DWD and Netatmo station
        coordinates to same reference system.

        Used for calculating the distance matrix between stations

    Keyword argument:
    -----------------
        epsg_initial_str: EPSG code as string for initial reference system
        epsg_final_str: EPSG code as string for final reference system
        first_coord: numpy array of X or Longitude coordinates
        second_coord: numpy array of Y or Latitude coordinates

    Returns:
    -------
        x, y: two numpy arrays containing the transformed coordinates in 
        the final coordinates system
    """
    initial_epsg = pyproj.Proj(epgs_initial_str)
    final_epsg = pyproj.Proj(epsg_final_str)
    x, y = pyproj.transform(initial_epsg, final_epsg,
                            first_coord, second_coord)
    return x, y
# ==============================================================================
# get number of station files
#nstats = len(glob.glob(os.path.join(database, '*.csv'))) - 1


metadata = pd.read_csv(ppt_coords, sep=';', index_col=0)


# get number of station files
nstats = metadata.shape[0]
print(nstats)
# initilize timeseries
dates = pd.date_range(start_dt, end_dt, freq=freq)
blank_df = pd.DataFrame(index=dates)  # , data=np.zeros(dates.shape))


hdf5_path = os.path.join('Reutlingen_pluvios_new.h5')

if not os.path.isfile(hdf5_path):
    # number of maximum timesteps
    nts_max = dates.shape[0]

    hf = tables.open_file(hdf5_path, 'w', filters=tables.Filters(complevel=6))

    # timestamps
    hf.create_group(where=hf.root,
                    name='timestamps',
                    title='Timestamps of respective Aggregation as Start Time')
    hf.create_carray(where=hf.root.timestamps,
                     name='isoformat',
                     atom=tables.StringAtom(19),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Strings of Timestamps in Isoformat')
    hf.create_carray(where=hf.root.timestamps,
                     name='year',
                     atom=tables.IntAtom(),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Yearly Timestamps')
    hf.create_carray(where=hf.root.timestamps,
                     name='month',
                     atom=tables.IntAtom(),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Monthly Timestamps')
    hf.create_carray(where=hf.root.timestamps,
                     name='day',
                     atom=tables.IntAtom(),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Daily Timestamps')
    hf.create_carray(where=hf.root.timestamps,
                     name='yday',
                     atom=tables.IntAtom(),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Yearday Timestamps')
    hf.create_carray(where=hf.root.timestamps,
                     name='hour',
                     atom=tables.IntAtom(),
                     shape=(nts_max,),
                     chunkshape=(10000,),
                     title='Hourly Timestamps')
    hf.create_carray(where=hf.root.timestamps,
                     name='start_idx',
                     atom=tables.Time64Atom(),
                     shape=(nstats,),
                     title='First Index of the Timeseries')
    hf.create_carray(where=hf.root.timestamps,
                     name='end_idx',
                     atom=tables.Time64Atom(),
                     shape=(nstats,),
                     title='Last Index of the Timeseries')

    # data
    hf.create_carray(where=hf.root,
                     name='data',
                     atom=tables.FloatAtom(dflt=np.nan),
                     shape=(nts_max, nstats),
                     chunkshape=(10000, 1),
                     title='Reutlingen Pluvios %s' % freq)

    # coordinates
    hf.create_group(where=hf.root,
                    name='coord',
                    title='stations coordiantes')
    hf.create_carray(where=hf.root.coord,
                     name='lon',
                     atom=tables.FloatAtom(dflt=np.nan),
                     shape=(nstats,),
                     title='Longitude (Decimal Degree WGS84)')
    hf.create_carray(where=hf.root.coord,
                     name='lat',
                     atom=tables.FloatAtom(dflt=np.nan),
                     shape=(nstats,),
                     title='Latitude (Decimal Degree WGS84)')
    hf.create_carray(where=hf.root.coord,
                     name='northing',
                     atom=tables.FloatAtom(dflt=np.nan),
                     shape=(nstats,),
                     title='Northing (ETRS89/UTM32) [m]')
    hf.create_carray(where=hf.root.coord,
                     name='easting',
                     atom=tables.FloatAtom(dflt=np.nan),
                     shape=(nstats,),
                     title='Easting (ETRS89/UTM32) [m]')

    # metadata
    hf.create_carray(where=hf.root,
                     name='name',
                     atom=tables.StringAtom(50),
                     shape=(nstats,),
                     title='Name of Station')

    # convert timestamp to isoformat
    ts_iso = []
    ts_year = []
    ts_month = []
    ts_day = []
    ts_yday = []
    ts_hour = []

    for ii in range(dates.shape[0]):
        ts = dates[ii]
        ts_iso.append(ts.isoformat())
        # get timestamp years
        ts_year.append(ts.year)
        # get timestamp months
        ts_month.append(ts.month)
        # get timestamp days
        ts_day.append(ts.day)
        # get timestamp year days
        ts_yday.append(ts.timetuple().tm_yday)
        # hours
        ts_hour.append(ts.hour)
    # fill hf5 with predefined stamps
    hf.root.timestamps.isoformat[:] = ts_iso[:]
    hf.root.timestamps.year[:] = ts_year[:]
    hf.root.timestamps.month[:] = ts_month[:]
    hf.root.timestamps.day[:] = ts_day[:]
    hf.root.timestamps.yday[:] = ts_yday[:]
    hf.root.timestamps.hour[:] = ts_hour[:]
    hf.close()

# write station data
hf = tables.open_file(hdf5_path, 'r+')
i_station = 0


df_coords = pd.read_csv(ppt_coords, sep=';', index_col=0)
# lons_float = [np.float(_v.replace(',', '.')) for _v in df_coords['lon'].values]
# lats_float = [np.float(_v.replace(',', '.')) for _v in df_coords['lat'].values]

lons_float = df_coords['lon'].values
lats_float = df_coords['lat'].values
for i_idx, stn_name in enumerate(df_ppt.columns):

    stationname = stn_name
    print('{} / {}: {}'.format(i_idx + 1, metadata.shape[0], stationname))

    stn_mac = stationname  # .replace('_', ':')

    # netatmo_stn_70_ee_50_02_cc_f2
#     temp_station = pd.read_csv(
#         os.path.join(database, 'netatmo_{}_{}_(({})).csv'.format(
#             os.path.basename(file_path).split('_')[1],  # freq
#             os.path.basename(file_path).split('_')[2],
#             stn_mac)), sep=';', index_col=0, engine='c')
    temp_station = df_ppt.loc[:, stn_name]

    assert not temp_station.index.duplicated().any(), 'still duplicates in DF'
    try:
        start_idx = temp_station.index[0]
        end_idx = temp_station.index[-1]
    except Exception as msg:
        print('Error with start-end index', msg)
    print(np.nansum(temp_station.values))
    # if temp_station.index.freq
    hf.root.data[:, i_idx] = blank_df.join(temp_station).values.flatten()
    hf.root.coord.lon[i_idx] = metadata['lon'].loc[int(stn_mac)]
    hf.root.coord.lat[i_idx] = metadata['lat'].loc[int(stn_mac)]
    #hf.root.coord.z[i_idx] = metadata['elev'].loc[stn_mac]

    etrs89 = convert_coords_fr_wgs84_to_utm32_(
        '+init=epsg:4326', '+init=epsg:25832',
        metadata['lon'].loc[int(stn_mac)],
        metadata['lat'].loc[int(stn_mac)])

    hf.root.coord.northing[i_idx] = etrs89[1]  # metadata['northing'].values
    hf.root.coord.easting[i_idx] = etrs89[0]  # metadata['easting'].values
    hf.root.name[i_idx] = np.string_(stationname)

    hf.root.timestamps.start_idx[i_station] = np.datetime64(start_idx)
    hf.root.timestamps.end_idx[i_station] = np.datetime64(end_idx)
    # hf.root.name[i_station] = np.string_(stationname)

    # hf.root.name[i_idx] = np.string_(stationname)
    i_station += 1

    plt.ioff()
    plt.figure(figsize=(12, 8))
    plt.plot(temp_station.index, temp_station.values)
    plt.savefig(r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\dataframe_as_HDF5_Reutlingen_Stations\%s.png'
                % stationname)
    plt.close()

hf.close()
