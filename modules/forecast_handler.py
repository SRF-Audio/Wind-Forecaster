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
    print(f"Forecast data frame: {forecast}")

    return forecast


def convert_data_dict_to_nested(data):
    """
    This function converts the input data dictionary into a nested dictionary structure where each model has a dictionary with
    two keys: 'hourly' and 'daily'. Each of these keys corresponds to a list of dictionaries where each dictionary
    represents the weather data for a specific time.

    Args:
    data (dict): The input data dictionary containing the weather forecast data.

    Returns:
    dict: A nested dictionary with the processed weather forecast data.

    Example usage:
    forecast_dict = convert_data_dict_to_dataframe(input_data)
    """

    # Initialize an empty dictionary
    forecast_dict = {}

    # Extract only the model data
    model_data = {
        key: value
        for key, value in data.items()
        if key
        not in [
            "latitude",
            "longitude",
            "generationtime_ms",
            "utc_offset_seconds",
            "timezone",
            "timezone_abbreviation",
            "elevation",
            "hourly_units",
            "daily_units",
        ]
    }

    print(f"Found {len(model_data.keys())} keys in model_data")

    # Pattern for keys
    pattern = re.compile(r"_(\w+)$")

    # Get unique model names
    model_names = set()
    for forecast_type in ["hourly", "daily"]:
        model_names.update(
            match.group(1)
            for key in model_data[forecast_type].keys()
            if (match := pattern.search(key))
        )

    print(f"Found {len(model_names)} models: {model_names}")

    # Process each model's data
    for model in model_names:
        print(f"Processing model: {model}")
        model_dict = {
            "hourly": {},
            "daily": {},
        }  # Initialize a dictionary for the model

        for forecast_type in ["hourly", "daily"]:
            for key, values in model_data[forecast_type].items():
                # If this key corresponds to the current model
                if f"_{model}" in key:
                    # Get the metric name from the key
                    metric_name = key.split(f"_{model}")[0]

                    print(
                        f"Processing metric: {metric_name} for forecast type: {forecast_type}"
                    )

                    # Add the metric data to the model dictionary
                    for value in values:
                        timestamp = value["timestamp"]

                        # If this is a new time slot, add a new dictionary
                        if timestamp not in model_dict[forecast_type]:
                            model_dict[forecast_type][timestamp] = {"time": timestamp}

                        # Add the metric data
                        model_dict[forecast_type][timestamp][metric_name] = value[
                            metric_name
                        ]

            # Convert the dictionary of timestamps to a list of dictionaries
            model_dict[forecast_type] = list(model_dict[forecast_type].values())

        # Add the model dictionary to the main dictionary
        forecast_dict[model] = model_dict

    print(f"Final forecast data structure: {forecast_dict}")

    return forecast_dict


def display_forecast():
    """
    Handles the entire process of fetching, processing, and displaying the forecast data.
    """
    # Check if a cached forecast is present
    is_present = is_cached_forecast_present()

    # Fetch the forecast data
    forecast = get_forecast(is_present)

    # Process the forecast data
    forecast_dict = convert_data_dict_to_nested(forecast)

    # Open the output file in write mode ('w')
    with open("output.txt", "w") as f:
        # Display the sorted forecasts
        for model, data in forecast_dict.items():
            # Write the model name to the file
            f.write(f"{model} forecasts:\n")
            for time_frame, forecasts in data.items():
                # Write the time frame and forecasts to the file
                f.write(f"\n{time_frame.capitalize()} forecasts:\n")
                for forecast in forecasts:
                    f.write(json.dumps(forecast, indent=4))
                    f.write("\n---\n")
