from AGOLLogin import get_gis_connection
from arcgis.features import FeatureLayerCollection

gis = get_gis_connection()

# Access the hosted feature layer by its item ID
item_id = "3af9ea97c229469aa52156e20c8f1460"
fl = gis.content.get(item_id)
flc = FeatureLayerCollection.fromitem(fl)

# create a view layer
view_name = "TempExportView"
view = flc.manager.create_view(name=view_name)

# list the layers
for lyr in view.layers:
    print(lyr.properties.name)
for tbl in view.tables:
    print(tbl.properties.name)

# identify layers and tables with attachments
lyr_attachments = [lyr.properties.name for lyr in view.layers if lyr.properties.hasAttachments]
tbl_attachments = [tbl.properties.name for tbl in view.tables if tbl.properties.hasAttachments]
print(f"Layers with attachments: {lyr_attachments}")
print(f"Tables with attachments: {tbl_attachments}")

# for layers with attachments disable attachment visibilty
for lyr in view.layers:
    if lyr.properties.hasAttachments:
        lyr.manager.update_definition({'hasAttachments': False})

# for tables with attachments disable attachment visibilty
for tbl in view.tables:
    if tbl.properties.hasAttachments:
        tbl.manager.update_definition({'hasAttachments': False})