import os
import credentials
# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskdemo:flaskdemo@flaskdemo.cwsaehb7ywmi.us-east-1.rds.amazonaws.com:3306/flaskdemo'

# APP Config
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']

# DATABASE CONFIG

#DB_DRIVER = 'postgresql+psycopg2://'
DB_DRIVER = 'mysql+pymysql://'
DB_HOSTNAME = 'bigneuron.clwja7eltdnj.us-west-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_NAME = 'vaa3d'
DB_USERNAME = 'vaa3d'
DB_PASSWORD = os.environ['VAA3D_DB_PASSWORD']
SQLALCHEMY_DATABASE_URI = DB_DRIVER + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME
print("URI " + SQLALCHEMY_DATABASE_URI)

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'wazzupman'
