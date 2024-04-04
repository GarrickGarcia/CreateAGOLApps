from AGOLLogin import get_gis_connection
from CreateView import create_view
import datetime

def export_view(view, export_name):
    export = view.export(export_name, "File Geodatabase")
    return export

def publish_gdb(gdb, name):
    # Define publish parameters
    publish_parameters = {"name": name}

    # Publish the geodatabase
    published_item = gdb.publish(publish_parameters)

    return published_item

def delete_files(view, export):
    view.delete()
    export.delete()

def republish_layer(item_id, include_attachments):
    gis = get_gis_connection()
    view = create_view(gis, item_id, include_attachments)
    export_name = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export = export_view(view, export_name)
    republished_layer = publish_gdb(export, export_name)
    return republished_layer

if __name__ == "__main__":
    item_id = "3af9ea97c229469aa52156e20c8f1460"
    include_attachments = True
    republish_layer(item_id, include_attachments)