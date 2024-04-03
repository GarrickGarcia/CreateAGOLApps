from AGOLLogin import get_gis_connection

gis = get_gis_connection()

# Access the hosted feature layer by its item ID
item_id = "3af9ea97c229469aa52156e20c8f1460"
item = gis.content.get(item_id)

# list the layers
flayers = item.layers
ftables = item.tables
for lyr in flayers:
    print(lyr.properties.name)
for tbl in ftables:
    print(tbl.properties.name)