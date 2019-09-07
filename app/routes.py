from app import app
from flask import render_template
from flask import jsonify
from datetime import datetime
from app import socketio
from time import sleep
from threading import Thread, Event
from app import thread, thread_stop_event
from app import MessageThread
import os
from app import messages

@app.route('/')
def hello_world():
   message = {'name':'Pos3d',
               'time' : datetime.now().time()}
   img = app.config['IMAGE_FOLDER']
   msgList = getMessageFiles(messages)
   full_filename = os.path.join(app.config['IMAGE_FOLDER'], 'Cyroc-Logo-Tansparent.png')
   return render_template('time.html',title='CyRoc Home',message=message,img=full_filename,msg_list = msgList)

@app.route('/messages')
def ind():
   img = app.config['IMAGE_FOLDER']
   msgList = getMessageFiles(messages)
   full_filename = os.path.join(app.config['IMAGE_FOLDER'], 'Cyroc-Logo-Tansparent.png')
   return render_template('messages.html',img=full_filename,msg_list = msgList)
# end def

def getMessageFiles(msgList):
   retList = list()
   for msg in msgList:
      fp = "static\\%s.txt" % msg.lower()
      message = {'name':msg.lower(), 'fp':fp}
      retList.append(message)
   return retList
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
   # end if
   thread.sendInitMessage()
# end def

@socketio.on('disconnect', namespace='/messaging')
def test_disconnect():
   print('Client disconnected')
   # don't do anything else
# end def
