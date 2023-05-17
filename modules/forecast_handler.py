import os
import re
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from modules.call_weather_api import call_weather_api
from modules.json_pretty_print import json_pretty_print


def is_cached_forecast_present() -> bool:
    """
    Check if there are any cached forecast files in the /responses directory.

    Returns:
        bool: True if one or more cached forecast files are present, False otherwise.
    """
    # Define the directory to check
    directory = "./responses"

    # Initialize the result as False
    is_present = False

    # Define the file naming pattern
    file_pattern = r"open-meteo-\d{4}-\d{2}-\d{2}T\d{6}Z\.json"

    # If the directory exists, get a list of all files in the directory
    if os.path.exists(directory):
        files_in_directory = os.listdir(directory)
        print(f"Found {len(files_in_directory)} files in {directory}")

        # Check each file against the pattern
        for filename in files_in_directory:
            if re.match(file_pattern, filename):
                is_present = True
                print(f"Found cached forecast file: {filename}")
                break

    return is_present


def get_forecast(is_present):
    """
    This function retrieves weather forecast data. It either fetches the data from the most recent file in the
    'responses' directory if it exists or makes a new API call if it doesn't.

    Args:
        is_present (bool): A boolean indicating whether a recent forecast file exists in the 'responses' directory.

    Returns:
        pd.DataFrame: The DataFrame containing forecast data, including both hourly and daily forecasts for each model.
    """
    print(is_present)
    if is_present:
        # Time one hour ago in UTC
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        print(f"one_hour_ago: {one_hour_ago}")

        # Get a list of all files in the /responses directory
        files = os.listdir("responses")

        # Filter the list to only include files created within the last hour
        recent_files = [
            file
            for file in files
            if datetime.strptime(file[11:-5], "%Y-%m-%dT%H%M%SZ") > one_hour_ago
        ]

        print(f"Found {len(recent_files)} recent files")

        # Check if there are any recent files
        if recent_files:
            # Get the most recent file among those
            print("Checking if date of recent file is in the last hour...")
            latest_file = max(
                recent_files,
                key=lambda x: datetime.strptime(x[11:-5], "%Y-%m-%dT%H%M%SZ"),
            )

            print(f"Using cached forecast file: {latest_file}")

            # Open and read the JSON data from the file
            with open(os.path.join("responses", latest_file), "r") as file:
                forecast = json.load(file)
        else:
            forecast = {}
    else:
        forecast = {}

    if not forecast:  # No forecast data available, make API call
        # Default parameters for the API call
        latitude = 38.59
        longitude = -89.91  # O'Fallon, IL
        hourly = "temperature_2m,precipitation,windspeed_10m,winddirection_10m,windgusts_10m,is_day"
        models = "ecmwf_ifs04,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless"
        daily = "windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant"
        windspeed_unit = "kn"
        timezone = "America/Chicago"

        print("Making API call...")

        # Make the API call
        forecast = call_weather_api(
            latitude,
            longitude,
            hourly=hourly,
            models=models,
            daily=daily,
            windspeed_unit=windspeed_unit,
            timezone=timezone,
        )

    # Convert the forecast data into a nested Dictionary
    forecast = convert_data_dict_to_nested(forecast)
    print(f"Forecast converted successfully!")

    return forecast


def convert_data_dict_to_nested(data):
    """
    Convert a dictionary of weather data into a nested dictionary structure.
    
    Args:
        data (dict): The original weather data dictionary. This should have the structure:
            {
                "hourly": {
                    "time": [...],
                    "temperature_model": [...],
                    ...
                },
                "daily": {
                    "time": [...],
                    "temperature_model": [...],
                    ...
                }
            }
            
    Returns:
        dict: The nested dictionary, structured as:
            {
                "model": {
                    "hourly": [{"time": ..., "temperature": ..., ...}],
                    "daily": [{"time": ..., "temperature": ..., ...}]
                },
                ...
            }
    """
    # List of models
    models = ['ecmwf_ifs04', 'gfs_seamless', 'jma_seamless', 'icon_seamless', 'gem_seamless', 'meteofrance_seamless']
    output = {}

    print("Converting data dictionary to nested structure...")

    for model in models:
        print(f"Processing model: {model}")
        output[model] = {
            "hourly": [],
            "daily": []
        }
        for i, time in enumerate(data["hourly"]["time"]):
            hourly_data = {
                "time": time
            }
            for key in data["hourly"]:
                if model in key:
                    new_key = key.replace(f"_{model}", "")
                    hourly_data[new_key] = data["hourly"][key][i]
            output[model]["hourly"].append(hourly_data)

        for i, time in enumerate(data["daily"]["time"]):
            daily_data = {
                "time": time
            }
            for key in data["daily"]:
                if model in key:
                    new_key = key.replace(f"_{model}", "")
                    daily_data[new_key] = data["daily"][key][i]
            output[model]["daily"].append(daily_data)

        print(f"Completed processing for model: {model}")
    
    print("Conversion complete!")
    return output

def display_forecast():
    """
    Handles the entire process of fetching, processing, and displaying the forecast data.
    """
    # Check if a cached forecast is present
    is_present = is_cached_forecast_present()

    # Fetch the forecast data
    forecast_dict = get_forecast(is_present)

    # If the forecast data did not come from a cached file, write a new output file
    if not is_present:
        # Check if the /outputs directory exists, if not, create it
        if not os.path.exists("outputs"):
            os.makedirs("outputs")

        # Get the current timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")

        # Create the file name
        file_name = f"model_sorted_output_{timestamp}.json"

        # Open the output file in write mode ('w')
        with open(os.path.join("outputs", file_name), "w") as f:
            # Write the forecast_dict as JSON to the file
            json.dump(forecast_dict, f, indent=4)
