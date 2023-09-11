from modules.forecast_handler import WeatherForecast

def main():
    """
    Main function that retrieves and prints the weather forecast data.
    """
    weather_forecast = WeatherForecast()
    
    weather_forecast.display_forecast()

if __name__ == "__main__":
    main()
