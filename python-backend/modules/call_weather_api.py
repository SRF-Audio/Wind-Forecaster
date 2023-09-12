import requests
from modules.mongo_handler import MongoHandler

class WeatherAPIException(Exception):
    """Custom exception for weather API related errors."""
    pass


def call_weather_api(latitude, longitude, mongo_handler, **kwargs):
    """
    Retrieve weather forecast from the Open-Meteo API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        **kwargs: Arbitrary keyword arguments for additional parameters.

    Returns:
        dict: A dictionary containing the weather forecast data.

    Raises:
        WeatherAPIException: If the API request is not successful.
    """
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    # Default parameters
    default_params = {
        "hourly": "windspeed_10m,winddirection_10m,windgusts_10m",
        "daily": "windspeed_10m_max,windgusts_10m_max",
        "timezone": "America/Chicago",
        "models": "best_match"
    }

    # Mandatory parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        **default_params,
        **kwargs  # This unpacks the kwargs directly into the params dict
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.

        # Parse JSON only once
        forecast_data = response.json()

        # Cache the API response in MongoDB
        mongo_handler.insert(data=forecast_data, collection_name="Forecasts")

        return forecast_data
        
    except requests.exceptions.HTTPError as http_err:
        raise WeatherAPIException(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        raise WeatherAPIException(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        raise WeatherAPIException(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        raise WeatherAPIException(f"An error occurred: {req_err}")
