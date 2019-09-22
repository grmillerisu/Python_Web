# Ground Station Website
Python Flask hosted webserver to relay information from the groundstation to nearby devices.

This uses python, python-flask and flask-socketio to work. I'd suggest using a virtual environment (venv) to run it from, since running flask can be a tad complicated. 

Most of the functionality is in the 'app' folder.
'routes.py' defines the routes the website responds to and how it displays information.
'messageThread.py' is currently a thread creating fake messages to send to the JS front end through socketio, but it will be updated to take real messages from the Serial connection to the ground station arduino board.
The html files in the 'templates' folder define the pages that are shown to people viewing the websites, based on which route they're on.
The files in the 'static' folder are files able to be viewed by the client. This is where all of the JS files are location, within the 'js' folder. 'application.js' is where all of the JS functionality is currently defined. Jquery and socket.io are js files used by application to be able to send/recieve messages and query the html.
