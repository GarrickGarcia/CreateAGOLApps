from arcgis.gis import GIS
import arcpy
import os

# Establish a GIS connection
gis = GIS("https://www.arcgis.com", "gogarcia", "Abonmarche95!")  

# Access the hosted feature layer by its item ID
item_id = "1b7309fdb0a7470bb7efbae847f2abc3"
item = gis.content.get(item_id)
flayers = item.layers
ftables = item.tables

# list the layers
for lyr in flayers:
    print(lyr.properties.name)

# create a gdb to store the downloaded data
out_folder = r"C:\Users\ggarcia\OneDrive - Abonmarche\Documents\GitHub\CreateAGOLApps\Data"
gdb_name = "DownloadedData.gdb"
arcpy.management.CreateFileGDB(out_folder, gdb_name)

# Set environment settings
arcpy.env.workspace = os.path.join(out_folder, gdb_name)
arcpy.env.maintainAttachments = False

for lyr in flayers:
    #URL of the layer
    fl_url = lyr.url
    # format output feature class name to replace spaces with underscores and remove special characters
    fc_name = lyr.properties.name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    # Download the feature layer as a feature class
    arcpy.conversion.ExportFeatures(fl_url, os.path.join(out_folder, gdb_name, fc_name))

for tbl in ftables:
    #URL of the table
    tbl_url = tbl.url
    # output table name
    tbl_name = tbl.properties.name
    # Download the table as a table
    arcpy.conversion.ExportTable(tbl_url, os.path.join(out_folder, gdb_name, tbl_name))