import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config.' + os.getenv('VAA3D_CONFIG', 'ProdConfig'))
db = SQLAlchemy(application)
