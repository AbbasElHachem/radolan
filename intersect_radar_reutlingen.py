from osgeo import osr

import numpy as np
import wradlib as wrl
import matplotlib.pyplot as plt

import shapefile
import os
import warnings
warnings.filterwarnings('ignore')

# radolan file
fpath = r'X:\hiwi\ElHachem\Jochen\Reutlingen_Radolan\raa01-rw_10000-1904021450-dwd---bin.gz'
assert os.path.exists(fpath), 'wrong radolan file location'

# =============================================================================
# Bounding Box REUTLINGEN
# =============================================================================
xMin, yMin = 9.02108, 48.3714
xMax, yMax = 9.39639, 48.614
shp_reutlingen = r'x:\exchange\seidel\tracks\RT_bbox.shp'
assert os.path.exists(shp_reutlingen), 'wrong shapefile location'
sf = shapefile.Reader(shp_reutlingen)

#==============================================================================
# Read RADOLAN FILE
#==============================================================================
data, metadata = wrl.io.read_radolan_composite(fpath)
maskeddata = np.ma.masked_equal(data, metadata["nodataflag"])
print(data.shape)
print(metadata.keys())

# create the necessary Spatial Reference Objects for
# the RADOLAN-projection and wgs84.
proj_stereo = wrl.georef.create_osr("dwd-radolan")
proj_wgs = osr.SpatialReference()
proj_wgs.ImportFromEPSG(4326)

# create Gauss Krueger zone 3 projection osr object
proj_gk3 = osr.SpatialReference()
proj_gk3.ImportFromEPSG(31467)

# Then, we call reproject with the osr-objects as projection_source
# and projection_target parameters.
radolan_grid_xy = wrl.georef.get_radolan_grid(900, 900)
radolan_grid_ll = wrl.georef.reproject(radolan_grid_xy,
                                       projection_source=proj_stereo,
                                       projection_target=proj_wgs)


# transform radolan polar stereographic projection to wgs84 and then to gk3
radolan_grid_ll = wrl.georef.reproject(radolan_grid_xy,
                                       projection_source=proj_stereo,
                                       projection_target=proj_wgs)
radolan_grid_gk = wrl.georef.reproject(radolan_grid_ll,
                                       projection_source=proj_wgs,
                                       projection_target=proj_gk3)

# extract converted coordinates
lons = radolan_grid_ll[:, :, 0]
lats = radolan_grid_ll[:, :, 1]

#==============================================================================
# PLOT RADOLAN and Reutlingen
#==============================================================================
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, aspect='equal')

pm = ax.pcolormesh(lons, lats, maskeddata, cmap='viridis')
cb = fig.colorbar(pm, shrink=0.85)
cb.set_label('Radolan data')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# plot shapefile Reutlingen
for shape_ in sf.shapeRecords():
    x0 = [i[0] for i in shape_.shape.points[:][::-1]]
    y0 = [i[1] for i in shape_.shape.points[:][::-1]]
    ax.plot(x0, y0,
            color='r', alpha=0.65,
            marker='+', linewidth=1,
            label='Reutlingen')
plt.show()
