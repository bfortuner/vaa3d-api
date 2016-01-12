import os
import logging

class Config(object):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_POOL_RECYCLE = 3600
    WTF_CSRF_ENABLED = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', 'password')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'password')
    AWS_REGION='us-west-2'
    AWS_ACCOUNT_ID='647215175976'

class ProdConfig(Config):
    WEBSITE_URL = 'http://vaa3d-website.s3-website-us-west-2.amazonaws.com'
    DB_DRIVER = 'mysql+pymysql://'
    DB_HOSTNAME = 'bigneuron.clwja7eltdnj.us-west-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'vaa3d'
    DB_USERNAME = 'vaa3d'
    DB_PASSWORD = os.getenv('VAA3D_DB_PASSWORD', 'password')
    SQLALCHEMY_DATABASE_URI = DB_DRIVER + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME
    DB_ISOLATION_LEVEL='READ COMMITTED'
    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'secret_key')
    S3_INPUT_BUCKET='vaa3d-input'
    S3_OUTPUT_BUCKET='vaa3d-output'
    S3_WORKING_INPUT_BUCKET='vaa3d-working'
    VAA3D_USER_AWS_ACCESS_KEY = os.getenv('VAA3D_USER_AWS_ACCESS_KEY', 'password')
    VAA3D_USER_AWS_SECRET_KEY = os.getenv('VAA3D_USER_AWS_SECRET_KEY', 'password')
    VAA3D_MIN_RUNTIME=1200 #20 mins
    VAA3D_MAX_RUNTIME=3600 #1 hour
    VAA3D_TIMEOUT_BUFFER_MULTIPLE=2
    DYNAMO_JOB_ITEMS_TABLE='job_items'
    SQS_JOB_ITEMS_QUEUE='vaa3d-job-items'
    SQS_JOB_ITEMS_DEAD_LETTER='vaa3d-job-items-dead'
    SQS_JOBS_QUEUE='vaa3d-jobs'
    SQS_MAX_JOB_ITEM_RUNS=3
    SQS_VISIBILITY_TIMEOUT=3960 #1.1 hours
    APP_LOG_LEVEL=logging.INFO
    MAIL_LOG_LEVEL=logging.ERROR
    DYNAMO_READS_PER_SEC=10
    DYNAMO_WRITES_PER_SEC=4
    ECS_JOBS_CLUSTER='vaa3d-jobs-prod'
    ECS_JOB_ITEMS_CLUSTER='vaa3d-job-items-prod'
    ECS_JOBS_SERVICE='vaa3d-jobs'
    ECS_JOB_ITEMS_SERVICE='vaa3d-job-items'
    ECS_JOBS_TASK='vaa3d-jobs-prod'
    ECS_JOB_ITEMS_TASK='vaa3d-job-items-prod'
    ECR_IMAGE=Config.AWS_ACCOUNT_ID+'.dkr.ecr.us-east-1.amazonaws.com/vaa3d-prod:latest'
    AUTOSCALING_GROUP_JOBS='Vaa3d-Jobs-Prod-Autoscaling'
    AUTOSCALING_GROUP_JOB_ITEMS='Vaa3d-Job-Items-Prod-Autoscaling'

class TestConfig(Config):
    WEBSITE_URL = 'http://localhost:9000'
    TESTING = True
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DB_DRIVER = 'mysql+pymysql://'
    DB_HOSTNAME = 'bigneuron.clwja7eltdnj.us-west-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'vaa3d-test'
    DB_USERNAME = 'vaa3d'
    DB_PASSWORD = os.getenv('VAA3D_DB_PASSWORD', 'password')
    SQLALCHEMY_DATABASE_URI = DB_DRIVER + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME    
    DB_ISOLATION_LEVEL='READ UNCOMMITTED'
    SECRET_KEY = 'secret'
    S3_INPUT_BUCKET='test-vaa3d-input'
    S3_OUTPUT_BUCKET='test-vaa3d-output'
    S3_WORKING_INPUT_BUCKET='test-vaa3d-working'
    VAA3D_USER_AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', 'password')
    VAA3D_USER_AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'password')
    VAA3D_MIN_RUNTIME=120 #2 mins
    VAA3D_MAX_RUNTIME=600 #10 mins
    VAA3D_TIMEOUT_BUFFER_MULTIPLE=2
    DYNAMO_JOB_ITEMS_TABLE='test_job_items'
    SQS_JOB_ITEMS_QUEUE='test-vaa3d-job-items'
    SQS_JOB_ITEMS_DEAD_LETTER='test-vaa3d-job-items-dead'
    SQS_JOBS_QUEUE='test-vaa3d-jobs'
    SQS_MAX_JOB_ITEM_RUNS=2
    SQS_VISIBILITY_TIMEOUT=1200 #20 mins
    APP_LOG_LEVEL=logging.INFO
    MAIL_LOG_LEVEL=logging.ERROR
    DYNAMO_READS_PER_SEC=3
    DYNAMO_WRITES_PER_SEC=2
    ECS_JOBS_CLUSTER='vaa3d-jobs-test'
    ECS_JOB_ITEMS_CLUSTER='vaa3d-job-items-test'
    ECS_JOBS_SERVICE='vaa3d-jobs'
    ECS_JOB_ITEMS_SERVICE='vaa3d-job-items'
    ECS_JOBS_TASK='vaa3d-jobs-test'
    ECS_JOB_ITEMS_TASK='vaa3d-job-items-test'
    ECR_IMAGE=Config.AWS_ACCOUNT_ID+'.dkr.ecr.us-east-1.amazonaws.com/vaa3d-test:latest'
    AUTOSCALING_GROUP_JOBS='Vaa3d-Jobs-Test-Autoscaling'
    AUTOSCALING_GROUP_JOB_ITEMS='Vaa3d-Job-Items-Test-Autoscaling'

config = globals()[os.getenv('VAA3D_CONFIG', 'ProdConfig')]