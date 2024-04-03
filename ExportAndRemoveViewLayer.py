from CreateView import create_view
import datetime

item_id = "3af9ea97c229469aa52156e20c8f1460"
include_attachments = False
view = create_view(item_id, include_attachments)

export_name = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Export the view to a file geodatabase
export = view.export(export_name, "File Geodatabase")

#download the exported file
path = r"C:\Users\ggarcia\OneDrive - Abonmarche\Documents\GitHub\CreateAGOLApps\Data"
export.download(path, export_name)