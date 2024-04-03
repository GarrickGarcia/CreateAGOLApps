from arcgis.gis import GIS
import arcpy
import os

# ask user to input their AGOL username and password
username = input("Enter your ArcGIS Online username: ")
password = input("Enter your ArcGIS Online password: ")

# Establish a GIS connection
gis = GIS("https://www.arcgis.com", username, password)

# Access the hosted feature layer by its item ID
item_id = "3af9ea97c229469aa52156e20c8f1460"
item = gis.content.get(item_id)
flayers = item.layers
ftables = item.tables

# list the layers
for lyr in flayers:
    print(lyr.properties.name)
    # Check if the layer has a relationship class
    if lyr.properties.relationships:
        for rel in lyr.properties.relationships:
            print(f"Layer {lyr.properties.name} has a relationship class with related table ID {rel['relatedTableId']}.")
            print(f"Cardinality: {rel['cardinality']}")
            print(f"Primary Key Field: {rel['keyField']}")

# list the tables
for tbl in ftables:
    print(tbl.properties.name)
    # Check if the table has a relationship class
    if tbl.properties.relationships:
        for rel in tbl.properties.relationships:
            print(f"Table {tbl.properties.name} has a relationship class with related table ID {rel['relatedTableId']}.")
            print(f"Cardinality: {rel['cardinality']}")
            print(f"Primary Key Field: {rel['keyField']}")

# Store relationship info from layers
relationship_info = {}
for lyr in flayers:
    if lyr.properties.relationships:
        for rel in lyr.properties.relationships:
            relationship_info[rel['relatedTableId']] = {
                'origin_table': lyr.properties.name,
                'cardinality': rel['cardinality'],
                'origin_primary_key': rel['keyField']
            }



# create a gdb to store the downloaded data
out_folder = r"C:\Users\ggarcia\OneDrive - Abonmarche\Documents\GitHub\CreateAGOLApps\Data"
gdb_name = "DownloadedLayersTables.gdb"
arcpy.management.CreateFileGDB(out_folder, gdb_name)

# Set environment settings
arcpy.env.workspace = os.path.join(out_folder, gdb_name)
arcpy.env.maintainAttachments = True
arcpy.env.preserveGlobalIds = True

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
    # format output table name
    tbl_name = tbl.properties.name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    # Download the table as a table
    arcpy.conversion.ExportTable(tbl_url, os.path.join(out_folder, gdb_name, tbl_name))

