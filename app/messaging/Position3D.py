from struct import pack as s_pack
from struct import unpack as s_unpack
from messaging import uids
##
 # This file is automatically generated. Do not hand modify.
 # @file Position3D.py
 # @author Garrett Miller
 # @date September 7 2019

class Position3D:
   def __init__(self):
      self.lat = 0.0
      self.lon = 0.0
      self.alt = 0.0
   # Position3D init constructor

   def getSizeWithHeader(self):
      size = 0
      # header
      size += 4
      size += self.getSize()
      return size
   # end def getSizeWithHeader

   def getSize(self):
      size = 0
      # lat
      size += 8
      # lon
      size += 8
      # alt
      size += 4
      return size
   # end def getSize

   def pack(self):
      bytes = b''
      # pack lat
      bytes += s_pack("d",self.lat)
      # pack lon
      bytes += s_pack("d",self.lon)
      # pack alt
      bytes += s_pack("f",self.alt)
      return bytes
   # end def pack

   def unpack(self,bytearray):
      lower_offset = 0
      upper_offset = 0
      # unpack lat
      upper_offset += 8
      bytes = bytearray[lower_offset:upper_offset]
      lower_offset = upper_offset
      self.lat = s_unpack("d",bytes)[0]
      # unpack lon
      upper_offset += 8
      bytes = bytearray[lower_offset:upper_offset]
      lower_offset = upper_offset
      self.lon = s_unpack("d",bytes)[0]
      # unpack alt
      upper_offset += 4
      bytes = bytearray[lower_offset:upper_offset]
      lower_offset = upper_offset
      self.alt = s_unpack("f",bytes)[0]
   # end def unpack

   def packHeader(self):
      uid = uids.Position3D_Uid
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
      str += " " * spaces + "lat = %8.4lf" % self.lat + ", "
      str += " " * spaces + "lon = %8.4lf" % self.lon + ", "
      str += " " * spaces + "alt = %6.2f" % self.alt
      return str
   # end def

   def toStringCsv(self):
      str = ""
      str += "lat, %8.4lf" % self.lat + ", "
      str += "lon, %8.4lf" % self.lon + ", "
      str += "alt, %6.2f" % self.alt
      return str
   # end def

   def toStringSpaces(self,spaces):
      str = ""
      str += " " * spaces + "lat = %8.4lf" % self.lat + ", "
      str += " " * spaces + "lon = %8.4lf" % self.lon + ", "
      str += " " * spaces + "alt = %6.2f" % self.alt
      return str

   def increment(self):
      self.lat += 0.4
      self.lon += 0.4
      self.alt += 0.1
   # end def
# end class