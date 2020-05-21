# All we have to do now is configure our run.py file so we can start the Flask server.
# This is the application's entry point. We'll run this file to start the Flask server 
# and launch our application.

from app import app

if __name__ == '__main__':
    app.run()