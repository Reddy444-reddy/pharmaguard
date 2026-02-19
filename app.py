# Root-level app.py for Render deployment
# This file allows Render to find the Flask app when running: gunicorn app:app

from backend.api import app

if __name__ == '__main__':
    app.run()
