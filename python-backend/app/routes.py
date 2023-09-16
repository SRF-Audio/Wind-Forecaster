from flask import Flask, json, jsonify
from flask_cors import CORS
from . import app
from modules.forecast_handler import WeatherForecast, fetch_and_write_forecast
from modules.mongo_handler import MongoHandler
from modules.json_encoder import JSONEncoder
from modules.hourly_retriever import HourlyRetriever

# Initialize the MongoHandler instance outside the route
mongo_handler = MongoHandler()
mongo_handler.test_connection()
mongo_handler.connect("weather_database", ["Forecasts"])
fetch_and_write_forecast()
print("Server started!")

CORS(app)

@app.route('/hourly', methods=['GET'])
def get_hourly_forecast():
    hourly_retriever = HourlyRetriever(mongo_handler)
    hourly_forecast = hourly_retriever.get_hourly_forecast()
    
    if hourly_forecast["success"]:
        response = app.response_class(
            response=json.dumps(hourly_forecast["data"], cls=JSONEncoder),
            status=200,
            mimetype='application/json'
        )
    else:
        response = jsonify({"error": hourly_forecast["error"]}), 500

    return response

@app.route('/daily', methods=['GET'])
def get_daily_forecast():
    # NOTE: You'll need to implement the functionality for this 
    # in the WeatherForecast class (or another module).
    daily_forecast = WeatherForecast(mongo_handler).get_daily_forecast()
    
    if daily_forecast["success"]:
        response = app.response_class(
            response=json.dumps(daily_forecast["data"], cls=JSONEncoder),
            status=200,
            mimetype='application/json'
        )
    else:
        response = jsonify({"error": daily_forecast["error"]}), 500

    return response
