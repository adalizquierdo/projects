'''
World-wide Earthquake Watch

CIS 210 F18 Project 8-1

Author: Bernardo Izquierdo

Credits: Python: Programming in Context, textbook

Description: Use K-means cluster algorithm to visualize
earthquakes on a world map.
'''
import math
import random
import turtle

def readFile(filename):
    '''
    (string) -> Dictionary

    Uses inputed file to create a dictionary containing all
    the latitude and longitude of each earthquake in the file.
    Return this dictionary.

    >>> readFile('equake1.txt')
    {1: [123.23, -43.3], 2: [213.2, -12.53]}
    '''
    datafile = open(filename, 'r') 
    datadict = {} # Creates empty dictionary. Will be used to store lon/lat.
    key = 0       # datadict example: {1: [123.3, -6.342]}
    datafile.readline() # Skips first line of file
    for aline in datafile:
        items = aline.strip().split(',') # Removes all white spaces/creats list by spliting on ,
        key = key + 1
        lat = float(items[1]) 
        lon = float(items[2])
        datadict[key] = [lon, lat] # Adds new entry to datadict
    return datadict

def euclidD(point1, point2):
    '''
    (list, list) -> float

    Uses two inputed points with n number of coordinates,
    in the form of a list, and determines/returns the
    distance between them using euclidian algorithme

    >>> euclidD([0, 0], [0, 2])
    2.0
    >>> euclidD([2, 4], [5, 8])
    5.0
    >>> euclidD([0, 0], [0, 0])
    0.0
    '''
    total = 0
    for index in range(len(point1)):  # Set up to be able to handle multidimentional points
        diff = (point1[index] - point2[index]) ** 2 # finds difference between same n coordinate
        total = total + diff
    euclidDistance = math.sqrt(total)
    return euclidDistance

def createCentroids(k, datadict):
    '''
    (int, dictionary) -> list

    Generates k centroids by randomly picking them
    from dictionary datadict. Returns a list of the
    chosen centroids.

    >>> createCentroids(2, {1: [142.8358, -6.2147], 2: [150.7321, -60.1778]})
    [[142.8358, -6.2147], [150.7321, -60.1778]]
    >>> createCentroids(3, {1: [142.8358, -6.2147], 2: [150.7321, -60.1778], 3: [142.8469, -6.0855]})
    [[150.7321, -60.1778], [142.8358, -6.2147], [142.8469, -6.0855]]
    '''
    centroids = [] # Stores centroids in list
    centroidCount = 0
    centroidKeys = []
    while centroidCount < k: # Runs until k number of different centroids are generated
        rkey = random.randint(1, len(datadict)) 
        if rkey not in centroidKeys: # Used to make sure no centroids are repeated
            centroids.append(datadict[rkey])
            centroidKeys.append(rkey)
            centroidCount += 1 
    return centroids

def createClusters(k, centroids, datadict, repeats):
    '''
    (int, list, dictionary, int) -> list

    Creates clusters using data inputed. Calls funtion eucliD
    in the process. Returns a list of clusters.

    >>> createClusters(2, [2, 3, 4], {1: [1, 2], 2: [2, 4], 3: [1, 3]}, 4)
    <generates list of clusters>
    '''
    for apass in range(repeats): # The main for-loop that will iterate as many times as inputed
        #print('****PASS', apass, '****') 
        clusters = []
        for i in range(k): # Creates k blank clusters and stores nests them in clusters list
            clusters.append([])
        for akey in datadict: # Loops through each pair of latitude and longitude point values in datadict
            distances = []
            for clusterIndex in range(k): # Finds distances between each value in datadict and each centroid
                dist = euclidD(datadict[akey], centroids[clusterIndex])
                distances.append(dist)
            mindist = min(distances) # Finds centroid most appicable for value
            index = distances.index(mindist) # Finds index of min distance and uses it to add it to appropriate cluster
            clusters[index].append(akey)
            
        dimensions = len(datadict[1]) # Determins number coordinates that make up each value in datadict
        for clusterIndex in range(k): # Recalculation of centroids begins.
            sums = [0] * dimensions 
            for akey in clusters[clusterIndex]:
                datapoints = datadict[akey]
                for ind in range(len(datapoints)):
                    sums[ind] = sums[ind] + datapoints[ind] # Sums up all points
            for ind in range(len(sums)):
                clusterLen = len(clusters[clusterIndex]) # Finds length of each cluster
                if clusterLen != 0:
                    sums[ind] = sums[ind]/clusterLen # Calculates new cluster by finding mean of all values in cluster
            centroids[clusterIndex] = sums

        #for c in clusters:
            #print('CLUSTER')
           # for key in c:
               # print(datadict[key], end = ' ')
           # print()
    return clusters

def visualizeQuakes(k, r, datafile):
    '''
    (int, int, string) -> None

    Provides illustration of earthquakes location by first
    calling functions readFile, createCentroids, and createClusters
    to generate a data dictionary, centroids, and clusters, which
    are then fed to eqDraw to finish illustration. Returns None

    >>> visualizeQuakes(6, 10, 'equakes.txt')
    <generates turtle illustration>
    '''
    datadict = readFile(datafile) # Creates Dictionary containing lat/lon coordinates
    quakeCentroids = createCentroids(k, datadict) # Generates starting centroids
    clusters = createClusters(k, quakeCentroids, datadict, r) # Generates Clusters
    eqDraw(k, datadict, clusters) # Called eqDraw to illustrate results
    return None
    
    
def eqDraw(k, eqDict, eqClusters):
    '''
    (int, dictionary, list) -> None

    Provides illustration of earthquakes location on world map
    with longitude and latitude. Illustrates clusters assigning
    unique color to each. Returns None

    >>> eqDraw(2, {1: [141.027, 12.1145], 2: [83.3674, 30.6877]}, [[121, 321], [-32, 21]])
    <generates turtle illustration>
    '''
    quakeT = turtle.Turtle()   
    quakeWin = turtle.Screen()
    quakeWin.bgpic('worldmap1800_900.gif') # Displays image of world map on turtle window
    quakeWin.screensize(1800, 900) # Sets window size to match image dimensions
    
    wFactor = ((quakeWin.screensize()[0])/2)/180 # Calculates both Width and height factors needed to get proper illustration
    hFactor = ((quakeWin.screensize()[1])/2)/90

    quakeT.hideturtle()
    quakeT.up()

    colorlist = ['red', 'green', 'blue', 'cyan', 'black', 'yellow', 'purple', 'pink', 'white', 'violet', 'brown', 'lime green']
    quakeT.speed('fastest')

    for clusterIndex in range(k): # Goes through each cluster and maps values in unique color
        quakeT.color(colorlist[clusterIndex])
        for akey in eqClusters[clusterIndex]:
            lon = eqDict[akey][0]
            lat = eqDict[akey][1]
            quakeT.goto(lon * wFactor, lat * hFactor)
            quakeT.dot(6) 
    quakeWin.exitonclick()
    return None

def main():
    '''
    Calls and executes visualizeQuakes with given inputs.
    Returns None.
    '''
    visualizeQuakes(6, 10, 'earthquakes.txt')
    return None

main()

