import json
import os
from datetime import datetime

def cache_api_response(forecast):
    """
    Cache the weather forecast data in a JSON file.

    Args:
        forecast (dict): The weather forecast data to cache.

    Returns:
        None
    """
    # Get the current datetime
    now = datetime.now()

    # Format the datetime as a string to use in the filename
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")

    # Define the directory where we'll store the responses
    directory = 'responses'

    # Check if the directory exists and create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create the filename
    filename = f"{directory}/open-meteo-{dt_string}.json"

    # Write the forecast data to the file
    with open(filename, 'w') as f:
        json.dump(forecast, f, indent=4)
