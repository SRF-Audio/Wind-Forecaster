import os
from datetime import datetime, timedelta
from modules.call_weather_api import call_weather_api
from modules.mongo_handler import MongoHandler

import os

class WeatherForecast:
    def __init__(self):
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')  # fetch from env or use default
        self.mongo = MongoHandler(mongo_uri)


    def is_cached_forecast_present(self) -> bool:
        """
        Check if there are any cached forecast files in the MongoDB.

        Returns:
            bool: True if one or more cached forecast files are present, False otherwise.
        """
        try:
            return self.mongo.is_forecast_present()
        except PyMongoError as e:
            print(f"Error checking for cached forecast: {e}")
            return False

    def get_forecast(self, is_present: bool) -> dict:
        """
        This function retrieves weather forecast data from MongoDB or makes a new API call.

        Args:
            is_present (bool): A boolean indicating whether a recent forecast exists in MongoDB.

        Returns:
            dict: The forecast data.
        """
        forecast = None
        try:
            if is_present:
                one_hour_ago = datetime.utcnow() - timedelta(hours=1)
                forecast = self.mongo.get_recent_forecast(one_hour_ago)

            if not forecast:
                # ... (rest of the API call setup)
                forecast = call_weather_api(
                    # ... (rest of the parameters)
                )
                self.mongo.save_forecast(forecast)
        except PyMongoError as e:
            print(f"Error fetching from or saving to MongoDB: {e}")
        except Exception as e:  # Catching potential API errors or any other unexpected errors
            print(f"Error getting forecast: {e}")

        if forecast:
            try:
                forecast = self.convert_data_dict_to_nested(forecast)
                print(f"Forecast converted successfully!")
            except Exception as e:
                print(f"Error processing forecast data: {e}")
        else:
            print("No forecast data available.")

        return forecast

    def convert_data_dict_to_nested(self, data: dict) -> dict:
        """
        Convert a dictionary of weather data into a nested dictionary structure.

        Args:
            data (dict): The original weather data dictionary.

        Returns:
            dict: The nested dictionary.
        """
        # List of models
        models = ['ecmwf_ifs04', 'gfs_seamless', 'jma_seamless', 'icon_seamless', 'gem_seamless', 'meteofrance_seamless']
        output = {}

        print("Converting data dictionary to nested structure...")

        for model in models:
            print(f"Processing model: {model}")
            output[model] = {
                "hourly": [],
                "daily": []
            }
            for i, time in enumerate(data["hourly"]["time"]):
                hourly_data = {
                    "time": time
                }
                for key in data["hourly"]:
                    if model in key:
                        new_key = key.replace(f"_{model}", "")
                        hourly_data[new_key] = data["hourly"][key][i]
                output[model]["hourly"].append(hourly_data)

            for i, time in enumerate(data["daily"]["time"]):
                daily_data = {
                    "time": time
                }
                for key in data["daily"]:
                    if model in key:
                        new_key = key.replace(f"_{model}", "")
                        daily_data[new_key] = data["daily"][key][i]
                output[model]["daily"].append(daily_data)

            print(f"Completed processing for model: {model}")

        print("Conversion complete!")
        return output

def get_forecast_data(self):
    """
    Fetches and processes the forecast data.
    Returns a dictionary containing the forecast data or error information.
    """
    try:
        is_present = self.is_cached_forecast_present()
        forecast_dict = self.get_forecast(is_present)
        return {"success": True, "data": forecast_dict}
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred while fetching the forecast: {e}")
        # Return an error message in a web-friendly format
        return {"success": False, "error": str(e)}

