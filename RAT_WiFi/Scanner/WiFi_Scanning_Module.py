#!/usr/bin/env python
"""
This is a module dedicated to providing router identification by scanning
surrouding routers. 

Written in Python 2
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
__version__ = "1.05"
__maintainer__ = "George Cadel-Munoz"
__email__ = "gec68@nau.edu"
__status__ = "Prototype"



def displayReq(an_interface_list, strengthReq, verboseFlag = False):
    """
    Displays all scanned connections and routers in currently
    scanned list. Separators added for readability.

    Args:
        ''an_interface_list'' (A list of strings): A network interface scan list.

        ''strengthReq'' (An integer): A minimum required signal strength.

        ''verboseFlag'' (A boolean): An optional verbose command.

    Returns:
        A formatted string of the interface list with required router information.

    """
    returnStr = ""
    for router in an_interface_list:
        router['Signal Level'] = abs(int(router['Signal Level']))
        ##### Replace this if statement below to enable ALL signal searching
        #if((router['Name'] == "NAU" or router['Name'] == "NAU Guest") and router['Signal Level'] >= strengthReq):
        if(router['Signal Level'] >= strengthReq):
            router['Signal Level'] = str(router['Signal Level'])
            if(verboseFlag):
                print "\n================="
            for cell in router:
                if (cell == "Frequency" or cell == "Signal Level" or
                    cell == "Name" or cell == "Channel" or cell == "Address"):
                    returnStr = returnStr + router[cell] + ","
                    if(verboseFlag):
                        printCells(cell, router[cell])
            if(verboseFlag):
                print "================\n"
    return returnStr



def printCells(cellTitle, cellValue):
    """
    Prints a cell found in a router list

    Args:
        ''cellTitle'' (A string): The title of the cell in the router list

        ''cellValue'' (A string): The value of the cell in the router list

    Returns:
        None.
    """
    print "{}: {}".format(cellTitle, cellValue)
    


def stringToList(a_list_of_strings, max_list_size):
    """
    Format a string and creates a list of routers used to be written
    to a CSV file.

    Args:
        ''a_list_of_strings'' (A List of strings): A string with values separated by
            a deliminator (in this case, a comma for creating CSV files).

        ''max_list_size'' (an integer): The total amount of items to be written to a 
            single row in the CSV file.

    Returns:
        A 2-dimensional list of lists. Each list within the list is to be written
        to a single row.
    """
    working_list = a_list_of_strings.split(",")
    working_list.pop()
    inner_list = []
    final_list = []
    while (len(working_list) > 0):
        while(len(inner_list) < max_list_size):
            inner_list.append(working_list[0])
            working_list.pop(0)
        final_list.append(inner_list)
        inner_list = []
    return final_list


def writeToFile( aTwoDimensionList, filePath, headerFlag = True):
    """
    Generates a CSV file given a 2-dimensional list.

    Args:
        ''aTwoDimensionList'' (A 2D list): Each individual list within
            the the list contains information of each row to be written
            into the CSV file.
        ''filePath'' (A string): A directory for the file to be written to.
        ''headerFlag'' (A boolean): A boolean to enable row header creation.

    Returns:
        None
    """
    with open(filePath, "wb") as csvfile:
        wr = csv.writer(csvfile, quoting = csv.QUOTE_MINIMAL)
        if(headerFlag):
            wr.writerow(["Frequency", "Name", "Signal Level", "Address", "Channel"])
        for aList in aTwoDimensionList:
            wr.writerow(aList)
    csvfile.close()


def runScan(retryCounter = 0):
    """
    Runs a scan for obtaining router information such as IP and MAC addresses.
    Uses all methods to create a CSV file with obtained user requirements.
    NOTE: In order to run this program, you must:
        1. Call This file in terminal
        2. Use flags to set up program (add the flag '--help' or '-h' for additional information)
    
    Args:
        ''retryCounter'' (An integer): Used for recursive function calling.

    Raises:
        Exception: After 3 failed scan attemps, the program will stop.
        TypeError: If the signal limit flag is not specified with an integer value.
        ValueError: If the integer value is not specified within 0 - 100.

    Returns:
        A string of the file name.
    """
    # Initiliaze Parser and Commands
    parser = argparse.ArgumentParser(description = 'A WiFi Scanner parser used for file configurations')
    parser.add_argument("--fileName", type = str, required = True, help = "Used to name the output CSV file (Required)")
    parser.add_argument("--sigLimit", type = int, default = 50, help = "Minimum signal strength requested (i.e. 50, 72, 90). Default = 50")
    parser.add_argument("--verbose", action = "store_true", help = "Displays router info in the terminal")
    args = parser.parse_args()

    # Test for appropriate signal variable
    if(type(args.sigLimit) != int):
        raise TypeError("The signal requirement must be an integer value")
    if(args.sigLimit < 0 or args.sigLimit > 100):
        raise ValueError("The signal requirement must be between 0 and 100, inclusive.")

    # Initialize Variables
    interface = 'wlp2s0'
    fileName = os.getcwd() + '/' + args.fileName + '.csv'
    stringList = []
    routerList = []
    refreshRate = 2 # Will wait this long (sec) before scanning again
    minRequiredRouters = 3 # How many routers do we need minimum?
    defaultListLength = 5
    routerListLen = len(routerList)

    # Stop running program after 3 attempts
    if(retryCounter > 3):
        raise Exception("Failed after 3 attempts")
    
    # Start Scans until fulfilled minimum router requirements
    print("Scanning, please wait...")
    while(routerListLen < minRequiredRouters):
        routerList = working_interface.get_interfaces(interface)
        routerListLen = len(routerList)
        time.sleep(refreshRate)
    print("\nScan completed")

    # Organize Data into lists and strings
    stringList = displayReq(routerList, args.sigLimit, args.verbose)
    routerList = stringToList(stringList, defaultListLength)

    # Write to CSV file
    writeToFile(routerList, fileName)

    # Check for appropriate data in CSV file
    try:
        with open(fileName, "r") as outputCSV:
            outputReader = csv.reader(outputCSV, delimiter = ',')
            outputCount = -1 # Negative 1 for row header
            if(args.verbose):
                print("Found these rows in the file:")
            for row in outputReader:
                if(args.verbose):
                    print(row)
                outputCount += 1
            # Run operation again
            if(outputCount < minRequiredRouters):
                retryCounter += 1
                print("FAILED {} time(s)...".format(retryCounter))
                runScan(retryCounter)

    except:
        if(retryCounter > 3):
            print "Failed to find enough routers"
        else:
            print "This file does not exist"
    # Return file name
    return fileName

    

    
'''
 Old Methods, Used for testing
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
'''


runScan()

