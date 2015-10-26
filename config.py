from application.credentials import *

# DATABASE CONFIG
#DB_DRIVER = 'postgresql+psycopg2://'
DB_DRIVER = 'mysql+pymysql://'
DB_HOSTNAME = 'bigneuron.clwja7eltdnj.us-west-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_NAME = 'vaa3d'
DB_USERNAME = 'vaa3d'
DB_PASSWORD = VAA3D_DB_PASSWORD
SQLALCHEMY_DATABASE_URI = DB_DRIVER + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME
print("URI " + SQLALCHEMY_DATABASE_URI)

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
