from threading import Thread, Event
from app import socketio
from app import thread_stop_event
from messaging import *
from time import sleep

class MessageThread(Thread):
   def __init__(self):
      self.delay = 1
      super(MessageThread, self).__init__()

   def sendMessages(self):
      """
      Generate a random number every 1 second and emit to a socketio instance (broadcast)
      Ideally to be run in a separate thread?
      """
      # infinite loop of magical random numbers
      pos = Position3D()
      pos.lat = 123.456
      pos.lon = 789.012
      pos.alt = 101.3
      acc = Acceleration()
      acc.accx = -123.444
      acc.accy = 567.777
      acc.accz = 890.001
      msg1 = {"name":"Position3D","length":2,'str':pos.toString()}
      msg2 = {"name":"Acceleration","length":3,'str':acc.toString()}
      msgs = [msg1,msg2]
      while not thread_stop_event.isSet():
         pos.lat += 0.1
         pos.lon -= 0.1
         pos.alt += 3.1
         msg1['str'] = pos.toString()
         socketio.emit('newmessage', msg1, namespace='/messaging')
         sleep(self.delay)
         acc.accx += 0.2
         acc.accy -= 0.2
         acc.accz += 1.1
         msg2['str'] = acc.toString()
         socketio.emit('newmessage', msg2, namespace='/messaging')
         sleep(self.delay)
         # end for
      # end while

   def run(self):
      self.sendMessages()
