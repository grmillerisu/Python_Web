from flask import Flask
from flask import render_template
from app import app

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)