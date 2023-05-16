from modules.call_weather_api import call_weather_api
from modules.cache_api_response import cache_api_response
from modules.json_pretty_print import json_pretty_print


def main():
    """
    Main function that retrieves and prints the weather forecast data.
    """
    latitude = 38.59
    longitude = -89.91  # O'Fallon, IL
    hourly = "temperature_2m,precipitation,windspeed_10m,winddirection_10m,windgusts_10m,is_day"
    models = "ecmwf_ifs04,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless"
    daily = "windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant"
    windspeed_unit = "kn"
    timezone = "America/Chicago"

    forecast = call_weather_api(
        latitude,
        longitude,
        hourly=hourly,
        models=models,
        daily=daily,
        windspeed_unit=windspeed_unit,
        timezone=timezone,
    )


if __name__ == "__main__":
    main()
