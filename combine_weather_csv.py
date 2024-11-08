import pandas as pd
import os

# Step 1: Load both CSVs
csv_file_1 = 'weather_data.csv'  # Replace with your actual first CSV file path
csv_file_2 = 'weather_data_1.csv'  # Replace with your actual second CSV file path

# Load both weather data files into DataFrames
df1 = pd.read_csv(csv_file_1)
df2 = pd.read_csv(csv_file_2)

# Step 2: Concatenate the two DataFrames
combined_df = pd.concat([df1, df2])

# Step 3: Drop duplicates based on 'airport_code' and 'time' if necessary
combined_df = combined_df.drop_duplicates(subset=['airport_code', 'time'], keep='first')

# Step 4: Convert 'time' to datetime format and format it to `YYYY-MM-DDTHH:MM`
combined_df['time'] = pd.to_datetime(combined_df['time'])  # Convert to datetime
combined_df['time'] = combined_df['time'].dt.strftime('%Y-%m-%dT%H:%M')  # Format to 'YYYY-MM-DDTHH:MM'

# Step 5: Save the combined DataFrame to a new CSV file
output_file = 'combined_weather_data.csv'  # Specify your output file path
combined_df.to_csv(output_file, index=False)

os.remove(csv_file_1)  # Delete the original file
os.rename(output_file, csv_file_1) 

print(f"Combined weather data saved to {csv_file_1}")
