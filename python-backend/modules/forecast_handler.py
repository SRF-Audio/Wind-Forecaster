import os
from datetime import datetime, timedelta
from modules.call_weather_api import call_weather_api
from modules.mongo_handler import MongoHandler
from pymongo import errors as pymongo_errors

class WeatherForecast:
    def __init__(self, mongo_handler: MongoHandler):
        self.latitude = None
        self.longitude = None
        self.additional_params = {}
        self.mongo = mongo_handler
        self.mongo.connect("weather_database", ["Forecasts"])
        
        
        # Temporary values for latitude and longitude
        # TODO: Replace with function return data in the future
        tempLat = 38.810608
        tempLong = -90.699844
        self.set_latitude(tempLat)
        self.set_longitude(tempLong)

    def set_latitude(self, latitude: float):
        self.latitude = latitude

    def set_longitude(self, longitude: float):
        self.longitude = longitude

    def set_additional_params(self, params: dict):
        self.additional_params = params

    def is_cached_forecast_present(self) -> bool:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        try:
            is_present = self.mongo.is_forecast_present(collection_name="Forecasts", query={"time": {"$gte": one_hour_ago}})
            print(f"Is forecast present in cache? {is_present}")
            return is_present
        except pymongo_errors.PyMongoError as e:
            print(f"Error checking for cached forecast: {e}")
            return False
        
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

    def get_forecast(self) -> dict:
        # Checking if a recent forecast exists
        is_present = self.is_cached_forecast_present()

        # If present, fetch it
        forecast = None
        if is_present:
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            forecast = self.mongo.fetch_all(collection_name="Forecasts", query={"time": {"$gte": one_hour_ago}})
            print(f"Forecast fetched from cache: {forecast}")

        # If not present or if there was an error fetching from DB, make an API call
        if not forecast:
            if not self.latitude or not self.longitude:
                return {"success": False, "error": "Latitude and Longitude not set!"}
            try:
                forecast = call_weather_api(latitude=self.latitude, longitude=self.longitude, mongo_handler=self.mongo, **self.additional_params)
                print(f"Forecast fetched from API: {forecast}")
                # Cache the forecast
                print("Attempting to cache the forecast...")
                forecast.pop('_id', None)
                self.mongo.insert(data=forecast, collection_name="Forecasts")

                print("Forecast cached successfully!")
            except Exception as e:
                print(f"Error during API call or caching: {e}")
                return {"success": False, "error": str(e)}

        # Convert the fetched forecast into the desired nested format
        try:
            print("Attempting to convert data dictionary to nested structure...")
            forecast = self.convert_data_dict_to_nested(forecast)
            print("Data conversion successful!")
            return {"success": True, "data": forecast}
        except Exception as e:
            print(f"Error during data conversion: {e}")
            return {"success": False, "error": str(e)}