from AGOLLogin import get_gis_connection
from arcgis.features import FeatureLayerCollection
import datetime

def create_view(item_id, include_attachments):
    gis = get_gis_connection()

    # Access the hosted feature layer by its item ID
    fl = gis.content.get(item_id)
    flc = FeatureLayerCollection.fromitem(fl)

    # create a view layer with current timestamp
    now = datetime.datetime.now()
    view_name = "TempExportView_" + now.strftime("%Y%m%d_%H%M%S")
    view = flc.manager.create_view(name=view_name)
    view_flc = FeatureLayerCollection.fromitem(view)

    # enable data export
    view_flc.manager.update_definition({'capabilities': 'Query, Extract'})

    # Check if the variable is set to False
    if not include_attachments:
        # for layers with attachments disable attachment visibilty
        for lyr in view.layers:
            if lyr.properties.hasAttachments:
                lyr.manager.update_definition({'hasAttachments': False})

        # for tables with attachments disable attachment visibilty
        for tbl in view.tables:
            if tbl.properties.hasAttachments:
                tbl.manager.update_definition({'hasAttachments': False})

    return view

if __name__ == "__main__":
    item_id = "3af9ea97c229469aa52156e20c8f1460"
    include_attachments = False
    view = create_view(item_id, include_attachments)
