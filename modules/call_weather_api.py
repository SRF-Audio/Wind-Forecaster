import requests
from modules.cache_api_response import cache_api_response
from modules.json_pretty_print import json_pretty_print


def call_weather_api(latitude, longitude, **kwargs):
    """
    Retrieve weather forecast from the Open-Meteo API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        **kwargs: Arbitrary keyword arguments for additional parameters.

    Returns:
        dict: A dictionary containing the weather forecast data.

    Raises:
        Exception: If the API request is not successful.
    """
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # Mandatory parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
    }

    # Optional parameters
    for key, value in kwargs.items():
        params[key] = value

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    else:
        cache_api_response(response.json())
        # Pretty-print the forecast data
        pretty_forecast = json_pretty_print(forecast)
        print(pretty_forecast)
        return response.json()
