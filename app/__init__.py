
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

class MessageThred(Thread):
   def __init__(self):
      self.delay = 1
      super(MessageThred, self).__init__()

   def sendMessages(self):
      """
      Generate a random number every 1 second and emit to a socketio instance (broadcast)
      Ideally to be run in a separate thread?
      """
      # infinite loop of magical random numbers

      msg1 = {"name":"Position3D","length":2,'str':0}
      msg2 = {"name":"Acceleration","length":3,'str':0}
      msgs = [msg1,msg2]
      while not thread_stop_event.isSet():
         for msg in msgs:
            number = round(random() * 10, 3)
            print("%s %f"%(msg["name"],number))
            msg['str'] = str(number)
            socketio.emit('newmessage', msg, namespace='/messaging')
            sleep(self.delay)
         # end for
      # end while

   def run(self):
      self.sendMessages()


@socketio.on('connect', namespace='/messaging')
def test_connect():
   # need visibility of the global thread object
   global thread
   print('Client connected')

   # Start the random number generator thread only if the thread has not been started before.
   if not thread.isAlive():
      print("Starting Thread")
      thread = MessageThred()
      thread_stop_event.clear()
      thread.start()


@socketio.on('disconnect', namespace='/messaging')
def test_disconnect():
   print('Client disconnected')
   thread_stop_event.set()
