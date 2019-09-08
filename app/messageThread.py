from threading import Thread, Event
from app import socketio
from app import thread_stop_event
from messaging import *
from time import sleep
import copy
import os
from datetime import datetime
import serial
import matplotlib.pyplot as plt
import numpy as np


class MessageThread(Thread):
   def __init__(self):
      self.delay = 1
      super(MessageThread, self).__init__()
      self.messages = messages
      self.default_msg_dict = {"name":"","length":0,"str":"","initMessage":False}
      self.displayLength = 5
      self.messaging = Message()
      self.messaging.setAllCallbacks(self.messageCallback)
      for message in self.messages:
         msg_lower = message.lower()
         cmd = "self.%s = %s()" %(msg_lower,message)
         exec(cmd)
         cmd = "self.%s_list = list()" % msg_lower
         exec(cmd)
         cmd = "self.%s_msg = copy.deepcopy(self.default_msg_dict)" % msg_lower
         exec(cmd)
         cmd = "self.%s_msg['name'] = \"%s\"" % (msg_lower, message)
         exec(cmd)
         cmd = "self.%s_msg['length'] = %s" % (msg_lower, self.displayLength)
         exec(cmd)
         cmd = "self.str = self.%s.toStringCsv() + \" | \" + str(datetime.now().time())" % msg_lower
         exec(cmd)
         cmd = "self.%s_msg['str'] = \"%s\"" % (msg_lower, self.str)
         exec(cmd)
         cmd = "self.%s_list = list()" % msg_lower
         exec(cmd)
         filename = "app/static/%s.txt" % msg_lower
         open(filename, 'w').close()
      # end for
   # end def

   def run(self):
      self.createLoop()
      print("MessageThread stopping")
   # end def

   def createLoop(self):
      """
      Loop until the thread stop event is set. Creates messages and sends them
      with socketio
      """
      global thread_stop_event
      while not thread_stop_event.isSet():
         for message in self.messages:
            msg_lower = message.lower()
            cmd = "self.%s.increment()" % msg_lower
            exec(cmd)
            cmd = "self.buff = self.%s.packWithHeader()" % msg_lower
            exec(cmd)
            self.messaging.recv(self.buff)
            sleep(self.delay)
         # end for
      # end while
   # end def

   def messageCallback(self,message):
      type_str = str(type(message))
      message_type = type_str.split(".")[1]
      msg_lower = message_type.lower()
      cmd = "self.%s = message" % msg_lower
      exec(cmd)
      cmd = "self.str = self.%s.toStringCsv() + \" | \" + str(datetime.now().time())" % msg_lower
      exec(cmd)
      cmd = "self.%s_msg['str'] = \"%s\"" % (msg_lower,self.str)
      exec(cmd)
      cmd = "self.addMessageToList(\"%s\",self.%s_msg)"% (message_type,msg_lower)
      exec(cmd)
      cmd = "self.msgToSend = self.%s_msg" % msg_lower
      exec(cmd)
      socketio.emit('newmessage', self.msgToSend, namespace='/messaging')
      if "acc" in msg_lower:
         print("Plotting acceleration")
         plotAcceleration()
      # end if
   # end def

   def addMessageToList(self,messageName,msg):
      self.writeMessage(messageName,msg)
      msg_lower = messageName.lower()
      cmd = "self.%s_list.append(copy.deepcopy(msg))" % msg_lower
      exec(cmd)
      cmd = "self.listLength = len(self.%s_list)" % msg_lower
      exec(cmd)
      if self.listLength > self.displayLength:
         cmd = "self.%s_list = self.%s_list[-self.listLength:]" %(msg_lower,msg_lower)
         exec(cmd)
      # end if
   # end def

   def sendInitMessage(self):
      self.combinedList = list()
      numMessages = 0
      for message in self.messages:
         msg_lower = message.lower()
         cmd = "self.listLength = len(self.%s_list)" % msg_lower
         exec(cmd)
         numMessages += self.listLength
         cmd = "self.combinedList.extend(self.%s_list)" % msg_lower
         exec(cmd)
      # end for
      msg = {'initMessage':True,'totalMessages':numMessages,'msgList':self.combinedList}
      socketio.emit('newmessage', msg, namespace='/messaging')
   # end def

   def writeMessage(self,message,msg):
      msg_lower = message.lower()
      filename = "app/static/%s.txt" % msg_lower
      with open(filename,"a") as f:
         f.write(msg['str'] + "\n")
   # end def

# end class

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
   plt.figure()
   plt.plot(n, accx, label='Accx')
   plt.plot(n, accy, label='Accy')
   plt.plot(n, accz, label='Accz')
   # Add a legend
   plt.legend()
   # Show the plot
   plt.savefig('app/static/acceleration.png', bbox_inches='tight')
# end def
