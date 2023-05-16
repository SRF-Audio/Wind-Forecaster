import json
import os
from datetime import datetime


def cache_api_response(response):
    """
    Caches the API response in a JSON file.

    Args:
        response (dict): The API response data.
    """
    # Get the current date and time
    now = datetime.utcnow()

    # Format the date and time string to be used in the filename
    dt_string = now.strftime("%Y-%m-%dT%H%M%S")  # Removes the colon characters

    # Define the filename
    filename = f"open-meteo-{dt_string}Z.json"

    # Define the file path
    file_path = f"responses/{filename}"

    # Write the API response data to the file
    with open(file_path, "w") as file:
        json.dump(response, file, indent=4)
