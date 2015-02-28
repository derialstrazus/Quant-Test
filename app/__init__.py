from flask import Flask
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__, static_folder=ASSETS_DIR)
app.config.from_object('config')

from app import views