from netCDF4 import Dataset 
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import LinearSegmentedColormap
'''
nc = Dataset('thk_28.map.08122018_04012019.nc', mode='r')
nlons = nc.variables['longitude'][:]
nlats = nc.variables['latitude'][:]
ndata = nc.variables['thickness'][:]
nc.close()
'''
import geopy.distance, collections, heapq
from math import cos, asin, sqrt

Location = collections.namedtuple("Location", "lat lon iceThickness std numValues distCOG".split())
data = {}

newData = open("thk_28.map.complete.08122018_04012019.txt").read().split('\n')
data = {}
lons = []
lats = []
th = []
#startLocation = (x,y)
#endLocation = (x,y)
for idx, d in enumerate(newData[1:]):
    try:
        data[idx] = Location(*[float(i) for i in d.split(' ')])
        lons.append(data[idx].lon)
        lats.append(data[idx].lat)
        th.append(data[idx].iceThickness)
    except Exception as e: 
        print e,'Failed to store index {}: {}'.format(idx,d)

lons = np.array(lons)
lats = np.array(lats)
th   = np.array(th)
def format_coord(x, y):
    return 'x=%.4f, y=%.4f'%(m(x, y, inverse = True))

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.clickedLat = []
        self.clickedLon = []
        #self.xs = list(line.get_xdata())
        #self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
    
    def formatCord(self,x,y):
		return np.around(m(x,y,inverse=True))

    def __call__(self, event):
    	currentLon, currentLat = self.formatCord(event.xdata, event.ydata)
        self.clickedLon.append(currentLon)
        self.clickedLat.append(currentLat)
        print "clicked", self.clickedLat, self.clickedLon
        if event.inaxes!=self.line.axes: return
        #self.xs.append(event.xdata)
        #self.ys.append(event.ydata)
        #self.line.set_data(self.xs, self.ys)
        #self.line.figure.canvas.draw()

m = Basemap(projection='npstere',boundinglat=45,lon_0=270,resolution='l')
# draw parallels and meridians.
m.drawparallels(np.arange(-80.,81.,20.))
m.drawmeridians(np.arange(-180.,181.,20.))
#m.drawmapboundary(fill_color='aqua')
#m.bluemarble()

x,y = m(lons,lats)
clev = np.arange(0,5.5,0.5)
cmap1 = LinearSegmentedColormap.from_list("my_colormap", ((1, 1, 1), (0, 0, 0)), N=len(clev), gamma=1.0)
#from IPython import embed; embed()
cs = m.contourf(x,y,th,clev,tri=True, cmap=plt.cm.jet)	
cbar = m.colorbar(cs,location='bottom',pad="5%")
#m.drawstates()
m.drawcoastlines()
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
m.drawcountries()
cbar.set_label('m')
ax = plt.gca()
ax.format_coord = format_coord
line, = ax.plot([0], [0])  # empty line
linebuilder = LineBuilder(line)
plt.show()
#from IPython import embed; embed()
#plt.show()

#lon,lat = np.meshgrid(lons,lats)
'''
xi,yi = m(lon,lat)

plt.show()

print "keys: ", nc.variables.keys()
'''