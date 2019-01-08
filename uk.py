import geopy.distance, collections, heapq
from math import cos, asin, sqrt

Location = collections.namedtuple("Location", "lat lon iceThickness std numValues distCOG".split())
data = {}

newData = open("thk_28.map.complete.05122018_01012019.txt").read().split('\n')
data = {}
#startLocation = (x,y)
#endLocation = (x,y)
for idx, d in enumerate(newData[1:]):
    try:
        data[idx] = Location(*[float(i) for i in d.split(' ')])
    except: 
        print 'Failed to store index {}: {}'.format(idx,d)

def coorDistance(start, end):
    return geopy.distance.distance(start,end).km

def closestIndex(data, target):
    return min(data.values(), key=lambda p: coorDistance((target[0], target[1]),(p.lat, p.lon)))

from IPython import embed; embed()

def calcH(start, end):
    #calculates distance between two lat,lng pairs
    coords_1 = (data[start].latitude, data[start].longitude)
    coords_2 = (data[end].latitude, data[end].longitude)
    distance = (geopy.distance.vincenty(coords_1, coords_2)).km
    return distance

def getneighbors(startlocation, n=10):
    return sorted(data.values(), key=lambda x: calcH(startlocation, x.ID))[1:n+1]

def getParent(closedlist, index):
    path = []
    while index is not None:
        path.append(index)
        index = closedlist.get(index, None)
    return [data[i] for i in path[::-1]]

startIndex = 25479 # Hessle
endIndex = 8262 # Leeds

Node = collections.namedtuple("Node", "ID F G H parentID".split())

h = calcH(startIndex, endIndex)
openlist = [(h, Node(startIndex, h, 0, h, None))] # heap
closedlist = {} # map visited nodes to parent

while len(openlist) >= 1:
    _, currentLocation = heapq.heappop(openlist)
    print(currentLocation)

    if currentLocation.ID in closedlist:
        continue
    closedlist[currentLocation.ID] = currentLocation.parentID

    if currentLocation.ID == endIndex:
        print("Complete")
        for p in getParent(closedlist, currentLocation.ID):
            print(p)
        break

    for other in getneighbors(currentLocation.ID):
        g = currentLocation.G + calcH(currentLocation.ID, other.ID)
        h = calcH(other.ID, endIndex)
        f = g + h
        heapq.heappush(openlist, (f, Node(other.ID, f, g, h, currentLocation.ID)))