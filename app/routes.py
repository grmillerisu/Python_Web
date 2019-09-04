from app import app
from flask import render_template
from flask import jsonify
from datetime import datetime
from app import socketio
from time import sleep
from threading import Thread, Event
from app import thread, thread_stop_event
from app import MessageThread

@app.route('/')
def hello_world():
    message = {'name':'Pos3d',
               'time' : datetime.now().time()}
    return render_template('message.html',title='The Title',message=message)

@app.route('/index')
def ind():
   print("Index")

   return render_template('index.html')
# end def

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
