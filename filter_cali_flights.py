import pandas as pd

# Step 1: Confirm the script is running
print("Starting the script...")

# Step 2: Load the CSV file into a DataFrame in chunks
file_path = r'C:/wamp64/www/BDA/bda_proj/airline.csv'
print(f"Using file path: {file_path}")  # Confirm the file path is correct

chunk_size = 10000  # Adjust chunk size based on your memory capacity

try:
    # Create an empty DataFrame to append chunks
    df_list = []
    
    # Process the CSV in chunks
    for chunk in pd.read_csv(file_path, encoding='ISO-8859-1', chunksize=chunk_size):
        ny_airports = ['LAX', 'SFO', 'SAN', 'OAK', 'SJC']
        # Filter each chunk
        filtered_chunk = chunk[(chunk['Dest'].isin(ny_airports))]
        df_list.append(filtered_chunk)
    
    # Combine all filtered chunks into a single DataFrame
    df = pd.concat(df_list)
    print("File loaded and filtered successfully")
    
except Exception as e:
    print(f"Error loading file: {e}")

# Step 3: Select the relevant columns
columns_to_keep = [
    'Year', 'Month', 'DayOfWeek', 'DayofMonth', 
    'CRSDepTime', 'CRSArrTime', 'DepTime', 'ArrTime',
    'DepDelay', 'ArrDelay', 'Distance', 'FlightNum', 
    'UniqueCarrier', 'Cancelled', 'CancellationCode', 
    'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 
    'LateAircraftDelay', 'Origin', 'Dest'
]
try:
    filtered_df = df[columns_to_keep]
    print("Relevant columns selected")
except Exception as e:
    print(f"Error selecting columns: {e}")

# Step 4: Save the filtered data to a new CSV
output_file_path = 'filtered_cali_flights.csv'
try:
    filtered_df.to_csv(output_file_path, index=False)
    print(f"Filtered data saved to {output_file_path}")
except Exception as e:
    print(f"Error saving filtered data: {e}")

# Confirm end of script
print("Script finished")
