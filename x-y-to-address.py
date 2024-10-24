import pandas as pd
import requests
import json

# Read the Excel file
input_file = '10_rows_entreprise.xlsx'  # Replace with your file path
df = pd.read_excel(input_file)

# Define a function to fetch data from the API
def get_location_data(lat, lon):
    url = f'https://photon.komoot.io/reverse?lon={lon}&lat={lat}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            props = data['features'][0]['properties']
            return {
                'country': props.get('country', ''),
                'city': props.get('city', ''),
                'county': props.get('county', ''),
                'state': props.get('state', ''),
                'osm_type': props.get('osm_type', ''),
                'osm_id': props.get('osm_id', ''),
                'osm_key': props.get('osm_key', ''),
                'osm_value': props.get('osm_value', ''),
                'name': props.get('name', ''),
                'type': props.get('type', '')
            }
    return {}

# Create new columns for the desired fields from the JSON
df['country'] = ''
df['city'] = ''
df['county'] = ''
df['state'] = ''
df['osm_type'] = ''
df['osm_id'] = ''
df['osm_key'] = ''
df['osm_value'] = ''
df['name'] = ''
df['type'] = ''

# Iterate over each row in the dataframe and populate the new columns
for index, row in df.iterrows():
    lat = row['Lat']
    lon = row['Long']
    
    location_data = get_location_data(lat, lon)
    
    df.at[index, 'country'] = location_data.get('country', '')
    df.at[index, 'city'] = location_data.get('city', '')
    df.at[index, 'county'] = location_data.get('county', '')
    df.at[index, 'state'] = location_data.get('state', '')
    df.at[index, 'osm_type'] = location_data.get('osm_type', '')
    df.at[index, 'osm_id'] = location_data.get('osm_id', '')
    df.at[index, 'osm_key'] = location_data.get('osm_key', '')
    df.at[index, 'osm_value'] = location_data.get('osm_value', '')
    df.at[index, 'name'] = location_data.get('name', '')
    df.at[index, 'type'] = location_data.get('type', '')

# Write the updated dataframe back to a new Excel file
output_file = 'output_file.xlsx'  # Replace with your output file path
df.to_excel(output_file, index=False)

print(f"Data written to {output_file}")
