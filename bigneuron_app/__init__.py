import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from bigneuron_app.config import config

# Initialize App
application = Flask(__name__)
CORS(application)
application.config.from_object('bigneuron_app.config.' + os.getenv('VAA3D_CONFIG', 'ProdConfig'))
db = SQLAlchemy(application)

# Initialize Logging
from bigneuron_app.utils import logger
application.logger.addHandler(logger.get_rotating_file_handler('app'))
application.logger.info("Starting Application!")

# Import Models
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItemStatus
from bigneuron_app.users.models import User

# Import APIs
import bigneuron_app.jobs.api
import bigneuron_app.job_items.api
import bigneuron_app.users.api
