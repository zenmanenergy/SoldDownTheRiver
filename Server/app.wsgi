import os
import sys
import logging



# Activate the virtual environment
venv_path = '/var/www/python/myenv/'  # Path to your virtual environment

activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Add the virtual environment site-packages to the path
sys.path.insert(0, os.path.join(venv_path, 'lib', 'python3.8', 'site-packages'))



# Import your Flask application object
sys.path.insert(0, "/var/www/python/")
from flask_app import app as application

# Logging
logging.basicConfig(stream=sys.stderr)
logging.debug('Working directory: %s', os.getcwd())
logging.debug('Python path: %s', sys.path)
