from app import app
from flask import render_template
from datetime import datetime

numbers = [1,2,3,4,5,6,7,8,9]

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
   return render_template('index.html',numb=numb)
