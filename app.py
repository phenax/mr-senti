
import os

from flask import Flask
from routes import initialize_routes

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

initialize_routes(app)

PORT = int(os.environ.get('PORT', 33507))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = PORT)
