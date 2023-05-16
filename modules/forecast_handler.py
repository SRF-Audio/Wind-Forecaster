import os
import re
import json
import time
from datetime import datetime
from modules.call_weather_api import call_weather_api


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
    file_pattern = r"open-meteo-\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\.json"

    # If the directory exists, get a list of all files in the directory
    if os.path.exists(directory):
        files_in_directory = os.listdir(directory)

        # Check each file against the pattern
        for filename in files_in_directory:
            if re.match(file_pattern, filename):
                is_present = True
                break

    return is_present


def get_forecast(is_present):
    """
    This function retrieves weather forecast data. It either fetches the data from the most recent file in the
    'responses' directory if it exists or makes a new API call if it doesn't.

    Args:
        is_present (bool): A boolean indicating whether a recent forecast file exists in the 'responses' directory.

    Returns:
        dict: The forecast data as a JSON object.
    """
    if is_present:
        # Time one hour ago
        one_hour_ago = time.time() - 60 * 60

        # Get a list of all files in the /responses directory
        files = os.listdir("responses")

        # Filter the list to only include files created within the last hour
        recent_files = [
            file
            for file in files
            if os.path.getctime(os.path.join("responses", file)) > one_hour_ago
        ]

        # Check if there are any recent files
        if recent_files:
            # Get the most recent file among those
            latest_file = max(
                recent_files,
                key=lambda x: os.path.getctime(os.path.join("responses", x)),
            )

            # Open and read the JSON data from the file
            with open(os.path.join("responses", latest_file), "r") as file:
                forecast = json.load(file)
        else:
            forecast = None
    else:
        # Default parameters for the API call
        latitude = 38.59
        longitude = -89.91  # O'Fallon, IL
        hourly = "temperature_2m,precipitation,windspeed_10m,winddirection_10m,windgusts_10m,is_day"
        models = "ecmwf_ifs04,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless"
        daily = "windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant"
        windspeed_unit = "kn"
        timezone = "America/Chicago"

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

    return forecast


def process_forecast(forecast):
    """
    Processes the forecast data and sorts it by each model type and then by hourly and daily forecasts.

    Args:
        forecast (dict): The forecast data.

    Returns:
        dict: The processed forecast data.
    """
    # Create a dictionary to hold the sorted data
    sorted_forecast = {}

    # Loop through the forecast data
    for model_name, model_data in forecast.items():
        # Initialize the model in the dictionary if it doesn't exist
        if model_name not in sorted_forecast:
            sorted_forecast[model_name] = {"hourly": [], "daily": []}

        # Loop through the forecast times for this model
        for forecast_time, forecast_data in model_data.items():
            # Check if this is an hourly or daily forecast and add it to the appropriate list
            if forecast_time == "hourly":
                for hourly_data in forecast_data:
                    sorted_forecast[model_name]["hourly"].append(
                        {
                            "Time": hourly_data["time"],
                            "Wind Speed": hourly_data["windspeed_10m"],
                            "Wind Gusts": hourly_data["windgusts_10m"],
                            "Wind Direction": hourly_data["winddirection_10m"],
                            "Day/Night": "Day"
                            if hourly_data["is_day"] == 1
                            else "Night",
                        }
                    )
            elif forecast_time == "daily":
                for daily_data in forecast_data:
                    sorted_forecast[model_name]["daily"].append(
                        {
                            "Day": daily_data["time"],
                            "Wind Speed": daily_data["windspeed_10m_max"],
                            "Wind Gusts": daily_data["windgusts_10m_max"],
                            "Wind Direction": daily_data["winddirection_10m_dominant"],
                        }
                    )

    return sorted_forecast
