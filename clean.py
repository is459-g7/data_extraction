import pandas as pd

# Step 1: Load the CSV file
weather_csv = 'weather_data.csv'  # Replace with your actual weather data file path

# Load the CSV data into a pandas DataFrame
df = pd.read_csv(weather_csv)

# Step 2: Remove rows where the 'time' column is empty or NaN
# This will drop rows where the 'time' column is empty or not a valid date
df_cleaned = df.dropna(subset=['time'])

# Step 3: Ensure the 'time' column is in the correct datetime format
# If any rows have invalid datetime formats, they will be converted to NaT (Not a Time)
df_cleaned['time'] = pd.to_datetime(df_cleaned['time'], errors='coerce')

# Step 4: Drop rows where 'time' is still NaT (after attempting to convert to datetime)
df_cleaned = df_cleaned.dropna(subset=['time'])

# Step 5: Save the cleaned DataFrame to a new CSV file
cleaned_csv = 'cleaned_weather_data.csv'  # Replace with your desired output file path
df_cleaned.to_csv(cleaned_csv, index=False)

print(f"Cleaned data saved to {cleaned_csv}")
