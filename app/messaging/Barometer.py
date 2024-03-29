from struct import pack as s_pack
from struct import unpack as s_unpack
from messaging import uids
##
 # This file is automatically generated. Do not hand modify.
 # @file Barometer.py
 # @author Garrett Miller
 # @date September 7 2019

class Barometer:
   def __init__(self):
      self.pressure = 0.0
      self.temperature = 0.0
   # Barometer init constructor

   def getSizeWithHeader(self):
      size = 0
      # header
      size += 4
      size += self.getSize()
      return size
   # end def getSizeWithHeader

   def getSize(self):
      size = 0
      # pressure
      size += 8
      # temperature
      size += 8
      return size
   # end def getSize

   def pack(self):
      bytes = b''
      # pack pressure
      bytes += s_pack("d",self.pressure)
      # pack temperature
      bytes += s_pack("d",self.temperature)
      return bytes
   # end def pack

   def unpack(self,bytearray):
      lower_offset = 0
      upper_offset = 0
      # unpack pressure
      upper_offset += 8
      bytes = bytearray[lower_offset:upper_offset]
      lower_offset = upper_offset
      self.pressure = s_unpack("d",bytes)[0]
      # unpack temperature
      upper_offset += 8
      bytes = bytearray[lower_offset:upper_offset]
      lower_offset = upper_offset
      self.temperature = s_unpack("d",bytes)[0]
   # end def unpack

   def packHeader(self):
      uid = uids.Barometer_Uid
      # pack uid
      return s_pack("I",uid)
   # end def packHeader


   def packWithHeader(self):
      buff = b''
      buff += self.packHeader()
      buff += self.pack()
      return buff
   # end def packWithHeader

   def toString(self):
      str = ""
      spaces = 0
      spaces += 3
      str += " " * spaces + "pressure = %8.4lf" % self.pressure + ", "
      str += " " * spaces + "temperature = %8.4lf" % self.temperature
      return str
   # end def

   def toStringCsv(self):
      str = ""
      str += "pressure, %8.4lf" % self.pressure + ", "
      str += "temperature, %8.4lf" % self.temperature
      return str
   # end def

   def toStringSpaces(self,spaces):
      str = ""
      str += " " * spaces + "pressure = %8.4lf" % self.pressure + ", "
      str += " " * spaces + "temperature = %8.4lf" % self.temperature
      return str

   def increment(self):
      self.pressure += 0.4
      self.temperature += 0.4
   # end def
# end class