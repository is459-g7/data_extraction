import pandas as pd
import json

# Step 1: Load the weather data CSV
weather_csv = 'weather_data.csv'  # Replace with your actual weather data file path
weather_df = pd.read_csv(weather_csv)

# Extract the unique airport codes from the weather CSV
weather_airports = set(weather_df['airport_code'].unique())

# Step 2: Load the missing weather data JSON
json_file = 'missing_weather_data_grouped.json'  # Replace with your actual JSON file path

with open(json_file, 'r') as f:
    missing_weather_data = json.load(f)

# Extract the airport codes from the JSON
missing_weather_airports = set(missing_weather_data.keys())

# Step 3: Find the common airport codes between both datasets
common_airports = weather_airports.intersection(missing_weather_airports)

# Step 4: Print the common airport codes
if common_airports:
    print(f"Airport codes present in both the weather CSV and missing weather JSON: {common_airports}")
else:
    print("No common airport codes found between the weather CSV and missing weather JSON.")
