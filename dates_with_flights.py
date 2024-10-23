import pandas as pd
import json

# Step 1: Load the flights CSV and the airport code CSV
flights_df = pd.read_csv('filtered_cali_flights.csv')
airport_coords_df = pd.read_csv('airport_longlat.csv')

# Step 2: Rename columns to match pandas expectations (year, month, day)
flights_df = flights_df.rename(columns={
    'Year': 'year', 
    'Month': 'month', 
    'DayofMonth': 'day'
})

# Step 3: Combine 'year', 'month', and 'day' into a proper 'FlightDate'
flights_df['FlightDate'] = pd.to_datetime(flights_df[['year', 'month', 'day']])

# Step 4: Group the flight data by 'Origin' and collect unique flight dates for each airport
flights_grouped = flights_df.groupby('Origin')['FlightDate'].unique().reset_index()

# Step 5: Create a dictionary to store the airport information (dates and coordinates)
airport_flight_data = {}

# Iterate over the grouped flights data
for index, row in flights_grouped.iterrows():
    origin = row['Origin']
    flight_dates = row['FlightDate']

    # Match with latitude and longitude from the airport coordinates CSV
    airport_info = airport_coords_df[airport_coords_df['airport_code'] == origin]

    if not airport_info.empty:
        lat = airport_info['latitude'].values[0]
        long = airport_info['longitude'].values[0]

        # Store the data in the dictionary
        airport_flight_data[origin] = {
            "dates": flight_dates.strftime('%Y-%m-%d').tolist(),
            "latitude": lat,
            "longitude": long
        }

# Step 6: Save the dictionary as a JSON file
with open('airport_flight_data.json', 'w') as f:
    json.dump(airport_flight_data, f, indent=4)

print("Flight dates and airport coordinates have been saved to 'airport_flight_data.json'.")
