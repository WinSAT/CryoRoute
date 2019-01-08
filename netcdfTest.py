from netCDF4 import Dataset 
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import LinearSegmentedColormap

nc = Dataset('thk_28.map.08122018_04012019.nc', mode='r')
lons = nc.variables['longitude'][:]
lats = nc.variables['latitude'][:]
data = nc.variables['thickness'][:]

nc.close()

m = Basemap(projection='npstere',boundinglat=45,lon_0=270,resolution='l')
m.drawcoastlines()
m.drawstates()
m.drawcountries()
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
#m.drawmapboundary(fill_color='aqua')
#m.bluemarble()

x,y = m(lons,lats)
clev = np.arange(11)*0.5
cmap1 = LinearSegmentedColormap.from_list("my_colormap", ((1, 1, 1), (0, 0, 0)), N=6, gamma=1.0)
cs = m.contourf(x,y,data,clev,tri=True, cmap=cmap1)
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label('m')
plt.show()
#from IPython import embed; embed()
#plt.show()

#lon,lat = np.meshgrid(lons,lats)
'''
xi,yi = m(lon,lat)

plt.show()

print "keys: ", nc.variables.keys()
'''