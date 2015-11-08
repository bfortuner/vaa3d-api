import os

class Config(object):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_POOL_RECYCLE = 3600
    WTF_CSRF_ENABLED = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class ProdConfig(Config):
    DB_DRIVER = 'mysql+pymysql://'
    DB_HOSTNAME = 'bigneuron.clwja7eltdnj.us-west-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'vaa3d'
    DB_USERNAME = 'vaa3d'
    DB_PASSWORD = os.getenv('VAA3D_DB_PASSWORD', 'password')
    SQLALCHEMY_DATABASE_URI = DB_DRIVER + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME
    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'secret_key')

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = 'secret'
