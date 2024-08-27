from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import datetime
import zipfile
import os

class GISUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.gis = self.login()

    def login(self):
        return GIS("https://www.arcgis.com", self.username, self.password)

class LayerViewCreator:
    def __init__(self, gis_user, item_id, include_attachments):
        self.gis = gis_user.gis
        self.item_id = item_id
        self.include_attachments = include_attachments
        self.view = self.create_view()

    def create_view(self):
        fl = self.gis.content.get(self.item_id)
        flc = FeatureLayerCollection.fromitem(fl)
        now = datetime.datetime.now()
        view_name = "TempExportView_" + now.strftime("%Y%m%d_%H%M%S")
        view = flc.manager.create_view(name=view_name)
        view_flc = FeatureLayerCollection.fromitem(view)
        view_flc.manager.update_definition({'capabilities': 'Query, Extract'})

        if not self.include_attachments:
            for lyr in view.layers + view.tables:
                if hasattr(lyr, 'properties') and getattr(lyr.properties, 'hasAttachments', False):
                    lyr.manager.update_definition({'hasAttachments': False})

        return view

class LayerExporter:
    def __init__(self, view):
        self.view = view

    def export_and_download(self, export_path, export_name=None):
        if export_name is None:
            export_name = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        export = self.view.export(export_name, "File Geodatabase")
        file_name = export_name + ".zip"
        export.download(export_path, file_name)
        
        # Unzip and cleanup
        with zipfile.ZipFile(os.path.join(export_path, file_name), 'r') as zip_ref:
            zip_ref.extractall(export_path)
            extracted_name = zip_ref.namelist()[0].split('/')[0]  # Assume first file in zip is the gdb
        os.rename(os.path.join(export_path, extracted_name), os.path.join(export_path, export_name + ".gdb"))
        os.remove(os.path.join(export_path, file_name))
        self.view.delete()
        export.delete()

# main usage
if __name__ == "__main__":
    user = GISUser('your_username', 'your_password')
    view_creator = LayerViewCreator(user, 'item_id_here', include_attachments=False)
    exporter = LayerExporter(view_creator.view)
    exporter.export_and_download('/path/to/your/download/folder')
