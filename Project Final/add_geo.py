import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Carregar les dades del CSV
file_path = '/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Project Final/Iroman_sedes_2.0_70.3.csv'  # Canvia-ho al nom real del fitxer
df = pd.read_csv(file_path)

# Configura el geolocalitzador
geolocator = Nominatim(user_agent="ironman_events_location", timeout=10)

# Funció per obtenir coordenades
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return f"{loc.latitude}, {loc.longitude}"
        else:
            return "Not Found"
    except GeocoderTimedOut:
        return "Timeout"

# Aplicar la funció a la columna de llocs
df["Coordinates"] = df["Location"].apply(get_coordinates)

# Guardar el nou CSV amb coordenades
output_file = "data_with_coordinates.csv"
df.to_csv(output_file, index=False)

print(f"Fitxer amb coordenades guardat com: {output_file}")
