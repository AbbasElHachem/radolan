# !/usr/bin/env python.
# -*- coding: utf-8 -*-
'''
Script to read RADOLAN RW Products for all of Germany

Extract from the data the coordinates and precipitation
Data of a city defined by it'S bounding box (coordinates)
Plot the results (longitude, Latitude, Rainfall (mm/h))

'''

__author__ = "Abbas El Hachem"
__copyright__ = 'Institut fuer Wasser- und Umweltsystemmodellierung - IWS'
__email__ = "abbas.el-hachem@iws.uni-stuttgart.de"

# =============================================================================

from osgeo import osr

import os
import time
import timeit

import shapefile
import numpy as np
import wradlib as wrl
import matplotlib.pyplot as plt


test_ftn = False

#==============================================================================
# Radolan file
#==============================================================================
fpath = (r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan'
         r'\raw_data_1_event_12012019_14012019_'
         r'\raa01-rw_10000-1901132350-dwd---bin.gz')
assert os.path.exists(fpath), 'wrong radolan file location'

# =============================================================================
# Bounding Box REUTLINGEN
# =============================================================================
shp_reutlingen = r'x:\exchange\seidel\tracks\RT_bbox.shp'
assert os.path.exists(shp_reutlingen), 'wrong shapefile location'

xMin, yMin = 9.02108, 48.3714
xMax, yMax = 9.39639, 48.614

#==============================================================================
# Transform Radolan Coords to WGS84 or Gauss Krieger 3
#==============================================================================


def tranform_radolan_coords(wanted_out_coor_syst='wgs84'):
    '''
    create the necessary Spatial Reference Objects for
    the RADOLAN-projection and wgs84.

    Then, we call reproject with the osr-objects as projection_source
    and projection_target parameters.
    '''
    print('Transforming Radolan Coordinates to same system as Shapefile')
    radolan_grid_xy = wrl.georef.get_radolan_grid(900, 900)

    # transform radolan polar stereographic projection to wgs84 and then to gk3

    if wanted_out_coor_syst == 'wgs84':
        proj_stereo = wrl.georef.create_osr("dwd-radolan")  # orig coords sys
        proj_wgs = osr.SpatialReference()
        proj_wgs.ImportFromEPSG(4326)
        # extract converted WGS84 coordinates
        radolan_grid_ll = wrl.georef.reproject(radolan_grid_xy,
                                               projection_source=proj_stereo,
                                               projection_target=proj_wgs)
        lons = radolan_grid_ll[:, :, 0]
        lats = radolan_grid_ll[:, :, 1]
    if wanted_out_coor_syst == 'gk3':
        # create Gauss Krueger zone 3 projection osr object
        proj_gk3 = osr.SpatialReference()
        proj_gk3.ImportFromEPSG(31467)
        # extract converted KausGrieger coordinates
        radolan_grid_gk = wrl.georef.reproject(radolan_grid_ll,
                                               projection_source=proj_wgs,
                                               projection_target=proj_gk3)
        lons = radolan_grid_gk[:, :, 0]
        lats = radolan_grid_gk[:, :, 1]
    print('Done transforming Radolan Coordinates to same system as Shapefile')
    return lons, lats


#==============================================================================
# Extract the coordinates of the shapefile that fall in Radolan Grid
#==============================================================================

def extract_wanted_data(xMin, yMin, xMax, yMax,
                        radar_lons, radar_lats,
                        buffer=0.025):
    ''' funtion to get coordinates that intersect radar and shpfile'''
    # extract coordinates that lay within the shapefile of Reutlingen
    print('Getting Coordinates and their Indices')
    wanted_lons = radar_lons[(xMin - buffer < radar_lons) &
                             (radar_lons < xMax + buffer) &
                             (yMin - buffer < radar_lats) &
                             (radar_lats < yMax + buffer)]

    wanted_lats = radar_lats[(xMin - buffer < radar_lons) &
                             (radar_lons < xMax + buffer)
                             & (yMin - buffer < radar_lats) &
                             (radar_lats < yMax + buffer)]

    # get the indices of these coordinates
    lons_idx = np.where(np.isin(radar_lons, wanted_lons))
    lats_idx = np.where(np.isin(radar_lats, wanted_lats))
    assert lons_idx[0].all() == lats_idx[0].all()  # assert are same
    assert lons_idx[1].all() == lats_idx[1].all()
    final_lons_idx, final_lats_idx = lons_idx[0], lons_idx[1]
    print('Done getting Coordinates and their Indices')
    return final_lons_idx, final_lats_idx, wanted_lons, wanted_lats


#==============================================================================
# Read Radolan File and extract the PPT values that are in the Shapefile
#==============================================================================


def read_radolanRW(radolan_fpath,
                   wanted_coords_lon_idx,
                   wanted_coords_lats_idx):
    data, metadata = wrl.io.read_radolan_composite(radolan_fpath)
    maskeddata = np.ma.masked_equal(data, metadata["nodataflag"])
    print('Shape of radolan data is: ', data.shape)
    print('Metadata in Radolan file is: ', metadata.keys())
    print('Time of Radolan file is: ', metadata['datetime'])
    # extract corresponding Radolan data
    wanted_ppt_data = maskeddata[wanted_coords_lon_idx, wanted_coords_lats_idx]
    print('Done getting wanted Radolan data section')
    return wanted_ppt_data, metadata['datetime']


#==============================================================================
# PLOT RADOLAN and Reutlingen Shapefile
#==============================================================================

def plot_ppt_Radolan_in_shpfile(extracted_lons,
                                extracted_lats,
                                extracted_ppt_data,
                                time_of_pic,
                                shapefile_path):
    print('Plotting extracted Radolan data and coordinates')
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, aspect='equal')
    # # ax.scatter(lons, lats, alpha=0.25, c='grey')
    # # pm = ax.pcolormesh(lons, lats, maskeddata, cmap='viridis')

    # plot shapefile Reutlingen
    sf = shapefile.Reader(shapefile_path)
    for shape_ in sf.shapeRecords():
        x0 = np.array([i[0] for i in shape_.shape.points[:][::-1]])
        y0 = np.array([i[1] for i in shape_.shape.points[:][::-1]])
        ax.plot(x0, y0,
                color='r', alpha=0.65,
                marker='+', linewidth=1,
                label='Reutlingen')

    pm = ax.scatter(extracted_lons, extracted_lats,
                    c=extracted_ppt_data, marker='o',
                    s=120, cmap=plt.get_cmap('viridis_r'))
    plt.title(time_of_pic)
    cb = fig.colorbar(pm, shrink=0.85)
    cb.set_label('Ppt (mm/h)')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.show()
    return


if __name__ == '__main__':
    start = time.asctime()
    start_time = timeit.default_timer()
    print('Program started at: ', start)

    if test_ftn:
        lons, lats = tranform_radolan_coords('wgs84')

        (final_lons_idx, final_lats_idx,
         wanted_lons, wanted_lats) = extract_wanted_data(xMin, yMin,
                                                         xMax, yMax,
                                                         lons, lats)
        wanted_ppt_data, time_of_pic = read_radolanRW(fpath,
                                                      final_lons_idx,
                                                      final_lats_idx)

        plot_ppt_Radolan_in_shpfile(wanted_lons,
                                    wanted_lats,
                                    wanted_ppt_data,
                                    time_of_pic,
                                    shp_reutlingen)

    end = time.asctime()
    end_time = timeit.default_timer()
    print('Program ended at: ', end,
          'Runtime was: %.2f s' % (end_time - start_time))
