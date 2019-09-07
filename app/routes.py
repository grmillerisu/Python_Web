from app import app
from flask import render_template
from app import socketio
from app import thread, thread_stop_event
from app import MessageThread
import os
from app import messages
import matplotlib.pyplot as plt
import numpy as np

@app.route('/')
def hello_world():
   img = app.config['IMAGE_FOLDER']
   msgList = getMessageFiles(messages)
   full_filename = getLogoFile()
   return render_template('home.html',title='CyRoc Home',img=full_filename,msg_list = msgList)

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


def plotAcceleration():
   accx = []
   accy = []
   accz = []
   with open("app/static/acceleration.txt","r") as fp:
      line = fp.readline()
      while line:
         split_line = line.split(",")
         accx.append(float(split_line[1]))
         accy.append(float(split_line[3]))
         accz.append(float(split_line[5].split("|")[0]))
         line = fp.readline()
   # Plot the data
   n = len(accx)
   n = np.linspace(1,n,n)
   plt.plot(n,accx, label='Accx')
   plt.plot(n, accy, label='Accy')
   plt.plot(n, accz, label='Accz')
   # Add a legend
   plt.legend()
   # Show the plot
   plt.savefig('app/static/acceleration.png', bbox_inches='tight')
# end def


@socketio.on('disconnect', namespace='/messaging')
def test_disconnect():
   print('Client disconnected')
   # don't do anything else
# end def
