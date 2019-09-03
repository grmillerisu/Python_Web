from flask import Flask
from flask import render_template
from app import app
from app import socketio

if __name__ == '__main__':
   import start_debugger
   socketio.run(app)
