from app import app
from flask import render_template
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
      numb += "]\n"
   else:
      numb = "var numbers_received = [];"
   msg1 = {"name":"first_message","length":5}
   msg2 = {"name":"second_message","length":8}
   messages = [msg1,msg2]
   msg_var = [str(msg1),str(msg2)]
   msg_str = ""
   msg_str += "var msg1 = " + str(msg1) + "\n"
   msg_str += "var msg2 = " + str(msg2) + "\n"
   msg_str += "var msg_Var = [msg1, msg2]\n"
   return render_template('index.html',numb=numb,messages=messages, msg_str=msg_str)
