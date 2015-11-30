import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from bigneuron_app.config import config
from bigneuron_app.database import db


# Initialize App
application = Flask(__name__)
CORS(application)
application.config.from_object('bigneuron_app.config.' + os.getenv('VAA3D_CONFIG', 'ProdConfig'))

# Initialize Logging
from bigneuron_app.utils import logger
application.logger.addHandler(logger.get_rotating_file_handler('app'))
application.logger.info("Starting Application!")

# Import APIs
import bigneuron_app.jobs.api
import bigneuron_app.job_items.api
import bigneuron_app.users.api


@application.teardown_appcontext
def shutdown_session(exception=None):
	db.remove()