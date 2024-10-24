import pandas as pd

# Step 1: Load both CSVs
weather_data_1 = 'weather_data.csv'  # Replace with your actual file path
weather_data_2 = 'weather_data_no_seconds.csv'  # Replace with your actual file path

# Load both weather data files
df1 = pd.read_csv(weather_data_1)
df2 = pd.read_csv(weather_data_2)

# Step 2: Concatenate the two DataFrames
combined_df = pd.concat([df1, df2])

# Step 3: Drop duplicates based on 'airport_code' and 'time'
# If there's a possibility of exact duplicate rows, we can use 'keep=first' or 'keep=last' to specify which to keep.
combined_df = combined_df.drop_duplicates(subset=['airport_code', 'time'], keep='first')

# Step 4: Ensure the 'time' column is parsed correctly using 'infer_datetime_format'
combined_df['time'] = pd.to_datetime(combined_df['time'], errors='coerce')

# Step 5: Sort by 'airport_code' and 'time'
combined_df = combined_df.sort_values(by=['airport_code', 'time'])

# Step 6: Save the combined DataFrame to a new CSV
output_file = 'combined_weather_data.csv'  # Replace with your desired output file path
combined_df.to_csv(output_file, index=False)

print(f"Combined weather data saved to {output_file}")
