import sys
import os

# Add the application's directory to the PYTHONPATH
sys.path.insert(0, '/var/www/flask_app')

# Import the Flask application
from app import app as application  # Assuming your Flask app is named 'app.py'
