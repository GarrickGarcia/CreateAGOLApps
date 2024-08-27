from arcgis.gis import GIS

def get_gis_connection():
    # ask user to input their AGOL username and password
    username = input("Enter your ArcGIS Online username: ")
    password = input("Enter your ArcGIS Online password: ")

    # Establish a GIS connection
    gis = GIS("https://www.arcgis.com", username, password)
    
    return gis

if __name__ == "__main__":
    gis = get_gis_connection()
    print("Connected to: " + gis.properties.portalHostname)