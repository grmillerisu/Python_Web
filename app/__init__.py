import os
from flask import Flask
from flask_socketio import SocketIO, emit
from messaging import *
from threading import Thread, Event
app = Flask(__name__)
app.config['IMAGE_FOLDER'] = os.path.join('static', 'images')
# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()

from messageThread import MessageThread

from app import routes
