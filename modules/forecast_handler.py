import os
import re
import json
import time
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

        print(f"Found {len(recent_files)} recent files")

        # Check if there are any recent files
        if recent_files:
            # Get the most recent file among those
            print("Checking if date of recent file is in the last hour...")
            latest_file = max(
                recent_files,
                key=lambda x: os.path.getctime(os.path.join("responses", x)),
            )
            print(f"Using cached forecast file: {latest_file}")

            # Open and read the JSON data from the file
            with open(os.path.join("responses", latest_file), "r") as file:
                forecast = json.load(file)
        else:
            print("No recent files found")
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

    # Convert the forecast data into a DataFrame
    forecast_df = convert_data_dict_to_dataframe(forecast)

    return forecast_df


def convert_data_dict_to_dataframe(data_dict):
    """
    Converts the nested dictionary of weather data into a DataFrame with the following columns:
    - 'Model': the model name
    - 'Type': the type of the forecast (hourly or daily)
    - 'Forecast Time': the time of the forecast
    - 'Temperature': temperature at 2m (only for hourly data)
    - 'Precipitation': precipitation (only for hourly data)
    - 'Wind Speed': wind speed at 10m
    - 'Wind Direction': wind direction at 10m
    - 'Wind Gusts': wind gusts at 10m
    - 'Day/Night': whether it's day (1) or night (0) (only for hourly data)

    Args:
        data_dict (dict): the nested dictionary of weather data.

    Returns:
        DataFrame: a DataFrame representation of the weather data.
    """
    df_list = []

    for model, model_data in data_dict.items():
        for forecast_type, forecast_data in model_data.items():
            for forecast in forecast_data:
                if forecast_type == "hourly":
                    df_list.append(
                        {
                            "Model": model,
                            "Type": "Hourly",
                            "Forecast Time": forecast["time"],
                            "Temperature": forecast["temperature_2m"],
                            "Precipitation": forecast["precipitation"],
                            "Wind Speed": forecast["windspeed_10m"],
                            "Wind Direction": forecast["winddirection_10m"],
                            "Wind Gusts": forecast["windgusts_10m"],
                            "Day/Night": "Day" if forecast["is_day"] == 1 else "Night",
                        }
                    )
                elif forecast_type == "daily":
                    df_list.append(
                        {
                            "Model": model,
                            "Type": "Daily",
                            "Forecast Time": forecast["time"],
                            "Temperature": None,
                            "Precipitation": None,
                            "Wind Speed": forecast["windspeed_10m_max"],
                            "Wind Direction": forecast["winddirection_10m_dominant"],
                            "Wind Gusts": forecast["windgusts_10m_max"],
                            "Day/Night": None,
                        }
                    )

    df = pd.DataFrame(df_list)
    return df


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

    # Print the type of 'forecast'
    print(f"Type of forecast: {type(forecast)}")
    print({key: type(value) for key, value in forecast.items()})
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
    print(sorted_forecast)

    return sorted_forecast


def display_forecast():
    """
    Handles the entire process of fetching, processing, and displaying the forecast data.
    """
    # Check if a cached forecast is present
    is_present = is_cached_forecast_present()

    # Fetch the forecast data
    forecast = get_forecast(is_present)

    # Process the forecast data
    sorted_forecast = process_forecast(forecast)

    # Display the sorted forecasts
    for model, data in sorted_forecast.items():
        print(f"{model} forecasts:")
        for time_frame, forecasts in data.items():
            print(f"\n{time_frame.capitalize()} forecasts:")
            for forecast in forecasts:
                print(json_pretty_print(forecast))
                print("---")
