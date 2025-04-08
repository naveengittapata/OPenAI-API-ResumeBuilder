import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Retrieve API Key from the environment
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

    return app
