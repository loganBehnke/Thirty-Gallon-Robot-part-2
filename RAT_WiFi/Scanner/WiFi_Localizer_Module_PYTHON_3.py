import math as m
import csv
import WiFi_Scanning_Module as wifi

routerDict = {}
# routerDict will be in the following format:
# { macAddr : (freq, name, signalLvl, channel)}

dist = {}
# dist will the in the following format:
# { macAddr : distance }

routerCoordinates = {}
# routerCoordinates will be in the following format:
# { macAddr : (X, Y) }

maxY = 100
maxX = 100
minY = 0
minX = 0

interList = []

def main():
    # run wifi scan
    fileName = wifi.runScan()

    # open csv file of recieved routers & signal strenghts
    readSignalStr(fileName)
    get_distances()
    remove_FSPL_outliers()
    print(dist)
    
    # open csv file of router coordinates
#    readCoordinates()
#    print(routerCoordinates)

#    # triangulate position
#    find_intersections()
#    remove_inter_outliers()
#    mid = calculate_midpoint()
#    print(mid)
    pass

def readSignalStr(fileName):
    # read in signal strengths with mac addresses
    # use the file format that George uses, and read into routerDict
    with open (fileName, newline='') as csvfile:
        routerReader = csv.reader(csvfile, delimiter=",")
        headers = next(routerReader)
        for row in routerReader:
            macAddr = row[3]
            if macAddr not in routerDict:
                name = row[1]
                if name != "NAU" and name != "NAU Guest":
                    continue
                else:
                    routerDict[macAddr] = (row[0], row[1], row[2], row[4])
            else:
                continue

def readCoordinates():
    # iterate through routerDict and known map to get coordinate points for
    # each router pinged.
        # read in signal strengths with mac addresses
    # use the file format that George uses, and read into routerDict
    with open ('routerlist2.csv', newline='') as csvfile:
        mapReader = csv.reader(csvfile, delimiter=",")
        headers = next(mapReader)
        for row in mapReader:
            macAddr = row[2]
            if macAddr not in routerCoordinates:
                routerCoordinates[macAddr] = (row[0], row[1])
            else:
                continue

def get_distances():
    # distance = 10 ** ((FSPL - K - (20 * m.log(f)))/20)
    # iterate through routerDict to get distances
    K = -27.55
    # Rxs will be recieved signal strength
    # Txp will be Transmitter power
    # test value: 16dB
    Txp = 16
    # Txa will be Transmitter antenna gain
    # test value: 2dBi
    Txa = 2
    # Rxa will be Reciever antenna gain
    # test value: 0dB
    Rxa = 0
    # FM will be the fade margin
    # test value: 20dB
    FM = 20
    # f will be the frequency
    for router in routerDict:
        Rxs = int(routerDict[router][2])
        f = int(float(routerDict[router][0]) * 1000)
        FSPL = Txp + Txa + Rxa - Rxs - FM
        freq = m.log(f, 10)
        freq = 20 * freq
        power = FSPL - K - freq
        power = power / 20
        distance = 10 ** power
        dist[router] = distance
    # add distance and macAddress key to dist dictionary
    

def find_intersections():
    # iterate through the coordinates dictionary
    for P1 in routerCoordinates:
        P1coord = routerCoordinates[P1]
        # iterate through the coordinates dictionary again
        for P2 in routerCoordinates:
            P2coord = routerCoordinates[P2]
            # distance = sqrt((y2-y1)^2 + (x2-x1)^2)
            d = m.sqrt(((P2coord[1] - P1coord[1])**2) + ((P2coord[0] - P1coord[0])**2))

            #if d > r1+r2, no intersections
            #if d < |r1-r2| no solutions
            #if d = 0 and r1=r2, same circle => infinite solutions
            if( d > (dist[P1] + dist[P2]) ):
                continue
            elif( d < abs(dist[P1] - dist[P2]) ):
                continue
            elif( d == 0 and dist[P1] == dist[P2] ):
                continue
            else:
                # calculate a
                a = (d**2 - dist[P2]**2 + dist[P1]**2)/(2 * d)
                
                # calculate h from a
                h = m.sqrt((dist[P1]**2) - (a**2))
                
                # calculate x3 and y3
                x3 = P1coord[0] + a(P2coord[0] - P1coord[0])/d
                y3 = P1coord[1] + a(P2coord[1] - P1coord[1])/d

                # calculate x4 and y4 using +-h
                x4 = x3 - h(P2coord[1] - P1coord[1])/d
                y4 = y3 - h(P2coord[0] - P1coord[0])/d

                intersection = (x4, y4)

                interlist.append(intersection)

                x4 = x3 + h(P2coord[1] - P1coord[1])/d
                y4 = y3 + h(P2coord[0] - P1coord[0])/d

                intersection = (x4, y4)

                interlist.append(intersection)

def remove_inter_outliers():
    # if any X or Y exceeds maxX or maxY or is <minX or minY,
    # remove it from the intersection list
    # max and min values set temporarily to 100 and 0 respectively
    for section in interlist:
        if(section[0] > maxX or section[0] < minX):
            interlist.remove(section)
        elif(section[1] > maxY or section[1] < minY):
            interlist.remove(section)

def remove_FSPL_outliers():
    removeList = []
    for d in dist:
        if dist[d] >= 100:
            removeList.append(d)
    for item in removeList:
        del(dist[item])

def calculate_midpoint():
    # use weighted average for midpoint calculation
    # data point * weight / # of points
    # for both x and y
    sumX = 0
    sumY = 0
    for section in interlist:
        sumX = sumX + section[0]
        sumY = sumY + section[1]
    avgX = sumX/len(interlist)
    avgY = sumY/len(interlist)
    midpoint = (avgX, avgY)
    return midpoint

main()
