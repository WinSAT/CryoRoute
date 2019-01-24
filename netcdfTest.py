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

Location = collections.namedtuple("Location", "ID lat lon iceThickness std numValues distCOG".split())
data = {}

#newData = open("thk_2018_11.map.txt").read().split('\n')
newData = open("thk_28.map.complete.08122018_04012019.txt").read().split('\n')
data = {}
indexDict = {}
lons = []
lats = []
th = []
pp1 = [-36.119341, 83.663903]
pp2 = [126.539772, 75.653207]
#startLocation = (x,y)
#endLocation = (x,y)
for idx, d in enumerate(newData[1:]):
    try:
    	#if idx % 200 == 0 or float(d.split()[1])==pp1[0] or float(d.split()[1])==pp2[0]:
        data[idx] = Location(*[idx]+[round(float(i),4) for i in d.split()])
        lons.append(data[idx].lon)
        lats.append(data[idx].lat)
        indexDict[tuple(np.around([data[idx].lon,data[idx].lat],4))] = idx
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
        self.p1 = np.around([-36.119341, 83.663903],4) #lon lat
        self.p2 = np.around([126.539772, 75.653207],4)
        self.startIndex = indexDict[tuple(self.p1)]
        self.endIndex = indexDict[tuple(self.p2)]
        pc1 = m(*self.p1)
        pc2 = m(*self.p2)
        self.xs = [pc1[0],pc2[0]]#list(line.get_xdata())
        self.ys = [pc1[1],pc2[1]]#list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        #self.line.set_data(self.xs, self.ys)
        #self.line.set_color('red')
        #self.line.figure.canvas.draw()
        #self.calcPath()
    
    def formatCord(self,lon,lat):
		return m(lon,lat,inverse=True)

    def __call__(self, event):
    	currentLon, currentLat = self.formatCord(event.xdata, event.ydata)
        self.clickedLon.append(currentLon)
        self.clickedLat.append(currentLat)
        print "clicked", currentLat, currentLon, m(currentLon,currentLat)
        #from IPython import embed; embed()
        #print checkValidPos(currentLat,currentLon)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        #self.line.set_data(self.xs, self.ys)
        #self.line.figure.canvas.draw()
    def drawLine(self,lineLats,lineLons):
    	self.line.set_data(lineLats,lineLons)
    	#self.line.figure.canvas.draw()

    def calcH(self, start, end):
    	coords_1 = (data[start].lat, data[start].lon)
    	coords_2 = (data[end].lat, data[end].lon)
    	return (geopy.distance.vincenty(coords_1, coords_2)).km*(1+data[end].iceThickness)

    def getNeigh(self, startlocation, n=10):
    	return sorted(data.values(), key=lambda x: self.calcH(startlocation, x.ID))[1:n+1]

    def getParent(self, closedlist, index):
	    path = []
	    while index is not None:
	        path.append(index)
	        index = closedlist.get(index, None)
	    return [data[i] for i in path[::-1]]

    def calcPath(self):
    	Node = collections.namedtuple("Node", "ID F G H parentID".split())
    	h = self.calcH(self.startIndex, self.endIndex)
    	openlist = [(h, Node(self.startIndex, h, 0, h, None))] # heap
    	closedlist = {} # map visited nodes to parent
    	while len(openlist) >= 1:
    		_, currentLocation = heapq.heappop(openlist)
    		print(currentLocation)
    		if currentLocation.ID in closedlist:
    			continue
    			closedlist[currentLocation.ID] = currentLocation.parentID

    		if currentLocation.ID == self.endIndex:
    			print("Complete")
    			for p in self.getParent(closedlist, currentLocation.ID):
    				print(p)
    			break

    		for other in self.getNeigh(currentLocation.ID):
    			g = currentLocation.G + self.calcH(currentLocation.ID, other.ID)
    			h = self.calcH(other.ID, self.endIndex)
    			f = g + h
    			heapq.heappush(openlist, (f, Node(other.ID, f, g, h, currentLocation.ID)))


m = Basemap(projection='npstere',boundinglat=45,lon_0=270,resolution='h')
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
cbar.set_label('Sea Ice Thickness (m)')
ax = plt.gca()
ax.format_coord = format_coord
line, = ax.plot([0], [0])  # empty line
#linebuilder = LineBuilder(line)
plt.show()
#from IPython import embed; embed()
#plt.show()

#lon,lat = np.meshgrid(lons,lats)
'''
xi,yi = m(lon,lat)

plt.show()

print "keys: ", nc.variables.keys()
'''