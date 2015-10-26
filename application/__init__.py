from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config.ProdConfig')
db = SQLAlchemy(application)
