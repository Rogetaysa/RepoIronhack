import pandas as pd
import googlemaps

# Clau API
gmaps = googlemaps.Client(key="LA_TEVA_CLAU_API")

# Funció per obtenir coordenades
def get_coordinates_google(location):
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            loc = geocode_result[0]["geometry"]["location"]
            return f"{loc['lat']}, {loc['lng']}"
        else:
            return "Not Found"
    except Exception as e:
        return str(e)

# Afegir coordenades utilitzant Google Maps
df["Coordinates"] = df["Pais"].apply(get_coordinates_google)

# Desa el fitxer resultant
output_file = "data_with_coordinates_google.csv"
df.to_csv(output_file, index=False)

print(f"Fitxer amb coordenades guardat com: {output_file}")
