
import os

from flask import Flask
from routes import initialize_routes

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

initialize_routes(app)

if __name__ == "__main__":
	app.run(port = os.environ.get('PORT') if os.environ.get('PORT') else 8080)
