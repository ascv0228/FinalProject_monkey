import flask
import json
import os
from flask_cors import CORS
from threading import Thread


import src.loader as loader
from src.app import App

app = App(__name__)
if __name__ == '__main__':
    # flask_thread = Thread(target=app.run)
    # flask_thread.start()
    app.run()