from app import app
from flask import render_template
from app import socketio
from app import thread, thread_stop_event
from app import MessageThread
import os
from app import messages

@app.route('/')
def hello_world():
   img = app.config['IMAGE_FOLDER']
   msgList = getMessageFiles(messages)
   full_filename = getLogoFile()
   acc_fn = "static/acceleration.png"
   return render_template('home.html',title='CyRoc Home',img=full_filename,msg_list = msgList, acc_fn=acc_fn)

@app.route('/messages')
def ind():
   img = app.config['IMAGE_FOLDER']
   msgList = getMessageFiles(messages)
   full_filename = getLogoFile()
   return render_template('messages.html',img=full_filename,msg_list = msgList)
# end def

def getLogoFile():
   return os.path.join(app.config['IMAGE_FOLDER'], 'Cyroc-Logo-Tansparent.png')
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
   print('Client connected')
   # Ensure the thread is alive and sending messages
   startThread()
# end def

def startThread():
   global thread
   # Ensure the thread is alive and sending messages
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
