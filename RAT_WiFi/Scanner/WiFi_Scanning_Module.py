#!/usr/bin/env python
"""
This is a module dedicated to providing router identification by scanning
surrouding routers. 
"""

# Imports
import iw_parse as working_interface
import csv
import time as time
import getmac
import argparse
import os


########## Info ###########
__author__ = "George Cadel-Munoz"
__credits__ = ["George Cadel-Munoz"]
__version__ = "0.9"
__maintainer__ = "George Cadel-Munoz"
__email__ = "gec68@nau.edu"
__status__ = "Prototype"



def displayReq(an_interface_list, strenghReq):
    """
    Displays all scanned connections and routers in currently
    scanned list. 
    Separators added for readability.
    """
    #print "Length of interface list: {}".format(len(an_interface_list))
    returnStr = ""
    for router in an_interface_list:
        router['Signal Level'] = abs(int(router['Signal Level']))
        if((router['Name'] == "NAU" or router['Name'] == "NAU Guest") and router['Signal Level'] >= strenghReq):
            router['Signal Level'] = str(router['Signal Level'])
            print "\n================="
            #print "Signal Strength: {}\nRequired: {}\n".format(router["Signal Level"], strenghReq)
            for cell in router:
                if (cell == "Frequency" or cell == "Signal Level" or
                    cell == "Name" or cell == "Channel" or cell == "Address"):
                    print "{}: {}".format(cell, router[cell])
                    returnStr = returnStr + router[cell] + ","
                #print "{}: {}".format(cell, router[cell])
            print "================\n"
    return returnStr


def displayAll(an_interface_list):
    """
    Displays all scanned connections and routers in currently
    scanned list. 
    Separators added for readability.
    """
    #print "Length of interface list: {}".format(len(an_interface_list))
    returnStr = ""
    for router in an_interface_list:
        print "\n================="
        for cell in router:
            #if cell == "Address"
            print "{}: {}".format(cell, router[cell])
            returnStr = returnStr + router[cell] + ","
            #print "{}: {}".format(cell, router[cell])
        print "================\n"
    return returnStr


def stringToList(a_list_of_strings, max_list_size):
    working_list = a_list_of_strings.split(",")
    working_list.pop()
    inner_list = []
    final_list = []
    while (len(working_list) > 0):
        while(len(inner_list) < max_list_size):
            #inner_list.append(" ")
            inner_list.append(working_list[0])
            working_list.pop(0)
        final_list.append(inner_list)
        inner_list = []
    return final_list


def writeToFile( aTwoDimensionList, filePath, headerFlag = True):
    with open(filePath, "wb") as csvfile:
        wr = csv.writer(csvfile, quoting = csv.QUOTE_MINIMAL)
        if(headerFlag):
            wr.writerow(["Frequency", "Name", "Signal Level", "Address", "Channel"])
        for aList in aTwoDimensionList:
            wr.writerow(aList)
    csvfile.close()


def runScan():
    # Initiliaze Parser and Commands
    parser = argparse.ArgumentParser(description = 'A WiFi Scanner parser used for file configurations')
    parser.add_argument("--fileName", type = str, required = True, help = "Used to name the output CSV file (Required)")
    parser.add_argument("--sigLimit", type = int, default = 50, help = "Minimum signal strength requested (i.e. 50, 72, 90). Default = 50")
    args = parser.parse_args()

    # Initialize Variables
    interface = 'wlp2s0'
    fileName = os.getcwd() + '/' + args.fileName + '.csv'
    stringList = []
    routerList = []
    refreshRate = 2 # Will wait this long (sec) before scanning again
    minRequiredRouters = 3 # How many routers do we need minimum?
    defaultListLength = 5
    routerListLen = len(routerList)
    
    # Start Scans until fulfilled minimum router requirements
    print("Scanning, please wait...")
    while(routerListLen < minRequiredRouters):
        routerList = working_interface.get_interfaces(interface)
        routerListLen = len(routerList)
        time.sleep(refreshRate)
    print("\nScan completed")

    # Organize Data into lists and strings
    stringList = displayReq(routerList, args.sigLimit)
    routerList = stringToList(stringList, defaultListLength)

    # Write to CSV file
    writeToFile(routerList, fileName)

    #print(stringList)
    

    
    

def getCSV():
    ### Constants ###
    interface = 'wlp2s0' # Network scanning device
    running_iter = 1 # Starting scan iteraction counter
    total_iter = 1 # Total scan interations
    refresh_rate = 1 # Delay between each scan in seconds
    minimum_router_list = 3 # The minimum amount of routers scanned
    interface_list = [] # Initial list of the interface list
    raw_string_list = [] # List of string lists
    default_list_length = 5 # Capture 4 items in the raw string list
    default_file_path = None
    default_csv_header_flag = True # Will add a header to the CSV file if true

    testvar = 0

    # To compare results to information obtained from the 
    # computer itself, run the following command in the 
    # ubuntu terminal:
    #     watch -n1 iwconfig
    # NOTE: This command shows the user what router and network is connected to
    while(running_iter <= total_iter ):
        # Collect connected router information
        # Show current iteration
        while(len(interface_list) < minimum_router_list and testvar < 3):
            print "Length of interface list: {}".format(len(interface_list))
            interface_list = working_interface.call_iwlist(interface).split()
            print "Length of interface list: {}".format(len(interface_list))
            testvar += 1
        # Pretty printing
        print "\n\n><><><><><><><><><><><><><><><"
        print "><><><>< Iteration {}  ><><><><".format(running_iter)
        print "><><><><><><><><><><><><><><><\n"
        new_list = working_interface.get_interfaces(interface)
        print(len(new_list))

        # Display All Routers
        rawDataString = displayReq(new_list)
        finalList = stringToList(rawDataString, default_list_length)

        # Write info to CSV file
        writeToFile(finalList, default_file_path, default_csv_header_flag)
        time.sleep(refresh_rate)
        running_iter += 1
        
        
    
    
    print "\n\nScanning terminated...\n\n" 

#getCSV()
runScan()

#if __name__ == "__main__":
    #main()