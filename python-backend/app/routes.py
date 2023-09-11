from flask import jsonify
from . import app
from modules.forecast_handler import WeatherForecast

@app.route('/weather', methods=['GET'])
def get_weather():
    weather_forecast = WeatherForecast()
    response_data = weather_forecast.get_forecast_data()
    
    if response_data["success"]:
        return jsonify(response_data["data"]), 200
    else:
        return jsonify({"error": response_data["error"]}), 500

