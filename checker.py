import json
import pandas as pd
from datetime import datetime, timedelta

# Load your weather data and JSON
weather_csv = 'weather_data.csv'  # Replace with your actual weather data file path
json_file = 'airport_flight_data_grouped.json'  # Replace with your actual JSON file path

# Load the weather data
weather_df = pd.read_csv(weather_csv)

# Ensure the time column in the weather data is in datetime format
weather_df['time'] = pd.to_datetime(weather_df['time'], errors='coerce')

# Extract just the date from the 'time' column for comparison
weather_df['date'] = weather_df['time'].dt.date

# Load the JSON data
with open(json_file, 'r') as f:
    airport_data = json.load(f)

# Helper function to get all dates between two dates
def get_date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start
    return [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

# Step 2: Check for missing dates for each airport
missing_data = {}

for airport_code, data in airport_data.items():
    lat = data['latitude']
    lon = data['longitude']
    
    for date_range in data['date_ranges']:
        start_date = date_range['start_date']
        end_date = date_range['end_date']
        
        # Get the expected date range for this airport
        expected_dates = set(get_date_range(start_date, end_date))
        
        # Filter weather data for this airport
        airport_weather_data = weather_df[weather_df['airport_code'] == airport_code]
        
        # Get the actual unique dates for which we have weather data
        actual_dates = set(airport_weather_data['date'].astype(str).unique())  # Convert to strings
        
        # Find the missing dates
        missing_dates = expected_dates - actual_dates
        
        if missing_dates:
            # Add missing dates to the dictionary
            if airport_code not in missing_data:
                missing_data[airport_code] = {
                    'latitude': lat,
                    'longitude': lon,
                    'missing_dates': list(sorted(missing_dates))  # Sort missing dates for readability
                }

# Step 3: Save the missing dates into a new JSON file
output_file = 'missing_weather_data.json'

# Ensure dates are serialized as strings
with open(output_file, 'w') as f:
    json.dump(missing_data, f, indent=4)

print(f"Missing weather data saved to {output_file}")
