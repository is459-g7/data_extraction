import json
from datetime import datetime, timedelta

# Step 1: Load the JSON file
with open('airport_flight_data_sorted.json', 'r') as f:
    airport_flight_data = json.load(f)

# Step 2: Define a function to group consecutive dates
def group_dates(dates_list):
    grouped_dates = []
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates_list]
    
    # Initialize the first range
    start_date = dates[0]
    end_date = dates[0]
    
    # Loop through the sorted dates to group them
    for i in range(1, len(dates)):
        # Check if the next date is consecutive (1 day apart)
        if dates[i] == end_date + timedelta(days=1):
            # If consecutive, update the end date
            end_date = dates[i]
        else:
            # If not consecutive, save the current range and start a new one
            grouped_dates.append({
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d")
            })
            # Start a new range
            start_date = dates[i]
            end_date = dates[i]
    
    # Add the final range
    grouped_dates.append({
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d")
    })
    
    return grouped_dates

# Step 3: Group the dates for each airport code
for airport_code, info in airport_flight_data.items():
    grouped_date_ranges = group_dates(info['dates'])
    # Replace the 'dates' list with grouped date ranges
    info['date_ranges'] = grouped_date_ranges
    # Remove the original 'dates' key
    del info['dates']

# Step 4: Save the updated JSON with grouped date ranges
with open('airport_flight_data_grouped.json', 'w') as f:
    json.dump(airport_flight_data, f, indent=4)

print("Dates have been grouped into consecutive ranges and saved in 'airport_flight_data_grouped.json'.")
