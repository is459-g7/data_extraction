import json
from datetime import datetime

# Step 1: Load the JSON file
with open('airport_flight_data.json', 'r') as f:
    airport_flight_data = json.load(f)

# Step 2: Define a function to sort dates for each airport
def sort_dates(dates_list):
    # Convert the string dates into datetime objects and sort them
    return sorted(dates_list, key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

# Step 3: Sort the dates for each airport code
for airport_code, info in airport_flight_data.items():
    sorted_dates = sort_dates(info['dates'])
    # Update the 'dates' field with the sorted dates
    info['dates'] = sorted_dates

# Step 4: Save the updated JSON with sorted dates back to the file
with open('airport_flight_data_sorted.json', 'w') as f:
    json.dump(airport_flight_data, f, indent=4)

print("Dates have been sorted and saved in 'airport_flight_data_sorted.json'.")
