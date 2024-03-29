from struct import unpack as s_unpack
from messaging import uids
from messaging import Position3D
from messaging import Gps
from messaging import Acceleration
from messaging import Barometer
##
 # This file is automatically generated. Do not hand modify.
 # @file Message.py
 # @author Garrett Miller
 # @date September 7 2019

class Message:
   def __init__(self):
      self.callbackDict = dict()
      self.internalCallbackDict = dict()
      self.position3d = Position3D()
      self.internalCallbackDict[uids.Position3D_Uid] = self.parsePosition3D
      self.callbackDict[uids.Position3D_Uid] = None
      self.gps = Gps()
      self.internalCallbackDict[uids.Gps_Uid] = self.parseGps
      self.callbackDict[uids.Gps_Uid] = None
      self.acceleration = Acceleration()
      self.internalCallbackDict[uids.Acceleration_Uid] = self.parseAcceleration
      self.callbackDict[uids.Acceleration_Uid] = None
      self.barometer = Barometer()
      self.internalCallbackDict[uids.Barometer_Uid] = self.parseBarometer
      self.callbackDict[uids.Barometer_Uid] = None
   # end def

   def getHeader(self,buff):
      uid = s_unpack("I",buff[:4])[0]
      return uid
   # end def

   def recv(self, buff):
      uid = self.getHeader(buff)
      buf = buff[4:]
      if uid in self.internalCallbackDict:
         return self.internalCallbackDict[uid](buf)
      else:
         return False
      # end if
   # end def

   def parsePosition3D(self, buff):
      self.position3d.unpack(buff)
      if(self.callbackDict[uids.Position3D_Uid] is not None):
         self.callbackDict[uids.Position3D_Uid](self.position3d)
         return True
      else:
         return False
      # end if
   # end def

   def setPosition3DCb(self, cb):
      self.callbackDict[uids.Position3D_Uid] = cb
   # end def

   def parseGps(self, buff):
      self.gps.unpack(buff)
      if(self.callbackDict[uids.Gps_Uid] is not None):
         self.callbackDict[uids.Gps_Uid](self.gps)
         return True
      else:
         return False
      # end if
   # end def

   def setGpsCb(self, cb):
      self.callbackDict[uids.Gps_Uid] = cb
   # end def

   def parseAcceleration(self, buff):
      self.acceleration.unpack(buff)
      if(self.callbackDict[uids.Acceleration_Uid] is not None):
         self.callbackDict[uids.Acceleration_Uid](self.acceleration)
         return True
      else:
         return False
      # end if
   # end def

   def setAccelerationCb(self, cb):
      self.callbackDict[uids.Acceleration_Uid] = cb
   # end def

   def parseBarometer(self, buff):
      self.barometer.unpack(buff)
      if(self.callbackDict[uids.Barometer_Uid] is not None):
         self.callbackDict[uids.Barometer_Uid](self.barometer)
         return True
      else:
         return False
      # end if
   # end def

   def setBarometerCb(self, cb):
      self.callbackDict[uids.Barometer_Uid] = cb
   # end def

   def setAllCallbacks(self,cb):
      self.setPosition3DCb(cb)
      self.setGpsCb(cb)
      self.setAccelerationCb(cb)
      self.setBarometerCb(cb)
   # end def

# end class