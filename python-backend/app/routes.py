from flask import Flask, json
from flask_cors import CORS
from . import app
from modules.forecast_handler import WeatherForecast
from modules.mongo_handler import MongoHandler
from modules.json_encoder import JSONEncoder

# Initialize the MongoHandler instance outside the route
mongo_handler = MongoHandler()
mongo_handler.test_connection()

CORS(app)

@app.route('/weather', methods=['GET'])
def get_weather():
    # Inject the mongo_handler instance when creating the WeatherForecast object
    weather_forecast = WeatherForecast(mongo_handler)
    
    response_data = weather_forecast.get_forecast()
    
    if response_data["success"]:
        response = app.response_class(
            response=json.dumps(response_data["data"], cls=JSONEncoder),
            status=200,
            mimetype='application/json'
        )
    else:
        response = jsonify({"error": response_data["error"]}), 500

    return response
