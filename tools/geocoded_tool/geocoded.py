import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
import pickle
import os

# Parameters
input_file = "input_file.xlsx"
output_file = "geocoded_output.xlsx"
cache_file = "geocode_cache.pkl"

# Load data
df = pd.read_excel(input_file)

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapi")

# Load cache if exists
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        cache = pickle.load(f)
    print("Cache loaded.")
else:
    cache = {}

# Geocoding function
def get_coordinates(row):
    if pd.isna(row['CITY']) or pd.isna(row['STATE']) or pd.isna(row['COUNTRY']):
        return pd.Series([None, None])

    # Include postal code only if it's not NaN
    if not pd.isna(row['POSTAL_CODE']):
        address = f"{row['POSTAL_CODE']}, {row['CITY']}, {row['STATE']}, {row['COUNTRY']}"
    else:
        address = f"{row['CITY']}, {row['STATE']}, {row['COUNTRY']}"

    if address in cache:
        return cache[address]

    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            coords = pd.Series([location.latitude, location.longitude])
            cache[address] = coords
            sleep(1)
            return coords
        else:
            print(f"Not found: {address}")
    except Exception as e:
        print(f"Error: {address} -> {e}")
    return pd.Series([None, None])

# Add placeholder columns
df['LATITUDE'] = None
df['LONGITUDE'] = None

# Run geocoding with progress
print("Starting geocoding...")
for idx, row in df.iterrows():
    lat, lon = get_coordinates(row)
    df.at[idx, 'LATITUDE'] = lat
    df.at[idx, 'LONGITUDE'] = lon

    if idx % 100 == 0:
        print(f"Processed {idx} rows...")
        with open(cache_file, 'wb') as f:
            pickle.dump(cache, f)

# Save final results
df.to_excel(output_file, index=False)
with open(cache_file, 'wb') as f:
    pickle.dump(cache, f)

print(f"Geocoding finished! Output saved to '{output_file}'.")
