from app import app
from flask import render_template
from datetime import datetime

@app.route('/')
def hello_world():
    message = {'name':'Pos3d',
               'time' : datetime.now().time()}
    return render_template('message.html',title='The Title',message=message)

@app.route('/index')
def ind():
   print("Index")
   return render_template('index.html')
