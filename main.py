from modules.get_weather_forecast import get_weather_forecast

def main():
    """
    Main function that retrieves and prints the weather forecast data.
    """
    latitude = 38.59
    longitude = -89.91 # O'Fallon, IL
    forecast = get_weather_forecast(latitude, longitude, hourly='temperature_2m', forecast_days=16)
    print(forecast)

if __name__ == "__main__":
    main()
