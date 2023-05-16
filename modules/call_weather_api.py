import requests

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
        'latitude': latitude,
        'longitude': longitude,
    }
    
    # Optional parameters
    for key, value in kwargs.items():
        params[key] = value
    
    response = requests.get(BASE_URL, params=params)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")
    
    return response.json()
