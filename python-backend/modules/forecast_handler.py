from datetime import datetime, timedelta
import pytz
from modules.call_weather_api import call_weather_api
from modules.mongo_handler import MongoHandler
from pymongo import errors as pymongo_errors
from modules.json_pretty_print import json_pretty_print

class WeatherForecast:
    def __init__(self, mongo_handler: MongoHandler):
        self.latitude = 38.810608  # Default
        self.longitude = -90.699844  # Default
        self.additional_params = {}
        self.mongo = mongo_handler
        self.mongo.connect("weather_database", ["Forecasts"])

    def set_latitude(self, latitude: float):
        self.latitude = latitude

    def set_longitude(self, longitude: float):
        self.longitude = longitude

    def set_additional_params(self, params: dict):
        self.additional_params = params

    def recent_forecast_in_db(self) -> bool:
        try:
            latest_forecast = self.mongo.db["Forecasts"].find_one(sort=[("_id", -1)])
            if not latest_forecast:
                print("No forecast found in database.")
                return False
            forecast_time = latest_forecast['_id'].generation_time.replace(tzinfo=None)
            one_hour_ago = datetime.utcnow().replace(tzinfo=None) - timedelta(hours=1)
            print(f"Latest forecast time: {forecast_time}")
            print(f"One hour ago: {one_hour_ago}")
            return forecast_time > one_hour_ago
        except pymongo_errors.PyMongoError as e:
            print(f"Error checking recent forecast in DB: {e}")
            return False

    def log_forecast(self, forecast):
        print(f"Forecast:\n{json_pretty_print(forecast)}")

    def fetch_from_api(self) -> dict:
        if not self.latitude or not self.longitude:
            print("Latitude and Longitude not set!")
            return None
        return call_weather_api(latitude=self.latitude, longitude=self.longitude, mongo_handler=self.mongo, **self.additional_params)

    def write_to_db(self, forecast):
        try:
            forecast.pop('_id', None)
            self.mongo.insert(data=forecast, collection_name="Forecasts")
            print("New forecast data inserted into MongoDB.")
        except Exception as e:
            print(f"Error writing to DB: {e}")

    def check_and_update_forecast(self):
        if self.recent_forecast_in_db():
            forecast = self.mongo.fetch_all(collection_name="Forecasts", query={"time": {"$gt": datetime.utcnow() - timedelta(hours=1)}})
            self.log_forecast(forecast)
        else:
            forecast = self.fetch_from_api()
            if forecast:
                self.log_forecast(forecast)
                self.write_to_db(forecast)

def fetch_and_write_forecast():
    mongo_handler = MongoHandler()
    weather_forecast = WeatherForecast(mongo_handler)
    weather_forecast.check_and_update_forecast()
