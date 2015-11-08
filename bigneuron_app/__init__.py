import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config.' + os.getenv('VAA3D_CONFIG', 'ProdConfig'))
db = SQLAlchemy(application)

# Import Models
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItem, JobItemStatus
from bigneuron_app.users.models import User

# Import APIs
import bigneuron_app.jobs.api
import bigneuron_app.job_items.api
import bigneuron_app.users.api