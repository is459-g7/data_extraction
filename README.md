# Data Extraction and Weather Data Integration Project

This project automates the extraction, transformation, and integration of weather data for flight records, specifically aligning weather conditions for each flight’s origin and destination airports based on the date and time of the flight.

## Project Structure

### Files

- **`auto_runner.py`**: Main script that orchestrates the data processing pipeline. It runs the necessary steps in order until all required weather data has been fetched and integrated.
- **`extract_weather.py`**: Extracts hourly weather data from a remote API for specific airports and date ranges. It checks the `missing_weather_data_grouped.json` file for any airports and dates needing data and retrieves it in batches.
- **`combine_weather_csv.py`**: Combines newly extracted weather data with existing weather data into a single CSV file, removing duplicates and ensuring chronological order.
- **`checker.py`**: Validates that all required weather data is available for each airport and date in the missing data JSON file. If data is missing, it triggers further extraction.
- **`flight_date_grouper.py`**: Groups dates for which weather data is required, organizing them by airport for efficient API querying.
- **`missing_weather_data_grouped.json`**: Contains the airports and date ranges for which weather data is missing or needed.

### Data Files

- **`latest_weather_data.csv`**: CSV containing structured weather data aligned with each flight’s date and time. Data includes temperature, humidity, precipitation, wind conditions, etc.
- **`wea.csv`**: Intermediate or final CSV file containing weather data fetched from the weather API.

## Workflow

1. **Data Extraction**: Run the `auto_runner.py` script to initiate the data extraction process. The script performs the following steps in a loop until all missing weather data is extracted:
    - Checks for missing data using `checker.py`.
    - Runs `extract_weather.py` to fetch missing data.
    - Combines the new data with the existing data using `combine_weather_csv.py`.
    - Updates missing data records as resolved.

2. **Weather Data Grouping**: `flight_date_grouper.py` organizes the list of dates and airports needing weather data, ensuring efficient API calls.

3. **Data Integration**: The integrated weather data is formatted to match the schema required for your analysis or database ingestion.

4. **Error Handling**: Each script logs any issues during execution, such as API request failures or missing data, and the `auto_runner.py` script repeats steps as necessary until all data is retrieved and combined.

## How to Run

1. Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
