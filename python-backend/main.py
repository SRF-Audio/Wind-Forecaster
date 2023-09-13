import os
from app import app

if __name__ == "__main__":
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=DEBUG_MODE, host=HOST)
