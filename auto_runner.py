import os
import pandas as pd
import json
import time
import subprocess

def check_empty_csv(file_path):
    """Check if the CSV file has no rows."""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.empty
    return True  # If file doesn't exist, consider it empty

def check_empty_json(file_path):
    """Check if the JSON file has no data."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return not bool(data)  # Returns True if data is empty
    return True  # If file doesn't exist, consider it empty

def run_script(script_path):
    """Run a Python script and wait for it to finish."""
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    print(result.stdout)  # Optionally print script output
    if result.stderr:
        print(f"Error in {script_path}:\n{result.stderr}")
    time.sleep(2)  # Optional delay between scripts

def main():
    # Paths to the scripts and files
    scripts = [
        'extract_weather.py',
        'combine_weather_csv.py',
        'checker.py',
        'flight_date_grouper.py'
    ]
    weather_data_1 = 'weather_data_1.csv'
    missing_weather_json = 'missing_weather_data_grouped.json'

    # Continuously run the scripts in the specified order until stopping condition is met
    while True:
        for script in scripts:
            run_script(script)
        
        # Check conditions after each full cycle of the four scripts
        if check_empty_csv(weather_data_1) or check_empty_json(missing_weather_json):
            print("Stopping conditions met. Exiting loop.")
            break

# Run the main function
if __name__ == "__main__":
    main()
