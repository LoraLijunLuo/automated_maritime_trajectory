from math import *
import math
from collections import defaultdict
import datetime as dt
import time
import arcpy, os.path

def haversine(lat1, lon1, lat2, lon2):     # Defines haversine function

    R = 6367.0        # Earth's radius in meters
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = R * c
    return km

# Get the text filename
inputTxtFile = arcpy.GetParameterAsText(0)

# Read a text file
inputfile = open(inputTxtFile)

# Parses the content of one record to the line variable
line = inputfile.readline()

# Create 2 new dictionaries
shipdict = defaultdict(list)
dict = defaultdict(list)

# Get the output path of file geodatabase
FGDBpath = arcpy.GetParameterAsText(1)
# Define the name of file geodatabase
FGDBname = "FCs.gdb"

# Check if the FGDB exists. If not, create it
if not arcpy.Exists(os.path.join(FGDBpath, FGDBname)):
    arcpy.CreateFileGDB_management(FGDBpath, FGDBname)
OutputFGDB = os.path.join(FGDBpath, FGDBname)

# In ArcGIS script tools outputs from print are ignored. Use arcpy.AddMessage instead
arcpy.AddMessage("FGDB = " + OutputFGDB)
# Return FGDB path
arcpy.AddMessage("FGDBpath = " + FGDBpath)
# Return FGDB name
arcpy.AddMessage("FGDBname = " + FGDBname)

# Set workspace = OutputFGDB
arcpy.env.workspace = OutputFGDB

# Loop over records sequentially in one file
for line in inputfile:
    # Split the line
    itemlist = line.split()
    # Skip the header
    if len(itemlist) != 6:
        continue
    # Get values of time, shipID and coordinates by the List
    time = itemlist[1] + " " + itemlist[2]
    time_dt = dt.datetime.strptime(str(time), "%y-%m-%d %H:%M:%S,%f") # Format the time
    shipID = itemlist[3]
    lat,long = float(itemlist[4]),float(itemlist[5])
    coordinates = [(itemlist[4], itemlist[5])]

    # Append values to the shipdict dictionary
    shipdict[shipID].append([time_dt, float(lat), float(long)])

# Loop over shipID in shipdict dictionary to define output feature classes
for key in shipdict:
    shipl = shipdict.get(key)
    FC_name = "FC" + str(key)
    geometry_type = "POLYLINE"
    template = "#"
    has_m = "DISABLED"
    has_z = "DISABLED"
    spatial_reference = arcpy.SpatialReference(4326) # 4326 = WGS84.

    # Check if the FC exists in the FGDB. If yes, delete it
    if arcpy.Exists(os.path.join(OutputFGDB,FC_name)):
        arcpy.Delete_management(os.path.join(OutputFGDB,FC_name))

    # Create FC
    arcpy.CreateFeatureclass_management(OutputFGDB, FC_name, geometry_type, template, has_m, has_z, spatial_reference)

    # Create fields
    arcpy.AddField_management(FC_name,"Length_km", "DOUBLE")
    arcpy.AddField_management(FC_name,"Time_secs", "DOUBLE")
    arcpy.AddField_management(FC_name,"Speed_KmPerHour", "DOUBLE")

    # Open an InsertCursor to insert new geometry and attributes
    icursor = arcpy.da.InsertCursor(FC_name, ["SHAPE@","Length_km","Time_secs","Speed_KmPerHour"])

    # Loop over records in each shipID and insert length, time difference(s) and speed(km/h) to each feature class
    for i in range(0, len(shipl) - 1):
        lat1,lon1 = float(shipl[i][1]),float(shipl[i][2])
        lat2,lon2 = float(shipl[i + 1][1]),float(shipl[i + 1][2])
        length = haversine(lat1,lon1,lat2,lon2)

        time1 = shipl[i][0]
        time2 = shipl[i + 1][0]
        timediff = time2-time1
        timediff_seconds = timediff.total_seconds()

        speed = ""
        # Calculate the speed and exclude error records with the length equals to 0 and time difference equals to 0
        if float(length) == 0 or float(timediff_seconds) == 0:
            continue
        else:
            speed = float(length) / (float(timediff_seconds)/(60*60))
        # exclude records with speed above 60 km/h
        if speed >= 60.0:
            continue
        # Append values to the dict dictionary
        dict[key].append((length,timediff_seconds,speed))

        # Create a polyline geometry from two successive coordicates saved in an arcpy array. Notice that lats -> y and longs -> x
        array = arcpy.Array([arcpy.Point(lon1, lat1),arcpy.Point(lon2, lat2)])
        polylin = arcpy.Polyline(array)
        # Insert geometry (one line segment) followed by length, time and speed
        icursor.insertRow([polylin,length,timediff_seconds,speed])
    # Hint a feature class has been created
    arcpy.AddMessage(FC_name + " " + "has been created")
    # Delete cursor object
    del icursor