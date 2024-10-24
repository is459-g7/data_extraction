import pandas as pd

# Load the weather CSV data
weather_csv = 'weather_data_1.csv'  # Replace with your actual weather data file path

# Load the CSV into a DataFrame
weather_df = pd.read_csv(weather_csv)

# Step 1: Convert 'time' column to datetime, ensuring any seconds are included
weather_df['time'] = pd.to_datetime(weather_df['time'], errors='coerce')

# Step 2: Remove the seconds by formatting the 'time' column to only keep up to minutes
weather_df['time'] = weather_df['time'].dt.strftime('%Y-%m-%dT%H:%M')

# Step 3: Save the updated DataFrame back to a CSV without seconds in the 'time' column
output_file = 'weather_data_no_seconds.csv'  # Replace with desired output file path
weather_df.to_csv(output_file, index=False)

print(f"Updated CSV saved to {output_file}")

