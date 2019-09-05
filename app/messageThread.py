from threading import Thread, Event
from app import socketio
from app import thread_stop_event
from messaging import *
from time import sleep

class MessageThread(Thread):
   def __init__(self):
      self.delay = 3
      super(MessageThread, self).__init__()
      self.pos = Position3D()
      self.acc = Acceleration()
   # end def

   def run(self):
      self.sendMessages()
   # end def

   def sendMessages(self):
      """
      Generate a random number every 1 second and emit to a socketio instance (broadcast)
      Ideally to be run in a separate thread?
      """
      self.pos.lat = 123.456
      self.pos.lon = 789.012
      self.pos.alt = 101.3
      self.acc.accx = -123.444
      self.acc.accy = 567.777
      self.acc.accz = 890.001
      self.msg1 = {"name":"Position3D","length":5,'str':self.pos.toString()}
      self.msg2 = {"name":"Acceleration","length":5,'str':self.acc.toString()}
      while not thread_stop_event.isSet():
         self.pos.lat += 0.1
         self.pos.lon -= 0.1
         self.pos.alt += 3.1
         self.msg1['str'] = self.pos.toString()
         socketio.emit('newmessage', self.msg1, namespace='/messaging')
         sleep(self.delay)
         self.acc.accx += 0.2
         self.acc.accy -= 0.2
         self.acc.accz += 1.1
         self.msg2['str'] = self.acc.toString()
         socketio.emit('newmessage', self.msg2, namespace='/messaging')
         sleep(self.delay)
         # end for
      # end while
   # end def
# end class
