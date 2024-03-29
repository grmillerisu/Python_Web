import os
import sys
os.sys.path.append("app")

from app import app
from app import socketio
from app import thread_stop_event
from app import routes

def get_ip():
   import subprocess
   result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE)
   res = str(result.stdout)
   res = res.split("\\r\\n")
   ip = ''
   for item in res:
      if 'IPv4' in item:
         items = item.split(':')
         ip = items[1].strip()
      # end if
   # end for
   return ip
# end def

if __name__ == '__main__':
   if 'debug' in sys.argv:
      import start_debugger
   # end if
   routes.startThread()
   socketio.run(app, host= get_ip() )
   global thread_stop_event
   thread_stop_event.set()
