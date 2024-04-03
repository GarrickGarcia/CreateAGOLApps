from AGOLLogin import get_gis_connection
from CreateView import create_view
import datetime
import zipfile
import os

def export_view(view, export_name):
    return view.export(export_name, "File Geodatabase")

def download_file(export, path, file_name):
    return export.download(path, file_name)

def unzip_file(path, file_name):
    with zipfile.ZipFile(path + "\\" + file_name, 'r') as zip_ref:
        zip_ref.extractall(path)
        return zip_ref.namelist()[0].split('/')[0]  # get the name of the geodatabase

def rename_file(path, old_name, new_name):
    os.rename(os.path.join(path, old_name), os.path.join(path, new_name))

def delete_files(path, file_name, view, export):
    os.remove(path + "\\" + file_name)
    view.delete()
    export.delete()

def main(item_id, include_attachments, path):
    gis = get_gis_connection()
    view = create_view(gis, item_id, include_attachments)
    export_name = "Export_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export = export_view(view, export_name)
    file_name = export_name + ".zip"
    download_file(export, path, file_name)
    extracted_file_name = unzip_file(path, file_name)
    new_file_name = export_name + ".gdb"
    rename_file(path, extracted_file_name, new_file_name)
    delete_files(path, file_name, view, export)

if __name__ == "__main__":
    item_id = "3af9ea97c229469aa52156e20c8f1460"
    include_attachments = True
    path = r"C:\Users\ggarcia\OneDrive - Abonmarche\Documents\GitHub\CreateAGOLApps\Data"
    main(item_id, include_attachments, path)