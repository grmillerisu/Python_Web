
from flask import Flask
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event


app = Flask(__name__)
# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()

from app import routes

class RandomThread(Thread):
   def __init__(self):
      self.delay = 1
      super(RandomThread, self).__init__()

   def randomNumberGenerator(self):
      """
      Generate a random number every 1 second and emit to a socketio instance (broadcast)
      Ideally to be run in a separate thread?
      """
      # infinite loop of magical random numbers
      print("Making random numbers")
      while not thread_stop_event.isSet():
         number = round(random() * 10, 3)
         print(number)
         socketio.emit('newnumber', {'number': number}, namespace='/test')
         sleep(self.delay)

   def run(self):
      self.randomNumberGenerator()


@socketio.on('connect', namespace='/test')
def test_connect():
   # need visibility of the global thread object
   global thread
   print('Client connected')

   # Start the random number generator thread only if the thread has not been started before.
   if not thread.isAlive():
      print("Starting Thread")
      thread = RandomThread()
      thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
   print('Client disconnected')
   thread.stop()
