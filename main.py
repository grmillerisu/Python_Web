import os
import sys
os.sys.path.append("app")

from app import app
from app import socketio

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
   #app.config['SERVER_NAME'] = 'serv'
   if 'debug' in sys.argv:
      import start_debugger
   # end if 
   socketio.run(app, host='0.0.0.0')
