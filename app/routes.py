from app import app
from flask import render_template
from flask import jsonify
from datetime import datetime

numbers = [1,2,3]

@app.route('/')
def hello_world():
    message = {'name':'Pos3d',
               'time' : datetime.now().time()}
    return render_template('message.html',title='The Title',message=message)

@app.route('/index')
def ind():
   print("Index")
   global numbers
   i=0
   leng = len(numbers)
   if len(numbers) > 0:
      numb = "var numbers_received = ["
      for number in numbers:
         i += 1
         numb += str(number)
         if i is not leng:
            numb += ", "
         # end if
      # end for
      numb += "];\n"
   else:
      numb = "var numbers_received = [];"
   msg1 = {"name":"Position3D","length":5}
   msg2 = {"name":"Acceleration","length":8}
   messages = [msg1,msg2]

   return render_template('index.html',numb=numb,messages=messages)
# end def



def dict_to_str(dic):
   string = "{"
   for key in dic:
      string += "%s%s%s" % ("'",key,"':")#"'" + key + '":'
      try:
         string += str(int(dic[key]))
      except ValueError:
         string += "'%s'" % dic[key]
      string += ", "
   # end for
   string = string[:-2]
   string += "}"
   return string
# end def
