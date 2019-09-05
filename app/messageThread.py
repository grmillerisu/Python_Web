from threading import Thread, Event
from app import socketio
from app import thread_stop_event
from messaging import *
from time import sleep
import copy

class MessageThread(Thread):
   def __init__(self):
      self.delay = 3
      super(MessageThread, self).__init__()
      self.pos = Position3D()
      self.acc = Acceleration()
      self.posList = list()
      self.accList = list()
      self.posLength = 5
      self.accLength = 5
      self.pos.lat = 123.456
      self.pos.lon = 789.012
      self.pos.alt = 101.3
      self.acc.accx = -123.444
      self.acc.accy = 567.777
      self.acc.accz = 890.001
      self.msg1 = {"name":"Position3D","length":5,'str':self.pos.toString(),'initMessage':False}
      self.msg2 = {"name":"Acceleration","length":5,'str':self.acc.toString(),'initMessage':False}
      self.addToPosList(self.msg1)
      self.addToAccList(self.msg2)
   # end def

   def run(self):
      self.sendMessages()
   # end def

   def sendMessages(self):
      """
      Generate a random number every 1 second and emit to a socketio instance (broadcast)
      Ideally to be run in a separate thread?
      """
      while not thread_stop_event.isSet():
         self.pos.lat += 0.1
         self.pos.lon -= 0.1
         self.pos.alt += 3.1
         self.msg1['str'] = self.pos.toString()
         self.addToPosList(self.msg1)
         socketio.emit('newmessage', self.msg1, namespace='/messaging')
         sleep(self.delay)
         self.acc.accx += 0.2
         self.acc.accy -= 0.2
         self.acc.accz += 1.1
         self.msg2['str'] = self.acc.toString()
         self.addToAccList(self.msg2)
         socketio.emit('newmessage', self.msg2, namespace='/messaging')
         sleep(self.delay)
         # end for
      # end while
   # end def

   def addToPosList(self, msg):
      self.posList.append(copy.deepcopy(msg))
      if len(self.posList) > self.posLength:
         self.posList = self.posList[-self.posLength:]
      # end if
   # end def

   def addToAccList(self, msg):
      self.accList.append(copy.deepcopy(msg))
      if len(self.accList) > self.accLength:
         self.accList = self.accList[-self.accLength:]
      # end if
   # end def

   def sendInitMessage(self):
      numMessages = len(self.accList) + len(self.posList)
      combinedList = list()
      combinedList.extend(self.posList)
      combinedList.extend(self.accList)
      msg = {'initMessage':True,'totalMessages':numMessages,'msgList':combinedList}
      socketio.emit('newmessage', msg, namespace='/messaging')
   # end def

# end class
