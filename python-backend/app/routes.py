from flask import jsonify
from . import app
from modules.forecast_handler import WeatherForecast
from modules.mongo_handler import MongoHandler

# Initialize the MongoHandler instance outside the route
mongo_handler = MongoHandler()
mongo_handler.test_connection()

@app.route('/weather', methods=['GET'])
def get_weather():
    # Inject the mongo_handler instance when creating the WeatherForecast object
    weather_forecast = WeatherForecast(mongo_handler)
    
    response_data = weather_forecast.get_forecast()
    
    if response_data["success"]:
        return jsonify(response_data["data"]), 200
    else:
        return jsonify({"error": response_data["error"]}), 500
