from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
#turn the flask app into a socketio app
socketio = SocketIO(app)

from app import routes