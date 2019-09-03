from flask import Flask
from flask import render_template
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
   socketio.run(app, host= get_ip())
