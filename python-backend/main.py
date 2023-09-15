import os
from app import app
from forecast_handler import fetch_and_cache_forecast

if __name__ == "__main__":
    # Fetch and cache the forecast when the backend starts
    fetch_and_cache_forecast()

    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=DEBUG_MODE, host=HOST)
