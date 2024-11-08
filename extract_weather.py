import dask
import pandas as pd
import requests
from dask import delayed
import json
import time

# Step 1: Load the grouped dates JSON file with latitude and longitude
with open('missing_weather_data_grouped.json', 'r') as f:
    flight_dates_json = json.load(f)

# Step 2: Define the API query function for Open-Meteo
def fetch_weather_data(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': 'temperature_2m,relative_humidity_2m,dew_point_2m,precipitation,snow_depth,pressure_msl,surface_pressure,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
        'timezone': 'America/Los_Angeles'  # Adjust based on your region
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for ({lat}, {lon}) from {start_date} to {end_date}: {e}")
        return None

# Step 3: Define a delayed function that will process each airport and its date ranges
@delayed
def process_airport_weather(airport_code, lat, lon, date_ranges):
    all_weather_rows = []
    
    # Loop over each group of consecutive date ranges
    for date_range in date_ranges:
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        print(f"Fetching weather data for {airport_code} ({lat}, {lon}) from {start_date} to {end_date}...")

        # Add delay between requests to avoid hitting API limits
        time.sleep(45)  # Pause for 30 seconds between each request

        # Fetch weather data for the current date range
        weather_data = fetch_weather_data(lat, lon, start_date, end_date)
        
        if weather_data:
            hourly_data = weather_data.get('hourly', {})
            
            # Combine hourly data into a list of dicts for each timestamp
            for i in range(len(hourly_data.get('time', []))):
                weather_row = {
                    'airport_code': airport_code,
                    'time': hourly_data['time'][i],
                    'temperature_2m': hourly_data['temperature_2m'][i],
                    'relative_humidity_2m': hourly_data['relative_humidity_2m'][i],
                    'dew_point_2m': hourly_data['dew_point_2m'][i],
                    'precipitation': hourly_data['precipitation'][i],
                    'snow_depth': hourly_data['snow_depth'][i],
                    'pressure_msl': hourly_data['pressure_msl'][i],
                    'surface_pressure': hourly_data['surface_pressure'][i],
                    'cloud_cover': hourly_data['cloud_cover'][i],
                    'wind_speed_10m': hourly_data['wind_speed_10m'][i],
                    'wind_direction_10m': hourly_data['wind_direction_10m'][i],
                    'wind_gusts_10m': hourly_data['wind_gusts_10m'][i],
                }
                all_weather_rows.append(weather_row)
    
    return all_weather_rows

# Step 4: Prepare to query weather data for each airport and its date ranges
tasks = []
for airport_code, airport_info in flight_dates_json.items():
    lat = airport_info['latitude']
    lon = airport_info['longitude']
    date_ranges = airport_info['date_ranges']
    
    # Add a task to process weather data for this airport and its date ranges
    tasks.append(process_airport_weather(airport_code, lat, lon, date_ranges))

# Step 5: Use Dask to compute the weather data for all airports in parallel
# This will return a list of lists, where each inner list contains weather data rows for one airport
results = dask.compute(*tasks)

# Step 6: Flatten the list of lists into a single list of weather data rows
weather_data_list = [item for sublist in results for item in sublist]  # Flatten the list

# Step 7: Convert the list of weather data into a DataFrame
weather_df = pd.DataFrame(weather_data_list)

# Step 8: Save the weather data to a CSV file
output_file_path = 'weather_data_1.csv'
weather_df.to_csv(output_file_path, index=False)
print(f"Weather data saved to {output_file_path}")
