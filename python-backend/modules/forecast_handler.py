import os
from datetime import datetime, timedelta
from modules.call_weather_api import call_weather_api
from modules.mongo_handler import MongoHandler
from pymongo import errors as pymongo_errors
from bson import ObjectId

class WeatherForecast:
    def __init__(self, mongo_handler: MongoHandler):
        self.latitude = None
        self.longitude = None
        self.additional_params = {}
        self.mongo = mongo_handler
        self.mongo.connect("weather_database", ["Forecasts"])
        
        
        # TODO: Replace with dynamic map coordinates once map is implemented
        # https://github.com/SRF-Audio/Wind-Forecaster/issues/2
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
        
        oid_one_hour_ago = ObjectId.from_datetime(one_hour_ago)
        
        try:
            is_present = self.mongo.is_forecast_present(collection_name="Forecasts", query={"_id": {"$gt": oid_one_hour_ago}})
            print(f"Is forecast present in cache? {is_present}")
            return is_present
        except pymongo_errors.PyMongoError as e:
            print(f"Error checking for cached forecast: {e}")
            return False
            
    def get_forecast(self) -> bool:
        forecast = None
        
        if self.is_cached_forecast_present():
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            forecast = self.mongo.fetch_all(collection_name="Forecasts", query={"time": {"$gte": one_hour_ago}})
            print(f"Forecast fetched from mongo: {forecast}")

        if not forecast:
            if not self.latitude or not self.longitude:
                print("Latitude and Longitude not set!")
                return False
            try:
                forecast = call_weather_api(latitude=self.latitude, longitude=self.longitude, mongo_handler=self.mongo, **self.additional_params)
                print(f"Forecast fetched from API: {forecast}")
                forecast.pop('_id', None)
                self.mongo.insert(data=forecast, collection_name="Forecasts")
                print("Forecast stored in mongo!")
            except Exception as e:
                print(f"Error during API call or inserting to mongo: {e}")
                return False

        return True

def fetch_and_cache_forecast():
    mongo_handler = MongoHandler()
    weather_forecast = WeatherForecast(mongo_handler)
    weather_forecast.get_forecast()