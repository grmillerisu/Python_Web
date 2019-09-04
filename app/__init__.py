
from flask import Flask
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event
from messaging import *

app = Flask(__name__)
# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()

from app import routes

from messageThread import MessageThread

@socketio.on('connect', namespace='/messaging')
def test_connect():
   # need visibility of the global thread object
   global thread
   print('Client connected')

   # Start the random number generator thread only if the thread has not been started before.
   if not thread.isAlive():
      print("Starting Thread")
      thread = MessageThread()
      thread_stop_event.clear()
      thread.start()


@socketio.on('disconnect', namespace='/messaging')
def test_disconnect():
   print('Client disconnected')
   thread_stop_event.set()
